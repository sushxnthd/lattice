#!/usr/bin/env python3
"""Execute frozen trusted sources in isolated CPython subprocesses, never model code."""
import hashlib,json,pathlib,subprocess,sys
from run307_versioned_transfer import classify

HERE=pathlib.Path(__file__).resolve().parent
manifest=HERE/'RUN307_FROZEN_SOURCES.json'
records=json.loads(manifest.read_text())['cases']
version=f'{sys.version_info.major}.{sys.version_info.minor}'
if version not in ('3.13','3.14'):
    raise SystemExit('UNSUPPORTED_RUNTIME_UNKNOWN: '+version)
results=[]
for rec in records:
    src=rec['source']
    assert hashlib.sha256(src.encode()).hexdigest()==rec['source_sha256']
    cp=subprocess.run([sys.executable,'-I','-S','-c',src],capture_output=True,text=True,timeout=8)
    if cp.returncode:
        raise RuntimeError((rec['id'],cp.stderr))
    observation=json.loads(cp.stdout.strip())
    expected=rec['expected'][version]
    facts=classify(src,version)
    assert observation==expected,(rec['id'],observation,expected)
    if observation['observed']==3 and facts['final_len']=='NOT_KNOWN_TARGET':
        raise AssertionError(('false negative',rec['id'],facts))
    # The subset has no unsupported effects. An explicit UNKNOWN is acceptable.
    assert facts['final_len'] in ('UNKNOWN_DYNAMIC','NOT_KNOWN_TARGET')
    results.append({'id':rec['id'],'source_sha256':rec['source_sha256'],
                    'observation':observation,'classification':facts['final_len'],
                    'annotation_effect_events':sum(x['event']=='UNKNOWN_ANNOTATION_EFFECT' for x in facts['events']),
                    'mode':facts['mode'],'status':facts['status']})
summary={'schema':'run307-original-functional-v1','python':sys.version,'version':version,
         'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
         'count':len(results),'restored_builtin':sum(x['observation']['observed']==3 for x in results),
         'definite_false_negatives':sum(x['observation']['observed']==3 and x['classification']=='NOT_KNOWN_TARGET' for x in results),
         'unknown':sum(x['classification']=='UNKNOWN_DYNAMIC' for x in results),
         'annotation_effect_events':sum(x['annotation_effect_events'] for x in results),
         'results':results}
p=HERE/f'RUN307_ORIGINAL_{version.replace(".","")}.json'
p.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
print('RESULT_SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
