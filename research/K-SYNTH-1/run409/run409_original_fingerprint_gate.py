#!/usr/bin/env python3
"""Run409 original-artifact fingerprint gate. Read-only; no oracle imports."""
import hashlib, json, sys, zipfile
from pathlib import Path

PINS = {
 'control903': ('b36bd8c58bf7a31ed77b6d190403116a13f84d234b02b1d67b9caf01c20b79ad',
                'a7d58d7a21b78581e636bbbdea13c66ad1657c1e','9.0.3'),
 'regression911': ('43d1cf6df8638915580ad8585663ddf3a7421ad98f32ea46536bc8989c770282',
                   'cf470ec0bf7eb89cd97dd56df4859eae5db46447','9.1.1'),
}
ORACLE='56ea237e58484cdb0e066acc02c0cb1982d657d91cc9df956f9300e17e2bd366'
FILES={'run408_pytest14992_oracle.py','run408_pytest14992_raw.jsonl',
       'run408_pytest14992_summary.json','run408_cloud_environment.json'}
sha=lambda x:hashlib.sha256(x).hexdigest()

def audit(label,path):
    expected,git,ver=PINS[label]
    assert sha(path.read_bytes())==expected, 'Original ZIP hash mismatch'
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist())==FILES and len(z.namelist())==4
        blobs={n:z.read(n) for n in FILES}
    assert sha(blobs['run408_pytest14992_oracle.py'])==ORACLE
    env=json.loads(blobs['run408_cloud_environment.json'])
    summary=json.loads(blobs['run408_pytest14992_summary.json'])
    rows=[json.loads(x) for x in blobs['run408_pytest14992_raw.jsonl'].splitlines()]
    assert env['matrix_source']==label
    assert env['source_git_head']==env['pinned_git_sha']==git
    assert env['pytest_version']==summary['installed_pytest']==ver
    for n in FILES-{'run408_cloud_environment.json'}:
        assert env['file_sha256'][n]==sha(blobs[n])
    assert summary['sha256']==sha(blobs['run408_pytest14992_raw.jsonl'])
    assert len(rows)==12
    for i,r in enumerate(rows):
        assert r['case']==i
        assert r['group']==('target_public' if i<3 else 'target_heldout' if i<6 else 'control')
        expect=(label=='control903' or i>=6)
        assert r['passed'] is expect
        assert r['returncode']==(0 if expect else 1)
        assert ('1 passed' if expect else '1 failed') in r['stdout']
    pairs=lambda seq:{(r['conftest_sha256'],r['test_sha256']) for r in seq}
    pub,held=pairs(rows[:3]),pairs(rows[3:6])
    assert len(pub)==len(held)==2 and pub==held
    assert len(pairs(rows))==4
    return {'version':ver,'targets_pass':sum(r['passed'] for r in rows[:6]),
            'controls_pass':sum(r['passed'] for r in rows[6:]),
            'unique_target_pairs':len(pub),'new_heldout_pairs':len(held-pub)}

if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: python run409_original_fingerprint_gate.py <control903.zip> <regression911.zip>')
    result={'control903':audit('control903',Path(sys.argv[1])),
            'regression911':audit('regression911',Path(sys.argv[2]))}
    print(json.dumps(result,indent=2))
