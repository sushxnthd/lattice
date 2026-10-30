#!/usr/bin/env python3
"""Original urllib3 2x2 factorial sharp bounds with one ABI-blocked source arm."""
import hashlib, itertools, json, sys, zipfile
from pathlib import Path

EXPECTED_ORIGINAL_SHA='09a787735ea2689c669002fa002034c8231f74db37203380ccd2b0f7eacb4314'

def analyze(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_ORIGINAL_SHA
    with zipfile.ZipFile(path) as z:
        manifest=json.loads(z.read('sha256_manifest.json'))
        assert len(manifest)==12
        assert all(hashlib.sha256(z.read(n)).hexdigest()==v for n,v in manifest.items())
        data={}
        for mask in (0,1,3):
            rows=json.loads(z.read(f'variant_{mask}.json'))['cases']
            assert len(rows)==13 and all(r['status']=='OBSERVED' for r in rows)
            data[mask]={r['case']:r['pass'] for r in rows}
        assert not z.read('variant_2.json')
        assert b"cannot import name '_is_same_host'" in z.read('variant_2.stderr')
    assert all(set(data[m])==set(data[0]) for m in data)
    records=[]
    for case in data[0]:
        a,b,c=(int(data[m][case]) for m in (0,1,3))
        # Interaction: f11 - f10 - f01 + f00, with f01 unknown in {0,1}.
        low=c-b-1+a
        high=c-b+a
        assert low==min(c-b-u+a for u in (0,1))
        assert high==max(c-b-u+a for u in (0,1))
        records.append({'case':case,'observed_base':a,'observed_connectionpool_only':b,
                        'observed_full':c,'poolmanager_only':'UNKNOWN_IMPORT_FAILURE',
                        'interaction_lower':low,'interaction_upper':high,
                        'naive_missing_as_failure_interaction':high})
    assert len(records)==13
    assert all(r['interaction_lower']==0 and r['interaction_upper']==1 for r in records)
    return {'schema':'lattice.run364.proxy_missingness.v1','original_zip_sha256':EXPECTED_ORIGINAL_SHA,
            'verified_original_payloads':12,'observed_cases':39,'missing_preoracle_cases':13,
            'sharp_interaction_bounds_per_case':[0,1],
            'naive_zero_imputation_positive_interactions':13,
            'naive_zero_imputation_false_positive_controls':6,
            'original_qualification':'INCONCLUSIVE','cases':records}

if __name__=='__main__':
    print(json.dumps(analyze(Path(sys.argv[1])),sort_keys=True,indent=2))
