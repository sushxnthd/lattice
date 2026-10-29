#!/usr/bin/env python3
"""Independent read-only Run332 original evidence audit. Never executes model code."""
import hashlib, json, sys, zipfile
from pathlib import Path

EXPECTED={"probe_a":("probe_a.py",False,True),"probe_b":("probe_b.py",True,False)}
def digest(blob):return hashlib.sha256(blob).hexdigest()

def audit(archive):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        manifest=json.loads(z.read("SHA256_MANIFEST.json"))
        assert set(manifest)==set(z.namelist())-{"SHA256_MANIFEST.json"}
        for name,h in manifest.items():assert digest(z.read(name))==h,name
        meta=json.loads(z.read("freeze.json"))
        rows=json.loads(z.read("gate_candidates.json"))
        by_qual={r["qual"]:r for r in rows}
        assert len(rows)==2 and set(by_qual)==set(EXPECTED)
        for name,(path,old,new) in EXPECTED.items():
            row=by_qual[name]
            assert row["path"]==path and row["param"]=="flag"
            assert row["old_expr"]==str(old)
            assert row["old_sha256"]==digest(str(old).encode())
            assert row["source_sha256"]==digest(f"def {name}(flag: bool = {old}):\n    return flag\n".encode())
            assert row["id"] not in EXPECTED
        assert meta["gate_requires_two_files"] and meta["gate_target_count"]==2
        arms={}
        for arm in ("IR","PYTHON_AST"):
            name="GATE_"+arm
            request=z.read("request_"+name+".json")
            assert digest(request)==meta["requests"][name]["request_sha256"]
            prompt=json.loads(request)["messages"][0]["content"]
            assert digest(prompt.encode())==meta["requests"][name]["prompt_sha256"]
            assert all(by_qual[q]["id"] in prompt for q in EXPECTED)
            infer=json.loads(z.read("inference_"+name+".json"))
            completion=z.read("completion_"+name+".txt")
            assert digest(completion)==infer["completion_sha256"]
            assert digest(z.read("raw_"+name+".json"))==infer["raw_sha256"]
            assert infer["finish_reason"]=="stop"
            obj=json.loads(completion)
            assert set(obj)=={"edits"} and isinstance(obj["edits"],list)
            edits=obj["edits"]
            structural=len(edits)==2 and all(isinstance(e,dict) and set(e)=={"id","new_expr"} for e in edits)
            ids=[e["id"] for e in edits] if structural else []
            opaque={r["id"] for r in rows}
            strict=structural and len(set(ids))==2 and set(ids)==opaque
            semantic=structural and len(set(ids))==2 and set(ids)==set(EXPECTED) and all(e["new_expr"]==str(EXPECTED[e["id"]][2]) for e in edits)
            compiled=json.loads(z.read("compile_"+name+".json"))
            assert compiled["accepted"] is False and compiled["error"]=="GATE_REQUIRES_BOTH_DISTINCT_IDS"
            assert strict is False
            translation=[{"id":by_qual[e["id"]]["id"],"new_expr":e["new_expr"]} for e in edits] if semantic else None
            arms[arm]={"completion_sha256":infer["completion_sha256"],"prompt_tokens":infer["usage"]["prompt_tokens"],"completion_tokens":infer["usage"]["completion_tokens"],"strict_accepted":strict,"semantic_two_action_correct":semantic,"counterfactual_not_original":translation}
        gate=json.loads(z.read("gate_summary.json"))
        assert gate=={"gates":{"IR":False,"PYTHON_AST":False},"both_pass":False}
        assert "completion_REAL_IR.txt" not in z.namelist() and "completion_REAL_PYTHON_AST.txt" not in z.namelist()
        assert "gate_failure.txt" in z.namelist()
        base=json.loads(z.read("oracle_BASE.json"))
        assert len(base["cases"])==9
        assert [bool(c["passed"]) for c in base["cases"]]==[False]*3+[True]*6
        return {"archive_sha256":digest(Path(archive).read_bytes()),"manifest_entries":len(manifest),"original_gate":gate,"real_inference_attempted":False,"arms":arms}

if __name__=="__main__":
    print(json.dumps({"schema":"run333-independent-original-run332-audit-v1","results":[audit(p) for p in sys.argv[1:]]},indent=2,sort_keys=True))
