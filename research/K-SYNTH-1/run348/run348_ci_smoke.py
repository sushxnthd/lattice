"""No-cost GitHub CI smoke checks; full 32,768 traces retained in local archive."""
import random
from run348_branch_dataflow import analyze

def main():
    cases=[
      ('def f(a):\n    x=1\n    if a:\n        pass\n    return x\n','MUST_UNIQUE_ON_REACH'),
      ('def f(a):\n    x=1\n    if a:\n        x=2\n    return x\n','MAY_SET_ON_REACH'),
      ('def f(a):\n    if a:\n        x=1\n    return x\n','UNKNOWN'),
      ('def f(a):\n    x=1\n    if a:\n        return 0\n    x=2\n    return x\n','MUST_UNIQUE_ON_REACH'),
    ]
    for src,want in cases:
        r=analyze('smoke.py',src)
        facts=[c for c in r['certificates'] if c['name']=='x']
        assert (facts[0]['modality'] if facts else 'UNKNOWN')==want,(want,r)
    rng=random.Random(348)
    for _ in range(256):
        init=rng.randrange(5)
        src=(f'def f(a,b):\n    x={init}\n    if a:\n        x={init+1}\n'
             f'    if b:\n        x={init+2}\n    return x\n')
        r=analyze('generated.py',src)
        facts=[c for c in r['certificates'] if c['name']=='x']
        assert len(facts)==1 and facts[0]['modality']=='MAY_SET_ON_REACH'
        allowed={init,init+1,init+2}
        scope={};exec(compile(src,'generated.py','exec'),scope)
        for a in (False,True):
            for b in (False,True):
                assert scope['f'](a,b) in allowed
    print('RUN348_SMOKE_PASS: 4 edge cases + 256 generated sources x 4 inputs')
if __name__=='__main__':main()
