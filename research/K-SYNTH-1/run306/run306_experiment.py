#!/usr/bin/env python3
"""Frozen trusted CPython alias-mutation experiment. No model output executes."""
import ast,builtins,hashlib,json,pathlib,sys
from run305_annotation_transfer import extract as old_extract
from run306_effect_aware_transfer import extract as new_extract
HERE=pathlib.Path(__file__).resolve().parent
SITES=('annotation','default','decorator')
EFFECTS=('restore','noop')
MODES=('eager','postponed')
VARIANTS=32

def canonical(o):return (json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()

def source(site,effect,mode,i):
    future='from __future__ import annotations\n' if mode=='postponed' else ''
    mutation="    globals()['len'] = builtins.len\n" if effect=='restore' else ''
    ret='    return lambda f: f\n' if site=='decorator' else '    return int\n'
    declaration={
        'annotation':'def f(x: install()):\n    pass\n',
        'default':'def f(x=install()):\n    pass\n',
        'decorator':'@install()\ndef f(x):\n    pass\n'}[site]
    k=1+i%13
    return (future+'import builtins\nlen = lambda xs: -777\ndef install():\n'+
            mutation+ret+declaration+f'observed = len([{i}] * {k})\n'+
            'runtime_is_builtin = (len is builtins.len)\n')

def cases():
    out=[]
    for site in SITES:
      for effect in EFFECTS:
       for mode in MODES:
        for i in range(VARIANTS):
         src=source(site,effect,mode,i)
         ast.parse(src)
         out.append(dict(id=f'{site}_{effect}_{mode}_{i:02d}',site=site,effect=effect,
             mode=mode,variant=i,source=src,source_sha256=sha(src.encode())))
    return out

def freeze():
    data=dict(schema='ksynth1-run306-frozen-v1',python_version=sys.version.split()[0],
              protocol_commit='f6d2a9c4c59d192a7642962668c385be83e4b53f',
              independence='12 template families x 32 correlated variants',cases=cases())
    p=HERE/'RUN306_FROZEN_SOURCES.json';p.write_bytes(canonical(data))
    print('FROZEN',len(data['cases']),'SHA256',sha(p.read_bytes()))

def runtime(src):
    ns={'__builtins__':builtins.__dict__,'__name__':'__run306_trusted__'}
    exec(compile(src,'<run306-trusted>','exec'),ns,ns)
    return dict(observed=ns['observed'],runtime_is_builtin=ns['runtime_is_builtin'])

def classify(extractor,src):
    calls=extractor(src)['calls']
    rows=[c for c in calls if c['name']=='len' and c['line']==len(src.splitlines())-1]
    assert len(rows)==1,(src,rows)
    return rows[0]['classification'],rows[0]['provenance']

def execute():
    frozen=json.loads((HERE/'RUN306_FROZEN_SOURCES.json').read_text())
    assert frozen['cases']==cases(),'source freeze mismatch'
    records=[]
    for c in frozen['cases']:
        rt=runtime(c['source'])
        old,op=classify(old_extract,c['source'])
        new,np=classify(new_extract,c['source'])
        executed=c['site']!='annotation' or c['mode']=='eager'
        expected_builtin=c['effect']=='restore' and executed
        expected_value=(1+c['variant']%13) if expected_builtin else -777
        records.append(dict(id=c['id'],source_sha256=c['source_sha256'],
            expected_builtin=expected_builtin,expected_value=expected_value,
            runtime=rt,old=old,new=new,old_provenance=op,new_provenance=np,
            old_false_negative=expected_builtin and old=='NOT_KNOWN_TARGET',
            new_false_negative=expected_builtin and new=='NOT_KNOWN_TARGET',
            runtime_match=rt==dict(observed=expected_value,runtime_is_builtin=expected_builtin)))
    stats=dict(n=len(records),families=12,old_false_negatives=sum(x['old_false_negative'] for x in records),
               new_false_negatives=sum(x['new_false_negative'] for x in records),
               runtime_matches=sum(x['runtime_match'] for x in records),
               new_unknown=sum(x['new']=='UNKNOWN_DYNAMIC' for x in records),
               old_unknown=sum(x['old']=='UNKNOWN_DYNAMIC' for x in records))
    out=dict(schema='ksynth1-run306-raw-v1',frozen_sha256=sha((HERE/'RUN306_FROZEN_SOURCES.json').read_bytes()),
             python_version=sys.version.split()[0],stats=stats,records=records)
    p=HERE/'RUN306_RAW_FUNCTIONAL.json';p.write_bytes(canonical(out))
    print('RESULT',json.dumps(stats,sort_keys=True),'SHA256',sha(p.read_bytes()))
    assert stats['runtime_matches']==len(records)
    assert stats['new_false_negatives']==0
    assert stats['old_false_negatives']>0

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='freeze':freeze()
    elif mode=='execute':execute()
    else:raise SystemExit('freeze|execute')
