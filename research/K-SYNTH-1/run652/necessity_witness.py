"""Run652: exact exhaustive witness-level audit, synthetic outcomes only."""
import itertools, json
ARMS=('base','parent','subclass')
CELLS=('target_a','target_b','control_a','control_b')
def classify(m):
    full_ok=all(m['full'].values())
    failures={a:{t for t in CELLS[:2] if not m[a][t]} for a in ARMS}
    suite=full_ok and all(failures[a] for a in ARMS)
    common=bool(failures['parent'] & failures['subclass'])
    return suite, suite and common, suite and not common
def main():
    counts={'enumerated':0,'suite_necessity':0,'shared_target_witness':0,'disjoint_target_witness':0}
    example=None
    for bits in itertools.product((False,True),repeat=12):
        m={a:dict(zip(CELLS,bits[i*4:i*4+4])) for i,a in enumerate(ARMS)}
        m['full']={c:True for c in CELLS}
        suite,shared,split=classify(m)
        counts['enumerated']+=1
        counts['suite_necessity']+=suite
        counts['shared_target_witness']+=shared
        counts['disjoint_target_witness']+=split
        if split and example is None:example=m
    assert counts=={'enumerated':4096,'suite_necessity':1728,'shared_target_witness':1344,'disjoint_target_witness':384},counts
    assert counts['suite_necessity']==counts['shared_target_witness']+counts['disjoint_target_witness']
    result={'counts':counts,'disjoint_counterexample':example,'scope':'Exact synthetic Boolean enumeration; no upstream execution or model evidence','qualification':'UNKNOWN'}
    with open('run652_raw.json','w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(counts,sort_keys=True))
if __name__=='__main__':main()
