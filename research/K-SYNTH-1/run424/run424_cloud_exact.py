#!/usr/bin/env python3
"""Run424 exact historical urllib3 PR5071 source replay (post-reference)."""
import hashlib, itertools, json, pathlib, shutil, subprocess, sys, tempfile

BASE=pathlib.Path(sys.argv[1]).resolve()
REF=pathlib.Path(sys.argv[2]).resolve()
OUT=pathlib.Path(sys.argv[3]).resolve()
OUT.mkdir(parents=True,exist_ok=True)
FILES=("connectionpool.py","poolmanager.py","util/url.py")
EXPECTED={
"connectionpool.py":"7e6f54c82e3b8d4b5bfee7b48c8717fa2b650f1f",
"poolmanager.py":"b7248d210dc8adea1b48dccab2c08860ad543328",
"util/url.py":"6d0c66a30f5abea74db7bf0cd99da1c62b23a10d"}
PATCHES={
"connectionpool.py":[("if self.port and not port:","if self.port is not None and port is None:"),
("elif not self.port and port == port_by_scheme.get(scheme):","elif self.port is None and port == port_by_scheme.get(scheme):")],
"poolmanager.py":[('if not port:\n            port = port_by_scheme.get(request_context["scheme"].lower(), 80)',
'if port is None:\n            port = port_by_scheme.get(request_context["scheme"].lower(), 80)'),
("if not proxy.port:","if proxy.port is None:")],
"util/url.py":[('if self.port:\n            return f"{self.host}:{self.port}"',
'if self.port is not None:\n            return f"{self.host}:{self.port}"')]}
ORACLE=r'''import json,sys,pathlib
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root))
for n in list(sys.modules):
 if n=="urllib3" or n.startswith("urllib3."):del sys.modules[n]
import urllib3
from urllib3 import PoolManager,ProxyManager,HTTPConnectionPool,HTTPSConnectionPool
from urllib3.util import Url
r={}
def get(k,f):
 try:r[k]={"status":"OK","value":f()}
 except Exception as e:r[k]={"status":"EXCEPTION","type":type(e).__name__,"message":str(e)}
for scheme in ("http","https"):
 for port in (None,0,1,80,443,8080,65535):
  k=f"{scheme}_{port}"
  get("netloc_"+k,lambda s=scheme,p=port:Url(scheme=s,host="example.com",port=p).netloc)
  get("poolhost_"+k,lambda s=scheme,p=port:PoolManager().connection_from_host("example.com",port=p,scheme=s).port)
  get("poolurl_"+k,lambda s=scheme,p=port:PoolManager().connection_from_url(s+"://example.com"+("" if p is None else ":"+str(p))+"/").port)
  get("samehost_"+k,lambda s=scheme,p=port:(HTTPConnectionPool if s=="http" else HTTPSConnectionPool)("example.com",port=p).is_same_host(s+"://example.com:0"))
  get("proxy_"+k,lambda s=scheme,p=port:ProxyManager(s+"://localhost"+("" if p is None else ":"+str(p))).proxy.port)
modules={k:str(pathlib.Path(v.__file__).resolve()) for k,v in sys.modules.items() if (k=="urllib3" or k.startswith("urllib3.")) and getattr(v,"__file__",None)}
assert modules and all(pathlib.Path(p).is_relative_to(root/"urllib3") for p in modules.values()),modules
print(json.dumps({"observations":r,"module_paths":modules},sort_keys=True))
'''
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
source={p:(BASE/"urllib3"/p).read_bytes() for p in FILES}
assert {p:blob(b) for p,b in source.items()}==EXPECTED,"historical base blob mismatch"
ref={p:(REF/"urllib3"/p).read_bytes() for p in FILES}
arms=[]
for flags in itertools.product((0,1),repeat=3):
 subset=[p for p,f in zip(FILES,flags) if f]
 edits={}
 for p,b in source.items():
  if p in subset:
   for old,new in PATCHES[p]:
    old=old.encode();new=new.encode()
    assert b.count(old)==1,(p,old,b.count(old))
    b=b.replace(old,new,1)
  edits[p]=b
 if flags==(1,1,1):assert edits==ref,"full production reference not reproduced byte-for-byte"
 with tempfile.TemporaryDirectory() as td:
  root=pathlib.Path(td)
  shutil.copytree(BASE/"urllib3",root/"urllib3")
  for p,b in edits.items():(root/"urllib3"/p).write_bytes(b)
  for cache in root.rglob("__pycache__"):shutil.rmtree(cache)
  proc=subprocess.run([sys.executable,"-I","-c",ORACLE,str(root)],capture_output=True,text=True,timeout=40)
  assert proc.returncode==0,(proc.returncode,proc.stderr)
  response=json.loads(proc.stdout)
 arms.append({"flags":flags,"files":subset,"output_sha256":{p:sha(b) for p,b in edits.items()},**response})
base=arms[0]["observations"];full=arms[-1]["observations"]
assert len(base)==len(full)==70
target={}
for s in ("http","https"):
 k=s+"_0"
 for kind,value in (("netloc","example.com:0"),("poolhost",0),("poolurl",0),("proxy",0),("samehost",True)):
  target[kind+"_"+k]={"status":"OK","value":value}
controls=set(base)-set(target)
stats=[]
for arm in arms:
 rows=arm["observations"]
 stats.append({"flags":arm["flags"],"target_pass":sum(rows[k]==v for k,v in target.items()),
 "controls_preserved":sum(rows[k]==base[k] for k in controls),
 "changed_vs_base":sum(rows[k]!=base[k] for k in base)})
violations=[k for k in sorted(controls) if base[k]!=full[k]]
raw={"classification":"POST_REFERENCE_EXACT_HISTORICAL_SOURCE","merge_commit":"f5cf122346141b187cca0db6e6445297d336b610",
"base_blobs":EXPECTED,"reference_sha256":{p:sha(b) for p,b in ref.items()},
"frozen_oracle_target_count":len(target),"frozen_oracle_control_count":len(controls),
"frozen_nonregression_failures":violations,"stats":stats,"arms":arms}
(OUT/"run424_cloud_raw.json").write_text(json.dumps(raw,indent=2,sort_keys=True)+"\n")
(OUT/"run424_cloud_summary.json").write_text(json.dumps({k:v for k,v in raw.items() if k!="arms"},indent=2,sort_keys=True)+"\n")
print(json.dumps({"historical_reference_exact":True,"arms":len(arms),"observations":sum(len(a["observations"]) for a in arms),
"full_target_pass":stats[-1]["target_pass"],"full_controls_preserved":stats[-1]["controls_preserved"],
"frozen_control_failures":violations},sort_keys=True))
assert stats[-1]["target_pass"]==10,"frozen target failure"
# Preserve any frozen control failures; do not relabel them as passed.
