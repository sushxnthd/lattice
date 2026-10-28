#!/usr/bin/env python3
"""Trusted deterministic source fixture generator; never executes generated source."""
import hashlib,json,pathlib,sys
OUT=pathlib.Path(__file__).resolve().parent
# Annotation expressions are evaluated at function definition in CPython 3.13
# without future annotations. No external dependencies, imports, or generated model code.
TEMPLATES=[
 ('pos_arg','def f(x: (len := saved_len)): pass',True),
 ('return','def f(x) -> (len := saved_len): pass',True),
 ('posonly','def f(x: (len := saved_len), /): pass',True),
 ('kwonly','def f(*, x: (len := saved_len)): pass',True),
 ('vararg','def f(*args: (len := saved_len)): pass',True),
 ('kwarg','def f(**kwargs: (len := saved_len)): pass',True),
 ('async','async def f(x: (len := saved_len)): pass',True),
 ('fstring','def f(x: f"{(len := saved_len)!s}"): pass',True),
 ('tuple','def f(x: (1, (len := saved_len))): pass',True),
 ('dict','def f(x: {"k": (len := saved_len)}): pass',True),
 ('false_if','def f(x: ((len := saved_len) if False else 0)): pass',False),
 ('false_and','def f(x: (False and (len := saved_len))): pass',False),
 ('lambda_local','def f(x: (lambda: (len := saved_len))): pass',False),
 ('nonbuiltin','def f(x: (len := (lambda xs: -888))): pass',False),
 ('literal','def f(x: 42): pass',False),
 ('alias_only','def f(x: saved_len): pass',False),
]
rows=[]
for i,(name,definition,expected) in enumerate(TEMPLATES):
 for variant in range(24):
  source=(f'from builtins import len as saved_len\n'
          f'len = lambda xs: -777\n'
          f'{definition}\n'
          f'observed = len([{", ".join(map(str,range(1+(variant%5))))}])\n'
          f'import json\nprint(json.dumps({{"observed":observed,"is_builtin":len is saved_len}},sort_keys=True))\n')
  rows.append({'id':f'{i:02d}-{name}-{variant:02d}','scenario':name,'source':source,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'expected_builtin':expected})
obj={'schema':'ksynth-run310-annotation-namedexpr-v1','runtime':'CPython 3.13 eager annotations without future import','count':len(rows),'templates':len(TEMPLATES),'cases':rows}
raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
(OUT/'RUN310_FROZEN_SOURCES.json').write_bytes(raw)
print(json.dumps({'sha256':hashlib.sha256(raw).hexdigest(),'count':len(rows),'templates':len(TEMPLATES),'bytes':len(raw)},sort_keys=True))
