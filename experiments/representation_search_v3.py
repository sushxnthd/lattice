"""Representation Search v3: contrastive option scoring.

Fixes the output-position prior exposed by v2. Each candidate change is scored
independently by logit(A=valid)-logit(R=invalid). The chosen option is the one
with the largest validity margin, so a global A/R prior cancels within a task.

The representation is selected on opened development domains only. Holdout
domains below were frozen before execution and are opened once.
"""
from __future__ import annotations
import hashlib, json, os
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL="Qwen/Qwen2.5-Coder-0.5B-Instruct"
CANDIDATES=("prose","explicit_nl","decision_table","violation_normal")
BATCH=64

DEV=[
 ("Document","draft","published","owner","viewer","document","revision"),
 ("Order","pending","paid","merchant","guest","order","amount"),
 ("Ticket","open","closed","agent","visitor","ticket","priority"),
 ("Dataset","staged","approved","curator","anonymous","dataset","records"),
]
HOLDOUT=[
 ("Ledger","open","sealed","auditor","guest","ledger","entries"),
 ("Workflow","idle","running","operator","viewer","workflow","attempts"),
 ("Artifact","draft","released","maintainer","anonymous","artifact","version"),
 ("Notebook","private","shared","owner","guest","notebook","cells"),
]

TEMPLATES=[
 ("valid_transition",("reverse_transition","outsider_write","negative_metric")),
 ("owner_write",("drop_commitment","remove_dependency","reverse_transition")),
 ("positive_metric",("outsider_write","drop_commitment","remove_dependency")),
 ("boundary_metric",("negative_metric","reverse_transition","outsider_write")),
]

def make_spec(raw):
    entity,s0,s1,owner,outsider,res,metric=raw
    return {"entity":entity,"s0":s0,"s1":s1,"owner":owner,"outsider":outsider,
            "resource":res,"metric":metric,"minimum":0,
            "commitment":f"{res}_protected",
            "dependency":[f"{res}_publish","authorization"]}

def pools(s):
    good={
      "valid_transition":f"transition {s['entity']} from {s['s0']} to {s['s1']}",
      "owner_write":f"grant {s['owner']} write access to {s['resource']}",
      "positive_metric":f"set {s['metric']} to 2",
      "boundary_metric":f"set {s['metric']} to {s['minimum']}",
    }
    bad={
      "reverse_transition":f"transition {s['entity']} from {s['s1']} to {s['s0']}",
      "outsider_write":f"grant {s['outsider']} write access to {s['resource']}",
      "drop_commitment":f"remove protected commitment {s['commitment']}",
      "remove_dependency":f"remove dependency {s['dependency'][0]} -> {s['dependency'][1]}",
      "negative_metric":f"set {s['metric']} to -1",
    }
    return good,bad

def tasks(domains,split):
    out=[]
    for di,raw in enumerate(domains):
        s=make_spec(raw); good,bad=pools(s)
        for qi,(g,bads) in enumerate(TEMPLATES):
            answer=(di*len(TEMPLATES)+qi)%4
            opts=[bad[x] for x in bads]
            opts.insert(answer,good[g])
            out.append({"id":f"{split}-{di}-{qi}","split":split,"spec":s,
                        "answer":answer,"options":opts,"kind":g})
    return out

def rule_text(s,c):
    if c=="prose":
        return " ".join([
          f"The commitment {s['commitment']} is protected and may not be removed.",
          f"The only permitted {s['entity']} transition is {s['s0']} to {s['s1']}; the reverse is forbidden.",
          f"{s['owner']} may write {s['resource']}, but {s['outsider']} may not.",
          f"{s['dependency'][0]} must retain its dependency on {s['dependency'][1]}.",
          f"{s['metric']} must be at least {s['minimum']}."
        ])
    if c=="explicit_nl":
        return "\n".join([
          f"MUST KEEP commitment: {s['commitment']}",
          f"ONLY LEGAL transition: {s['entity']} {s['s0']} -> {s['s1']}",
          f"PERMIT: {s['owner']} write {s['resource']}",
          f"FORBID: {s['outsider']} write {s['resource']}",
          f"MUST KEEP dependency: {s['dependency'][0]} -> {s['dependency'][1]}",
          f"INVARIANT: {s['metric']} >= {s['minimum']}",
        ])
    if c=="decision_table":
        return "\n".join([
          "RULE | DECISION",
          f"drop({s['commitment']}) | INVALID",
          f"transition({s['entity']},{s['s0']},{s['s1']}) | VALID",
          f"transition({s['entity']},anything_else) | INVALID",
          f"write({s['owner']},{s['resource']}) | VALID",
          f"write(any_other_role,{s['resource']}) | INVALID",
          f"remove_dependency({s['dependency'][0]},{s['dependency'][1]}) | INVALID",
          f"{s['metric']} < {s['minimum']} | INVALID",
          "otherwise | VALID",
        ])
    if c=="violation_normal":
        return "\n".join([
          "A change is invalid iff at least one violation predicate is true:",
          f"V1 = drops({s['commitment']})",
          f"V2 = changes {s['entity']} except {s['s0']} -> {s['s1']}",
          f"V3 = grants write({s['resource']}) to role != {s['owner']}",
          f"V4 = removes dependency {s['dependency'][0]} -> {s['dependency'][1]}",
          f"V5 = {s['metric']} < {s['minimum']}",
          "VALID iff NOT(V1 OR V2 OR V3 OR V4 OR V5).",
        ])
    raise ValueError(c)

def prompt(task,cand,option):
    return ("Review one proposed software change against all binding project rules. "
            "Reply exactly A if the change preserves every rule, or R if it violates any rule. "
            "No explanation.\n\nPROJECT RULES:\n"+rule_text(task["spec"],cand)+
            "\n\nPROPOSED CHANGE:\n"+option)

def margins(model,tok,prompts):
    tok.padding_side="left"
    if tok.pad_token_id is None: tok.pad_token=tok.eos_token
    aid=tok("A",add_special_tokens=False).input_ids
    rid=tok("R",add_special_tokens=False).input_ids
    assert len(aid)==len(rid)==1
    out=[]
    for st in range(0,len(prompts),BATCH):
        xs=prompts[st:st+BATCH]
        rendered=[tok.apply_chat_template([{"role":"user","content":p}],tokenize=False,add_generation_prompt=True) for p in xs]
        z=tok(rendered,padding=True,return_tensors="pt",add_special_tokens=False)
        with torch.inference_mode(): logits=model(**z).logits[:,-1,:]
        diff=(logits[:,aid[0]]-logits[:,rid[0]]).tolist()
        lengths=z["attention_mask"].sum(dim=1).tolist()
        out.extend({"margin":float(m),"tokens":int(n)} for m,n in zip(diff,lengths))
    return out

def agg(rows,split,cand):
    r=[x for x in rows if x["split"]==split and x["candidate"]==cand]
    return {"n":len(r),"correct":sum(x["correct"] for x in r),
            "accuracy":sum(x["correct"] for x in r)/len(r),
            "mean_separation":sum(x["separation"] for x in r)/len(r),
            "mean_option_tokens":sum(x["mean_option_tokens"] for x in r)/len(r)}

def main():
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    dev=tasks(DEV,"dev"); hold=tasks(HOLDOUT,"holdout"); all_tasks=dev+hold
    manifest=hashlib.sha256(json.dumps(all_tasks,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    tok=AutoTokenizer.from_pretrained(MODEL)
    model=AutoModelForCausalLM.from_pretrained(MODEL); model.eval()
    rows=[]
    for cand in CANDIDATES:
        flat=[]; index=[]
        for task in all_tasks:
            for oi,opt in enumerate(task["options"]):
                flat.append(prompt(task,cand,opt)); index.append((task,oi))
        scored=margins(model,tok,flat)
        grouped={}
        for (task,oi),sc in zip(index,scored):
            grouped.setdefault(task["id"],{"task":task,"scores":[]})["scores"].append((oi,sc))
        for item in grouped.values():
            task=item["task"]; ss=sorted(item["scores"])
            ms=[x[1]["margin"] for x in ss]
            pred=max(range(4),key=lambda i:ms[i])
            valid=ms[task["answer"]]
            invalid=max(m for i,m in enumerate(ms) if i!=task["answer"])
            rows.append({"candidate":cand,"task_id":task["id"],"split":task["split"],
                         "kind":task["kind"],"gold_index":task["answer"],"pred_index":pred,
                         "correct":pred==task["answer"],"separation":valid-invalid,
                         "margins":ms,
                         "mean_option_tokens":sum(x[1]["tokens"] for x in ss)/4})
    development={c:agg(rows,"dev",c) for c in CANDIDATES}
    holdout={c:agg(rows,"holdout",c) for c in CANDIDATES}
    selected=max(CANDIDATES,key=lambda c:(development[c]["accuracy"],development[c]["mean_separation"],-development[c]["mean_option_tokens"],c))
    out={"model":MODEL,"benchmark":"representation-search-v3-contrastive",
         "manifest_sha256":manifest,"development_domains":[x[0] for x in DEV],
         "holdout_domains":[x[0] for x in HOLDOUT],"development":development,
         "holdout":holdout,"selected_on_development":selected,
         "selected_holdout_accuracy":holdout[selected]["accuracy"],"rows":rows,
         "claim_boundary":"Contrastive semantic-choice gate. Global A/R output priors cancel within each question. Still not a code-generation or repository-evolution result."}
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/representation_search_v3.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ("manifest_sha256","development","holdout","selected_on_development","selected_holdout_accuracy")},indent=2,sort_keys=True))
if __name__=="__main__":main()
