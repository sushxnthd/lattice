"""Exact repository-level sign-flip randomization; sharp exchangeable cluster null."""
from fractions import Fraction
from itertools import product
from math import comb

def exact_cluster_p(deltas):
    if not deltas or len(deltas)>20: raise ValueError("1..20 clusters required")
    if any(not isinstance(x,int) for x in deltas): raise TypeError("integer deltas")
    observed=sum(deltas)
    extreme=sum(sum(s*x for s,x in zip(signs,deltas))>=observed for signs in product((-1,1),repeat=len(deltas)))
    return Fraction(extreme,2**len(deltas))

def naive_issue_sign_p(wins,losses):
    n=wins+losses
    if n<=0: raise ValueError("no discordant issues")
    return Fraction(sum(comb(n,k) for k in range(wins,n+1)),2**n)

def sensitivity():
    concentrated=[10,10,10,10,-10,-10]
    dispersed=[5,5,5,5,5,5,5,5,-5,-5,-5,-5]
    assert sum(concentrated)==sum(dispersed)==20
    assert exact_cluster_p(concentrated)==Fraction(11,32)
    assert exact_cluster_p(dispersed)==Fraction(397,2048)
    assert naive_issue_sign_p(40,20)<Fraction(1,100)
    assert exact_cluster_p([0]*6)==1
    for n in range(1,8):
        assert exact_cluster_p(list(range(1,n+1)))==Fraction(1,2**n)
    return {"concentrated_p":str(exact_cluster_p(concentrated)),"dispersed_p":str(exact_cluster_p(dispersed)),"naive_p":str(naive_issue_sign_p(40,20)),"tests":"passed"}

if __name__=="__main__":
    import json
    print(json.dumps(sensitivity(),sort_keys=True))
