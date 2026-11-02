import hashlib,json,os,pathlib,shutil,subprocess,sys
ROOT=pathlib.Path('/tmp/lattice437');ROOT.mkdir(exist_ok=True)
REF='190dd4df86874495f56bb088fbd0cb1d9f0e77a0'
FILES=['app.py','blueprints.py','helpers.py','scaffold.py','typing.py']
BLOBS={'app.py':'23b99e2ca08a9aaf6cb1b5f4b000efc324538812','blueprints.py':'5c23a735c8555b00b1793f47552442d49c50a96b','scaffold.py':'07ca5c6542a4da7e150850ef8a4cf1d500db1fbc','typing.py':'f1c84670292900fe9e7eb96edcd00fbc6a30ead0'}
def run(cmd,env=None,timeout=90):
 try:
  p=subprocess.run(cmd,env=env,text=True,capture_output=True,timeout=timeout)
  return {'exit':p.returncode,'stdout':p.stdout[-4000:],'stderr':p.stderr[-4000:]}
 except subprocess.TimeoutExpired as e:return {'exit':'TIMEOUT','stdout':str(e.stdout)[-100:],'stderr':str(e.stderr)[-100:]}
def must(cmd,timeout=180):
 r=run(cmd,timeout=timeout)
 if r['exit']!=0:raise RuntimeError(str((cmd,r)))
 return r['stdout'].strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
must(['git','clone','-q','--filter=blob:none','https://github.com/pallets/flask.git',str(ROOT/'repo')],240)
must(['git','-C',str(ROOT/'repo'),'fetch','-q','--tags','origin',REF],180)
for label,ref in [('base','2.0.2'),('ref',REF)]:must(['git','-C',str(ROOT/'repo'),'worktree','add','-q','--detach',str(ROOT/label),ref])
assert must(['git','-C',str(ROOT/'ref'),'rev-parse','HEAD'])==REF
base=ROOT/'base';reference=ROOT/'ref'
for file,expected in BLOBS.items():assert must(['git','-C',str(base),'hash-object','src/flask/'+file])==expected
HEAD=must(['git','-C',str(base),'rev-parse','HEAD'])
cases={
'T1_reporter':"from flask import Blueprint\nbp=Blueprint('b',__name__)\nclass A(Exception): pass\nclass B(Exception): pass\n@bp.errorhandler(B)\n@bp.errorhandler(A)\ndef error(e): return 'example'\n",
'T2_reverse':"from flask import Blueprint\nbp=Blueprint('b',__name__)\nclass A(Exception): pass\nclass B(Exception): pass\n@bp.errorhandler(A)\n@bp.errorhandler(B)\ndef error(e): return 'example'\n",
'T3_three':"from flask import Blueprint\nbp=Blueprint('b',__name__)\nclass A(Exception): pass\nclass B(Exception): pass\nclass C(Exception): pass\n@bp.errorhandler(C)\n@bp.errorhandler(B)\n@bp.errorhandler(A)\ndef error(e): return 'example'\n",
'C1_single':"from flask import Blueprint\nbp=Blueprint('b',__name__)\nclass A(Exception): pass\n@bp.errorhandler(A)\ndef error(e): return 'example'\n",
'C2_app':"from flask import Flask\na=Flask(__name__)\nclass A(Exception): pass\n@a.errorhandler(A)\ndef error(e): return 'example'\n",
'C3_bad_return':"from flask import Blueprint\nbp=Blueprint('b',__name__)\nclass A(Exception): pass\n@bp.errorhandler(A)\ndef error(e: A) -> int: return 42\n",
'C4_runtime':"from flask import Flask,Blueprint\na=Flask(__name__);b=Blueprint('b',__name__)\nclass A(Exception): pass\nclass B(Exception): pass\n@b.errorhandler(B)\n@b.errorhandler(A)\ndef error(e): return 'example'\n@b.route('/a')\ndef ra(): raise A()\n@b.route('/b')\ndef rb(): raise B()\na.register_blueprint(b)\nwith a.test_client() as c:\n assert c.get('/a').data==b'example' and c.get('/b').data==b'example'\nprint('RUNTIME_OK')\n"}
variants={'base':[],'ref':FILES}
for f in FILES:variants['only_'+f]=[f];variants['minus_'+f]=[x for x in FILES if x!=f]
receipts=[]
for variant,selected in variants.items():
 d=ROOT/'variants'/variant;d.parent.mkdir(exist_ok=True)
 shutil.copytree(base/'src/flask',d/'flask')
 for f in selected:shutil.copy2(reference/'src/flask'/f,d/'flask'/f)
 env=os.environ.copy();env['PYTHONPATH']=str(d);env['MYPYPATH']=str(d);env['PYTHONDONTWRITEBYTECODE']='1'
 for case,src in cases.items():
  p=ROOT/(case+'.py');p.write_text(src)
  cmd=[sys.executable,str(p)] if case=='C4_runtime' else [sys.executable,'-m','mypy','--no-incremental','--follow-imports=silent','--show-error-codes',str(p)]
  result=run(cmd,env=env,timeout=90)
  receipts.append({'variant':variant,'files':selected,'case':case,'result':result,'source_sha256':{f:sha(d/'flask'/f) for f in FILES}})
 print(variant,[(x['case'],x['result']['exit']) for x in receipts if x['variant']==variant],flush=True)
meta={'base_commit':HEAD,'reference_commit':REF,'verified_baseline_blobs':BLOBS,'python':sys.version,'mypy':run([sys.executable,'-m','mypy','--version']),'warning':'exploratory post-reference oracle implementation; NOT independently qualified'}
(ROOT/'meta.json').write_text(json.dumps(meta,indent=2))
(ROOT/'raw.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in receipts))
(ROOT/'sha256.json').write_text(json.dumps({p.name:sha(p) for p in [ROOT/'meta.json',ROOT/'raw.jsonl']},indent=2))
print('COMPLETE',len(receipts),flush=True)
