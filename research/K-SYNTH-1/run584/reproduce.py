#!/usr/bin/env python3
"""Exact mean-zero asymmetric cluster-sign counterexample."""
from fractions import Fraction
from itertools import product
from math import comb
import json

def signflip_p(xs):
    obs=abs(sum(xs))
    return Fraction(sum(abs(sum(s*x for s,x in zip(signs,xs)))>=obs
        for signs in product((-1,1),repeat=len(xs))),2**len(xs))

def analyze(n):
    rejection=Fraction(0); rows=[]
    for k in range(n+1):
        p=signflip_p([9]*k+[-1]*(n-k))
        probability=Fraction(comb(n,k)*9**(n-k),10**n)
        if p<=Fraction(1,20):rejection+=probability
        rows.append(dict(positive=k,negative=n-k,p=str(p),probability=str(probability)))
    return dict(n=n,false_positive=str(rejection),float=float(rejection),rows=rows)

if __name__=="__main__":
    assert Fraction(1,10)*9+Fraction(9,10)*(-1)==0
    data=[analyze(n) for n in (6,8,10,12)]
    assert data[0]["false_positive"]=="265721/500000"
    print(json.dumps(data,indent=2))
