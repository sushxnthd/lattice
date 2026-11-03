"""Fail-closed paired model receipt audit. Standard library only.
This checks mechanical equality, NOT semantic information equivalence.
"""
import hashlib
REQUIRED=("task","arm","model_sha256","source_sha256","facts_sha256","authority_sha256","compiler_sha256","oracle_sha256","decoding_sha256","prompt_sha256","raw_completion_sha256","compiler_trace_sha256","oracle_trace_sha256","status")
COMMON=("model_sha256","source_sha256","facts_sha256","authority_sha256","compiler_sha256","oracle_sha256","decoding_sha256")
def audit(rows):
    errors=[]; pairs={}
    for i,r in enumerate(rows):
        missing=[k for k in REQUIRED if k not in r]
        if missing:
            errors.append((i,"missing",missing));continue
        if r["arm"] not in ("IR","PYTHON"):
            errors.append((i,"unknown_arm"));continue
        for k in REQUIRED:
            if k.endswith("_sha256") and (not isinstance(r[k],str) or len(r[k])!=64 or any(c not in "0123456789abcdef" for c in r[k])):
                errors.append((i,"invalid_sha256",k))
        key=(r["task"],r["arm"])
        if key in pairs: errors.append((i,"duplicate",key))
        pairs[key]=r
    reports=[]
    for task in sorted({key[0] for key in pairs}):
        a=pairs.get((task,"IR"));b=pairs.get((task,"PYTHON"))
        if not a or not b:
            errors.append((task,"unpaired"));continue
        for k in COMMON:
            if a[k]!=b[k]:errors.append((task,"mismatched_common_contract",k))
        reports.append({"task":task,"semantic_information_equivalence":"UNKNOWN","superiority_eligible":False,"status_ir":a["status"],"status_python":b["status"]})
    return {"errors":errors,"pairs":reports,"superiority_eligible_pairs":0}
def self_test():
    h="a"*64;j="b"*64
    def row(arm):
        r={k:h for k in REQUIRED if k.endswith("_sha256")}
        r.update(task="t",arm=arm,status="complete",prompt_sha256=h if arm=="IR" else j)
        return r
    assert audit([row("IR"),row("PYTHON")])["errors"]==[]
    assert audit([row("IR"),row("PYTHON")])["superiority_eligible_pairs"]==0
    assert audit([row("IR")])["errors"]
    assert audit([row("IR"),row("IR"),row("PYTHON")])["errors"]
    bad=row("PYTHON");bad["oracle_sha256"]=j
    assert any(e[1]=="mismatched_common_contract" for e in audit([row("IR"),bad])["errors"])
    bad=row("PYTHON");bad["source_sha256"]="broken"
    assert any(e[1]=="invalid_sha256" for e in audit([row("IR"),bad])["errors"])
if __name__=="__main__":
    self_test()
    print("SELF_TEST_PASS")
