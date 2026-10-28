#!/usr/bin/env python3
"""Prospectively frozen, trusted-source Python builtin shadowing experiment.

Usage: python run304_experiment.py freeze|run
Only hardcoded trusted templates are executed, never model-generated code.
"""
import ast
import builtins
import hashlib
import json
import pathlib
import sys
from run301_decorator_transfer import extract as old_extract
from run304_shadowing_transfer import extract as new_extract

HERE = pathlib.Path(__file__).resolve().parent
SEEDS = range(64)

# 24 distinct syntactic templates; 64 correlated seed variants each.
TEMPLATES = []
for target in ('len', 'sum'):
    for variant in range(4):
        body = ('x[0]', 'x[0] + 1', 'x[0] * 2', 'x[0] - 1')[variant]
        TEMPLATES.append((f'shadow_{target}_{variant}', 'shadow', target,
            f'def {target}(x):\n    return {body}\nresult = {target}([{{s}}, {{s}}+1])\n', target))
for target in ('len', 'sum'):
    for variant in range(2):
        seq = '[{s}, {s}+1]' if variant == 0 else '[{s}, {s}+1, {s}+2]'
        TEMPLATES.append((f'direct_{target}_{variant}', 'direct', target,
            f'result = {target}({seq})\n', target))
for target in ('len', 'sum'):
    for variant in range(2):
        seq = '[{s}, {s}+1]' if variant == 0 else '[{s}, {s}+1, {s}+2]'
        TEMPLATES.append((f'import_{target}_{variant}', 'import', target,
            f'from builtins import {target} as alias\nresult = alias({seq})\n', 'alias'))
for target in ('len', 'sum'):
    for variant in range(2):
        seq = '[{s}, {s}+1]' if variant == 0 else '[{s}, {s}+1, {s}+2]'
        TEMPLATES.append((f'decorated_{target}_{variant}', 'decorated', target,
            f'def choose(fn):\n    return {target}\n@choose\ndef f(x):\n    return -1\nresult = f({seq})\n', 'f'))
for variant in range(4):
    body = ('x[0]', 'x[0] + 1', 'x[0] * 2', 'x[0] - 1')[variant]
    TEMPLATES.append((f'control_{variant}', 'control', 'none',
        f'def f(x):\n    return {body}\nresult = f([{{s}}, {{s}}+1])\n', 'f'))
assert len(TEMPLATES) == 24

def records():
    for name, group, target, template, call_name in TEMPLATES:
        for seed in SEEDS:
            source = template.format(s=seed)
            yield {'id': f'{name}_{seed:02d}', 'template': name, 'group': group,
                   'target': target, 'seed': seed, 'call_name': call_name,
                   'source': source, 'source_sha256': hashlib.sha256(source.encode()).hexdigest()}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()

def write_json(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')

def freeze():
    items = list(records())
    manifest = {'schema':'ksynth1-run304-shadowing-freeze-v1', 'python':sys.version,
                'record_count':len(items), 'template_count':len(TEMPLATES),
                'records':items}
    root = hashlib.sha256(canonical(manifest)).hexdigest()
    write_json(HERE/'RUN304_FROZEN_SOURCES.json', manifest)
    spec = {'schema':'ksynth1-run304-prospective-v1', 'source_manifest_sha256':root,
            'record_count':len(items), 'template_count':len(TEMPLATES),
            'seeds_per_template':64, 'target_builtin_names':['len','sum'],
            'expected_groups':{
                'shadow':{'n':512,'old':'MAY_TARGET','new':'NOT_KNOWN_TARGET','runtime_target_calls':0},
                'direct':{'n':256,'old':'MAY_TARGET','new':'MAY_TARGET','runtime_target_calls':1},
                'import':{'n':256,'old':'MAY_TARGET','new':'MAY_TARGET','runtime_target_calls':1},
                'decorated':{'n':256,'old':'UNKNOWN_DYNAMIC','new':'UNKNOWN_DYNAMIC','runtime_target_calls':1},
                'control':{'n':256,'old':'NOT_KNOWN_TARGET','new':'NOT_KNOWN_TARGET','runtime_target_calls':0}},
            'strict_failure_policy':'Any mismatched classification or trusted CPython builtin identity is a failure; preserve all outcomes.',
            'independence':'64 variants/template correlated; no issue-level power claim',
            'scope':'trusted hardcoded templates, module-level no-unmodeled-mutation; not general Python soundness'}
    write_json(HERE/'RUN304_PROSPECTIVE_FREEZE.json', spec)
    print(json.dumps({'root':root, 'n':len(items), 'templates':len(TEMPLATES)},sort_keys=True))

def classify(extractor, source, call_name):
    calls = [c for c in extractor(source)['calls'] if c['name'] == call_name]
    if len(calls) != 1:
        return {'classification':'AMBIGUOUS', 'matching_calls':calls}
    return calls[0]

def run():
    manifest = json.loads((HERE/'RUN304_FROZEN_SOURCES.json').read_text())
    freeze_spec = json.loads((HERE/'RUN304_PROSPECTIVE_FREEZE.json').read_text())
    assert hashlib.sha256(canonical(manifest)).hexdigest() == freeze_spec['source_manifest_sha256']
    results = []
    for rec in manifest['records']:
        assert hashlib.sha256(rec['source'].encode()).hexdigest() == rec['source_sha256']
        old = classify(old_extract, rec['source'], rec['call_name'])
        new = classify(new_extract, rec['source'], rec['call_name'])
        observed = []
        filename = f"<ksynth-run304-{rec['id']}>"
        def profile(frame, event, arg):
            if frame.f_code.co_filename != filename:
                return
            if event == 'c_call' and (arg is builtins.len or arg is builtins.sum):
                observed.append(arg.__name__)
        ns = {'__builtins__':builtins.__dict__}
        compiled = compile(rec['source'], filename, 'exec')
        try:
            sys.setprofile(profile)
            exec(compiled, ns, ns)
        finally:
            sys.setprofile(None)
        row = {k:rec[k] for k in ('id','template','group','target','seed','source_sha256')}
        row.update(old=old['classification'], new=new['classification'],
                   old_provenance=old.get('provenance'), new_provenance=new.get('provenance'),
                   observed_builtin_calls=observed, result=ns.get('result'))
        expected = freeze_spec['expected_groups'][rec['group']]
        row['passed'] = (row['old']==expected['old'] and row['new']==expected['new'] and
                         len(observed)==expected['runtime_target_calls'] and
                         (not observed or observed == [rec['target']]))
        results.append(row)
    out = {'schema':'ksynth1-run304-shadowing-results-v1',
           'source_manifest_sha256':freeze_spec['source_manifest_sha256'],
           'count':len(results),'passed':sum(r['passed'] for r in results),
           'failed':sum(not r['passed'] for r in results),'rows':results}
    write_json(HERE/'RUN304_RAW_FUNCTIONAL.json', out)
    print(json.dumps({'count':out['count'],'passed':out['passed'],'failed':out['failed']},sort_keys=True))
    if out['failed']:
        for row in results:
            if not row['passed']: print('FAIL',row['id'],row['old'],row['new'],row['observed_builtin_calls'])
        raise SystemExit(1)

if __name__ == '__main__':
    {'freeze':freeze,'run':run}[sys.argv[1]]()
