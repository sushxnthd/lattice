#!/usr/bin/env python3
"""Independent read-only Run327 cloud ZIP audit. Never imports tested urllib3."""
import hashlib
import json
import pathlib
import sys
import zipfile

BASE = ("daf9e4445a1cbef127bca1ac744e896b8534f6b7",
        "3167e6a8524bc0a6c886091901f686c79c0ca393",
        "ab562906a3e99fa1496d6efcd28d98533be84c72")
REF = ("7f37a860159eea97f515efc742e9f24884d8b9bd",
       "de5bb1f5e230e4be88b235867705abbcb0d3b393",
       "7ff0d903d62e7d5c8764e8de3c01992e6ee98c77")
FILES = ("connection.py", "connectionpool.py", "exceptions.py")
CASES = ("target_proxy_tls", "target_proxy_certificate",
         "target_proxy_http_exception", "control_direct_tls",
         "control_direct_certificate", "control_direct_http_exception",
         "control_direct_oserror", "control_proxy_valueerror",
         "control_direct_valueerror")

def load(path, expected_sha):
    data=pathlib.Path(path).read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected_sha
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        m=json.loads(z.read("SHA256_MANIFEST.json"))
        assert set(m)==set(z.namelist())-{"SHA256_MANIFEST.json"}
        assert all(hashlib.sha256(z.read(n)).hexdigest()==v for n,v in m.items())
        return {n:z.read(n) for n in z.namelist()},len(m)

def audit(original, corrected):
    a,an=load(original,"894863f0cc09c2bb66f580753a9271ea33903116f150b4998c51acd46c4a2597")
    b,bn=load(corrected,"eb1ed8fb3ba92496561c0348ddbde5002a86428e0f9b8d4fa52e1c0ca7f4f466")
    assert (an,bn)==(12,24)
    assert b["pinned_commits.txt"].decode().splitlines()==[
        "1c6405832e5348c740bc3b67b8b171b5da100a26",
        "111e609250bc7bf67b080b124298e0cf59efef9d"]
    pinned={row.split()[0]:tuple(row.split()[1:])
            for row in b["pinned_blobs.txt"].decode().splitlines()}
    assert pinned=={name:(BASE[i],REF[i]) for i,name in enumerate(FILES)}
    variants={}
    for line in b["variant_blobs.txt"].decode().splitlines():
        bits,name,sha=line.split()
        assert name in FILES and len(bits)==3 and all(c in "01" for c in bits)
        i=FILES.index(name)
        assert sha==(BASE[i],REF[i])[int(bits[i])]
        variants.setdefault(bits,{})[name]=sha
    assert len(variants)==8 and all(len(v)==3 for v in variants.values())
    status={bits:int(code) for bits,code in
            (line.split() for line in b["process_exit_status.txt"].decode().splitlines())}
    assert set(status)==set(variants)
    assert {k for k,v in status.items() if v==0}=={"000","110","111"}
    matrix={}; raw={}; unimportable={}
    for bits in sorted(status):
        if status[bits]:
            assert not b[f"oracle_{bits}.json"]
            tail=b[f"oracle_{bits}.stderr"].decode().strip().splitlines()[-1]
            assert tail.startswith("ImportError:")
            unimportable[bits]=tail
        else:
            r=json.loads(b[f"oracle_{bits}.json"])
            assert [x["case"] for x in r["rows"]]==list(CASES)
            assert all(x["pass"]==(x["observed"]==x["expected"]) for x in r["rows"])
            assert sum(x["pass"] for x in r["rows"][:3])==r["targets"]
            assert sum(x["pass"] for x in r["rows"][3:])==r["controls"]
            matrix[bits]=(r["targets"],r["controls"])
            raw[bits]=[(x["case"],x["observed"]) for x in r["rows"]]
    assert matrix=={"000":(0,6),"110":(3,6),"111":(3,6)}
    assert raw["110"]==raw["111"]
    assert json.loads(a["qualification.json"])["qualified"] is False
    result=json.loads(b["qualification.json"])
    assert result["qualified"] is False
    assert set(result["errors"])==set(unimportable)
    assert all(result["matrix"][k]["targets"]==v[0] and
               result["matrix"][k]["controls"]==v[1] for k,v in matrix.items())
    return {"manifest_verified":[an,bn],"source_blobs_verified":24,
            "executed_functional_cases":27,"unimportable":unimportable,
            "matrix":matrix,"full_equals_without_exceptions":True,
            "qualification":False,"audit_discrepancies":0}

if __name__=="__main__":
    print(json.dumps(audit(sys.argv[1],sys.argv[2]),indent=2,sort_keys=True))
