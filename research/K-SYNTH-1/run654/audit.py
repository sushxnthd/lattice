"""Exact finite audit: component necessity versus same-target synergy.
No model inference; synthetic Boolean configurations only.
"""
import itertools,json,collections
ARMS=('base','left','right','full')
def classify(bits):
    a={arm:bits[4*i:4*i+4] for i,arm in enumerate(ARMS)}
    target=lambda arm:a[arm][:2]
    controls=lambda arm:a[arm][2:]
    qualified=(target('base')!=(1,1) and target('full')==(1,1)
               and controls('base')==(1,1) and controls('full')==(1,1))
    if not qualified:return None
    necessity=all(target(arm)!=(1,1) for arm in ('left','right'))
    if not necessity:return 'no_target_necessity'
    common=any(a['left'][i]==0 and a['right'][i]==0 for i in range(2))
    interactions=tuple(a['full'][i]-a['left'][i]-a['right'][i]+a['base'][i] for i in range(2))
    return ('common_witness' if common else 'disjoint_witness',interactions)
def main():
    counts=collections.Counter()
    witnesses={}
    for bits in itertools.product((0,1),repeat=16):
        result=classify(bits)
        if result is None:continue
        key=str(result)
        counts[key]+=1
        witnesses.setdefault(key,''.join(map(str,bits)))
    ex=(0,0,1,1, 0,1,1,1, 1,0,1,1, 1,1,1,1)
    assert classify(ex)[0]=='disjoint_witness'
    assert sum(counts.values())==3*16*16
    result={'total_configurations':65536,'qualified_patterns':sum(counts.values()),
            'classes':dict(sorted(counts.items())), 'first_witnesses':witnesses,
            'constructive_disjoint':''.join(map(str,ex)),
            'scope':'synthetic exhaustive Boolean truth-table, no upstream execution'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
