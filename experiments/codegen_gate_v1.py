"""Frozen code-generation gate for representation search.

Same model, same semantic task family, same hidden tests. Only the representation
of binding software rules changes. This branch was frozen before reading v2.
"""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL="Qwen/Qwen2.5-Coder-0.5B-Instruct"
CANDIDATES=("prose","explicit_nl","decision_table","violation_normal")

DEV=[
 ("Document","draft","published","owner","viewer"),
 ("Order","pending","paid","merchant","guest"),
 ("Ticket","open","closed","agent","visitor"),
 ("Dataset","staged","approved","curator","anonymous"),
]
HOLDOUT=[
 ("Job","queued","running","operator","guest"),
 ("Case","open","resolved","analyst","viewer"),
 ("Model","draft","deployed","maintainer","observer"),
 ("Session","idle","active","owner","guest"),
]

def spec(raw):
    entity,s0,s1,owner,outsider=raw
    return dict(entity=entity,s0=s0,s1=s1,owner=owner,outsider=outsider)

def rules(s,c):
    if c=="prose":
        return " ".join([
          f"The only valid state advance is {s['s0']} to {s['s1']}; reversing or advancing again is rejected.",
          f"A write action is accepted only for actor {s['owner']}; actor {s['outsider']} is not allowed to write.",
          "Setting the metric is accepted only when the new value is nonnegative.",
          "Dropping protection is always rejected. Unknown actions are rejected.",
          "Rejected changes leave state and metric unchanged."
        ])
    if c=="explicit_nl":
        return "\n".join([
          f"ONLY LEGAL ADVANCE: {s['s0']} -> {s['s1']}",
          "FORBID: reverse transition",
          f"PERMIT write IFF actor == {s['owner']}",
          f"FORBID write IF actor == {s['outsider']}",
          "PERMIT set_metric IFF value >= 0",
          "FORBID drop_protection",
          "FORBID unknown actions",
          "ON REJECT: preserve state AND metric"
        ])
    if c=="decision_table":
        return "\n".join([
          "ACTION | CONDITION | RESULT",
          f"advance | state == {s['s0']} | state={s['s1']}, accepted=True",
          "advance | otherwise | unchanged, accepted=False",
          f"write | actor == {s['owner']} | unchanged, accepted=True",
          "write | otherwise | unchanged, accepted=False",
          "set_metric | value >= 0 | metric=value, accepted=True",
          "set_metric | value < 0 | unchanged, accepted=False",
          "rewind | any | unchanged, accepted=False",
          "drop_protection | any | unchanged, accepted=False",
          "other | any | unchanged, accepted=False"
        ])
    if c=="violation_normal":
        return "\n".join([
          "A request is rejected iff any applicable violation predicate is true:",
          f"V1 := action=='advance' AND state!={s['s0']}",
          f"V2 := action=='write' AND actor!={s['owner']}",
          "V3 := action=='set_metric' AND value<0",
          "V4 := action IN {'rewind','drop_protection'}",
          "V5 := action NOT IN {'advance','write','set_metric','rewind','drop_protection'}",
          f"If action=='advance' and no violation: state becomes {s['s1']}.",
          "If action=='set_metric' and no violation: metric becomes value.",
          "Otherwise accepted valid actions preserve state and metric.",
          "All rejected requests preserve state and metric."
        ])
    raise ValueError(c)

def prompt(s,c):
    return f"""Implement the Python function below. Return only Python code, no markdown.

def apply_change(state: str, metric: int, actor: str, action: str, value: int) -> tuple[str, int, bool]:
    ...

Binding rules:
{rules(s,c)}

Return exactly (new_state, new_metric, accepted). Do not import anything and do not perform I/O."""

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
    return [
      ([s["s0"],3,s["owner"],"advance",0],[s["s1"],3,True]),
      ([s["s1"],3,s["owner"],"advance",0],[s["s1"],3,False]),
      ([s["s1"],3,s["owner"],"rewind",0],[s["s1"],3,False]),
      ([s["s0"],3,s["owner"],"write",0],[s["s0"],3,True]),
      ([s["s0"],3,s["outsider"],"write",0],[s["s0"],3,False]),
      ([s["s0"],3,s["owner"],"set_metric",7],[s["s0"],7,True]),
      ([s["s0"],3,s["owner"],"set_metric",0],[s["s0"],0,True]),
      ([s["s0"],3,s["owner"],"set_metric",-1],[s["s0"],3,False]),
      ([s["s0"],3,s["owner"],"drop_protection",0],[s["s0"],3,False]),
      ([s["s0"],3,s["owner"],"something_else",0],[s["s0"],3,False]),
    ]

def run_hidden(code,s):
    if not code:return {"passed":0,"total":10,"error":"no_safe_function"}
    cases=tests_for(s)
    harness=code+"\n\n"+f"CASES={repr(cases)}\n"+r'''
import json
passed=0
errors=[]
for i,(args,expected) in enumerate(CASES):
    try:
        got=apply_change(*args)
        got=list(got) if isinstance(got,tuple) else got
        if got==expected:
            passed+=1
        else:
            errors.append([i,got,expected])
    except Exception as exc:
        errors.append([i,type(exc).__name__])
print(json.dumps({"passed":passed,"total":len(CASES),"errors":errors}))
'''
    try:
        p=subprocess.run([sys.executable,"-I","-c",harness],capture_output=True,text=True,timeout=3)
        if p.returncode!=0:return {"passed":0,"total":10,"error":p.stderr[-300:]}
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception as exc:
        return {"passed":0,"total":10,"error":type(exc).__name__}

def generate(model,tok,p):
    chat=tok.apply_chat_template([{"role":"user","content":p}],tokenize=False,add_generation_prompt=True)
    x=tok(chat,return_tensors="pt",add_special_tokens=False)
    with torch.inference_mode():
        y=model.generate(**x,max_new_tokens=220,do_sample=False,pad_token_id=tok.eos_token_id)
    return tok.decode(y[0,x.input_ids.shape[1]:],skip_special_tokens=True),int(x.input_ids.shape[1])

def main():
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    tok=AutoTokenizer.from_pretrained(MODEL)
    model=AutoModelForCausalLM.from_pretrained(MODEL); model.eval()
    tasks=[("dev",x) for x in DEV]+[("holdout",x) for x in HOLDOUT]
    manifest=hashlib.sha256(json.dumps(tasks,sort_keys=True).encode()).hexdigest()
    rows=[]
    for cand in CANDIDATES:
        for split,raw in tasks:
            s=spec(raw); p=prompt(s,cand)
            raw_out,n_tokens=generate(model,tok,p)
            code=extract(raw_out)
            result=run_hidden(code,s)
            rows.append({"candidate":cand,"split":split,"domain":s["entity"],
                         "passed":result["passed"],"total":result["total"],
                         "score":result["passed"]/result["total"],
                         "prompt_tokens":n_tokens,"code":code,"raw_output":raw_out,
                         "error":result.get("error"),"errors":result.get("errors",[])})
    summary={}
    for split in ("dev","holdout"):
        summary[split]={}
        for cand in CANDIDATES:
            r=[x for x in rows if x["split"]==split and x["candidate"]==cand]
            summary[split][cand]={
              "domains":len(r),
              "tests_passed":sum(x["passed"] for x in r),
              "tests_total":sum(x["total"] for x in r),
              "test_accuracy":sum(x["passed"] for x in r)/sum(x["total"] for x in r),
              "perfect_programs":sum(x["passed"]==x["total"] for x in r),
              "mean_prompt_tokens":sum(x["prompt_tokens"] for x in r)/len(r),
            }
    selected=max(CANDIDATES,key=lambda c:(summary["dev"][c]["test_accuracy"],
                                           summary["dev"][c]["perfect_programs"],
                                           -summary["dev"][c]["mean_prompt_tokens"],c))
    out={"model":MODEL,"manifest_sha256":manifest,"development_domains":[x[0] for x in DEV],
         "holdout_domains":[x[0] for x in HOLDOUT],"summary":summary,
         "selected_on_development":selected,
         "selected_holdout_test_accuracy":summary["holdout"][selected]["test_accuracy"],
         "rows":rows,
         "claim_boundary":"Prospective small-function code-generation gate with hidden tests; not long-horizon repository evolution."}
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/codegen_gate_v1.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"manifest_sha256":manifest,"summary":summary,
                      "selected_on_development":selected,
                      "selected_holdout_test_accuracy":out["selected_holdout_test_accuracy"]},
                     indent=2,sort_keys=True))
if __name__=="__main__":main()
