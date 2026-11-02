#!/usr/bin/env python3
"""Real urllib3 2.7.0 counterexample: observed C->U call, but only C edit repairs.

Requires installed urllib3 2.7.0 with exact source hashes. Never executes model code.
"""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
SOURCE_SHA={
 'connectionpool.py':'b0616775d5d8c25c7b282e0908fd602af74d18b34af984c22437460021a3dd8f',
 'util/url.py':'59187e4cc617a2c9a0a7c9bc953e07e6ca681f0e7252395c3027d4e77024a00b',
}
CHILD=r'''
import json,pathlib,socket,sys
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root))
for k in list(sys.modules):
 if k=='urllib3' or k.startswith('urllib3.'):del sys.modules[k]
import urllib3
assert pathlib.Path(urllib3.__file__).resolve().is_relative_to(root)
from urllib3.connectionpool import HTTPConnectionPool
socket.socket.connect=lambda *a,**kw: (_ for _ in ()).throw(RuntimeError('NETWORK_FORBIDDEN'))
seen=[]
def prof(f,event,arg):
 if event=='call' and f.f_code.co_name=='parse_url' and f.f_code.co_filename.endswith('util/url.py'):
  p=f.f_back
  if p is not None and p.f_code.co_name=='is_same_host' and p.f_code.co_filename.endswith('connectionpool.py'):
   seen.append('connectionpool.py:is_same_host -> util/url.py:parse_url')
sys.setprofile(prof)
with HTTPConnectionPool('example.com',port=80) as pool:actual=pool.is_same_host('http://example.com:0/')
sys.setprofile(None)
print(json.dumps({'actual':actual,'expected':False,'observed_call':bool(seen)}))
'''
def replace_one(p,old,new):
 data=p.read_text();assert data.count(old)==1,(p,old,data.count(old));p.write_text(data.replace(old,new))
def main():
 import urllib3
 assert urllib3.__version__=='2.7.0'
 src=pathlib.Path(urllib3.__file__).parent
 for name,sha in SOURCE_SHA.items():
  got=hashlib.sha256((src/name).read_bytes()).hexdigest()
  assert got==sha,(name,got,sha)
 with tempfile.TemporaryDirectory() as td:
  result={}
  for variant in ('BASE','U','C'):
   root=pathlib.Path(td)/variant
   shutil.copytree(src,root/'urllib3',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
   if variant=='U':replace_one(root/'urllib3/util/url.py','if self.port:\n            return f"{self.host}:{self.port}"','if self.port is not None:\n            return f"{self.host}:{self.port}"')
   if variant=='C':
    p=root/'urllib3/connectionpool.py'
    replace_one(p,'if self.port and not port:', 'if self.port is not None and port is None:')
    replace_one(p,'elif not self.port and port == port_by_scheme.get(scheme):','elif self.port is None and port == port_by_scheme.get(scheme):')
   proc=subprocess.run([sys.executable,'-c',CHILD,str(root)],capture_output=True,text=True,check=True)
   result[variant]=json.loads(proc.stdout)
 assert result['BASE']==result['U']=={'actual':True,'expected':False,'observed_call':True}
 assert result['C']=={'actual':False,'expected':False,'observed_call':True}
 print(json.dumps({'result':result,'conclusion':'OBSERVED_CALL does not entail EDIT_NECESSITY'},sort_keys=True))
if __name__=='__main__':main()
