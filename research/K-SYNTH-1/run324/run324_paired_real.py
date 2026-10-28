"""Source-only blinded paired production repair pilot, no reference localization."""
import ast, hashlib, json, pathlib, re, shutil, sys, traceback, urllib.request
BASE='f4e4bc31f40f8c94c6a1f1685df28f97ff48c305'
MODEL_SHA='509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c'
ISSUE='In urllib3, explicitly supplied port=0 is distinct from an absent port. Some pool selection, proxy configuration, and URL formatting paths treat zero as false and use the scheme default. Repair the production source without changing omitted or nonzero port behavior.'

def sha(b): return hashlib.sha256(b).hexdigest()
def save(p,x):
 p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def discover(root):
 rows=[]
 for p in sorted((root/'src/urllib3').rglob('*.py')):
  rel=str(p.relative_to(root));b=p.read_bytes();s=b.decode();lines=s.splitlines()
  for n in ast.walk(ast.parse(s,rel)):
   if not isinstance(n,(ast.If,ast.IfExp)):continue
   t=n.test;expr=ast.get_source_segment(s,t)
   if not expr or 'port' not in expr or len(expr)>220:continue
   reads=sorted({x.id for x in ast.walk(t) if isinstance(x,ast.Name) and isinstance(x.ctx,ast.Load)})
   ident='C'+sha((rel+':'+str(t.lineno)+':'+ast.dump(t)).encode())[:12]
   lo=max(0,t.lineno-4);hi=min(len(lines),t.end_lineno+3)
   context='\n'.join(f'{i+1:04d} {lines[i]}' for i in range(lo,hi))
   rows.append(dict(id=ident,path=rel,line=t.lineno,col=t.col_offset,end_line=t.end_lineno,end_col=t.end_col_offset,expr=expr,reads=reads,context=context,node_sha256=sha(ast.dump(t).encode()),source_sha256=sha(b),certainty='UNKNOWN'))
 rows.sort(key=lambda x:(x['path'],x['line'],x['col']))
 assert len(rows)>=8 and len({x['id'] for x in rows})==len(rows)
 return rows

def freeze(root,out):
 out.mkdir(parents=True,exist_ok=True);c=discover(root);save(out/'candidates.json',c)
 prompts={}
 for arm in ('IR','PYTHON_AST'):
  lines=['Repair a historical public Python package from the PRE-CHANGE SOURCE ONLY. Return exactly JSON {"edits":[{"id":"C...","new_expr":"Python expression"}]}. At most 15 edits. You may replace ONLY listed If/IfExp tests. Preserve absent and nonzero ports. No diffs or prose. Empty edits means abstention.',ISSUE,'SOURCE-ONLY CANDIDATES:']
  for x in c:
   if arm=='IR':
    header=f"IR_TEST {x['id']} @ {x['path']}:{x['line']} MAY_READ={x['reads']} ZERO_TRUTHINESS=UNKNOWN TEST={x['expr']!r}"
   else:
    header=f"PYTHON_AST_ACTION_TARGET {x['id']} @ {x['path']}:{x['line']} ast.If(test=ast.parse({x['expr']!r},mode='eval').body) READ_NAMES={x['reads']} ZERO_TRUTHINESS=UNKNOWN"
   lines.extend((header,x['context']))
  lines.append('FORMAT ONLY, NOT A SOLUTION: {"edits":[{"id":"C123456789abc","new_expr":"x is not None"}]}')
  prompt='\n\n'.join(lines)
  req=dict(model='Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M',model_sha256=MODEL_SHA,seed=3242026,temperature=0,max_tokens=2048,messages=[dict(role='user',content=prompt)])
  save(out/f'request_{arm}.json',req);prompts[arm]=dict(prompt_sha256=sha(prompt.encode()),request_sha256=sha((out/f'request_{arm}.json').read_bytes()),characters=len(prompt))
 save(out/'freeze.json',dict(base=BASE,issue=ISSUE,model_sha256=MODEL_SHA,candidates=len(c),prompts=prompts,reference_localization=False,design='exploratory n=1; not powered'))
 print(json.dumps(dict(candidates=len(c),prompts=prompts)))

def infer(out):
 for arm in ('IR','PYTHON_AST'):
  req=json.loads((out/f'request_{arm}.json').read_text());payload={k:req[k] for k in ('model','seed','temperature','max_tokens','messages')}
  r=urllib.request.Request('http://127.0.0.1:8080/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(r,timeout=1800) as response:raw=response.read()
   (out/f'raw_{arm}.json').write_bytes(raw);answer=json.loads(raw)['choices'][0]['message']['content'];(out/f'completion_{arm}.txt').write_text(answer)
   print(arm,'RAW_SHA',sha(raw),'CHARS',len(answer))
  except Exception as e:
   save(out/f'inference_error_{arm}.json',dict(error_type=type(e).__name__,error=str(e),traceback=traceback.format_exc()))
   print(arm,'PRECOMPLETION_FAILURE',repr(e))

def span(lines,n):
 return (sum(len(x.encode()) for x in lines[:n.lineno-1])+n.col_offset,sum(len(x.encode()) for x in lines[:n.end_lineno-1])+n.end_col_offset)
def compile_arm(root,out,arm):
 txt=(out/f'completion_{arm}.txt').read_text().strip();fence=chr(96)*3
 if txt.startswith(fence):
  txt=re.sub('^'+fence+r'(?:json)?\s*\n','',txt);txt=re.sub('\n'+fence+r'\s*$','',txt)
 obj=json.loads(txt);assert isinstance(obj,dict) and set(obj)=={'edits'}
 edits=obj['edits'];assert isinstance(edits,list) and len(edits)<=15
 lookup={c['id']:c for c in json.loads((out/'candidates.json').read_text())};assert len({e['id'] for e in edits})==len(edits)
 bypath={}
 for e in edits:
  assert isinstance(e,dict) and set(e)=={'id','new_expr'} and e['id'] in lookup
  new=e['new_expr'];assert isinstance(new,str) and 0<len(new)<=300 and not any(x in new for x in ('\n','#',';','\\'))
  ast.parse(new,mode='eval');c=lookup[e['id']];bypath.setdefault(c['path'],[]).append((c,new))
 stage=out/'stages'/arm
 if stage.exists():shutil.rmtree(stage)
 shutil.copytree(root/'src/urllib3',stage/'src/urllib3')
 for rel,actions in bypath.items():
  raw=(root/rel).read_bytes();assert sha(raw)==actions[0][0]['source_sha256'];src=raw.decode();tree=ast.parse(src)
  nodes={(n.test.lineno,n.test.col_offset,n.test.end_lineno,n.test.end_col_offset):n.test for n in ast.walk(tree) if isinstance(n,(ast.If,ast.IfExp))}
  mapping={};replacements=[];lines=src.splitlines(keepends=True)
  for c,new in actions:
   key=(c['line'],c['col'],c['end_line'],c['end_col']);old=nodes[key]
   assert sha(ast.dump(old).encode())==c['node_sha256'] and ast.get_source_segment(src,old)==c['expr']
   a,b=span(lines,old);assert raw[a:b].decode()==c['expr'];replacements.append((a,b,new.encode()));mapping[key]=ast.parse(new,mode='eval').body
  class Sub(ast.NodeTransformer):
   def visit_If(self,n):
    key=(n.test.lineno,n.test.col_offset,n.test.end_lineno,n.test.end_col_offset)
    if key in mapping:n.test=mapping[key]
    return self.generic_visit(n)
   def visit_IfExp(self,n):
    key=(n.test.lineno,n.test.col_offset,n.test.end_lineno,n.test.end_col_offset)
    if key in mapping:n.test=mapping[key]
    return self.generic_visit(n)
  expected=Sub().visit(ast.parse(src));patched=raw
  for a,b,new in sorted(replacements,reverse=True):patched=patched[:a]+new+patched[b:]
  assert ast.dump(ast.parse(patched.decode()))==ast.dump(expected),'AST_CONGRUENCE'
  dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(patched)
 save(out/f'compile_{arm}.json',dict(accepted=True,edits=len(edits),files=len(bypath),stage=str(stage),patched_sha256={p:sha((stage/p).read_bytes()) for p in bypath}))
 print(arm,'ACCEPTED',len(edits))
def manifest(out):
 save(out/'SHA256_MANIFEST.json',{str(p.relative_to(out)):sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256_MANIFEST.json'})
if __name__=='__main__':
 cmd=sys.argv[1];out=pathlib.Path(sys.argv[3] if cmd in ('freeze','compile') else sys.argv[2])
 if cmd=='freeze':freeze(pathlib.Path(sys.argv[2]),out)
 elif cmd=='infer':infer(out)
 elif cmd=='compile':
  try:compile_arm(pathlib.Path(sys.argv[2]),out,sys.argv[4])
  except Exception as e:save(out/f'compile_{sys.argv[4]}.json',dict(accepted=False,error_type=type(e).__name__,error=str(e),traceback=traceback.format_exc()));print('REJECTED',repr(e))
 elif cmd=='manifest':manifest(out)
 else:raise SystemExit('unknown command')
