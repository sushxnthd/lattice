"""Frozen violation-mechanism discrimination experiment. See VIOLATION_MECHANISM_CONTROL_V1_PREREG.md."""
import codegen_equal_budget_v1 as exp
from pathlib import Path
import hashlib,json,os,torch
from transformers import AutoModelForCausalLM,AutoTokenizer

exp.CANDIDATES=("positive_normal","violation_normal")
exp.DEV=[
 ("Session","new","ready","controller","guest"),("Ticket","open","resolved","agent","viewer"),
 ("Dataset","raw","validated","steward","reader"),("Job","queued","running","scheduler","guest"),
 ("Document","draft","published","publisher","viewer"),("Vault","locked","unlocked","custodian","visitor")]
exp.HOLDOUT=[
 ("Channel","closed","open","moderator","viewer"),("Snapshot","pending","committed","operator","guest"),
 ("Case","unreviewed","reviewed","auditor","reader"),("Queue","paused","active","dispatcher","observer"),
 ("Asset","staged","deployed","manager","visitor"),("Request","created","approved","approver","guest")]

_base=exp.rules
def rules(s,c):
    if c=="violation_normal": return _base(s,c)
    if c=="positive_normal":
        return "\n".join([
          "Accept a request iff an applicable acceptance predicate below is true:",
          f"A1: action == 'advance' AND state == '{s['s0']}'.",
          f"A2: action == 'write' AND actor == '{s['owner']}'.",
          "A3: action == 'set_metric' AND value >= 0.",
          "No acceptance predicate exists for 'rewind' OR 'drop_protection'.",
          "No acceptance predicate exists for any action other than advance, write, set_metric, rewind, or drop_protection.",
          f"On accepted advance, change state to '{s['s1']}'.",
          "On accepted set_metric, change metric to value.",
          "On accepted write, preserve state and metric.",
          "Every rejected request preserves state and metric exactly."
        ])
    raise ValueError(c)
exp.rules=rules

def main():
    torch.set_num_threads(min(4,os.cpu_count() or 2))
    tok=AutoTokenizer.from_pretrained(exp.MODEL)
    tasks=[("dev",x) for x in exp.DEV]+[("holdout",x) for x in exp.HOLDOUT]
    manifest=hashlib.sha256(json.dumps(tasks,sort_keys=True).encode()).hexdigest()
    prepared=[]; budget=[]
    for split,raw in tasks:
        s=exp.spec(raw); ps={c:exp.prompt(s,c) for c in exp.CANDIDATES}; ns={c:exp.prompt_tokens(tok,ps[c]) for c in exp.CANDIDATES}
        gap=abs(ns["positive_normal"]-ns["violation_normal"])/max(ns.values())
        budget.append({"split":split,"domain":s["entity"],"tokens":ns,"relative_gap":gap})
        if gap>0.05:
            Path("artifacts").mkdir(exist_ok=True)
            Path("artifacts/violation_mechanism_control_v1_budget_failure.json").write_text(json.dumps({"manifest_sha256":manifest,"budget":budget},indent=2)+"\n")
            raise SystemExit(f"TOKEN_BUDGET_GATE_FAILED {s['entity']} {ns} gap={gap:.4f}")
        for c in exp.CANDIDATES: prepared.append((c,split,s,ps[c],ns[c]))
    model=AutoModelForCausalLM.from_pretrained(exp.MODEL); model.eval(); rows=[]
    for c in exp.CANDIDATES:
        items=[x for x in prepared if x[0]==c]
        for start in range(0,len(items),4):
            batch=items[start:start+4]; outputs=exp.generate_batch(model,tok,[x[3] for x in batch])
            for (_,split,s,_,n),raw_out in zip(batch,outputs):
                code=exp.extract(raw_out); result=exp.run_hidden(code,s)
                rows.append({"candidate":c,"split":split,"domain":s["entity"],"passed":result["passed"],"total":result["total"],"score":result["passed"]/result["total"],"prompt_tokens":n,"code":code,"raw_output":raw_out,"error":result.get("error"),"errors":result.get("errors",[])})
    summary={}
    for split in ("dev","holdout"):
        summary[split]={}
        for c in exp.CANDIDATES:
            r=[x for x in rows if x["split"]==split and x["candidate"]==c]
            summary[split][c]={"domains":len(r),"tests_passed":sum(x["passed"] for x in r),"tests_total":sum(x["total"] for x in r),"test_accuracy":sum(x["passed"] for x in r)/sum(x["total"] for x in r),"perfect_programs":sum(x["passed"]==x["total"] for x in r),"mean_prompt_tokens":sum(x["prompt_tokens"] for x in r)/len(r)}
    selected=max(exp.CANDIDATES,key=lambda c:(summary["dev"][c]["test_accuracy"],summary["dev"][c]["perfect_programs"],-summary["dev"][c]["mean_prompt_tokens"]))
    delta=summary["holdout"]["violation_normal"]["test_accuracy"]-summary["holdout"]["positive_normal"]["test_accuracy"]
    verdict="FAIL" if selected!="violation_normal" or delta<=0 else ("PASS_VIOLATION_SPECIFIC" if delta>=.10 else "INCONCLUSIVE")
    out={"model":exp.MODEL,"manifest_sha256":manifest,"budget":budget,"summary":summary,"selected_on_development":selected,"holdout_violation_minus_positive":delta,"verdict":verdict,"rows":rows,"claim_boundary":"Frozen causal discrimination of violation-normal vs equally structured positive-normal; not a Lattice breakthrough."}
    Path("artifacts").mkdir(exist_ok=True); Path("artifacts/violation_mechanism_control_v1.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ("manifest_sha256","summary","selected_on_development","holdout_violation_minus_positive","verdict")},indent=2,sort_keys=True))
if __name__=="__main__": main()
