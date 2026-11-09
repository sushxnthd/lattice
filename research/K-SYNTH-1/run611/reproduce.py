import ast,hashlib,json,subprocess,sys
CASES={
 'plain':('def target():\n print("ORIGINAL")\n','from provider import target\ntarget()\n'),
 'rebound':('def target():\n print("ORIGINAL")\n','from provider import target\ntarget=lambda:print("REBOUND")\ntarget()\n'),
 'conditional_false':('def target():\n print("ORIGINAL")\n','if False:\n from provider import target\ntry: target()\nexcept NameError: print("NAME_ERROR")\n'),
 'star_import':('def target():\n print("ORIGINAL")\n','from provider import *\ntarget()\n'),
 'module_getattr':('def target():\n print("ORIGINAL")\ndef __getattr__(name):\n return lambda:print("DYNAMIC")\n','from provider import absent\nabsent()\n'),
 'dynamic_exec':('def target():\n print("ORIGINAL")\n','exec("from provider import target")\ntarget()\n'),
 'globals_mutation':('def target():\n print("ORIGINAL")\n','from provider import target\nglobals()["target"]=lambda:print("REBOUND")\ntarget()\n'),
 'module_replacement':('def target():\n print("ORIGINAL")\n','import sys,types\nm=types.ModuleType("provider")\nm.target=lambda:print("REPLACED")\nsys.modules["provider"]=m\nfrom provider import target\ntarget()\n')}
rows=[]
for name,(provider,consumer) in CASES.items():
 tree=ast.parse(consumer)
 syntactic_import=any(isinstance(n,ast.ImportFrom) and n.module=='provider' for n in ast.walk(tree))
 wrapper='import sys,types\np=types.ModuleType("provider")\nexec('+repr(provider)+',p.__dict__)\nsys.modules["provider"]=p\n'+consumer
 p=subprocess.run([sys.executable,'-I','-c',wrapper],capture_output=True,text=True,timeout=5)
 row={'case':name,'provider_sha256':hashlib.sha256(provider.encode()).hexdigest(),'consumer_sha256':hashlib.sha256(consumer.encode()).hexdigest(),'syntactic_import':syntactic_import,'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
 assert p.returncode==0,row
 rows.append(row)
assert [r['stdout'] for r in rows]==['ORIGINAL','REBOUND','NAME_ERROR','ORIGINAL','DYNAMIC','ORIGINAL','REBOUND','REPLACED']
print(json.dumps({'cases':rows,'count':len(rows),'direct_import_syntax':sum(r['syntactic_import'] for r in rows),'original_target_executions':sum(r['stdout']=='ORIGINAL' for r in rows)},indent=2))
