#!/usr/bin/env python3
"""Original prospective trusted CPython execution with both frozen analyzers."""
import hashlib,json,pathlib,subprocess,sys
from run307_versioned_transfer import classify as old
from run308_binding_transfer import classify as new
H=pathlib.Path(__file__).resolve().parent
P=H/'RUN308_FROZEN_SOURCES.json'
EXPECTED='d0f9a6e07cdcb09b7a1e1db7ce2e71e06cf4de6a53d1259110afcf4672d0f4f8'
assert hashlib.sha256(P.read_bytes()).hexdigest()==EXPECTED
assert sys.version_info[:2]==(3,13),sys.version
rows=[]
for case in json.loads(P.read_text())['cases']:
    src=case['source']
    assert hashlib.sha256(src.encode()).hexdigest()==case['source_sha256']
    cp=subprocess.run([sys.executable,'-I','-S','-c',src],capture_output=True,text=True,timeout=6)
    obs=json.loads(cp.stdout.strip()) if cp.returncode==0 else None
    o=old(src,'3.13')
    n=new(src,'3.13')
    row={'id':case['id'],'scenario':case['scenario'],'source_sha256':case['source_sha256'],
         'returncode':cp.returncode,'stderr':cp.stderr,'stdout':cp.stdout,
         'observation':obs,'old':o['final_len'],'new':n['final_len'],
         'new_status':n['status']}
    rows.append(row)
summary={'schema':'run308-original-v1','python':sys.version,'manifest_sha256':EXPECTED,
         'count':len(rows),'errors':sum(r['returncode']!=0 for r in rows),
         'builtin':sum(bool(r['observation'] and r['observation']['is_builtin']) for r in rows),
         'old_false_negative':sum(bool(r['observation'] and r['observation']['is_builtin'] and r['old']=='NOT_KNOWN_TARGET') for r in rows),
         'new_false_negative':sum(bool(r['observation'] and r['observation']['is_builtin'] and r['new']=='NOT_KNOWN_TARGET') for r in rows),
         'new_unknown':sum(r['new']=='UNKNOWN_DYNAMIC' for r in rows),
         'rows':rows}
Q=H/'RUN308_ORIGINAL_313.json';Q.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
print('RESULT_SHA256',hashlib.sha256(Q.read_bytes()).hexdigest())
assert summary['count']==384 and summary['errors']==0
assert summary['old_false_negative']>0 and summary['new_false_negative']==0
