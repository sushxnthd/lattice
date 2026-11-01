#!/usr/bin/env python3
"""Run407 original pytest14997 GitHub evidence auditor (read-only, standard library)."""
import hashlib,json,re,sys,zipfile
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else ".")
SPECS={
 "903":("8476adf7ac95eb32c4d92be3e4269093945761cb4f851bdeef84d1f3cc63a15e","a7d58d7a21b78581e636bbbdea13c66ad1657c1e",(3,3,6)),
 "911":("89bbb9ecf1269044cc5ee78b27bf6ec2c384cd49bbc73374bbb12a250e971633","cf470ec0bf7eb89cd97dd56df4859eae5db46447",(0,0,6))}
IDS=["P1","P2","P3","H1","H2","H3","C1","C2","C3","C4","C5","C6"]
GROUPS=["public_target"]*3+["heldout_target"]*3+["control"]*6
def sha(b):return hashlib.sha256(b).hexdigest()
def audit(version):
 expected,ref,counts=SPECS[version]
 p=ROOT/("run407_original"+version+"_frozen.zip")
 assert sha(p.read_bytes())==expected
 with zipfile.ZipFile(p) as z:
  manifest=json.loads(z.read("SHA256_MANIFEST.json"))
  assert set(manifest)==set(z.namelist())-{"SHA256_MANIFEST.json"}
  for name,digest in manifest.items():assert sha(z.read(name))==digest,(version,name)
  assert z.read("pinned_source_commit.txt").decode().strip()==ref
  raw=json.loads(z.read("evidence/raw_oracle.json"))
  assert raw["schema"]=="lattice.run405.pytest14997.v1"
  assert raw["issue"]=="pytest-dev/pytest#14997"
  assert ref[:9] in raw["version_stdout"]
  assert raw["version_rc"]==0 and len(raw["source_sha256"])==14
  assert [r["id"] for r in raw["rows"]]==IDS
  assert [r["kind"] for r in raw["rows"]]==GROUPS
  for r in raw["rows"]:
   assert r["status"]==("PASS" if r["returncode"]==0 else "FAIL")
   if r["status"]=="PASS":
    assert re.search(r"\b[23] passed in ",r["stdout"])
   else:
    assert r["returncode"]==1 and "2 passed, 1 error" in r["stdout"]
    assert "fixture '" in r["stdout"] and "' not found" in r["stdout"]
  observed=tuple(sum(r["status"]=="PASS" for r in raw["rows"] if r["kind"]==g) for g in ("public_target","heldout_target","control"))
  assert observed==counts,(version,observed,counts)
  original=json.loads(z.read("evidence/summary.json"))
  assert tuple(original[g] for g in ("public_target","heldout_target","control"))==observed
  return {"version":version,"source_commit":ref,"counts":observed,"artifact_sha256":expected,"oracle_sha256":z.read("oracle_sha256.txt").decode().split()[0]}
if __name__=="__main__":
 result=[audit(v) for v in ("903","911")]
 print(json.dumps({"results":result,"baseline_reproduced":True,"qualified_repair":False},indent=2))
