#!/usr/bin/env python3
"""Run337 finite cardinality theorem, independent of model inference.
Historical httpcore PR1000 was reference-exposed before freezing: NOT QUALIFIED.
"""
from itertools import product

def original(bits, k):
    remaining=list(enumerate(bits)); removed=[]
    for i,b in enumerate(bits):
        if (i,b) in remaining and b and len(remaining)>k:
            remaining.remove((i,b));removed.append(i)
    return removed

def corrected(bits, k):
    remaining=list(enumerate(bits));removed=[]
    for i,b in enumerate(bits):
        if (i,b) in remaining and b and sum(x for _,x in remaining)>k:
            remaining.remove((i,b));removed.append(i)
    return removed

def independent_oracle(bits,k):
    return [i for i,b in enumerate(bits) if b][:max(0,sum(bits)-k)]

def run():
    total=bad_old=bad_new=0
    for n in range(9):
        for bits in product((False,True),repeat=n):
            for k in range(n+1):
                total+=1
                goal=independent_oracle(bits,k)
                bad_old+=original(bits,k)!=goal
                bad_new+=corrected(bits,k)!=goal
    assert (total,bad_old,bad_new)==(4097,3020,0)
    return dict(states_per_module=total,baseline_deviations=bad_old,
                corrected_deviations=bad_new,modules=2,
                provenance='bounded post-reference-exposure mechanism; not production qualification')
if __name__=='__main__':
    print(run())
