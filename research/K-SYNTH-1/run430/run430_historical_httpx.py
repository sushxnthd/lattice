#!/usr/bin/env python3
"""Run430 historical HTTPX #1833 exact-source factorial replay; no model code."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
MERGE="57daabf673705954afa94686c0002801c93d31f3"
CASES=[
("https://example.com/?[]","/","https://example.com/"),
("https://example.com/?f[author][]=nick","/next","https://example.com/next"),
("https://example.com/a/b?x=1","../c","https://example.com/c"),
("https://example.com/a?x=1","/z","https://example.com/z"),
("https://example.com/a?x=1","?y=2","https://example.com/a?y=2"),
("https://example.com/a/b","/","https://example.com/"),
("https://example.com/a/b?x=1","#frag","https://example.com/a/b?x=1#frag"),
("https://example.com/a/b","../c","https://example.com/c")]
OUT=pathlib.Path(os.environ.get("RUN430_OUT","run430_cloud_output")).resolve();OUT.mkdir(parents=True,exist_ok=True)
def command(*args):
 p=subprocess.run(args,text=True,capture_output=True,timeout=300)
 if p.returncode:raise RuntimeError(f"{args!r} failed: {p.stderr[-2000:]}")
 return p.stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
probe=r'''import json,sys,traceback
p=sys.argv[1];sys.path.insert(0,p)
try:
 import httpx
 assert httpx.__file__.startswith(p),(httpx.__file__,p)
 print(json.dumps({"type":"import","path":httpx.__file__,"version":getattr(httpx,"__version__",None)}))
 for base,rel,expect in json.loads(sys.argv[2]):
  try: got=str(httpx.URL(base).join(rel));err=None
  except Exception as exc:got=None;err=type(exc).__name__+": "+str(exc)
  print(json.dumps({"type":"case","base":base,"relative":rel,"expected":expect,"actual":got,"error":err,"passed":got==expect and err is None}))
except Exception as exc:
 print(json.dumps({"type":"import_error","error":type(exc).__name__+": "+str(exc),"trace":traceback.format_exc()}))
'''
with tempfile.TemporaryDirectory(prefix="run430-") as td:
 root=pathlib.Path(td);repo=root/"upstream"
 try:command("git","clone","-q","--filter=blob:none","https://github.com/encode/httpx.git",str(repo))
 except Exception:command("git","clone","-q","https://github.com/encode/httpx.git",str(repo))
 command("git","-C",str(repo),"fetch","-q","origin",MERGE)
 base=command("git","-C",str(repo),"rev-parse",MERGE+"^")
 base_dir=root/"base";ref_dir=root/"ref"
 command("git","-C",str(repo),"worktree","add","--detach",str(base_dir),base)
 command("git","-C",str(repo),"worktree","add","--detach",str(ref_dir),MERGE)
 variants={}
 for name,source in [("base",base_dir),("full_ref",ref_dir),("onefile_query_strip",base_dir),("reference_urls_only",base_dir),("reference_parser_only",base_dir)]:
  dest=root/("variant_"+name);shutil.copytree(source,dest,ignore=shutil.ignore_patterns(".git"));variants[name]=dest
 p=variants["onefile_query_strip"]/"httpx/_urls.py";s=p.read_text();needle="copy_with(fragment=None)"
 assert s.count(needle)==1,(s.count(needle),str(p))
 p.write_text(s.replace(needle,"copy_with(fragment=None, query=None)",1))
 shutil.copy2(ref_dir/"httpx/_urls.py",variants["reference_urls_only"]/"httpx/_urls.py")
 shutil.copy2(ref_dir/"httpx/_urlparse.py",variants["reference_parser_only"]/"httpx/_urlparse.py")
 manifest={"merge":MERGE,"first_parent":base,"cases":CASES,"variants":{}}
 results=[]
 for name,d in variants.items():
  files=["httpx/__init__.py","httpx/_urls.py","httpx/_urlparse.py"]
  manifest["variants"][name]={"source_sha256":{f:sha(d/f) for f in files}}
  env=os.environ.copy();env["PYTHONNOUSERSITE"]="1";env.pop("PYTHONPATH",None)
  p=subprocess.run([sys.executable,"-c",probe,str(d),json.dumps(CASES)],cwd=str(root),env=env,text=True,capture_output=True,timeout=60)
  (OUT/(name+"_stdout.txt")).write_text(p.stdout);(OUT/(name+"_stderr.txt")).write_text(p.stderr)
  manifest["variants"][name]["returncode"]=p.returncode
  for line in p.stdout.splitlines():
   try:obj=json.loads(line)
   except Exception:obj={"type":"non_json","text":line}
   results.append({"variant":name,"record":obj})
 (OUT/"run430_historical_manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
 (OUT/"run430_historical_raw.jsonl").write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in results))
 summary={name:{"cases":sum(r["record"].get("type")=="case" for r in results if r["variant"]==name),"passed":sum(r["record"].get("passed") is True for r in results if r["variant"]==name),"import_errors":[r["record"].get("error") for r in results if r["variant"]==name and r["record"].get("type")=="import_error"]} for name in variants}
 (OUT/"run430_historical_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"first_parent":base,"summary":summary},sort_keys=True))
