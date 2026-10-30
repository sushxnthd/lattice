#!/usr/bin/env python3
"""Read-only independent audit of original GitHub Actions ZIPs. No network."""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
CASES=['T1','T2','C1','C2','C3','C4','C5','C6','H1','H2','H3','H4']
BASE='5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e'
EXPECT={'T1':'CancelledError','T2':'PoolTimeout','C1':'PoolTimeout','C2':'PoolTimeout','C3':'OK','C4':'OK','C5':'UnsupportedProtocol','C6':'UnsupportedProtocol','H1':'CancelledError,CancelledError','H2':'PoolTimeout,PoolTimeout','H3':'CancelledError','H4':'PoolTimeout'}
BLOBS={'httpcore/_async/connection_pool.py':'e6c4ef66312d4d6f31fcbfc417905ae329ef5885','httpcore/_sync/connection_pool.py':'53536d05e8c3d127b466e44dcf20e9f028aadab0','httpcore/_synchronization.py':'be3dcfda72158d1430c34c0387988eacac3452b8'}
BASE_PART={'async':BLOBS['httpcore/_async/connection_pool.py'],'sync':BLOBS['httpcore/_sync/connection_pool.py']}
REF={'async':'10b7a55a4d0cc89b18247bde06724a561b5f4e7d','sync':'1a7025e1724d933e1dffc1bcdf28bac5328d5435'}

def openzip(path):
    raw=Path(path).read_bytes();z=zipfile.ZipFile(io.BytesIO(raw))
    assert len(z.namelist())==len(set(z.namelist()))
    assert all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist())
    return z,hashlib.sha256(raw).hexdigest()

def case(row):
    k=row['case'];assert k in EXPECT and row['expected']==EXPECT[k]
    assert row['passed']==(row['observed']==row['expected'] and row['queue_remaining']==0)
    assert isinstance(row['elapsed_ms'],(float,int)) and 0<=row['elapsed_ms']<20000
    return k,row['passed']

def audit(original,factorial):
    z1,h1=openzip(original);z2,h2=openzip(factorial)
    assert z1.read('exit_code.txt').strip()==b'0'
    base=json.loads(z1.read('public.json'))
    assert base['phase']=='public' and base['integrity']=={'commit':BASE,'blobs':BLOBS}
    bmap=dict(case(x) for x in base['cases'])
    assert set(bmap)==set(CASES[:8]) and all(bmap[k] for k in CASES[2:8])
    assert not bmap['T1'] and not bmap['T2']
    assert [x['observed'] for x in base['cases'][:2]]==['ValueError','ValueError']
    assert z2.read('exit_code.txt').strip()==b'0'
    s=json.loads(z2.read('factorial_summary.json'))
    assert s['baseline']==BASE and set(s['arms'])=={'none','async_only','sync_only','full'}
    matrix={}
    for name,arm in s['arms'].items():
        keys=set(arm['repaired'])
        assert keys=={'none':set(),'async_only':{'async'},'sync_only':{'sync'},'full':{'async','sync'}}[name]
        assert arm['blobs']=={k:REF[k] if k in keys else BASE_PART[k] for k in ('async','sync')}
        vals={}
        for phase,expected in [('public',CASES[:8]),('heldout',CASES[8:])]:
            raw=z2.read(f'{name}_{phase}.json')
            assert hashlib.sha256(raw).hexdigest()==arm['phases'][phase]['raw_sha256']
            p=json.loads(raw)
            assert p['phase']==phase and p['integrity']=={'commit':BASE,'blobs':BLOBS}
            assert [x['case'] for x in p['cases']]==expected
            vals.update(dict(case(x) for x in p['cases']))
            assert [x['observed'] for x in p['cases']]==[x['observed'] for x in arm['phases'][phase]['cases']]
        matrix[name]=vals
    assert {k:matrix['none'][k] for k in CASES[:8]}==bmap
    interactions={k:int(matrix['full'][k])-int(matrix['async_only'][k])-int(matrix['sync_only'][k])+int(matrix['none'][k]) for k in CASES}
    assert interactions==s['casewise_interaction']
    totals={k:sum(v.values()) for k,v in matrix.items()}
    assert all(s['summary'][k]=={'pass':totals[k],'total':12} for k in totals)
    gates={'baseline_public_targets_fail':not matrix['none']['T1'] and not matrix['none']['T2'],
           'baseline_public_controls_pass':all(matrix['none'][k] for k in CASES[2:8]),
           'full_public_and_heldout_pass':all(matrix['full'].values()),
           'each_partial_fails_some_target_or_control':all(not all(matrix[k].values()) for k in ('async_only','sync_only')),
           'exact_two_production_file_reference':True,'source_blobs_match_reference':True}
    assert gates==s['qualification_gates']
    return {'original_sha256':h1,'factorial_sha256':h2,'totals':totals,'gates':gates,
            'interactions':interactions,'qualified':all(gates.values())}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('original');p.add_argument('factorial');p.add_argument('--out',required=True);a=p.parse_args()
    result=audit(a.original,a.factorial)
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
