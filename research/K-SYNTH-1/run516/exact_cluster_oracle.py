# Run516: exact cluster sign-flip, independent subset-sum oracle
from itertools import product
from collections import Counter
def exact(v):
 a=[abs(x) for x in v if x]; obs=abs(sum(v))
 if not a: return 1.0
 return sum(abs(sum(x*s for x,s in zip(a,z)))>=obs for z in product((-1,1),repeat=len(a)))/2**len(a)
def oracle(v):
 a=[abs(x) for x in v if x]; obs=abs(sum(v)); d=Counter({0:1})
 for x in a:
  e=Counter()
  for s,c in d.items():e[s]+=c;e[s+x]+=c
  d=e
 return sum(c for s,c in d.items() if abs(2*s-sum(a))>=obs)/2**len(a)
if __name__=="__main__":
 import random,json
 r=random.Random(516); checks=0
 for n in range(1,12):
  for _ in range(80):
   v=[r.randint(-6,6) for _ in range(n)]
   assert exact(v)==oracle(v);checks+=1
 cases={"one_repo_eight_wins":[[1]*8],"eight_repos_eight_wins":[[1] for _ in range(8)],"seven_small_positive_one_large_negative":[[1] for _ in range(7)]+[[-10]]}
 result={k:{"cluster":exact([sum(x) for x in repos]),"naive":exact([y for x in repos for y in x])} for k,repos in cases.items()}
 assert result["one_repo_eight_wins"]=={"cluster":1.0,"naive":0.0078125}
 assert result["eight_repos_eight_wins"]["cluster"]==0.0078125
 assert result["seven_small_positive_one_large_negative"]["cluster"]==1.0
 print(json.dumps({"crosschecks":checks,"results":result},indent=2))
