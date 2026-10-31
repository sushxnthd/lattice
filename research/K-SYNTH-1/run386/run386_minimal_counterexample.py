#!/usr/bin/env python3
"""Self-contained executable effect-only counterexample and one-hot ANF proof check."""

def mobius(bits):
    assert len(bits)==16 and all(type(v) is bool for v in bits)
    out=[int(v) for v in bits]
    for j in range(4):
        for m in range(16):
            if m&(1<<j): out[m]^=out[m^(1<<j)]
    return tuple(out)

def invert(coeff):
    return tuple(bool(x) for x in mobius(tuple(bool(x) for x in coeff)))

def observation(table,x,y,with_effect):
    producer_output=bool((table>>((int(x)<<1)|int(y)))&1)
    events=(('audit',True),) if with_effect and producer_output else ()
    return events,('return',False)

def main():
    inputs=((False,False),(False,True),(True,False),(True,True))
    a=tuple(tuple(observation(t,x,y,True) for t in range(16)) for x,y in inputs)
    b=tuple(tuple(observation(t,x,y,False) for t in range(16)) for x,y in inputs)
    assert all(a[i][t][1]==b[i][t][1] for i in range(4) for t in range(16))
    assert any(a[i][t]!=b[i][t] for i in range(4) for t in range(16))
    alphabet=tuple(sorted(set(v for row in a for v in row),key=repr))
    for row in a:
        coeffs=[mobius(tuple(value==out for value in row)) for out in alphabet]
        for t in range(16):
            active=[j for j,c in enumerate(coeffs) if invert(c)[t]]
            assert len(active)==1 and alphabet[active[0]]==row[t]
    for truth in range(65536):
        values=tuple(bool((truth>>j)&1) for j in range(16))
        assert invert(mobius(values))==values
    print('PASS: 64 counterfactual traces, return-only collision, 65,536 ANF roundtrips')

if __name__=='__main__':main()
