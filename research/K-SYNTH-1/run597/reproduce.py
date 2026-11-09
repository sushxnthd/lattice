import itertools, json
from fractions import Fraction

def exact_p(signs, weights):
    observed = abs(sum(s*w for s,w in zip(signs, weights)))
    vals = [abs(sum(s*w for s,w in zip(z,weights))) for z in itertools.product((-1,1),repeat=len(weights))]
    return Fraction(sum(v>=observed for v in vals),len(vals))

def distribution(weights):
    n=len(weights); outcomes=[]
    for signs in itertools.product((-1,1),repeat=n):
        outcomes.append((exact_p(signs,weights),exact_p(signs,[1]*n)))
    return dict(repos=n,weights=weights,null_configs=2**n,
      issue_weighted_reject=str(Fraction(sum(a<=Fraction(1,20) for a,b in outcomes),len(outcomes))),
      repo_equal_reject=str(Fraction(sum(b<=Fraction(1,20) for a,b in outcomes),len(outcomes))))
rows=[distribution([100]+[1]*(r-1)) for r in (4,6,8,10)]
assert all(Fraction(row[k])<=Fraction(1,20) for row in rows for k in ('issue_weighted_reject','repo_equal_reject'))
print(json.dumps(dict(method='exact repository sign-flip',alpha='1/20',results=rows),indent=2))
