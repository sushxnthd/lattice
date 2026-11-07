from itertools import product
from math import comb
STATES = ("PASS","FAIL","ABSTAIN","INFRA")
def classify(ir, py):
    if "INFRA" in (ir,py): return "EXCLUDE_PRECOMPLETION"
    if ir=="PASS" and py!="PASS": return "IR_ONLY"
    if py=="PASS" and ir!="PASS": return "PY_ONLY"
    if ir=="PASS": return "BOTH_PASS"
    return "NEITHER_PASS"
rows=[(a,b,classify(a,b)) for a,b in product(STATES,repeat=2)]
assert len(rows)==16
assert sum(r[2]=="EXCLUDE_PRECOMPLETION" for r in rows)==7
assert sum(r[2]=="IR_ONLY" for r in rows)==2
assert sum(r[2]=="PY_ONLY" for r in rows)==2
def exact_p(a,b):
    n=a+b
    return min(1,2*sum(comb(n,k) for k in range(min(a,b)+1))/2**n) if n else 1
assert exact_p(4,2)==0.6875
assert exact_p(4,7)==0.548828125
print(rows)
print("complete-case",exact_p(4,2),"worst-case",exact_p(4,7))
