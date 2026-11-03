"""Exact repository-cluster sign-flip randomization audit; standard library only."""
from fractions import Fraction
from itertools import product
from math import comb
import json

def cluster_p(effects):
    effects=tuple(int(x) for x in effects)
    if not effects or len(effects)>22: raise ValueError("cluster count outside exact-enumeration range")
    observed=sum(effects)
    favorable=sum(sum(s*x for s,x in zip(signs,effects))>=observed
                  for signs in product((-1,1),repeat=len(effects)))
    return Fraction(favorable,2**len(effects))

def naive_issue_p(wins,losses):
    n=wins+losses
    return Fraction(sum(comb(n,k) for k in range(wins,n+1)),2**n)

def test():
    assert cluster_p([1]*4)==Fraction(1,16)
    assert naive_issue_p(8,0)==Fraction(1,256)
    assert cluster_p([1,-1])==Fraction(3,4)
    assert cluster_p([0,0])==1
    for n in range(1,11):
        assert cluster_p([1]*n)==Fraction(1,2**n)
        for m in range(1,8):
            assert naive_issue_p(n*m,0)==Fraction(1,2**(n*m))
    return 84

if __name__=="__main__":
    print(json.dumps({"assertions":test(),
      "six_repos_three_identical_wins_each":{"cluster":str(cluster_p([3]*6)),
        "naive":str(naive_issue_p(18,0))},
      "four_winning_two_losing_repos_ten_issues_each":{"cluster":str(cluster_p([10]*4+[-10]*2)),
        "naive":str(naive_issue_p(40,20))},
      "caveat":"Constructed null examples, not empirical model outcomes. Requires independent exchangeable clusters under sharp null."},indent=2))
