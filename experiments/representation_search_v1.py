"""Representation Search v1.

Searches four logically equivalent ways to expose project constraints to a fixed
coding LLM. Candidate selection uses only development domains. The holdout
domains were frozen before this run and are opened once.
"""
from __future__ import annotations
import hashlib, json, math, os
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL="Qwen/Qwen2.5-Coder-0.5B-Instruct"
CANDIDATES=("prose","explicit_nl","decision_table","violation_normal")
BATCH=32

DEV=[
 ("Document","draft","published","owner","viewer","document","revision"),
 ("Order","pending","paid","merchant","guest","order","amount"),
 ("Report","private","released","author","reader","report","version"),
 ("Ticket","open","closed","agent","visitor","ticket","priority"),
 ("Dataset","staged","approved","curator","anonymous","dataset","records"),
]
HOLDOUT=[
 ("Shipment","queued","dispatched","courier","guest","shipment","packages"),
 ("Account","unverified","verified","admin","anonymous","account","quota"),
 ("Experiment","planned","running","scientist","observer","experiment","samples"),
]

def tasks(domains, split):
    out=[]
    for i,(entity,s0,s1,owner,outsider,res,metric) in enumerate(domains):
        s={"commitment":f"{res}_protected","entity":entity,"transition":[s0,s1],
           "owner":owner,"outsider":outsider,"resource":res,"metric":metric,
           "minimum":0,"dependency":[f"{res}_publish","authorization"]}
        ps=[
          ("valid_transition","A",{"transition":[s0,s1],"metric":i+1}),
          ("valid_owner_write","A",{"permission":[owner,"write",res],"metric":i}),
          ("valid_metric","A",{"metric":i+2}),
          ("drop_commitment","R",{"drop":s["commitment"],"metric":i}),
          ("illegal_transition","R",{"transition":[s1,s0],"metric":i}),
          ("permission_broadening","R",{"permission":[outsider,"write",res],"metric":i}),
          ("dependency_removal","R",{"remove_dependency":s["dependency"],"metric":i}),
          ("invariant_failure","R",{"metric":-1}),
        ]
        for kind,label,p in ps:
            out.append({"id":f"{split}-{i:02d}-{kind}","split":split,"kind":kind,
                        "label":label,"spec":s,"proposal":p})
    return out

def proposal_text(s,p):
    bits=[]
    if "drop" in p: bits.append(f"drop commitment {p['drop']}")
    if "transition" in p: bits.append(f"transition {s['entity']} {p['transition'][0]} -> {p['transition'][1]}")
    if "permission" in p: bits.append(f"grant {p['permission'][0]} {p['permission'][1]} {p['permission'][2]}")
    if "remove_dependency" in p: bits.append(f"remove dependency {p['remove_dependency'][0]} -> {p['remove_dependency'][1]}")
    bits.append(f"set {s['metric']} = {p.get('metric',s['minimum'])}")
    return "; ".join(bits)

def render(t,c):
    s,p=t["spec"],t["proposal"]
    prop=proposal_text(s,p)
    if c=="prose":
        body=" ".join([
          f"The commitment {s['commitment']} is protected and must not be removed.",
          f"{s['entity']} may transition from {s['transition'][0]} to {s['transition'][1]}, but not in reverse.",
          f"Only {s['owner']} may write {s['resource']}; {s['outsider']} may not be granted write access.",
          f"{s['dependency'][0]} must retain its dependency on {s['dependency'][1]}.",
          f"{s['metric']} must always be at least {s['minimum']}.",
          f"Proposed change: {prop}."
        ])
    elif c=="explicit_nl":
        body="\n".join([
          f"MUST KEEP commitment: {s['commitment']}",
          f"ONLY LEGAL {s['entity']} transition: {s['transition'][0]} -> {s['transition'][1]}",
          f"ONLY {s['owner']} MAY write {s['resource']}",
          f"{s['outsider']} MUST NOT write {s['resource']}",
          f"MUST KEEP dependency: {s['dependency'][0]} -> {s['dependency'][1]}",
          f"MUST SATISFY: {s['metric']} >= {s['minimum']}",
          f"CHANGE: {prop}"
        ])
    elif c=="decision_table":
        body="\n".join([
          "DECISION RULES:",
          f"drop({s['commitment']}) | REJECT",
          f"transition({s['entity']},{s['transition'][0]},{s['transition'][1]}) | ALLOW",
          f"any other transition({s['entity']},*,*) | REJECT",
          f"grant({s['owner']},write,{s['resource']}) | ALLOW",
          f"grant(anyone_else,write,{s['resource']}) | REJECT",
          f"remove_dependency({s['dependency'][0]},{s['dependency'][1]}) | REJECT",
          f"{s['metric']} < {s['minimum']} | REJECT",
          "otherwise | ALLOW",
          f"CHANGE: {prop}"
        ])
    elif c=="violation_normal":
        body="\n".join([
          "A change is invalid iff at least one violation predicate is true:",
          f"V1 = drops({s['commitment']})",
          f"V2 = transition({s['entity']}) != ({s['transition'][0]} -> {s['transition'][1]})",
          f"V3 = grants_write({s['resource']}, role) AND role != {s['owner']}",
          f"V4 = removes_dependency({s['dependency'][0]} -> {s['dependency'][1]})",
          f"V5 = {s['metric']} < {s['minimum']}",
          "REJECT iff V1 OR V2 OR V3 OR V4 OR V5; otherwise ALLOW.",
          f"CHANGE: {prop}"
        ])
    else: raise ValueError(c)
    return ("Review the proposed software change against every binding rule. "
            "Output exactly A for ALLOW or R for REJECT; output nothing else.\n\n"+body)

def score(model,tok,prompts):
    tok.padding_side="left"
    if tok.pad_token_id is None: tok.pad_token=tok.eos_token
    aids=tok("A",add_special_tokens=False).input_ids
    rids=tok("R",add_special_tokens=False).input_ids
    assert len(aids)==len(rids)==1
    out=[]
    for st in range(0,len(prompts),BATCH):
        xs=prompts[st:st+BATCH]
        rendered=[tok.apply_chat_template([{"role":"user","content":x}],tokenize=False,add_generation_prompt=True) for x in xs]
        z=tok(rendered,padding=True,return_tensors="pt",add_special_tokens=False)
        with torch.inference_mode(): logits=model(**z).logits[:,-1,:]
        pair=logits[:,[aids[0],rids[0]]]
        prob=torch.softmax(pair,dim=-1)
        pred=torch.argmax(pair,dim=-1).tolist()
        lengths=z["attention_mask"].sum(dim=1).tolist()
        for j,k in enumerate(pred):
            out.append({"pred":"A" if k==0 else "R","confidence":float(prob[j,k]),"tokens":int(lengths[j])})
    return out

def agg(rows, split, cand):
    r=[x for x in rows if x["split"]==split and x["candidate"]==cand]
    return {"n":len(r),"correct":sum(x["correct"] for x in r),
            "accuracy":sum(x["correct"] for x in r)/len(r),
            "mean_tokens":sum(x["tokens"] for x in r)/len(r)}

def exact_discordant(selected, baseline):
    pairs=list(zip(selected,baseline))
    b=sum(a["correct"] and not z["correct"] for a,z in pairs)
    c=sum(z["correct"] and not a["correct"] for a,z in pairs)
    n=b+c
    if n==0:return {"selected_only":b,"baseline_only":c,"two_sided_p":1.0}
    tail=sum(math.comb(n,k) for k in range(0,min(b,c)+1))/(2**n)
    return {"selected_only":b,"baseline_only":c,"two_sided_p":min(1.0,2*tail)}

def main():
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    all_tasks=tasks(DEV,"dev")+tasks(HOLDOUT,"holdout")
    manifest=hashlib.sha256(json.dumps(all_tasks,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    tok=AutoTokenizer.from_pretrained(MODEL)
    model=AutoModelForCausalLM.from_pretrained(MODEL); model.eval()
    rows=[]
    for cand in CANDIDATES:
        sc=score(model,tok,[render(t,cand) for t in all_tasks])
        for t,s in zip(all_tasks,sc):
            rows.append({**s,"candidate":cand,"task_id":t["id"],"split":t["split"],
                         "kind":t["kind"],"gold":t["label"],"correct":s["pred"]==t["label"]})
    dev={c:agg(rows,"dev",c) for c in CANDIDATES}
    hold={c:agg(rows,"holdout",c) for c in CANDIDATES}
    selected=max(CANDIDATES,key=lambda c:(dev[c]["accuracy"],-dev[c]["mean_tokens"],c))
    sr=sorted([x for x in rows if x["split"]=="holdout" and x["candidate"]==selected],key=lambda x:x["task_id"])
    br=sorted([x for x in rows if x["split"]=="holdout" and x["candidate"]=="prose"],key=lambda x:x["task_id"])
    out={"model":MODEL,"manifest_sha256":manifest,"candidates":list(CANDIDATES),
         "development":dev,"holdout":hold,"selected_on_development":selected,
         "selected_holdout_accuracy":hold[selected]["accuracy"],
         "selected_vs_prose_holdout":exact_discordant(sr,br),"rows":rows,
         "claim_boundary":"Finite representation search over four hand-specified, logically equivalent encodings; fresh domain holdout. Not yet repository-level coding or proof of generality."}
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/representation_search_v1.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["manifest_sha256","development","holdout","selected_on_development","selected_holdout_accuracy","selected_vs_prose_holdout"]},indent=2,sort_keys=True))
if __name__=="__main__": main()
