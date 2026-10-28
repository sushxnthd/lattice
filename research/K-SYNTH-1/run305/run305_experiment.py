#!/usr/bin/env python3
"""Run305: prospective source-only annotation MAY-call coverage witness.

This is a bounded CPython module-definition experiment with trusted source
fixtures. It neither executes model output nor establishes general soundness.
"""
import argparse
import ast
import builtins
import hashlib
import json
import pathlib
import random
import sys
from collections import Counter
from run304_shadowing_transfer import extract as legacy_extract
from run305_annotation_transfer import extract as corrected_extract

HERE = pathlib.Path(__file__).resolve().parent
SEED = 30520261028
TEMPLATES = [
    ('pos_len', '', 'def f(x: len([N])): pass', ['len'], False),
    ('pos_sum', '', 'def f(x: sum([N])): pass', ['sum'], False),
    ('posonly_len', '', 'def f(x: len([N]), /): pass', ['len'], False),
    ('kwonly_sum', '', 'def f(*, x: sum([N])): pass', ['sum'], False),
    ('vararg_len', '', 'def f(*args: len([N])): pass', ['len'], False),
    ('varkw_sum', '', 'def f(**kwargs: sum([N])): pass', ['sum'], False),
    ('return_len', '', 'def f() -> len([N]): pass', ['len'], False),
    ('return_sum', '', 'def f() -> sum([N]): pass', ['sum'], False),
    ('two_annotations', '', 'def f(x: len([N]), y: sum([N])): pass', ['len','sum'], False),
    ('async_len', '', 'async def f(x: len([N])): pass', ['len'], False),
    ('default_and_annot', '', 'def f(x: len([N]) = sum([N])): pass', ['sum','len'], False),
    ('named_len_prebinding', '', 'def len(x: len([N])): pass', ['len'], False),
    ('alias_import', 'from builtins import len as L\n', 'def f(x: L([N])): pass', ['len'], False),
    ('quoted_annotation', '', "def f(x: 'len([N])'): pass", [], False),
    ('future_annotation', 'from __future__ import annotations\n', 'def f(x: len([N])) -> sum([N]): pass', [], True),
    ('future_default', 'from __future__ import annotations\n', 'def f(x: len([N]) = sum([N])): pass', ['sum'], True),
]

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')

def sha(b):return hashlib.sha256(b).hexdigest()

def generate():
    rng=random.Random(SEED)
    cases=[]
    for tid,prefix,stmt,expected,future in TEMPLATES:
        for variant in range(64):
            n=rng.randrange(0,1000000)
            src=prefix+stmt.replace('[N]',f'[{n}]')+'\n'
            ast.parse(src)
            cases.append(dict(id=f'{tid}_{variant:02d}',template=tid,variant=variant,
                source=src,source_sha256=sha(src.encode()),expected_calls=sorted(expected),
                future_annotations=future))
    return cases

def freeze():
    cases=generate()
    out=dict(schema='ksynth1-run305-frozen-annotation-v1',seed=SEED,
        python_executable_version=sys.version.split()[0],
        independence='16 correlated templates x 64 variants; not independent repairs',
        scope='trusted top-level FunctionDef/AsyncFunctionDef, direct builtins and builtins alias, no dynamic rebinding',
        cases=cases)
    dest=HERE/'RUN305_FROZEN_SOURCES.json'
    dest.write_bytes(canonical(out)+b'\n')
    print('FROZEN',len(cases),'SHA256',sha(dest.read_bytes()))

def trace(source):
    code=compile(source,'<run305-trusted-fixture>','exec')
    calls=[]
    def profiler(frame,event,arg):
        if event=='c_call':
            if arg is builtins.len:calls.append('len')
            elif arg is builtins.sum:calls.append('sum')
    env={'__builtins__':builtins.__dict__,'__name__':'__run305_fixture__'}
    previous=sys.getprofile()
    try:
        sys.setprofile(profiler)
        exec(code,env,env)
    finally:
        sys.setprofile(previous)
    return sorted(calls)

def analyzed(extractor,source):
    rows=extractor(source)['calls']
    return [r for r in rows if r['classification']=='MAY_TARGET']

def execute():
    frozen=json.loads((HERE/'RUN305_FROZEN_SOURCES.json').read_text())
    assert frozen['cases']==generate(), 'Frozen sources do not match registered generator'
    results=[]
    for c in frozen['cases']:
        observed=trace(c['source'])
        old=analyzed(legacy_extract,c['source'])
        new=analyzed(corrected_extract,c['source'])
        def recognized(rows):
            return sorted(next(iter(r['provenance']['candidates'])) for r in rows if len(r['provenance']['candidates'])==1)
        old_rec=recognized(old);new_rec=recognized(new)
        results.append(dict(id=c['id'],template=c['template'],source_sha256=c['source_sha256'],
            expected_calls=c['expected_calls'],observed_calls=observed,
            legacy_calls=old_rec,corrected_calls=new_rec,
            observed_match=(observed==c['expected_calls']),
            legacy_match=(old_rec==observed),corrected_match=(new_rec==observed),
            legacy_rows=old,corrected_rows=new))
    stats={k:sum(bool(r[k]) for r in results) for k in ('observed_match','legacy_match','corrected_match')}
    stats.update(n=len(results), templates=len(TEMPLATES),
        legacy_missing=sum(len(Counter(r['observed_calls'])-Counter(r['legacy_calls'])) for r in results),
        corrected_missing=sum(len(Counter(r['observed_calls'])-Counter(r['corrected_calls'])) for r in results))
    out=dict(schema='ksynth1-run305-raw-v1',frozen_sha256=sha((HERE/'RUN305_FROZEN_SOURCES.json').read_bytes()),
        stats=stats,records=results)
    path=HERE/'RUN305_RAW_FUNCTIONAL.json'
    path.write_bytes(canonical(out)+b'\n')
    print('RESULT',json.dumps(stats,sort_keys=True),'SHA256',sha(path.read_bytes()))
    if stats['observed_match']!=len(results) or stats['corrected_match']!=len(results):
        raise SystemExit('FROZEN WITNESS FAILURE')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=('freeze','execute'));a=p.parse_args()
    if a.mode=='freeze':freeze()
    else:execute()
