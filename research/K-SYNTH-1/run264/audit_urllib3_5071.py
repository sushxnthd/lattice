#!/usr/bin/env python3
"""Independent offline replay of Run264 urllib3 PR5071 six-arm qualification."""
import hashlib,json,zipfile,sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else "run264_urllib3.zip")
assert hashlib.sha256(p.read_bytes()).hexdigest()=="5fa25d28fe6ffa1e4c2a72daa624d96162a68389affb90a6aa6757ddf77c7301"
with zipfile.ZipFile(p) as z:
    m=json.loads(z.read("SHA256_MANIFEST.json"))
    validity={n:hashlib.sha256(z.read(n)).hexdigest()==h for n,h in m.items()}
    assert validity["qualification.json"]
    d=json.loads(z.read("qualification.json"))
assert d["base_commit"]=="f4e4bc31f40f8c94c6a1f1685df28f97ff48c305"
assert d["reference_commit"]=="f5cf122346141b187cca0db6e6445297d336b610"
expected={
    "baseline":(False,False,False),
    "poolmanager_only":(True,True,False),
    "url_only":(False,False,True),
    "connectionpool_only":(False,False,False),
    "poolmanager_plus_url":(True,True,True),
    "full_reference":(True,True,True),
}
target=("public_manager_explicit_port_zero","heldout_proxy_explicit_zero","heldout_url_netloc_explicit_zero")
nonreg=("nonreg_default_manager_port","nonreg_pool_host_identity","nonreg_url_default_port")
assert set(d["variants"])==set(expected)
for name,v in d["variants"].items():
    assert v["returncode"]==0 and not v["stderr"]
    assert json.loads(v["stdout"])==v["parsed"]
    checks=v["parsed"]["checks"]
    assert tuple(checks[k]["pass"] for k in target)==expected[name]
    assert all(checks[k]["pass"] for k in nonreg)
    for f in d["base_sha256"]:
        correct=d["reference_sha256"][f] if f in v["changed_files"] else d["base_sha256"][f]
        assert v["source_sha256"][f]==correct
assert d["qualifies"] is True
print(json.dumps({"independent_replay":"PASS","qualifies":True,"manifest_validity":validity,
                  "limits":"Only reference-patch component necessity under frozen endpoints, not all possible one-file fixes."},sort_keys=True))
