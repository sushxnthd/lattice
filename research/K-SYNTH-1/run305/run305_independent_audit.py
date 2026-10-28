#!/usr/bin/env python3
"""Independent Run305 audit: no imports of either Lattice analyzer or runner."""
import ast
import builtins
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
P=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
fr=P/'RUN305_FROZEN_SOURCES.json'; rr=P/'RUN305_RAW_FUNCTIONAL.json'
frozen=json.loads(fr.read_text()); raw=json.loads(rr.read_text())
assert raw['frozen_sha256']==H(fr.read_bytes())
assert len(frozen['cases'])==len(raw['records'])==1024
assert len({x['id'] for x in frozen['cases']})==1024

def static_builtin_calls(src):
    t=ast.parse(src)
    postponed=any(isinstance(s,ast.ImportFrom) and s.module=='__future__' and any(a.name=='annotations' for a in s.names) for s in t.body)
    aliases={'len':'len','sum':'sum'}
    for s in t.body:
        if isinstance(s,ast.ImportFrom) and s.module=='builtins':
            for a in s.names:
                if a.name in ('len','sum'):aliases[a.asname or a.name]=a.name
    out=[]
    for s in t.body:
        if not isinstance(s,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
        exprs=[*s.args.defaults,*[x for x in s.args.kw_defaults if x is not None]]
        if not postponed:
            args=[*s.args.posonlyargs,*s.args.args,*s.args.kwonlyargs]
            if s.args.vararg:args.append(s.args.vararg)
            if s.args.kwarg:args.append(s.args.kwarg)
            exprs.extend(a.annotation for a in args if a.annotation is not None)
            if s.returns is not None:exprs.append(s.returns)
        for e in exprs:
            for n in ast.walk(e):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in aliases:
                    out.append(aliases[n.func.id])
        aliases.pop(s.name,None)
    return sorted(out)

def independently_profile(src):
    seen=Counter()
    code=compile(src,'<independent-run305>','exec')
    def callback(frame,event,arg):
        if event!='c_call':return
        if arg is builtins.len:seen['len']+=1
        if arg is builtins.sum:seen['sum']+=1
    old=sys.getprofile()
    try:
        sys.setprofile(callback)
        exec(code,{'__name__':'__independent_run305__'})
    finally:
        sys.setprofile(old)
    return sorted(seen.elements())

by_template=defaultdict(lambda:dict(n=0,old_missed=0,corrected_missed=0))
for case,row in zip(frozen['cases'],raw['records']):
    assert case['id']==row['id'] and case['source_sha256']==row['source_sha256']
    assert H(case['source'].encode())==case['source_sha256']
    static=static_builtin_calls(case['source'])
    replay=independently_profile(case['source'])
    assert static==replay==case['expected_calls']==row['observed_calls'],(case['id'],static,replay)
    assert sorted(row['corrected_calls'])==replay
    t=by_template[case['template']];t['n']+=1
    t['old_missed']+=sum((Counter(replay)-Counter(row['legacy_calls'])).values())
    t['corrected_missed']+=sum((Counter(replay)-Counter(row['corrected_calls'])).values())
assert len(by_template)==16
out=dict(schema='ksynth1-run305-independent-audit-v1',
    frozen_sha256=H(fr.read_bytes()),raw_sha256=H(rr.read_bytes()),
    replayed=1024,static_matches=1024,cp_replay_matches=1024,corrected_matches=1024,
    old_missed=sum(x['old_missed'] for x in by_template.values()),
    corrected_missed=sum(x['corrected_missed'] for x in by_template.values()),
    template_summary=dict(sorted(by_template.items())),discrepancies=0,
    scope='trusted source only; correlated variants; no general soundness or model-repair claim')
(P/'RUN305_INDEPENDENT_AUDIT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:out[k] for k in ('replayed','static_matches','cp_replay_matches','corrected_matches','old_missed','corrected_missed','discrepancies')},sort_keys=True))
