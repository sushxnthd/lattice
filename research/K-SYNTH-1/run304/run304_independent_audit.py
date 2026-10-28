#!/usr/bin/env python3
"""Independent read-only audit of Run304, without importing either analyzer.

Executes only SHA-pinned trusted hardcoded template sources, not model output.
Checks profiler builtin identities, values, source hashes and frozen decisions.
"""
import ast
import builtins
import collections
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()

def expected_value(name, seed):
    if name.startswith('shadow_'):
        variant = int(name.rsplit('_',1)[-1])
    elif name.startswith('control_'):
        variant = int(name.rsplit('_',1)[-1])
    else:
        target = 'len' if '_len_' in name else 'sum'
        n = 2 if name.endswith('_0') else 3
        return n if target=='len' else n*seed + n*(n-1)//2
    return (seed,seed+1,seed*2,seed-1)[variant]

def audit():
    manifest = json.loads((ROOT/'RUN304_FROZEN_SOURCES.json').read_text())
    freeze = json.loads((ROOT/'RUN304_PROSPECTIVE_FREEZE.json').read_text())
    raw = json.loads((ROOT/'RUN304_RAW_FUNCTIONAL.json').read_text())
    failures=[];counts=collections.Counter(); different=0
    if hashlib.sha256(canonical(manifest)).hexdigest()!=freeze['source_manifest_sha256']:
        failures.append('manifest root mismatch')
    if raw['source_manifest_sha256']!=freeze['source_manifest_sha256']:
        failures.append('result root mismatch')
    rows={r['id']:r for r in raw['rows']}
    if len(rows)!=len(raw['rows']) or len(rows)!=len(manifest['records']):
        failures.append('missing or duplicate rows')
    for rec in manifest['records']:
        name=rec['id']; row=rows.get(name)
        if row is None:
            failures.append('missing '+name);continue
        if hashlib.sha256(rec['source'].encode()).hexdigest()!=rec['source_sha256'] or row['source_sha256']!=rec['source_sha256']:
            failures.append('source hash '+name);continue
        tree=ast.parse(rec['source'])
        calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==rec['call_name']]
        if len(calls)!=1:
            failures.append('call grammar '+name);continue
        events=[]; filename='<ksynth-independent-'+name+'>'
        def trace(frame,event,arg):
            if frame.f_code.co_filename==filename and event=='c_call':
                if arg is builtins.len:events.append('len')
                if arg is builtins.sum:events.append('sum')
        ns={'__builtins__':builtins.__dict__}
        code=compile(rec['source'],filename,'exec')
        try:
            sys.setprofile(trace)
            exec(code,ns,ns)
        finally:
            sys.setprofile(None)
        expected=freeze['expected_groups'][rec['group']]
        expected_events=[] if expected['runtime_target_calls']==0 else [rec['target']]
        if events!=expected_events or events!=row['observed_builtin_calls']:
            failures.append('builtin identity '+name)
        if ns.get('result')!=expected_value(rec['template'],rec['seed']) or ns.get('result')!=row['result']:
            failures.append('value '+name)
        if row['old']!=expected['old'] or row['new']!=expected['new'] or not row['passed']:
            failures.append('classification '+name)
        if rec['group']=='shadow':
            if row['old_provenance']['candidates']!=[rec['target']] or row['new_provenance']['candidates'] or row['new_provenance']['unknown']:
                failures.append('shadow provenance '+name)
        if rec['group']=='decorated':
            if not row['old_provenance']['unknown'] or not row['new_provenance']['unknown']:
                failures.append('decorator unknown '+name)
        counts[rec['group']]+=1
        different += (row['old']!=row['new'])
    for group, expect in freeze['expected_groups'].items():
        if counts[group]!=expect['n']:failures.append('group count '+group)
    if different!=512:failures.append('unexpected precision delta '+str(different))
    report={'schema':'ksynth1-run304-independent-audit-v1','source_manifest_sha256':freeze['source_manifest_sha256'],
            'records_checked':sum(counts.values()),'group_counts':dict(counts),
            'classification_differences':different,'discrepancies':len(failures),
            'failure_examples':failures[:30], 'independence':'does not import source analyzer or primary experiment'}
    (ROOT/'RUN304_INDEPENDENT_AUDIT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))
    if failures:raise SystemExit(1)

if __name__=='__main__':audit()
