"""Exact pinned Flask #5804 qualification, frozen issue-first gate."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,traceback
BASE='330123258e8c3dc391cbe55ab1ed94891ca83af3'
REF='c2705ffd9ce1dc8476cb29eaf5ff5d4c719852d9'
repo=pathlib.Path(os.environ.get('RUN426_FLASK_REPO','/tmp/run426-flask'))
out=pathlib.Path(os.environ.get('RUN426_OUTPUT','run426_cloud_raw.json'))
child=r'''
import json,os,pathlib,sys
root=pathlib.Path(os.environ['RUN426_ROOT']).resolve()
sys.path.insert(0,str(root/'src'))
from flask import Flask,Response,g,stream_with_context,has_request_context,has_app_context
import flask
assert pathlib.Path(flask.__file__).resolve().is_relative_to(root/'src')
results={}
def record(k,ok,detail):results[k]={'pass':bool(ok),'detail':detail}
def make():
 a=Flask('run426');a.testing=True;ev=[]
 @a.teardown_request
 def td(exc):ev.append('td')
 @a.get('/stream')
 def stream():
  g.hello='world'
  def gen():
   ev.append('start');yield 'HELLO:'+g.hello;ev.append('end')
  return Response(stream_with_context(gen()))
 @a.get('/plain')
 def plain():return 'plain-ok'
 @a.get('/plain-stream')
 def plainstream():
  def gen():yield 'UNEXPECTED:'+g.hello
  return Response(gen())
 @a.get('/raising')
 def raising():
  def gen():yield 'first';raise ValueError('frozen-midstream-marker')
  return Response(stream_with_context(gen()))
 return a,ev
app,ev=make()
try:body=app.test_client().get('/stream',buffered=True).get_data(as_text=True);err=None
except Exception as e:body=None;err=type(e).__name__+': '+str(e)
record('positive_stream_body',body=='HELLO:world',[body,err])
record('positive_start_before_teardown','start' in ev and ('td' not in ev or ev.index('start')<ev.index('td')),list(ev))
record('positive_teardown_once',ev.count('td')==1,list(ev))
record('positive_stream_complete',body=='HELLO:world' and 'end' in ev,list(ev))
record('control_no_context_leak',not has_request_context() and not has_app_context(),[has_request_context(),has_app_context()])
a,e=make()
try:plain=a.test_client().get('/plain').get_data(as_text=True);err=None
except Exception as ex:plain=None;err=repr(ex)
record('negative_plain_teardown_once',e.count('td')==1,[e,err])
record('control_plain_response',plain=='plain-ok',plain)
record('control_plain_teardown_before_return',plain=='plain-ok' and e.count('td')==1,list(e))
a,e=make()
try:a.test_client().get('/plain-stream',buffered=True);err=None
except Exception as ex:err=type(ex).__name__
record('negative_plain_stream_no_ambient_context',err=='RuntimeError',err)
a,e=make()
try:a.test_client().get('/raising',buffered=True);err=None
except Exception as ex:err=type(ex).__name__+': '+str(ex)
record('negative_stream_exception_preserved',err=='ValueError: frozen-midstream-marker',err)
a,e=make()
try:
 x=a.test_client().get('/stream',buffered=True).get_data(as_text=True)
 y=a.test_client().get('/stream',buffered=True).get_data(as_text=True)
 err=None
except Exception as ex:x=y=None;err=repr(ex)
record('control_repeated_teardown',e.count('td')==2,[e,x,y,err])
print(json.dumps({'results':results,'passed':sum(v['pass'] for v in results.values()),'total':len(results),'import':flask.__file__},sort_keys=True))
'''
def cmd(*args):
 p=subprocess.run(args,capture_output=True,text=True,check=True,timeout=90)
 return p.stdout.strip()
assert cmd('git','-C',str(repo),'rev-parse',BASE)==BASE
assert cmd('git','-C',str(repo),'rev-parse',REF)==REF
changed=cmd('git','-C',str(repo),'diff','--name-only',BASE,REF).splitlines()
prod=[p for p in changed if p.startswith('src/flask/') and p.endswith('.py')]
with tempfile.TemporaryDirectory(prefix='run426-') as td:
 t=pathlib.Path(td)
 def archive(sha,name):
  dest=t/name;dest.mkdir()
  a=subprocess.Popen(['git','-C',str(repo),'archive',sha],stdout=subprocess.PIPE)
  b=subprocess.run(['tar','-xf','-','-C',str(dest)],stdin=a.stdout,capture_output=True,text=True,timeout=60)
  a.stdout.close();assert a.wait()==0 and b.returncode==0,b.stderr
  return dest
 base=archive(BASE,'base');ref=archive(REF,'reference')
 variants={'base':base,'reference':ref}
 for p in prod:
  key='without_'+p.replace('/','_')
  dest=t/key;shutil.copytree(ref,dest);shutil.copy2(base/p,dest/p)
  variants[key]=dest
 results={}
 for name,path in variants.items():
  env=os.environ.copy();env['RUN426_ROOT']=str(path)
  p=subprocess.run([sys.executable,'-c',child],env=env,capture_output=True,text=True,timeout=60)
  try:res=json.loads(p.stdout)
  except Exception:res=None
  results[name]={'exit':p.returncode,'data':res,'stdout':p.stdout[-4000:],'stderr':p.stderr[-4000:]}
 full=results['reference']['data']
 refpass=bool(full and full['passed']==full['total']==11)
 necessary=[]
 for p in prod:
  d=results['without_'+p.replace('/','_')]['data']
  if d and d['total']==11 and d['passed']<11:necessary.append(p)
 report={'issue':'https://github.com/pallets/flask/issues/5804','base':BASE,'reference':REF,
         'changed':changed,'production_changed':prod,'results':results,
         'reference_passes':refpass,'importable_leave_one_out_failures':necessary,
         'qualified':bool(refpass and len(necessary)>=2),
         'warning':'Broad PR #5812. Import failures never count as component necessity.'}
 out.write_text(json.dumps(report,indent=2,sort_keys=True))
 print(json.dumps({'qualified':report['qualified'],'reference_passes':refpass,
                   'production_changed':len(prod),'importable_leave_one_out_failures':necessary,
                   'raw_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},sort_keys=True))
