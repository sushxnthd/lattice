#!/usr/bin/env python3
"""Read-only audit of original Run280 source-equivalent cloud artifact ZIP."""
import argparse,hashlib,json,pathlib,zipfile
from run280_transport_alias import BASE,ORIGINAL_REF,MERGE_REF,ORIGINAL_BLOBS
EXPECTED={'baseline':{'target':0,'control':6},'sync_only':{'target':2,'control':6},'async_only':{'target':2,'control':6},'full_reference':{'target':4,'control':6}}
CASES=['T_sync_limit1_active2','T_sync_limit2_active3','T_async_limit1_active2','T_async_limit2_active3','C_sync_no_keepalive','C_sync_one_idle','C_sync_reuse','C_async_no_keepalive','C_async_one_idle','C_async_reuse']
def sha(b):return hashlib.sha256(b).hexdigest()
def audit(path):
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist())
        needed={'raw_results.json','frozen_oracle.py','sha256_manifest.json','transport_alias_provenance.json','FROZEN_RUN279.json','ARTIFACT_SHA256SUMS'}
        assert needed<=names,needed-names
        manifest=json.loads(z.read('sha256_manifest.json'))
        for name,h in manifest.items():assert sha(z.read(name))==h,(name,h)
        for line in z.read('ARTIFACT_SHA256SUMS').decode().splitlines():
            h,name=line.split(None,1);name=name.lstrip('*')
            assert sha(z.read(name))==h,(name,h)
        p=json.loads(z.read('transport_alias_provenance.json'))
        assert p['original_frozen_ref']==ORIGINAL_REF and p['reachable_merge_ref']==MERGE_REF and p['base_commit']==BASE
        assert p['production_git_blobs']==ORIGINAL_BLOBS
        frozen=json.loads(z.read('FROZEN_RUN279.json'))
        assert frozen['base']==BASE and frozen['ref']==ORIGINAL_REF
        assert frozen['cases']==CASES and frozen['expected_pass_counts']==EXPECTED
        r=json.loads(z.read('raw_results.json'))
        assert r['base_commit']==BASE and r['reference_commit']==MERGE_REF
        assert r['predeclared_expected_counts']=={k:[v['target'],v['control']] for k,v in EXPECTED.items()}
        assert r['oracle_sha256']==sha(z.read('frozen_oracle.py'))
        assert len(r['records'])==4
        records={x['configuration']:x for x in r['records']}
        assert set(records)==set(EXPECTED)
        for name,record in records.items():
            assert [x['case'] for x in record['rows']]==CASES
            for f in ORIGINAL_BLOBS:
                ref=(name=='full_reference' or (name=='sync_only' and '_sync/' in f) or (name=='async_only' and '_async/' in f))
                assert record['source_sha256'][f]==r['source_sha256'][f]['reference_sha256' if ref else 'base_sha256']
        counts={name:{'target':sum(bool(x['pass']) for x in record['rows'] if x['case'].startswith('T_')),'control':sum(bool(x['pass']) for x in record['rows'] if x['case'].startswith('C_'))} for name,record in records.items()}
        assert {name:{'target':r['counts'][name]['target'],'control':r['counts'][name]['control']} for name in records}==counts
        assert r['qualified']==(counts==EXPECTED)
        return {'artifact_sha256':sha(pathlib.Path(path).read_bytes()),'entries':len(names),'manifest_entries':len(manifest),'rows':40,'counts':counts,'qualified':r['qualified'],'original_ref':ORIGINAL_REF,'transport_ref':MERGE_REF}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('zip',type=pathlib.Path);a=p.parse_args();print(json.dumps(audit(a.zip),sort_keys=True))
