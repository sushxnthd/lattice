"""Independent finite 2x2 mechanism classification gate, Python 3 stdlib only.

Full subprocess-level source/profile evidence is in the Run349 local archive.
This committed gate reproduces only the casewise truth-table mechanism contrasts.
"""
def contrast(outcomes):
    assert set(outcomes) == {'00','10','01','11'}
    return outcomes['11'] - outcomes['10'] - outcomes['01'] + outcomes['00']

def semantic(x):
    expected = x + 1 if x > 0 else x
    outputs = {'00':x,'10':x,'01':x,'11':expected}
    return {a:int(v == expected) for a,v in outputs.items()}

def parallel(entry,x):
    expected = x + 1 if x > 0 else x
    p = lambda active: expected if active else x
    return {a:int(p((a[0]=='1') if entry=='produce' else (a[1]=='1')) == expected)
            for a in ('00','10','01','11')}

def abi(x,adapter=False):
    expected = x + 1 if x > 0 else x
    fixed = expected
    outcomes = {'00':x,'10':fixed,'01':x if adapter else None,'11':fixed}
    return {a:int(v == expected) for a,v in outcomes.items()}

def run():
    xs=range(-3,5)
    result={'semantic':[contrast(semantic(x)) for x in xs],
            'parallel':[contrast(parallel(entry,x)) for entry in ('produce','consume') for x in xs],
            'abi':[contrast(abi(x)) for x in xs],
            'abi_normalized':[contrast(abi(x,True)) for x in xs]}
    assert result['semantic'].count(1)==4 and result['semantic'].count(0)==4
    assert result['parallel']==[0]*16
    assert result['abi'].count(1)==4 and result['abi'].count(0)==4
    assert result['abi_normalized']==[0]*8
    return result

if __name__=='__main__':
    import json
    print(json.dumps(run(),sort_keys=True))
