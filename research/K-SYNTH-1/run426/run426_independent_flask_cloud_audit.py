"""Independent read-only audit of original/corrected Run426 cloud raw JSON.

No imports from Flask or the original compiler/oracle runner.
"""
import argparse,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('raw',nargs='?',default='original_cloud/run426_cloud_raw.json')
a=p.parse_args();root=pathlib.Path(__file__).resolve().parent
raw=pathlib.Path(a.raw);raw=raw if raw.is_absolute() else root/raw
x=json.loads(raw.read_text())
assert x['base']=='330123258e8c3dc391cbe55ab1ed94891ca83af3'
assert x['reference']=='c2705ffd9ce1dc8476cb29eaf5ff5d4c719852d9'
paths=x['production_changed'];assert len(paths)==11 and len(set(paths))==11
assert all(z.startswith('src/flask/') and z.endswith('.py') for z in paths)
assert len(x['results'])==13
base=x['results']['base']['data'];ref=x['results']['reference']['data']
assert base['passed']==8 and base['total']==11
assert ref['passed']==ref['total']==11
assert {k for k,v in base['results'].items() if not v['pass']}=={
 'positive_start_before_teardown','positive_teardown_once','control_repeated_teardown'}
assert all(v['pass'] for v in ref['results'].values())
assert x['reference_passes'] is True and x['qualified'] is False
assert x['importable_leave_one_out_failures']==[]
import_fail=[];importable=[];source_checks=0
base_sha=x['results']['base'].get('source_sha256')
ref_sha=x['results']['reference'].get('source_sha256')
if base_sha or ref_sha:
 assert base_sha and ref_sha and set(base_sha)==set(ref_sha)==set(paths)
for path in paths:
 label='without_'+path.replace('/','_')
 row=x['results'][label];data=row['data']
 if data is None:
  assert row['exit']!=0 and 'ImportError' in row['stderr']
  import_fail.append(path)
 else:
  assert row['exit']==0 and data['passed']==data['total']==11
  importable.append(path)
 if base_sha:
  assert set(row['source_sha256'])==set(paths)
  for q,h in ref_sha.items():
   assert row['source_sha256'][q]==(base_sha[q] if q==path else h)
   source_checks+=1
assert len(import_fail)==4 and len(importable)==7
assert set(import_fail)=={'src/flask/app.py','src/flask/ctx.py',
                         'src/flask/helpers.py','src/flask/templating.py'}
print(json.dumps({'original_or_corrected_raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
 'reference':'11/11','base':'8/11','importable_ablations_passing':'7/7',
 'unimportable_ablations':len(import_fail),'qualified':False,
 'observed_frozen_oracle_checks':9*11,'source_hash_parity_checks':source_checks,
 'source_receipts_present':bool(base_sha)},sort_keys=True))
