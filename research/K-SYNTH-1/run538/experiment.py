import hashlib,json,subprocess,tempfile,pathlib,sys
H=lambda b:hashlib.sha256(b).hexdigest()
CASES=[('stable','print("A")\n','print("A")\n','A','A'),('mutated_after_hash','print("A")\n','print("B")\n','B','A'),('syntax_corruption','print("A")\n','print(\n','','A'),('same_bytes','print("A")\n','print("A")\n','A','A'),('semantic_swap','print(1+1)\n','print(1+2)\n','3','2'),('empty','print("A")\n','','','A'),('exit_change','print("A")\n','raise SystemExit(7)\n','','A'),('unicode','print("λ")\n','print("μ")\n','μ','λ')]
def run(path):
 try:
  p=subprocess.run([sys.executable,'-I',str(path)],capture_output=True,text=True,timeout=3,cwd=str(path.parent))
  return {'code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr[-150:]}
 except subprocess.TimeoutExpired:return {'timeout':True}
results=[]
with tempfile.TemporaryDirectory() as td:
 root=pathlib.Path(td)
 for name,original,modified,expected_live,expected_snapshot in CASES:
  live=root/(name+'.py');snap=root/(name+'.snapshot.py');live.write_bytes(original.encode());frozen=H(live.read_bytes());snap.write_bytes(live.read_bytes());live.write_bytes(modified.encode());r_live=run(live);r_snap=run(snap)
  entry={'case':name,'frozen_sha':frozen,'live_sha':H(live.read_bytes()),'snapshot_sha':H(snap.read_bytes()),'live':r_live,'snapshot':r_snap,'expected_live':expected_live,'expected_snapshot':expected_snapshot,'hash_detects_mutation':frozen!=H(live.read_bytes())}
  assert entry['snapshot_sha']==frozen
  assert r_live['stdout']==expected_live,(name,r_live)
  assert r_snap['stdout']==expected_snapshot,(name,r_snap)
  results.append(entry)
print(json.dumps({'experiment':'run538 TOCTOU provenance','cases':results,'passed':len(results),'limitations':['snapshot copy is not an OS sandbox','concurrent mutation during snapshot creation not ruled out','trusted interpreter and filesystem assumed','no public-repo repair or model inference']},indent=2,ensure_ascii=False))
