"""Run332: corrected, preregistered two-action-gated paired HTTPX pilot.

Uses the unchanged Run330 compiler, isolated Run328 oracle and frozen pre-fix issue.
No reference commit/diff is accessed here. Never execute model-produced Python on host.
"""
from __future__ import annotations
import ast, json, sys
from pathlib import Path
import run330_paired_httpx as prior
from run329_signature_editor import sha, _functions, _default_slot, Rejected
from run329_postfreeze_boolean_guard import compile_boolean_defaults

SEED = 3322026
PROBES = {
    'probe_a.py': b'def probe_a(flag: bool = False):\n    return flag\n',
    'probe_b.py': b'def probe_b(flag: bool = True):\n    return flag\n',
}
GATE_TARGETS = {'probe_a': 'True', 'probe_b': 'False'}
ORIGINAL_DECODE = prior.decode_and_compile


def exact_slot(source: bytes, qual: str, param: str) -> str:
    tree = ast.parse(source.decode('utf-8'))
    funcs = _functions(tree)[qual]
    if len(funcs) != 1:
        raise AssertionError('AMBIGUOUS_FUNCTION')
    fn = funcs[0]
    defaults, ix = _default_slot(fn, param)
    if param in [p.arg for p in fn.args.kwonlyargs]:
        assert defaults is fn.args.kw_defaults
        return 'KW_ONLY'
    assert defaults is fn.args.defaults
    return 'POSITIONAL'


def render(arm: str, rows: list[dict]) -> str:
    lines = []
    for c in rows:
        slot = c['slot']
        common = (f"{c['id']} {c['path']} {c['qual']} param={c['param']} "
                  f"old={c['old_expr']} sha={c['old_sha256']} "
                  f"MAY_FORWARD={json.dumps(c['flows'],sort_keys=True,separators=(',',':'))} "
                  "CALLEE=UNKNOWN RUNTIME_EFFECT=UNKNOWN")
        if arm == 'IR':
            lines.append(f'IR_DEFAULT {common} SLOT={slot}')
        elif arm == 'PYTHON_AST':
            field = 'ast.arguments.kw_defaults' if slot == 'KW_ONLY' else 'ast.arguments.defaults'
            lines.append(f'PY_AST_DEFAULT {common} SLOT={field}')
        else:
            raise ValueError(arm)
    return '\n'.join(lines)


def make_request(arm, rows, kind):
    r = prior.request(arm, rows, kind)
    if kind == 'GATE':
        issue = ('Positive control: change probe_a(flag: bool = False) to True AND '
                 'probe_b(flag: bool = True) to False. Both independent edits are required; '
                 'a one-edit answer is incorrect. No function-body edits.')
    else:
        issue = 'Original pre-fix GitHub issue #1146, original wording with normalized line endings:\n'+prior.ISSUE
    prompt = ('Repair Python source using ONLY the listed authorized default-argument edits. '
              'Return ONLY JSON {"edits":[{"id":"...","new_expr":"True"}]}. '
              'new_expr must be the literal string True or False. Do not invent IDs, add prose, '
              'or infer a runtime callee from MAY_FORWARD. SLOT=KW_ONLY maps to '
              'ast.arguments.kw_defaults; SLOT=POSITIONAL maps to ast.arguments.defaults.\n\n'
              +issue+'\n\nAUTHORIZED SOURCE FACTS:\n'+render(arm,rows)+'\n')
    r['messages']=[{'role':'user','content':prompt}]
    r['seed']=SEED
    r['max_tokens']=768
    return r


def freeze(root: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    rows, sources = prior.eligible(root)
    assert len(rows) == 31 and len(sources) == 2
    slots={'KW_ONLY':0,'POSITIONAL':0}
    for c in rows:
        source=sources[c['path']]
        assert sha(source)==c['source_sha256']
        c['slot']=exact_slot(source,c['qual'],c['param'])
        slots[c['slot']]+=1
    assert slots == {'KW_ONLY':29,'POSITIONAL':2}, slots
    gates=[]
    for path,source in sorted(PROBES.items()):
        qual=path.removesuffix('.py')
        old='False' if qual=='probe_a' else 'True'
        gates.append({'id':'D'+sha((path+'|'+qual+'|flag').encode())[:12],
            'path':path,'qual':qual,'param':'flag','old_expr':old,
            'old_sha256':sha(old.encode()),'source_sha256':sha(source),
            'flows':[],'slot':'POSITIONAL', 'call_target':'UNKNOWN','runtime_effect':'UNKNOWN'})
    prior.save(out/'candidates.json',rows)
    prior.save(out/'gate_candidates.json',gates)
    meta={'protocol':'RUN332_TWO_ACTION_GATE_AST_CORRECTED','base':prior.BASE,
        'issue_sha256':sha(prior.ISSUE.encode()),'model_sha256':prior.MODEL_SHA,
        'seed':SEED,'temperature':0,'max_tokens':768,'reference_source_access':False,
        'source_sha256':{p:sha(b) for p,b in sources.items()},
        'candidate_count':len(rows),'ast_slot_counts':slots,
        'gate_requires_two_files':True,'gate_target_count':2,'requests':{}}
    for kind,selection in [('GATE',gates),('REAL',rows)]:
        for arm in ('IR','PYTHON_AST'):
            name=f'{kind}_{arm}';r=make_request(arm,selection,kind)
            prior.save(out/f'request_{name}.json',r)
            meta['requests'][name]={'request_sha256':sha((out/f'request_{name}.json').read_bytes()),
                'prompt_sha256':sha(r['messages'][0]['content'].encode()),
                'prompt_chars':len(r['messages'][0]['content'])}
    prior.save(out/'freeze.json',meta)
    print(json.dumps({'slots':slots,'requests':meta['requests']}))


def decode_and_compile(root, out, name):
    kind,arm=name.split('_',1)
    if kind=='REAL':
        return ORIGINAL_DECODE(root,out,name)
    rows=json.loads((out/'gate_candidates.json').read_text())
    lookup={c['id']:c for c in rows}
    obj=json.loads((out/f'completion_{name}.txt').read_text())
    if not isinstance(obj,dict) or set(obj)!={'edits' } or not isinstance(obj['edits'],list):
        raise Rejected('INVALID_RESPONSE_SCHEMA')
    edits=obj['edits']
    if len(edits)!=2 or any(not isinstance(e,dict) or set(e)!={'id','new_expr'} for e in edits):
        raise Rejected('GATE_REQUIRES_EXACTLY_TWO_EDITS')
    if len({e['id'] for e in edits})!=2 or set(e['id'] for e in edits)!=set(lookup):
        raise Rejected('GATE_REQUIRES_BOTH_DISTINCT_IDS')
    sources={}; authority={'files':{},'targets':[]};translated=[]
    for e in edits:
        c=lookup[e['id']];p=c['path'];data=PROBES[p]
        assert sha(data)==c['source_sha256']
        sources[p]=data;authority['files'][p]=sha(data)
        authority['targets'].append([p,c['qual'],c['param']])
        translated.append({'path':p,'qual':c['qual'],'param':c['param'],
            'old_sha256':c['old_sha256'],'new_expr':e['new_expr']})
    updated=compile_boolean_defaults(sources,authority,translated)
    for p,blob in updated.items():
        fn=ast.parse(blob.decode()).body[0]
        val=fn.args.defaults[0]
        if not isinstance(val,ast.Constant) or type(val.value) is not bool:
            raise Rejected('GATE_NONBOOLEAN')
        if str(val.value)!=GATE_TARGETS[fn.name]:
            raise Rejected('GATE_WRONG_VALUE')
    return {'accepted':True,'gate_pass':True,'edits':translated,
        'patched_sha256':{p:sha(b) for p,b in updated.items()}}


prior.decode_and_compile=decode_and_compile
if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='freeze':freeze(Path(sys.argv[2]),Path(sys.argv[3]))
    elif cmd=='infer':prior.infer_one(Path(sys.argv[2]),sys.argv[3])
    elif cmd=='compile':prior.compile_name(Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4])
    elif cmd=='manifest':prior.manifest(Path(sys.argv[2]))
    else:raise SystemExit('unknown command')
