#!/usr/bin/env python3
"""Independent, read-only audit of original Run280 cloud ZIP. No scientific retuning."""
import argparse, hashlib, io, json, pathlib, zipfile
EXPECTED_ZIP_SHA='2f4b9a501d3cf9c4bcfa893c94adf34c1beba588a2135ecf283dec5f80b25aa2'
EXPECTED_FROZEN_SHA='769d660400e39511bfbc80c93b2c9688ca555fc037903f80d82436b0895f60cd'
EXPECTED_ORACLE_SHA='6d1fbb5d18aa7b58da802fb34f43ec6a5efcfc7a3842049df2fb02f18d2e2e96'
EXPECTED_RAW_SHA='cf6d50774a416db2f3adc92c5b279998241d2610cb13dc45f73385b08b004e2a'

def sha(b): return hashlib.sha256(b).hexdigest()
def audit(path):
    path=pathlib.Path(path)
    assert sha(path.read_bytes())==EXPECTED_ZIP_SHA,'original cloud ZIP digest mismatch'
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        assert len(names)==len(set(names))==11
        assert all(not x.startswith('/') and '..' not in pathlib.PurePosixPath(x).parts for x in names)
        raw={x:z.read(x) for x in names}
    manifest=raw['ARTIFACT_SHA256SUMS'].decode().splitlines()
    assert len(manifest)==10
    for line in manifest:
        digest,name=line.split('  ',1)
        assert name in raw and sha(raw[name])==digest,(name,digest)
    assert sha(raw['FROZEN_RUN279.json'])==EXPECTED_FROZEN_SHA
    assert sha(raw['frozen_oracle.py'])==EXPECTED_ORACLE_SHA
    assert sha(raw['raw_results.json'])==EXPECTED_RAW_SHA
    spec=json.loads(raw['FROZEN_RUN279.json'])
    data=json.loads(raw['raw_results.json'])
    assert data['oracle_sha256']==EXPECTED_ORACLE_SHA
    assert data['predeclared_expected_counts']=={'baseline':[0,6],'sync_only':[2,6],'async_only':[2,6],'full_reference':[4,6]}
    assert data['qualified'] is False
    assert len(data['records'])==4
    rows=[row for record in data['records'] for row in record['rows']]
    assert len(rows)==40
    assert len({row['case'] for row in rows})==10
    assert all(row['observed'] is None and row['error']=='HARNESS_EXIT:1' and not row['pass'] for row in rows)
    assert all("ModuleNotFoundError: No module named 'certifi'" in record['stderr'] for record in data['records'])
    assert all(record['returncode']==1 for record in data['records'])
    assert spec['expected_pass_counts']['full_reference']=={'target':4,'control':6}
    return {'zip_sha256':EXPECTED_ZIP_SHA,'entries':len(raw),'manifest_entries':len(manifest),
            'frozen_oracle_sha256':EXPECTED_ORACLE_SHA,'frozen_spec_sha256':EXPECTED_FROZEN_SHA,
            'raw_results_sha256':EXPECTED_RAW_SHA,'configurations':4,'case_records':40,
            'actual_functional_checks_executed':0,'pre_import_failures':4,
            'root_cause':'missing certifi, declared in pinned upstream pyproject.toml',
            'qualified':False,'interpretation':'All 40 are censored pre-oracle; not 40 failed functional checks.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('zip');p.add_argument('--out');a=p.parse_args()
    x=audit(a.zip);s=json.dumps(x,indent=2,sort_keys=True)+'\n'
    if a.out:pathlib.Path(a.out).write_text(s)
    print(s)
