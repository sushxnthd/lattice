"""Run336 minimal original Run335 evidence and retrospective issue-only baseline.
Usage: python run336_issue_only_baseline.py lattice_run335_original.zip
Never executes model-generated or historical source code.
"""
import hashlib, json, sys, zipfile
from pathlib import Path
z=zipfile.ZipFile(sys.argv[1])
names=z.namelist()
assert len(names)==len(set(names))
assert all(not n.startswith("/") and ".." not in Path(n).parts for n in names)
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads(z.read("SHA256_MANIFEST.json"))
assert len(m)==44
for n,h in m.items(): assert sha(z.read(n))==h,n
c=json.loads(z.read("candidates.json"))
assert len(c)==31 and len({r["id"] for r in c})==31
r=json.loads(z.read("request_REAL_IR.json"))
issue=r["messages"][0]["content"]
assert "different `allow_redirects` default on HEAD requests" in issue
assert "stay consistent" in issue
assert "allow the user to switch `allow_redirects=False`" in issue
selected=sorted([x for x in c if x["qual"].split(".")[-1].lower()=="head"
                 and x["param"]=="allow_redirects" and x["old_expr"]=="False"],
                key=lambda x:(x["path"],x["qual"]))
assert len(selected)==3 and len({x["path"] for x in selected})==2
assert all(x["old_expr"]=="True" for x in c
           if x["qual"].split(".")[-1].lower() in {"get","post","put","patch","delete","options"})
g=json.loads(z.read("gate_summary.json"));assert g["both_pass"]
a=z.read("completion_REAL_IR.txt");b=z.read("completion_REAL_PYTHON_AST.txt")
assert a==b
for arm in ("IR","PYTHON_AST"):
    o=json.loads(z.read("oracle_"+arm+".json"))
    assert len(o["cases"])==9 and o["passed"]==7
    assert all(x["passed"]==(x["error"] is None and x["expected"]==x["observed"])
               for x in o["cases"])
    assert json.loads(z.read("compile_REAL_"+arm+".json"))["accepted"]
print(json.dumps({"manifest_verified":len(m),"gates":"both pass",
                  "real_completions_identical":True,
                  "model_oracle":"1/3 targets + 6/6 controls each",
                  "retrospective_rule_edits":[{"id":x["id"],"new_expr":"True"} for x in selected],
                  "warning":"POST-OUTCOME DIAGNOSTIC; not model success or prospective baseline"},indent=2))
