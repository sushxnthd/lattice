#!/usr/bin/env python3
"""Run234: prospective 12-repository paired capable-model feasibility experiment.

Gold-blind selection from Run199 discovery only. Semantic-node JSON and
annotated Python are invertible presentations of identical bounded source
facts. Both arms use the same five-field action schema, model, seed, shared
retrieval, edit authority and trusted transactional compiler. This runner
NEVER calls compiler acceptance a functional issue resolution.
"""
from __future__ import annotations
import argparse
import ast
import difflib
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import traceback
import urllib.request
from collections import Counter

import paired_repo_pilot as prior
from repo_transaction import digest, tracked_authority, Rejected

PROTOCOL='K-SYNTH-1/run234-new-repository-paired-v1'
SEED='lattice-run234-multirepo-paired-v1-2026-10-25'
PUBLIC_SHA='f615b8c5f4f7e4b1996992105515b3e15e9678fb57a3cc0cff5cf1aef64641f2'
ARMS=('semantic_ir_json','python_annotated')
EXCLUDE=frozenset(('datadog/guarddog','gridtools/gt4py','marketsquare/robotframework-robocop',
 'qchackers/tqec','spikeinterface/spikeinterface','jlowin/fastmcp',
 'pybamm-team/pybamm','googlecloudplatform/cloud-sql-python-connector',
 'googlefonts/ufo2ft','zulip/zulip-terminal','quansight/ragna'))
MODEL=prior.MODEL
MODEL_SHA=prior.MODEL_SHA


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def select(public):
    eligible=[r for r in public if r['split']=='discovery' and r['repo'] not in EXCLUDE
              and 70<=len(r['problem_statement'].split())<=350]
    eligible.sort(key=lambda r:(sha((SEED+'|'+r['instance_id']).encode()),r['instance_id']))
    out=[];seen=set()
    for r in eligible:
        if r['repo'] in seen:continue
        out.append(r);seen.add(r['repo'])
        if len(out)==12:break
    if len(out)!=12:raise ValueError('insufficient distinct discovery repositories')
    return out


def freeze_public(public_bytes, prereg):
    if sha(public_bytes)!=PUBLIC_SHA:raise ValueError('public Run199 SHA mismatch')
    cohort=select(json.loads(public_bytes))
    observed=[{'instance_id':r['instance_id'],'repo':r['repo'],
               'base_commit':r['base_commit'],'issue_sha256':sha(r['problem_statement'].encode())}
              for r in cohort]
    if observed!=prereg['cohort']:raise ValueError('preregistered cohort mismatch')
    if prereg['public_sha256']!=PUBLIC_SHA:raise ValueError('public digest mismatch')
    if prereg['schema_sha256']!=sha(canonical(schema())):raise ValueError('schema digest mismatch')
    if prereg['model_sha256']!=MODEL_SHA:raise ValueError('model digest mismatch')
    return cohort


def facts(files,issue,max_chars=26000):
    names=set(re.findall(r'([A-Za-z_][A-Za-z_0-9]*)[(]',issue['problem_statement']))
    words=set(re.findall(r'[a-z_][a-z_0-9]{3,}',issue['problem_statement'].lower()))
    out={}
    for path,item in sorted(prior.target_facts(files).items()):
        def score(t):
            named=t['kind'] in ('FunctionDef','AsyncFunctionDef','ClassDef')
            return (10000*(t['name'] in names)+100*named+
                    20*sum(w in t['name'].lower() for w in words)+
                    sum(min(2,t['old_text'].lower().count(w)) for w in words),
                    -len(t['old_text']),-t['start_line'])
        eligible=[t for t in item['targets'] if 0<len(t['old_text'])<=5500]
        chosen=sorted(eligible,key=score,reverse=True)[:(4 if path.endswith('.py') else 2)]
        if not chosen:continue
        targets=[{k:t[k] for k in ('target_id','kind','name','start_line','end_line','old_text')}
                 for t in chosen]
        lines=item['source'].splitlines(keepends=True)
        excerpts=[]
        for t in chosen[:2]:
            a=max(0,t['start_line']-2)
            excerpts.append(''.join(f'{j+1}: {lines[j]}'
                for j in range(a,min(len(lines),t['end_line']+2,a+12))))
        out[path]={'file_sha256':item['file_sha256'],'full_source_bytes':len(files[path]),
                   'targets':targets,'source_excerpt':'\n'.join(excerpts)[:1200]}
    def size():return len(canonical(out))
    while size()>max_chars:
        removable=[(len(t['old_text']),p,i) for p,d in out.items()
                   for i,t in enumerate(d['targets'])
                   if not(t['kind'] in ('FunctionDef','AsyncFunctionDef') and t['name'] in names)]
        if removable:
            _,p,i=max(removable);out[p]['targets'].pop(i)
        else:
            for p in sorted(out,key=lambda p:len(out[p]['source_excerpt']),reverse=True):
                out[p]['source_excerpt']=''
                if size()<=max_chars:break
            if size()>max_chars:raise ValueError('protected targets exceed context budget')
    return out


def python_view(f):
    parts=[]
    for path,item in sorted(f.items()):
        parts.append('### FILE '+json.dumps(path))
        parts.append('# file_sha256: '+item['file_sha256'])
        parts.append('# full_source_bytes: '+str(item['full_source_bytes']))
        for t in item['targets']:
            parts.append('# AST_TARGET '+json.dumps(t,sort_keys=True,ensure_ascii=False))
        parts.append('### SOURCE_EXCERPT '+json.dumps(item['source_excerpt'],ensure_ascii=False))
        parts.append('### END_FILE')
    return '\n'.join(parts)


def parse_python_view(s):
    out={};path=None;item=None
    for line in s.splitlines():
        if line.startswith('### FILE '):
            if path is not None:raise ValueError('nested FILE')
            path=json.loads(line[9:]);item={'targets':[]}
        elif line.startswith('# file_sha256: '):item['file_sha256']=line[15:]
        elif line.startswith('# full_source_bytes: '):item['full_source_bytes']=int(line[21:])
        elif line.startswith('# AST_TARGET '):item['targets'].append(json.loads(line[13:]))
        elif line.startswith('### SOURCE_EXCERPT '):item['source_excerpt']=json.loads(line[19:])
        elif line=='### END_FILE':
            if set(item)!={'file_sha256','full_source_bytes','targets','source_excerpt'}:
                raise ValueError('malformed file view')
            out[path]=item;path=item=None
        else:raise ValueError('invalid view line')
    if path is not None:raise ValueError('unterminated FILE')
    return out


def schema():
    item={'type':'object','properties':{
        'op':{'type':'string','enum':['replace','create','delete']},
        'path':{'type':'string'},'file_sha256':{'type':'string'},
        'selector':{'type':'string'},'content':{'type':'string'}},
        'required':['op','path','file_sha256','selector','content'],
        'additionalProperties':False}
    s={'type':'object','properties':{'actions':{'type':'array','minItems':1,'maxItems':8,
        'items':item}},'required':['actions'],'additionalProperties':False}
    return {'type':'json_schema','json_schema':{'name':'lattice_run234_five_field',
        'strict':True,'schema':s}}


def normalize(output):
    if not isinstance(output,dict) or set(output)!={'actions'}:raise Rejected('invalid envelope')
    actions=output['actions']
    if not isinstance(actions,list) or not 1<=len(actions)<=8:raise Rejected('invalid action count')
    converted=[]
    for act in actions:
        if not isinstance(act,dict) or set(act)!={'op','path','file_sha256','selector','content'}:
            raise Rejected('invalid action keys')
        if not all(isinstance(v,str) for v in act.values()):raise Rejected('nonstring action field')
        op=act['op'];p=act['path'];h=act['file_sha256'];sel=act['selector'];body=act['content']
        if op=='replace':
            if not h or not sel or not body:raise Rejected('missing replace field')
            converted.append(dict(op=op,path=p,file_sha256=h,selector=sel,replacement=body,content=''))
        elif op=='create':
            if h or sel:raise Rejected('nonempty unused create field')
            converted.append(dict(op=op,path=p,file_sha256='',selector='',replacement='',content=body))
        elif op=='delete':
            if sel or body or not h:raise Rejected('nonempty unused delete field')
            converted.append(dict(op=op,path=p,file_sha256=h,selector='',replacement='',content=''))
        else:raise Rejected('unknown operation')
    return {'actions':converted}


def compile_common(files,output,authority):
    # The only normalization is a bijective five-field-to-six-field wire encoding.
    # Both representations use the SAME compiler and selector type.
    return prior.compile_arm(files,normalize(output),authority,'python_short_id')


def prompt(issue,f,arm):
    if arm not in ARMS:raise ValueError('unknown arm')
    view=canonical(f).decode() if arm==ARMS[0] else python_view(f)
    guide='semantic-node JSON' if arm==ARMS[0] else 'annotated ordinary Python'
    return ('Fix this real repository issue by making the smallest correct multi-file edit. '
       'You are viewing '+guide+'; the other condition has identical source facts, AST targets, '
       'hashes, authority, model and action grammar. '
       'Return only a JSON object with actions (1-8). Each action has exactly five string fields: '
       'op,path,file_sha256,selector,content. '
       'To edit existing code, op="replace", copy an exact listed path, file_sha256, '
       '24-character target_id into selector; content is the COMPLETE replacement for the '
       'selected old_text, with correct indentation. '
       'For a new file, op="create", path and content are nonempty, file_sha256 and selector empty. '
       'For a deletion, op="delete", path and file_sha256 are nonempty, selector and content empty. '
       'Never delete an existing file just to change a method. Preserve licenses and valid Python syntax. '
       'Do not invent selectors or assume the target class has the same lifecycle as another class. '
       'No gold patch or hidden tests are available.\nISSUE:\n'+issue['problem_statement']+
       '\nSOURCE_FACTS:\n'+view)


def patch_text(files,tx):
    parts=[]
    for p,new in sorted(tx.changes.items()):
        old=files.get(p)
        before=[] if old is None else old.decode('utf-8').splitlines(keepends=True)
        after=[] if new is None else new.decode('utf-8').splitlines(keepends=True)
        diff=''.join(difflib.unified_diff(before,after,
            fromfile='a/'+p if old is not None else '/dev/null',
            tofile='b/'+p if new is not None else '/dev/null'))
        if not diff:continue
        header=f'diff --git a/{p} b/{p}\n'
        if old is None:header+='new file mode 100644\n'
        if new is None:header+='deleted file mode 100644\n'
        parts.append(header+diff)
    return ''.join(parts)


def diagnostics(files,tx):
    paths=[];changed_bytes=0;ast_delta=[];syntax=[]
    for p,new in sorted(tx.changes.items()):
        old=files.get(p)
        paths.append(p);changed_bytes+=len(new or b'')+len(old or b'')
        if p.endswith('.py') and new is not None:
            try:
                a=ast.dump(ast.parse((old or b'').decode()),include_attributes=False) if old else ''
                b=ast.dump(ast.parse(new.decode()),include_attributes=False)
                if a!=b:ast_delta.append(p)
                syntax.append({'path':p,'valid':True})
            except Exception as exc:syntax.append({'path':p,'valid':False,'error':repr(exc)})
    return {'changed_paths':paths,'ast_delta_paths':ast_delta,
            'total_before_after_bytes':changed_bytes,'syntax':syntax}


def positive_controls():
    files={'src/a.py':b'def compute(x):\n    return x + 1\n',
           'src/b.py':b'from .a import compute\n\ndef run(x):\n    return compute(x)\n'}
    facts0=prior.target_facts(files)
    acts=[]
    for p,name,new in [('src/a.py','compute','def compute(x):\n    return x + 2\n'),
                       ('src/b.py','run','def run(x):\n    return compute(x) * 2\n')]:
        target=next(t for t in facts0[p]['targets'] if t['name']==name and t['kind']=='FunctionDef')
        acts.append(dict(op='replace',path=p,file_sha256=digest(files[p]),
                         selector=target['target_id'],content=new))
    tx=compile_common(files,{'actions':acts},set(files))
    assert set(tx.changes)==set(files)
    ns={};exec(tx.changes['src/a.py'].decode(),ns)
    ns2={'compute':ns['compute']}
    exec(tx.changes['src/b.py'].decode().replace('from .a import compute',''),ns2)
    assert ns2['run'](2)==8
    bad=dict(acts[0]);bad['file_sha256']='0'*64
    try:compile_common(files,{'actions':[bad]},set(files))
    except Rejected:pass
    else:raise AssertionError('stale hash accepted')
    bad=dict(acts[0]);bad['selector']='0'*24
    try:compile_common(files,{'actions':[bad]},set(files))
    except Rejected:pass
    else:raise AssertionError('invalid selector accepted')
    return {'positive_two_file_result':8,'positive_compiler_accepted':True,
            'stale_hash_rejected':True,'unknown_target_rejected':True,
            'common_schema_sha256':sha(canonical(schema()))}


def invoke(endpoint,raw,issue,f,files,authority,arm,seed,root):
    text=prompt(issue,f,arm)
    req={'model':MODEL,'messages':[{'role':'user','content':text}],
         'temperature':0,'seed':seed,'max_tokens':2048,'stream':False,
         'response_format':schema()}
    tag=issue['instance_id']+'-'+arm
    (raw/(tag+'-request.json')).write_bytes(canonical(req))
    record={'task':issue['instance_id'],'arm':arm,'seed':seed,'model':MODEL,
            'model_sha256':MODEL_SHA,'prompt_sha256':sha(text.encode()),
            'facts_sha256':sha(canonical(f)),'accepted':False,
            'functional_resolution':'NOT_EVALUATED','schema_sha256':sha(canonical(schema()))}
    try:
        body=urllib.request.urlopen(urllib.request.Request(endpoint,data=canonical(req),
            headers={'Content-Type':'application/json'},method='POST'),timeout=2400).read(4_000_000)
        (raw/(tag+'-response.json')).write_bytes(body)
        response=json.loads(body);choice=response['choices'][0]
        record.update(usage=response.get('usage'),finish_reason=choice.get('finish_reason'),
                      model_reported=response.get('model'))
        tx=compile_common(files,json.loads(choice['message']['content']),authority)
        patch=patch_text(files,tx)
        (raw/(tag+'-patch.diff')).write_text(patch)
        (raw/(tag+'-after.json')).write_bytes(canonical({p:(None if b is None else b.decode())
                                                         for p,b in tx.changes.items()}))
        try:
            check=subprocess.run(['git','-C',str(root),'apply','--check','-'],input=patch,
                                 text=True,capture_output=True,timeout=45)
            applycheck={'returncode':check.returncode,'stdout':check.stdout,'stderr':check.stderr}
        except Exception as exc:applycheck={'error':repr(exc)}
        record.update(accepted=True,trace=tx.trace,before=tx.before,after=tx.after,
                      patch_sha256=sha(patch.encode()),patch_apply_check=applycheck,
                      **diagnostics(files,tx))
    except Exception as exc:
        record['error']=repr(exc);record['error_traceback']=traceback.format_exc()[-5000:]
    (raw/(tag+'-verifier.json')).write_bytes(canonical(record))
    return record


def manifest(out):
    files=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST.json')
    (out/'SHA256_MANIFEST.json').write_bytes(canonical({str(p.relative_to(out)):sha(p.read_bytes())
                                                        for p in files}))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--public',type=pathlib.Path,required=True)
    ap.add_argument('--prereg',type=pathlib.Path,required=True)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--task-index',type=int,choices=range(12),required=True)
    ap.add_argument('--freeze-only',action='store_true')
    ap.add_argument('--endpoint',default='http://127.0.0.1:8080/v1/chat/completions')
    a=ap.parse_args();out=a.out;out.mkdir(parents=True,exist_ok=True)
    try:
        prereg=json.loads(a.prereg.read_bytes())
        cohort=freeze_public(a.public.read_bytes(),prereg)
        issue=cohort[a.task_index]
        seed=int(sha((PROTOCOL+'|'+issue['instance_id']).encode())[:8],16)
        frozen={'protocol':PROTOCOL,'issue':issue['instance_id'],'repo':issue['repo'],
            'base_commit':issue['base_commit'],'issue_sha256':sha(issue['problem_statement'].encode()),
            'public_sha256':PUBLIC_SHA,'model':MODEL,'model_sha256':MODEL_SHA,
            'schema_sha256':sha(canonical(schema())),'arms':ARMS,'seed':seed,
            'temperature':0,'max_tokens':2048,'functional_resolution':'NOT_EVALUATED',
            'same_retrieval':True,'same_authority':True,'same_compiler':True,
            'same_output_grammar':True,'unseen_boundary_used':False}
        (out/'freeze.json').write_bytes(canonical(frozen))
        (out/'controls.json').write_bytes(canonical(positive_controls()))
        if a.freeze_only:
            manifest(out);return
        root=pathlib.Path('/tmp')/('lattice-run234-'+str(a.task_index))
        prior.clone_issue(issue,root)
        authority=tracked_authority(root)
        files=prior.retrieve(issue,root,authority,out,a.endpoint)
        f=facts(files,issue)
        assert json.loads(canonical(f))==parse_python_view(python_view(f))
        (out/'facts.json').write_bytes(canonical(f))
        (out/'equivalence.json').write_bytes(canonical({'facts_sha256':sha(canonical(f)),
            'paths':sorted(files),'authority_sha256':sha(canonical(sorted(authority))),
            'authority_count':len(authority),'verified_roundtrip':True,
            'source_context_bytes':sum(map(len,files.values()))}))
        raw=out/'raw';raw.mkdir(exist_ok=True)
        records=[]
        order=ARMS if a.task_index%2==0 else tuple(reversed(ARMS))
        for arm in order:
            records.append(invoke(a.endpoint,raw,issue,f,files,authority,arm,seed,root))
            (out/'records.json').write_bytes(canonical(records))
        manifest(out)
    except Exception as exc:
        (out/'fatal.json').write_bytes(canonical({'error':repr(exc),
            'traceback':traceback.format_exc()[-15000:]}))
        manifest(out)
        raise

if __name__=='__main__':main()
