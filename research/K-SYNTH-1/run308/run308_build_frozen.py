#!/usr/bin/env python3
"""Freeze twelve independently specified module-binding scenarios x 32 variants."""
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
CASES={
 'direct_builtin_import': 'from builtins import len',
 'explicit_builtin_alias': 'from builtins import len as len',
 'builtin_via_intermediary': 'from builtins import len as restored\nlen = restored',
 'delete_exposes_builtin': 'del len',
 'delete_then_reshadow': 'del len\nlen = lambda x: 2',
 'unrelated_import': 'from builtins import sum as other',
 'sum_via_intermediary': 'from builtins import sum as restored\nlen = restored',
 'local_lambda_control': 'other = 1',
 'sum_direct_as_len': 'from builtins import sum as len',
 'import_then_reshadow': 'from builtins import len as other\nlen = lambda x: 2',
 'function_rebinding_control': 'def len(x):\n    return 2',
 'wildcard_import_unknown': 'from builtins import *',
}
records=[]
for scenario,body in CASES.items():
    for k in range(32):
        arg=['x','items','sequence','values'][k%4]
        space=' '*(k%3)
        benign=['','marker = 0\n','marker = (0)\n','marker = 0 # inert\n'][k%4]
        source=(f'# Run308 frozen scenario={scenario} variant={k}\n'
                'import builtins\nimport json\n'
                f'len = lambda {arg}:{space}2\n'
                f'{benign}{body}\n'
                'observed = len([1, 2, 3])\n'
                'print(json.dumps({"value": observed, "is_builtin": len is builtins.len}, sort_keys=True))\n')
        records.append({'id':f'{scenario}:{k:02d}','scenario':scenario,
                        'source':source,'source_sha256':hashlib.sha256(source.encode()).hexdigest()})
obj={'schema':'run308-frozen-source-v1','cases':records,
     'scenarios':list(CASES),'variants_per_scenario':32,
     'note':'All cases correlated; trusted CPython standard-library code only.'}
p=HERE/'RUN308_FROZEN_SOURCES.json'
p.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
print('cases',len(records),'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
