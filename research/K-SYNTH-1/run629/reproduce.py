"""Exact repository sign-flip counterexample; synthetic, not model evidence."""
import itertools,math,json
from collections import defaultdict
def mcnemar(a,b):
 n=a+b
 return min(1.,2*sum(math.comb(n,k) for k in range(min(a,b)+1))/2**n) if n else 1.
def cluster_test(rows):
 d=defaultdict(int)
 for repo,ir,py in rows:
  if ir not in (0,1) or py not in (0,1):raise ValueError("binary outcomes required")
  d[repo]+=ir-py
 if not 1<=len(d)<=20:raise ValueError("1..20 clusters required")
 vals=list(d.values());obs=abs(sum(vals))
 return sum(abs(sum(s*v for s,v in zip(signs,vals)))>=obs for signs in itertools.product((-1,1),repeat=len(vals)))/2**len(vals)
rows=[(f"repo{i}",int(i<5),int(i==5)) for i in range(6) for _ in range(5)]
a=sum(i==1 and p==0 for _,i,p in rows);b=sum(i==0 and p==1 for _,i,p in rows)
assert (a,b)==(25,5)
assert cluster_test(rows)==14/64
assert cluster_test([r for r in rows for _ in range(3)])==14/64
assert mcnemar(a,b)<.001
for bad in [("x",None,0),("x",1,2)]:
 try:cluster_test([bad])
 except ValueError:pass
 else:raise AssertionError("invalid outcome accepted")
print(json.dumps({"kind":"synthetic_counterexample","repositories":6,"tasks":30,"ir_only":a,"python_only":b,"naive_mcnemar_p":mcnemar(a,b),"repository_signflip_p":cluster_test(rows)},indent=2))
