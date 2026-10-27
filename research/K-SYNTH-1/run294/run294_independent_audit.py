#!/usr/bin/env python3
"""Read-only independent audit: no import of compiler or experiment modules."""
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
read=lambda name:json.loads((HERE/name).read_text())
freeze=read('RUN294_PROSPECTIVE_FREEZE.json')
rows=read('RUN294_RAW_ADVERSARIAL.json')
fuzz=read('RUN294_RAW_FUZZ_PARITY.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((HERE/'run294_transaction_compiler.py').read_bytes())==freeze['compiler_sha256']
assert len(rows)==len(freeze['scenarios'])*len(freeze['representations'])==48
seen=set();groups={}
for r in rows:
    key=(r['case'],r['representation'])
    assert key not in seen,key
    seen.add(key)
    assert r['observed']==freeze['scenarios'][r['case']],r
    assert r['expected']==freeze['scenarios'][r['case']],r
    assert r['match'] is True and r['input_unchanged'] is True,r
    assert len(r['raw_sha256'])==64
    if r['observed']=='ACCEPT':
        assert len(r['canonical_sha256'])==64 and r['staged_file_sha256']
    else:assert r['canonical_sha256'] is None and r['staged_file_sha256'] is None
    groups.setdefault(r['case'],[]).append(r)
for case,group in groups.items():
    assert len(group)==2
    if freeze['scenarios'][case]=='ACCEPT':
        assert group[0]['canonical_sha256']==group[1]['canonical_sha256']
        assert group[0]['staged_file_sha256']==group[1]['staged_file_sha256']
assert len(fuzz)==freeze['random_valid_parity_trials']==1024
assert {r['trial'] for r in fuzz}==set(range(1024))
for r in fuzz:
    assert r['same'] is True
    assert r['ir_canonical']==r['python_canonical']
    assert r['ir_files']==r['python_files']
    assert r['edits'] in (1,2)
report={'schema':'ksynth1-run294-independent-readonly-audit-v1',
        'compiler_sha256':freeze['compiler_sha256'],
        'freeze_sha256':sha((HERE/'RUN294_PROSPECTIVE_FREEZE.json').read_bytes()),
        'adversarial_pairs':len(groups),'adversarial_rows':len(rows),
        'adversarial_mismatches':0,'input_snapshot_mutations':0,
        'accepted_scenario_representation_disagreements':0,
        'seeded_valid_pairs':len(fuzz),'seeded_parity_disagreements':0,
        'limitations':['Only compiler behavior on trusted fixtures, no model-generated edits','No crash-atomic multi-file commit, no concurrent hostile snapshot mutation','AST parse validates syntax only, not semantics or safety','One repository snapshot per test, no real repair qualification']}
(HERE/'RUN294_INDEPENDENT_AUDIT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2))
