#!/usr/bin/env python3
"""Repository-cluster e-process for conditional weak null; not a sign-flip test."""
import math
from fractions import Fraction

BETS=(.025,.05,.1,.2,.4,.8)

def e_process(xs,bets=BETS):
    wealth=[1.0]*len(bets)
    trace=[]
    total=0.0
    for t,x in enumerate(xs,1):
        if not -1<=x<=1:
            raise ValueError("cluster mean outside [-1,1]")
        total+=x
        for i,lam in enumerate(bets):
            wealth[i]*=1+lam*x
        trace.append({"t":t,"e_value":sum(wealth)/len(wealth),"mean":total/t})
    return trace

def exact_weak_null():
    """Run392 counterexample: +1 w.p. 1/6, -1/5 w.p. 5/6, 20 clusters."""
    from math import comb
    bets=tuple(Fraction(s) for s in ("0.025","0.05","0.1","0.2","0.4","0.8"))
    p=Fraction(0)
    for k in range(21):
        e=sum((1+b)**k*(1-b/5)**(20-k) for b in bets)/len(bets)
        if e>=20:
            p+=Fraction(comb(20,k)*5**(20-k),6**20)
    return p

def reject_anytime(xs,alpha=.05):
    return any(z["e_value"]>=1/alpha for z in e_process(xs))

if __name__=="__main__":
    print("Exact weak-null rejection probability:",exact_weak_null())
    print("One-sided e-process; valid only under E[X_t | past] <= 0 and X_t in [-1,1].")
