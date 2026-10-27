#!/usr/bin/env python3
"""Read-only independent audit of ORIGINAL Run296 Click PR2956 artifact."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

EXPECTED_ZIP_SHA='ab457185c962f306d1c90592c645e24a6e84fce6b40806204c120e09f4858c58'
EXPECTED_RAW_SHA='650ed47b983f10874afb30fa1d782992d64d2cd39765386b67e72aab1cc2907d'
EXPECTED_IDS=['T1_default_true_present','T2_nonbool_env_off','T3_nonbool_env_on',
              'C1_bool_env_on','C2_bool_env_off','C3_bool_default_off',
              'C4_bool_cli_on','C5_nonbool_cli_on','C6_invalid_bool_env','C7_int_env_argument']

def sha(data):return hashlib.sha256(data).hexdigest()

def audit(zip_path):
    zip_path=Path(zip_path)
    assert sha(zip_path.read_bytes())==EXPECTED_ZIP_SHA,'original ZIP SHA mismatch'
    with zipfile.ZipFile(zip_path) as z:
        assert set(z.namelist())=={'RUN296_RAW.json','RUN296_RAW_SHA256.txt','RUN296_CONSOLE.log'}
        raw=z.read('RUN296_RAW.json')
        assert sha(raw)==EXPECTED_RAW_SHA,'raw SHA mismatch'
        assert z.read('RUN296_RAW_SHA256.txt').decode().strip()==EXPECTED_RAW_SHA+'  RUN296_RAW.json'
        d=json.loads(raw)
        assert d['protocol']=='RUN296_CLICK_PR2956_V1'
        assert [c['id'] for c in d['cases']]==EXPECTED_IDS
        assert len(d['cases'])==10
        results=d['results']
        assert set(results)=={'base','core_only','types_only','full'}
        counts={}
        by_id={}
        for name,part in results.items():
            assert part['returncode']==0
            rows=part['rows']
            assert len(rows)==10
            assert [r['id'] for r in rows]==EXPECTED_IDS
            assert [r['expected'] for r in rows]==[c['expected'] for c in d['cases']]
            assert all(r['pass']==(r['got']==r['expected']) for r in rows)
            assert part['pass_count']==sum(r['pass'] for r in rows)
            counts[name]={'total':sum(r['pass'] for r in rows),
                          'targets':sum(r['pass'] for r in rows[:3]),
                          'controls':sum(r['pass'] for r in rows[3:])}
            by_id[name]={r['id']:r for r in rows}
        h={name:part['source_sha256'] for name,part in results.items()}
        core='src/click/core.py'; types='src/click/types.py'
        assert h['base'][core]==h['types_only'][core]
        assert h['base'][types]==h['core_only'][types]
        assert h['full'][core]==h['core_only'][core]
        assert h['full'][types]==h['types_only'][types]
        assert h['base'][core]!=h['full'][core]
        assert h['base'][types]!=h['full'][types]
        full=counts['full'];base=counts['base'];co=counts['core_only'];ty=counts['types_only']
        qualified=(full['total']==10 and base['controls']==7 and base['targets']<3
                   and co['total']<10 and ty['total']<10)
        assert not qualified and d['prospective_qualified']==qualified
        failed_controls={name:[r['id'] for r in results[name]['rows'][3:] if not r['pass']]
                         for name in results}
        assert failed_controls['base']==['C2_bool_env_off','C6_invalid_bool_env']
        assert failed_controls['full']==['C6_invalid_bool_env']
        assert by_id['full']['C6_invalid_bool_env']['got']==['exit',1]
        report={'audit':'RUN296_ORIGINAL_READ_ONLY_V1',
                'original_zip_sha256':EXPECTED_ZIP_SHA,'original_raw_sha256':EXPECTED_RAW_SHA,
                'original_evidence_files':sorted(z.namelist()),
                'records_verified':40,'source_ablation_sha_relations_verified':6,
                'counts':counts,'failed_controls':failed_controls,
                'frozen_qualified':qualified,
                'conclusion':'NOT QUALIFIED: full fails C6; base fails C2 and C6; no criteria altered.',
                'posthoc_interpretation':'C6 exit-code expectation is incompatible with standalone_mode=False; do not rescore frozen protocol.'}
        return report

if __name__=='__main__':
    report=audit(sys.argv[1]); print(json.dumps(report,sort_keys=True,indent=2))
