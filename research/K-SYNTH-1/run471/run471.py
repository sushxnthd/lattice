"""Exact finite repository sign-flip enumeration. Python standard library only."""
from itertools import product
from fractions import Fraction
import json

def exact_p(margins):
    active = [int(x) for x in margins if x]
    if not active:
        return {"p": "1", "active": 0, "total": 1, "extreme": 1}
    observed = abs(sum(active))
    extreme = sum(abs(sum(x*s for x,s in zip(active, signs))) >= observed
                  for signs in product((-1, 1), repeat=len(active)))
    return {"p": str(Fraction(extreme, 2**len(active))),
            "active": len(active), "total": 2**len(active), "extreme": extreme}

cases = {
    "twelve_repos_two_active": [10, 10]+[0]*10,
    "twelve_repos_six_active": [1]*6+[0]*6,
    "twelve_repos_twelve_active": [1]*12,
    "one_dominant_cluster": [100]+[-1]*11,
    "balanced_null": [1, -1]*6,
}
results = {k: exact_p(v) for k,v in cases.items()}
assert results["twelve_repos_two_active"]["p"] == "1/2"
assert results["twelve_repos_six_active"]["p"] == "1/32"
assert results["twelve_repos_twelve_active"]["p"] == "1/2048"
assert results["one_dominant_cluster"]["p"] == "1"
assert results["balanced_null"]["p"] == "1"
print(json.dumps(results, indent=2))
