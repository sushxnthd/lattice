"""Prospectively frozen 2x2 structural-ID vs exact-text pilot; compiler acceptance only."""
import argparse,ast,hashlib,json,pathlib,urllib.request
from multifile_editor import sha256,canonical,compile_patch
from real_pilot import clone_issue,retrieve
MODEL='Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M'
MODEL_SHA='509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c'
TASKS=('gtalarico__pyairtable-431','wntrblm__nox-933')
ARMS=(('targets_first','id'),('source_first','text'),('targets_first','text'),('source_first','id'))
CONTROL={'src/a.py':b'def compute(x):\n    return x + 1\n','src/b.py':b'from .a import compute\n\ndef run(x):\n    return compute(x)\n'}
def facts(files):
 out={}
 for path,body in sorted(files.items()):
  source=body.decode();lines=body.splitlines(keepends=True);tree=ast.parse(source)
  raw=[('Module','',1,len(lines))]
  for n in ast.walk(tree):
   if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef,ast.Import,ast.ImportFrom,ast.Assign,ast.If,ast.Return)):
    a=getattr(n,'lineno',None);b=getattr(n,'end_lineno',None)
    if a is not None and b is not None and 1<=a<=b<=len(lines):
     if hasattr(n,'decorator_list') and n.decorator_list:a=min([a]+[d.lineno for d in n.decorator_list])
     raw.append((type(n).__name__,getattr(n,'name',''),a,b))
  by_span={}
  for kind,name,a,b in sorted(raw,key=lambda t:(t[2],t[3],t[0]=='Module',t[0])):
   by_span.setdefault((a,b),(kind,name,a,b))
  targets=[];seen=set();fs=sha256(body)
  for kind,name,a,b in sorted(by_span.values(),key=lambda t:(t[0]!='Module',t[0] not in ('FunctionDef','ClassDef'),t[2])):
   old=b''.join(lines[a-1:b]).decode()
   if old in seen:continue
   seen.add(old)
   ident=hashlib.sha256((path+'\0'+fs+'\0'+kind+'\0'+str(a)+'\0'+str(b)+'\0'+old).encode()).hexdigest()[:16]
   targets.append({'target_id':ident,'kind':kind,'name':name,'start_line':a,'end_line':b,'old_text':old})
   if len(targets)>=12:break
  assert targets
  out[path]={'file_sha256':fs,'source':source,'targets':targets}
 return out
def schema(address):
 key='target_id' if address=='id' else 'old_text'
 props={k:{'type':'string'} for k in ('path','file_sha256',key,'replacement')}
 return {'type':'json_schema','json_schema':{'name':'lattice_paired_edit','strict':True,'schema':{'type':'object','properties':{'edits':{'type':'array','minItems':1,'maxItems':8,'items':{'type':'object','properties':props,'required':list(props),'additionalProperties':False}}},'required':['edits'],'additionalProperties':False}}}
def prompt(issue,tab,view,address):
 key='target_id' if address=='id' else 'old_text';blocks=[]
 for path,v in tab.items():
  a='TARGETS='+json.dumps(v['targets'],ensure_ascii=False,separators=(',',':'))
  b='PYTHON_SOURCE='+json.dumps(v['source'],ensure_ascii=False)
  blocks.append('PATH='+path+' FILE_SHA256='+v['file_sha256']+'\n'+'\n'.join([a,b] if view=='targets_first' else [b,a]))
 example={'edits':[{'path':'src/a.py','file_sha256':'<copy SHA>',key:'<copy address>','replacement':'def compute(x):\n    return x + 2\n'}]}
 return ('Repair the issue using only listed files and complete TARGETS. All edits refer to original snapshot. Respond with one JSON object, exactly edits: 1-8 objects with path,file_sha256,'+key+',replacement. Copy hashes and addresses exactly. replacement must be valid Python including indentation. No prose. Example: '+json.dumps(example)+'\nISSUE:\n'+issue['problem_statement']+'\nAUTHORIZED FACTS:\n'+'\n'.join(blocks))
def compile_output(files,tab,reply,address):
 if not isinstance(reply,dict) or set(reply)!={'edits'}:raise ValueError('envelope')
 edits=reply['edits']
 if not isinstance(edits,list) or not 1<=len(edits)<=8:raise ValueError('edit count')
 normalized=[];key='target_id' if address=='id' else 'old_text'
 for e in edits:
  if not isinstance(e,dict) or set(e)!={'path','file_sha256',key,'replacement'}:raise ValueError('schema')
  path=e['path']
  if path not in files or e['file_sha256']!=tab[path]['file_sha256']:raise ValueError('authority/hash')
  matches=[t for t in tab[path]['targets'] if t[key]==e[key]]
  if len(matches)!=1:raise ValueError('ambiguous/unknown target')
  t=matches[0]
  normalized.append({'path':path,'file_sha256':e['file_sha256'],'start_line':t['start_line'],'end_line':t['end_line'],'old_text':t['old_text'],'replacement':e['replacement']})
 return compile_patch(files,{'edits':normalized},set(files))
def run(task,issue,files,arm,folder,endpoint):
 view,address=arm;tag=task+'-'+view+'-'+address;tab=facts(files);p=prompt(issue,tab,view,address)
 seed=int(sha256(('run204:'+task).encode())[:8],16)
 req={'model':MODEL,'messages':[{'role':'user','content':p}],'temperature':0,'seed':seed,'max_tokens':1536,'stream':False,'response_format':schema(address)}
 (folder/(tag+'-request.json')).write_bytes(canonical(req))
 rec={'task':task,'view':view,'address':address,'seed':seed,'prompt_sha256':sha256(p.encode()),'model_requested':MODEL,'model_sha256':MODEL_SHA,'context_sha256':sha256(canonical(tab)),'accepted':False,'functional_resolution':'NOT_EVALUATED'}
 try:
  request=urllib.request.Request(endpoint,data=canonical(req),headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(request,timeout=1800) as response:body=response.read(4000000)
  (folder/(tag+'-response.json')).write_bytes(body)
  resp=json.loads(body);choice=resp['choices'][0]
  rec.update(usage=resp.get('usage',{}),model_reported=resp.get('model'),finish_reason=choice.get('finish_reason'))
  compiled=compile_output(files,tab,json.loads(choice['message']['content']),address)
  rec.update(accepted=True,trace=compiled.trace,before=compiled.before,after=compiled.after)
 except Exception as exc:rec['error']=repr(exc)
 (folder/(tag+'-verifier.json')).write_bytes(canonical(rec))
 return rec
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public',required=True);ap.add_argument('--out',required=True)
 ap.add_argument('--task-index',type=int,choices=(0,1),required=True);ap.add_argument('--freeze-only',action='store_true')
 ap.add_argument('--endpoint',default='http://127.0.0.1:8080/v1/chat/completions')
 args=ap.parse_args();out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
 data=pathlib.Path(args.public).read_bytes();public=json.loads(data);by_id={x['instance_id']:x for x in public}
 assert len(by_id)==len(public) and all(by_id[t]['split']=='discovery' for t in TASKS)
 freeze={'protocol':'K-SYNTH-1/run204-prospective-v1','public_sha256':sha256(data),'tasks':[{'instance_id':t,'repo':by_id[t]['repo'],'base_commit':by_id[t]['base_commit']} for t in TASKS],'arms':ARMS,'model':MODEL,'model_sha256':MODEL_SHA,'max_tokens':1536,'primary':'compiler acceptance only','boundary_issues_used':0,'design':'feasibility pilot, not powered; target IDs do not prove semantic superiority'}
 (out/'freeze.json').write_bytes(canonical(freeze))
 if args.freeze_only:return
 raw=out/'raw';raw.mkdir(exist_ok=True);records=[];control={'problem_statement':'Change compute(x) in src/a.py to return x + 2.'}
 for arm in ARMS:
  records.append(run('control',control,CONTROL,arm,raw,args.endpoint))
  (out/'records.json').write_bytes(canonical(records))
 expected=sha256(b'def compute(x):\n    return x + 2\n')
 passed=all(r['accepted'] and r.get('after')=={'src/a.py':expected} for r in records)
 (out/'control_gate.json').write_bytes(canonical({'passed':passed,'n':len(records)}))
 if not passed:return
 task=TASKS[args.task_index];issue=by_id[task];root=pathlib.Path('/tmp')/('lattice-run204-'+str(args.task_index))
 clone_issue(issue,root);files=retrieve(issue,root,max_files=3,max_file_bytes=2500,max_total=6000)
 (out/'context.json').write_bytes(canonical({'task':task,'sha256':{k:sha256(v) for k,v in files.items()}}))
 arms=ARMS if args.task_index==0 else tuple(reversed(ARMS))
 for arm in arms:
  records.append(run(task,issue,files,arm,raw,args.endpoint))
  (out/'records.json').write_bytes(canonical(records))
if __name__=='__main__':main()
