#!/usr/bin/env python3
"""Run449 finite-factorial theorem checker: exact for a finite cube, not Python soundness."""
import itertools

BITS=("P","U","C")
def certify(outcomes, owner):
    """outcomes maps each 3-bit tuple to any equality-comparable observed result."""
    assert set(outcomes)==set(itertools.product((0,1), repeat=3))
    assert owner in BITS
    for j,k in enumerate(BITS):
        if k==owner: continue
        for bits in itertools.product((0,1), repeat=3):
            low=list(bits);high=list(bits);low[j]=0;high[j]=1
            if outcomes[tuple(low)] != outcomes[tuple(high)]: return False
    return True

def test():
    for owner in BITS:
        index=BITS.index(owner)
        x={bits:(bits[index]*10) for bits in itertools.product((0,1),repeat=3)}
        assert certify(x,owner)
        j=(index+1)%3
        y={bits:(bits[index]*10+bits[j]) for bits in x}
        assert not certify(y,owner)
    # A conjunctive success metric may show interaction without source dependency.
    # Finite output equality is the only certified premise here.
    print("6/6 finite positive/adversarial checks passed; scope=finite cube")
if __name__=="__main__":test()
