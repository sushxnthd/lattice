#!/usr/bin/env python3
"""Read-only independent CPython replay; no imports from analyzer or runner."""
import hashlib,json,pathlib,subprocess,sys,collections
H=pathlib.Path(__file__).resolve().parent
M=H/'RUN308_FROZEN_SOURCES.json';R=H/'RUN308_ORIGINAL_313.json'
assert hashlib.sha256(M.read_bytes()).hexdigest()=='d0f9a6e07cdcb09b7a1e1db7ce2e71e06cf4de6a53d1259110afcf4672d0f4f8'
source=json.loads(M.read_text())['cases'];orig=json.loads(R.read_text());rows=orig['rows']
assert len(source)==len(rows)==384
expected_builtin={'direct_builtin_import','explicit_builtin_alias','builtin_via_intermediary',
                  'delete_exposes_builtin','wildcard_import_unknown'}
counts=collections.Counter(); failures=[]
for src,rec in zip(source,rows):
    assert src['id']==rec['id'] and src['scenario']==rec['scenario']
    assert hashlib.sha256(src['source'].encode()).hexdigest()==src['source_sha256']==rec['source_sha256']
    replay=subprocess.run([sys.executable,'-I','-S','-c',src['source']],capture_output=True,text=True,timeout=6)
    if (replay.returncode,replay.stdout,replay.stderr)!=(rec['returncode'],rec['stdout'],rec['stderr']):
        failures.append({'id':rec['id'],'reason':'original vs replay mismatch'})
    obj=json.loads(replay.stdout)
    if obj['is_builtin']!=(src['scenario'] in expected_builtin):
        failures.append({'id':rec['id'],'reason':'scenario identity mismatch'})
    if obj['is_builtin'] and obj['value']!=3: failures.append({'id':rec['id'],'reason':'builtin wrong value'})
    if obj['is_builtin'] and rec['new']=='NOT_KNOWN_TARGET': failures.append({'id':rec['id'],'reason':'corrected false negative'})
    counts[(src['scenario'],rec['old'],rec['new'],obj['is_builtin'])]+=1
summary={'schema':'run308-independent-audit-v1','python':sys.version,
         'manifest_sha256':hashlib.sha256(M.read_bytes()).hexdigest(),
         'original_sha256':hashlib.sha256(R.read_bytes()).hexdigest(),
         'replayed':len(rows),'discrepancies':len(failures),'failures':failures,
         'matrix':[{'scenario':s,'old':o,'new':n,'is_builtin':b,'count':c} for (s,o,n,b),c in sorted(counts.items())]}
Q=H/'RUN308_INDEPENDENT_AUDIT.json';Q.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('matrix','failures')},indent=2))
print('RESULT_SHA256',hashlib.sha256(Q.read_bytes()).hexdigest())
assert not failures
