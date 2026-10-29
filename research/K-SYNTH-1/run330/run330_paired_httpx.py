"""K-SYNTH-1 Run330: prospectively frozen paired model pilot on historical HTTPX.

This runner never reads the historical reference commit. Model code is never imported
or executed by this process. Untrusted patches are evaluated by an isolated oracle.
"""
from __future__ import annotations
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import traceback
import urllib.request

from run329_signature_editor import sha, _functions, _default_slot, _span, Rejected
from run329_postfreeze_boolean_guard import compile_boolean_defaults

BASE = '891d865044d27c229278f0fa20d84ba4007cb289'
MODEL_SHA = '509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c'
SEED = 3302026
ISSUE = ("We've currently got a different `allow_redirects` default on HEAD requests "
         "to all other request methods.\n\n"
         "https://github.com/encode/httpx/blob/a25d924bb910e85ca597c7b4ed819c6e9e17aecd/httpx/_api.py#L217\n\n"
         "This is in line with behaviour in `requests`, but I'm not convinced it's something we ought to do. "
         "It'd seem to me that we'd do better just to stay consistent rather than have this odd exclusion. "
         "I get why it *could* be a reasonable choice, but I think it'd *probably* be better just to stay consistent, "
         "and allow the user to switch `allow_redirects=False` if that's their intent.\n\n"
         "Flagging this to be addressed pre-1.0.")
ISSUE_URL = 'https://github.com/encode/httpx/issues/1146'
PROBE = b'def probe(flag: bool = False):\n    return flag\n'
MODEL = 'Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M'


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n')


def eligible(root):
    """No reference-diff localization: scan ALL httpx/*.py defaulted bool params named allow_redirects."""
    candidates = []
    source = {}
    for file in sorted((root/'httpx').rglob('*.py')):
        rel = str(file.relative_to(root))
        data = file.read_bytes()
        tree = ast.parse(data.decode('utf-8'), filename=rel)
        for qual, functions in sorted(_functions(tree).items()):
            if len(functions) != 1:
                continue
            fn = functions[0]
            try:
                defaults, ix = _default_slot(fn, 'allow_redirects')
            except Rejected:
                continue
            old = defaults[ix]
            if not isinstance(old, ast.Constant) or type(old.value) is not bool:
                continue
            a,b = _span(data,old)
            flows = []
            for call in ast.walk(fn):
                if isinstance(call,ast.Call):
                    for kw in call.keywords:
                        if kw.arg == 'allow_redirects' and isinstance(kw.value,ast.Name) and kw.value.id == 'allow_redirects':
                            flows.append({'line':call.lineno, 'callee':ast.unparse(call.func), 'keyword':'allow_redirects'})
            ident = 'D'+sha((rel+'|'+qual+'|allow_redirects').encode())[:12]
            candidates.append(dict(id=ident,path=rel,qual=qual,param='allow_redirects',old_expr=data[a:b].decode(),
                                   old_sha256=sha(data[a:b]),source_sha256=sha(data),flows=flows[:5],
                                   call_target='UNKNOWN',runtime_effect='UNKNOWN'))
            source[rel] = data
    candidates.sort(key=lambda c:(c['path'],c['qual']))
    assert candidates and len({c['id'] for c in candidates}) == len(candidates)
    return candidates,source


def schema():
    return {'type':'object','additionalProperties':False,'required':['edits'],
            'properties':{'edits':{'type':'array','maxItems':32,'items':{
                'type':'object','additionalProperties':False,'required':['id','new_expr'],
                'properties':{'id':{'type':'string'},'new_expr':{'type':'string'}}}}}}


def render(arm, rows):
    lines=[]
    for c in rows:
        base = f"{c['id']} {c['path']} {c['qual']} param={c['param']} old={c['old_expr']} sha={c['old_sha256']}"
        if arm == 'IR':
            lines.append('IR_DEFAULT '+base+' MAY_FORWARD='+json.dumps(c['flows'],sort_keys=True)+
                         ' CALLEE=UNKNOWN RUNTIME_EFFECT=UNKNOWN')
        else:
            lines.append('PY_AST_DEFAULT '+base+' ast.FunctionDef.args.defaults[allow_redirects]='+repr(c['old_expr'])+
                         ' ast.Call.keywords[allow_redirects]='+json.dumps(c['flows'],sort_keys=True)+
                         ' CALLEE=UNKNOWN RUNTIME_EFFECT=UNKNOWN')
    return '\n'.join(lines)


def request(arm,rows,kind):
    if kind=='GATE':
        issue='Positive control: for probe(flag: bool = False), change the flag default to True. Do not change the function body.'
    else:
        issue='Original pre-fix GitHub issue #1146, original wording with normalized line endings:\n'+ISSUE
    prompt = ('Repair Python source using the listed, authorized default-argument edit targets only. '
              'Return ONLY a JSON object with key edits, an array of {id,new_expr}. '
              'Each new_expr MUST be Python literal True or False. Do not invent IDs. '
              'Do not output code blocks, prose, comments, or extra fields. '
              'Use only facts below; CALLEE=UNKNOWN means syntactic forwarding does not prove runtime call resolution.\n\n'
              +issue+'\n\nAUTHORIZED SOURCE FACTS:\n'+render(arm,rows)+'\n\n'
              'FORMAT EXAMPLE ONLY (fake ID, not a solution): {"edits":[{"id":"D000000000000","new_expr":"True"}]}')
    return {'model':MODEL,'model_sha256':MODEL_SHA,'seed':SEED,'temperature':0,
            'max_tokens':512,'messages':[{'role':'user','content':prompt}],
            'response_format':{'type':'json_schema','json_schema':{'name':'lattice_edits','strict':True,'schema':schema()}}}


def freeze(root,out):
    out.mkdir(parents=True,exist_ok=True)
    rows,sources=eligible(root)
    gate=[{'id':'D'+sha(b'probe|flag')[:12], 'path':'probe.py','qual':'probe','param':'flag',
           'old_expr':'False','old_sha256':sha(b'False'),'source_sha256':sha(PROBE),
           'flows':[],'call_target':'UNKNOWN','runtime_effect':'UNKNOWN'}]
    save(out/'candidates.json',rows)
    save(out/'gate_candidates.json',gate)
    freeze_meta={'base':BASE,'issue_url':ISSUE_URL,'issue_sha256':sha(ISSUE.encode()),
                 'model_sha256':MODEL_SHA,'seed':SEED,'source_sha256':{p:sha(b) for p,b in sources.items()},
                 'candidate_count':len(rows),'reference_source_access':False,'requests':{}}
    for kind,selection in [('GATE',gate),('REAL',rows)]:
        for arm in ('IR','PYTHON_AST'):
            r=request(arm,selection,kind)
            name=f'{kind}_{arm}'
            save(out/f'request_{name}.json',r)
            freeze_meta['requests'][name]={'request_sha256':sha((out/f'request_{name}.json').read_bytes()),
                                          'prompt_sha256':sha(r['messages'][0]['content'].encode()),
                                          'prompt_chars':len(r['messages'][0]['content'])}
    save(out/'freeze.json',freeze_meta)
    print(json.dumps({'candidate_count':len(rows),'paths':sorted(sources),'requests':freeze_meta['requests']}))


def infer_one(out,name):
    r=json.loads((out/f'request_{name}.json').read_text())
    payload={k:r[k] for k in ('model','seed','temperature','max_tokens','messages','response_format')}
    req=urllib.request.Request('http://127.0.0.1:8080/v1/chat/completions',data=json.dumps(payload).encode(),
                               headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=1800) as response: raw=response.read()
        (out/f'raw_{name}.json').write_bytes(raw)
        result=json.loads(raw)
        completion=result['choices'][0]['message']['content']
        (out/f'completion_{name}.txt').write_text(completion)
        save(out/f'inference_{name}.json',{'raw_sha256':sha(raw),'finish_reason':result['choices'][0]['finish_reason'],
                                          'usage':result.get('usage'),'completion_sha256':sha(completion.encode())})
        print(name,'FINISHED',len(completion))
    except Exception as exc:
        save(out/f'inference_{name}.json',{'precompletion_error':type(exc).__name__+':'+str(exc),
                                          'traceback':traceback.format_exc()})
        print(name,'PRECOMPLETION',repr(exc))


def decode_and_compile(root,out,name):
    kind,arm=name.split('_',1)
    rows=json.loads((out/('gate_candidates.json' if kind=='GATE' else 'candidates.json')).read_text())
    lookup={c['id']:c for c in rows}
    response=(out/f'completion_{name}.txt').read_text()
    # No post-hoc fence removal or syntax repair; strict original score.
    obj=json.loads(response)
    if not isinstance(obj,dict) or set(obj)!={'edits'} or not isinstance(obj['edits'],list):
        raise Rejected('INVALID_RESPONSE_SCHEMA')
    edits=obj['edits']
    if not edits: raise Rejected('ABSTENTION_EMPTY_EDIT_LIST')
    if len(edits)>32: raise Rejected('TOO_MANY_EDITS')
    sources={}
    authority={'files':{},'targets':[]}
    translated=[]
    for edit in edits:
        if not isinstance(edit,dict) or set(edit)!={'id','new_expr'} or edit['id'] not in lookup:
            raise Rejected('UNKNOWN_ID_OR_SCHEMA')
        c=lookup[edit['id']]
        path=c['path']
        data=PROBE if kind=='GATE' else (root/path).read_bytes()
        if sha(data)!=c['source_sha256']:raise Rejected('STALE_SOURCE')
        sources[path]=data
        authority['files'][path]=sha(data)
        target=[path,c['qual'],c['param']]
        authority['targets'].append(target)
        translated.append({'path':path,'qual':c['qual'],'param':c['param'],
                           'old_sha256':c['old_sha256'],'new_expr':edit['new_expr']})
    updated=compile_boolean_defaults(sources,authority,translated)
    if kind=='GATE':
        assert set(updated)=={'probe.py'}
        tree=ast.parse(updated['probe.py'].decode())
        defaults=tree.body[0].args.defaults
        passed=(len(edits)==1 and isinstance(defaults[0],ast.Constant) and defaults[0].value is True)
        return {'accepted':True,'gate_pass':passed,'edits':translated,'patched_sha256':{'probe.py':sha(updated['probe.py'])}}
    stage=out/'stages'/arm
    if stage.exists():shutil.rmtree(stage)
    shutil.copytree(root,stage,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
    for p,b in updated.items():
        dest=stage/p;dest.write_bytes(b)
    return {'accepted':True,'stage':str(stage),'edits':translated,
            'patched_sha256':{p:sha(b) for p,b in updated.items()}}


def compile_name(root,out,name):
    try:result=decode_and_compile(root,out,name)
    except Exception as exc:result={'accepted':False,'error_type':type(exc).__name__,'error':str(exc),
                                    'traceback':traceback.format_exc()}
    save(out/f'compile_{name}.json',result)
    print(name,'ACCEPTED' if result['accepted'] else 'REJECTED',result.get('error',''))


def manifest(out):
    save(out/'SHA256_MANIFEST.json',{str(p.relative_to(out)):sha(p.read_bytes()) for p in sorted(out.rglob('*'))
                                     if p.is_file() and p.name!='SHA256_MANIFEST.json' and 'stages' not in p.parts})

if __name__=='__main__':
    cmd=sys.argv[1];out=Path(sys.argv[3] if cmd in ('freeze','compile') else sys.argv[2])
    if cmd=='freeze':freeze(Path(sys.argv[2]),out)
    elif cmd=='infer':infer_one(out,sys.argv[3])
    elif cmd=='compile':compile_name(Path(sys.argv[2]),out,sys.argv[4])
    elif cmd=='manifest':manifest(out)
    else:raise SystemExit('unknown command')
