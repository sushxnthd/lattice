#!/usr/bin/env python3
"""Deterministically construct immutable trusted source fixtures without running them."""
import hashlib, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent

def source_for(future,effect,access,variant):
    f=f'f{variant:02d}';g=f'g{variant:02d}'
    lines=[]
    if future:lines.append('from __future__ import annotations')
    lines += [
        'import builtins',
        'events = []',
        'len = lambda xs: -777',
        'def install():',
        '    events.append("annotation")',
        "    globals()['len'] = builtins.len",
        '    return int',
        'def noop():',
        '    events.append("annotation")',
        '    return int',
        f'def {f}(x: {"install" if effect == "restore" else "noop"}()):',
        '    pass',
    ]
    if access=='direct': lines.append(f'_ = {f}.__annotations__')
    if access=='alias': lines += [f'{g} = {f}', f'_ = {g}.__annotations__']
    if access=='repeat': lines += [f'_ = {f}.__annotations__',f'_ = {f}.__annotations__']
    lines += ['observed = len([0, 1, 2])',
              'import json',
              'print(json.dumps({"observed": observed, "events": events}, sort_keys=True))']
    return '\n'.join(lines)+'\n'

records=[]
for future in (False,True):
 for effect in ('restore','noop'):
  for access in ('none','direct','alias','repeat'):
   for variant in range(16):
    s=source_for(future,effect,access,variant)
    # Expected based on normative version rules, NOT observed interpreter results.
    expected={}
    for version in ('3.13','3.14'):
     triggers=(not future and (version=='3.13' or access!='none'))
     count=int(triggers)
     expected[version]={'observed':3 if triggers and effect=='restore' else -777,
                        'events':['annotation']*count}
    records.append({'id':f'{int(future)}-{effect}-{access}-{variant:02d}',
                    'future':future,'effect':effect,'access':access,'variant':variant,
                    'source':s,'source_sha256':hashlib.sha256(s.encode()).hexdigest(),
                    'expected':expected})
payload={'schema':'ksynth1-run307-frozen-fixtures-v1','cases':records,
         'count':len(records),'semantic_basis':'PEP 649/749 and CPython 3.13 eager/future behavior'}
p=HERE/'RUN307_FROZEN_SOURCES.json'
p.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
print(len(records),hashlib.sha256(p.read_bytes()).hexdigest())
