import itertools, math, json
from fractions import Fraction

def pvalue(n,k):
    upper=sum(math.comb(n,j) for j in range(max(k,n-k),n+1))
    return min(Fraction(1),Fraction(2*upper,2**n))

rows=[]
for n in (2,4,8,12,16):
    weights=[100]+[1]*(n-1)
    invalid=valid=0
    for signs in itertools.product((-1,1),repeat=n):
        k=sum(w for w,s in zip(weights,signs) if s>0)
        j=sum(s>0 for s in signs)
        invalid+=pvalue(sum(weights),k)<=Fraction(1,20)
        valid+=pvalue(n,j)<=Fraction(1,20)
    rows.append(dict(repositories=n,issues=sum(weights),
        invalid_issue_rate=str(Fraction(invalid,2**n)),
        valid_repo_rate=str(Fraction(valid,2**n))))
assert all(Fraction(r["valid_repo_rate"])<=Fraction(1,20) for r in rows)
print(json.dumps(rows,indent=2))
