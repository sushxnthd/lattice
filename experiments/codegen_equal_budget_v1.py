"""Frozen equal-information/equal-budget replication for Lattice.

Preregistered in CODEGEN_EQUAL_BUDGET_V1_PREREG.md before model execution.
Do not modify after the first model output exists.
"""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL="Qwen/Qwen2.5-Coder-1.5B-Instruct"
CANDIDATES=("strong_prose","violation_normal")
DEV=[
 ("Account","pending","active","administrator","visitor"),
 ("Build","created","verified","engineer","guest"),
 ("Report","draft","approved","reviewer","reader"),
 ("Device","offline","online","operator","observer"),
 ("Experiment","planned","running","scientist","viewer"),
 ("Package","staged","released","maintainer","guest"),
]
HOLDOUT=[
 ("Review","requested","completed","moderator","viewer"),
 ("Deployment","prepared","live","deployer","guest"),
 ("Profile","new","verified","owner","visitor"),
 ("Archive","open","sealed","curator","reader"),
 ("Workflow","idle","executing","operator","observer"),
 ("Record","draft","final","editor","guest"),
]

def spec(raw):
    e,s0,s1,owner,outsider=raw
    return dict(entity=e,s0=s0,s1=s1,owner=owner,outsider=outsider)

def rules(s,c):
    if c=="strong_prose":
        return " ".join([
          f"Accept an advance exactly when the current state is {s['s0']}; when accepted, change state to {s['s1']}.",
          f"Reject advance from {s['s1']} or any other state, and reject every rewind.",
          f"Accept a write exactly when actor is {s['owner']}; reject writes by {s['outsider']} or every other actor.",
          "Accept set_metric exactly when value is nonnegative, including zero; when accepted, set metric to value.",
          "Reject set_metric when value is negative. Always reject drop_protection and every unknown action.",
          "Every rejected request must preserve both state and metric exactly. Accepted write requests also preserve state and metric."
        ])
    if c=="violation_normal":
        return "\n".join([
          "Reject a request iff an applicable violation below is true:",
          f"V1: action == 'advance' AND state != '{s['s0']}'.",
          f"V2: action == 'write' AND actor != '{s['owner']}'.",
          "V3: action == 'set_metric' AND value < 0.",
          "V4: action is 'rewind' OR 'drop_protection'.",
          "V5: action is not advance, write, set_metric, rewind, or drop_protection.",
          f"With no violation, advance changes state to '{s['s1']}'.",
          "With no violation, set_metric changes metric to value.",
          "With no violation, write preserves state and metric.",
          "Every rejected request preserves state and metric exactly."
        ])
    raise ValueError(c)

def prompt(s,c):
    return f"""Implement the Python function below. Return only Python code, no markdown.

def apply_change(state: str, metric: int, actor: str, action: str, value: int) -> tuple[str, int, bool]:
    ...

Binding rules:
{rules(s,c)}

Return exactly (new_state, new_metric, accepted). Do not import anything and do not perform I/O."""

def chat(tok,p):
    return tok.apply_chat_template([{"role":"user","content":p}],tokenize=False,add_generation_prompt=True)

def prompt_tokens(tok,p):
    return len(tok(chat(tok,p),add_special_tokens=False).input_ids)

def extract(text):
    fence=chr(96)*3
    text=text.replace(fence+"python","").replace(fence,"").strip()
    m=re.search(r"def\s+apply_change\s*\(",text)
    if not m:return ""
    code=text[m.start():]
    forbidden=("import ","open(","exec(","eval(","__import__","subprocess","os.","sys.","socket")
    if any(x in code for x in forbidden):return ""
    return code

def tests_for(s):
    third="intruder"
    while third in (s["owner"],s["outsider"]): third+="_x"
    unrelated="unknown_state"
    while unrelated in (s["s0"],s["s1"]): unrelated+="_x"
    return [
      ([s["s0"],3,s["owner"],"advance",0],[s["s1"],3,True]),
      ([s["s1"],3,s["owner"],"advance",0],[s["s1"],3,False]),
      ([unrelated,3,s["owner"],"advance",0],[unrelated,3,False]),
      ([s["s1"],3,s["owner"],"rewind",0],[s["s1"],3,False]),
      ([s["s0"],3,s["owner"],"write",0],[s["s0"],3,True]),
      ([s["s0"],3,s["outsider"],"write",0],[s["s0"],3,False]),
      ([s["s0"],3,third,"write",0],[s["s0"],3,False]),
      ([s["s0"],3,s["owner"],"set_metric",7],[s["s0"],7,True]),
      ([s["s0"],3,s["owner"],"set_metric",0],[s["s0"],0,True]),
      ([s["s0"],3,s["owner"],"set_metric",-1],[s["s0"],3,False]),
      ([s["s0"],3,s["owner"],"drop_protection",0],[s["s0"],3,False]),
      ([s["s0"],3,s["owner"],"something_else",0],[s["s0"],3,False]),
    ]

def run_hidden(code,s):
    cases=tests_for(s)
    if not code:return {"passed":0,"total":len(cases),"error":"no_safe_function"}
    harness=code+"\n\n"+f"CASES={repr(cases)}\n"+r'''
import json
passed=0
errors=[]
for i,(args,expected) in enumerate(CASES):
    try:
        got=apply_change(*args)
        got=list(got) if isinstance(got,tuple) else got
        if got==expected: passed+=1
        else: errors.append([i,got,expected])
    except Exception as exc: errors.append([i,type(exc).__name__])
print(json.dumps({"passed":passed,"total":len(CASES),"errors":errors}))
'''
    try:
        p=subprocess.run([sys.executable,"-I","-c",harness],capture_output=True,text=True,timeout=3)
        if p.returncode!=0:return {"passed":0,"total":len(cases),"error":p.stderr[-300:]}
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception as exc:return {"passed":0,"total":len(cases),"error":type(exc).__name__}

def generate_batch(model,tok,prompts):
    tok.padding_side="left"
    if tok.pad_token_id is None: tok.pad_token=tok.eos_token
    chats=[chat(tok,p) for p in prompts]
    x=tok(chats,return_tensors="pt",padding=True,add_special_tokens=False)
    with torch.inference_mode():
        y=model.generate(**x,max_new_tokens=220,do_sample=False,pad_token_id=tok.pad_token_id)
    width=x.input_ids.shape[1]
    return [tok.decode(row[width:],skip_special_tokens=True) for row in y]

def main():
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    tok=AutoTokenizer.from_pretrained(MODEL)
    tasks=[("dev",x) for x in DEV]+[("holdout",x) for x in HOLDOUT]
    manifest=hashlib.sha256(json.dumps(tasks,sort_keys=True).encode()).hexdigest()

    prepared=[]
    budget=[]
    for split,raw in tasks:
        s=spec(raw)
        ps={c:prompt(s,c) for c in CANDIDATES}
        ns={c:prompt_tokens(tok,ps[c]) for c in CANDIDATES}
        gap=abs(ns["strong_prose"]-ns["violation_normal"])/max(ns.values())
        budget.append({"split":split,"domain":s["entity"],"tokens":ns,"relative_gap":gap})
        if gap>0.05:
            Path("artifacts").mkdir(exist_ok=True)
            Path("artifacts/codegen_equal_budget_v1_budget_failure.json").write_text(json.dumps({"manifest_sha256":manifest,"budget":budget},indent=2)+"\n")
            raise SystemExit(f"TOKEN_BUDGET_GATE_FAILED {s['entity']} {ns} gap={gap:.4f}")
        for c in CANDIDATES: prepared.append((c,split,s,ps[c],ns[c]))

    # Only after every prompt passes the frozen token gate may model generation begin.
    model=AutoModelForCausalLM.from_pretrained(MODEL); model.eval()
    rows=[]
    for c in CANDIDATES:
        items=[x for x in prepared if x[0]==c]
        for start in range(0,len(items),4):
            batch=items[start:start+4]
            outputs=generate_batch(model,tok,[x[3] for x in batch])
            for (_,split,s,_,n_tokens),raw_out in zip(batch,outputs):
                code=extract(raw_out); result=run_hidden(code,s)
                rows.append({"candidate":c,"split":split,"domain":s["entity"],"passed":result["passed"],
                  "total":result["total"],"score":result["passed"]/result["total"],"prompt_tokens":n_tokens,
                  "code":code,"raw_output":raw_out,"error":result.get("error"),"errors":result.get("errors",[])})

    summary={}
    for split in ("dev","holdout"):
        summary[split]={}
        for c in CANDIDATES:
            r=[x for x in rows if x["split"]==split and x["candidate"]==c]
            summary[split][c]={"domains":len(r),"tests_passed":sum(x["passed"] for x in r),
              "tests_total":sum(x["total"] for x in r),"test_accuracy":sum(x["passed"] for x in r)/sum(x["total"] for x in r),
              "perfect_programs":sum(x["passed"]==x["total"] for x in r),
              "mean_prompt_tokens":sum(x["prompt_tokens"] for x in r)/len(r)}
    selected=max(CANDIDATES,key=lambda c:(summary["dev"][c]["test_accuracy"],summary["dev"][c]["perfect_programs"],-summary["dev"][c]["mean_prompt_tokens"]))
    delta=summary["holdout"]["violation_normal"]["test_accuracy"]-summary["holdout"]["strong_prose"]["test_accuracy"]
    if selected!="violation_normal" or delta<=0: verdict="FAIL"
    elif delta>=0.10: verdict="PASS_CANDIDATE_EFFECT"
    else: verdict="INCONCLUSIVE"
    out={"model":MODEL,"manifest_sha256":manifest,"budget":budget,"summary":summary,
      "selected_on_development":selected,"holdout_violation_minus_prose":delta,"verdict":verdict,"rows":rows,
      "claim_boundary":"Frozen equal-information/equal-token small-function replication; not a Lattice breakthrough or repository-evolution result."}
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/codegen_equal_budget_v1.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ("manifest_sha256","summary","selected_on_development","holdout_violation_minus_prose","verdict")},indent=2,sort_keys=True))

if __name__=="__main__": main()
