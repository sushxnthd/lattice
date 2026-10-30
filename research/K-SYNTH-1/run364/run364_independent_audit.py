#!/usr/bin/env python3
"""Read-only independent Run364 historical factorial auditor; never retune freeze."""
from __future__ import annotations
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ORACLE_SHA = '30896d34a903203c27a5da55275d16faaa6eb9f95879f49d3e1b1968152d5ffb'
BLOBS = {
    0: ('7556b50f6d685bdb30e7afac11484a05ef07b767', '007b31dcfe8aae4f24bebff8bfafa1a06a7bd3eb'),
    1: ('1c8a56597c5728a2a377b3399b427403f753915e', '007b31dcfe8aae4f24bebff8bfafa1a06a7bd3eb'),
    2: ('7556b50f6d685bdb30e7afac11484a05ef07b767', '1ac39a8d5cb048a2c791f5d757ab6e4602624911'),
    3: ('1c8a56597c5728a2a377b3399b427403f753915e', '1ac39a8d5cb048a2c791f5d757ab6e4602624911'),
}

def sha(b): return hashlib.sha256(b).hexdigest()

def audit(path):
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist())
        manifest=json.loads(z.read('sha256_manifest.json'))
        assert all(n in names and sha(z.read(n)) == h for n,h in manifest.items()), 'payload SHA mismatch'
        assert sha(z.read('oracle.py')) == ORACLE_SHA, 'oracle changed after freeze'
        lines=z.read('source_blobs.txt').decode().splitlines()
        assert len(lines)==4
        assert {int(parts[0]):tuple(parts[1:]) for parts in (x.split() for x in lines)} == BLOBS
        data={}
        for mask in range(4):
            try:
                d=json.loads(z.read(f'variant_{mask}.json'))
                assert d['schema']=='lattice.run364.proxy_redirect.v1'
                cases=d['cases']
                assert len(cases)==13 and len({x['case'] for x in cases})==13
                assert sum(x['case'].startswith('T') for x in cases)==7
                assert sum(x['case'].startswith('C') for x in cases)==6
                data[mask]={x['case']:x['pass'] if x['status']=='OBSERVED' else None for x in cases}
            except (KeyError,ValueError,AssertionError,UnicodeDecodeError) as e:
                return {'status':'INCONCLUSIVE','reason':f'variant_{mask} unobserved: {type(e).__name__}',
                        'manifest_verified':len(manifest)}
        names=list(data[0])
        assert all(set(data[m])==set(names) for m in range(4))
        observed=sum(data[m][n] is not None for m in range(4) for n in names)
        if observed!=52:
            return {'status':'INCONCLUSIVE','reason':'pre-oracle failures or missing case observations',
                    'observed':observed,'manifest_verified':len(manifest)}
        targets=[n for n in names if n.startswith('T')]
        controls=[n for n in names if n.startswith('C')]
        scores={m:{'targets':sum(data[m][n] for n in targets),
                   'controls':sum(data[m][n] for n in controls)} for m in range(4)}
        positive=[n for n in targets if int(data[3][n])-int(data[2][n])-int(data[1][n])+int(data[0][n])>0]
        qualified=(scores[0]['targets']<7 and scores[0]['controls']==6
                   and scores[3]=={'targets':7,'controls':6}
                   and all(scores[m]!={'targets':7,'controls':6} for m in (1,2))
                   and bool(positive))
        return {'status':'QUALIFIED' if qualified else 'NOT_QUALIFIED',
                'observed':observed,'manifest_verified':len(manifest),
                'scores':scores,'positive_target_interactions':positive,
                'scope':'finite historical reference source only; not model inference'}

if __name__=='__main__':
    print(json.dumps(audit(Path(sys.argv[1])),sort_keys=True,indent=2))
