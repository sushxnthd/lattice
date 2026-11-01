#!/usr/bin/env python3
"""Independent finite-factorial comparison of raw historical four-arm cloud results.

Only tests the post-reference mocked SSL policy grid; cannot qualify a real repair.
"""
import json,sys,zipfile
ARMS=('base','connection_only','poolmanager_only','full')
def analyze(path):
    with zipfile.ZipFile(path) as z:
        rows={a:json.loads(z.read(a+'.json'))['cases'] for a in ARMS}
    n=len(rows['base'])
    assert n==8 and all(len(rows[a])==n for a in ARMS)
    keys=('proxy_verify','target_verify','hostname','explicit','expected')
    for i in range(n):
        assert len({tuple(rows[a][i][k] for k in keys) for a in ARMS})==1
    scores={a:sum(bool(x['passed']) for x in rows[a]) for a in ARMS}
    disagreements={}
    for a,b in (('base','poolmanager_only'),('connection_only','full')):
        d=[i for i in range(n) if rows[a][i]!=rows[b][i]]
        if d:disagreements[a+' vs '+b]=d
    return {'scores':scores,'case_count':n,'full_trace_parity_comparisons':2*n,
        'full_trace_disagreements':disagreements,
        'interaction':scores['full']-scores['connection_only']-scores['poolmanager_only']+scores['base'],
        'connection_needed_on_this_grid':scores['full']>scores['poolmanager_only'],
        'poolmanager_needed_on_this_grid':scores['full']>scores['connection_only'],
        'qualification':'NOT_QUALIFIED',
        'scope':'post-reference mock SSL policy grid, not actual TLS'}
if __name__=='__main__':print(json.dumps(analyze(sys.argv[1]),indent=2,sort_keys=True))
