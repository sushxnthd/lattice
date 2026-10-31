"""Run380: independently audit original Qwen GitHub Actions artifact.

Usage: python run380_verify_original.py original_artifact.zip run379_archive.zip
Read-only; never imports or executes model-generated code.
"""
import ast
import hashlib
import json
import sys
import zipfile

ARMS = ("A_IR", "A_PYTHON_AST", "B_IR", "B_PYTHON_AST")
MODEL = "509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c"
COMPLETION = "522c56839327533457909ee01dc9fe68e5f2061e0160a47e6713222f27831c77"

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()

def run(artifact, previous):
    with zipfile.ZipFile(artifact) as z, zipfile.ZipFile(previous) as prior:
        names = z.namelist()
        assert len(names) == len(set(names))
        manifest = json.loads(z.read("manifest.json"))
        assert set(names) == set(manifest) | {"manifest.json"}
        for name, entry in manifest.items():
            data = z.read(name)
            assert len(data) == entry["size"] and sha(data) == entry["sha256"], name
        freeze = json.loads(z.read("freeze.json"))
        assert z.read("freeze.json") == prior.read("run379_frozen_requests.json")
        assert freeze["model_sha256"] == MODEL
        assert freeze["investigator_blind"] is False
        assert json.loads(z.read("preflight.json"))["unrelated_positive_control"] is True
        completions = set()
        patch_hashes = set()
        for arm in ARMS:
            req = json.loads(z.read("request_" + arm + ".json"))
            assert req == freeze["requests"][arm]
            assert sha(canonical(req)) == freeze["metadata"][arm]["request_sha256"]
            assert sha(req["messages"][0]["content"].encode()) == freeze["metadata"][arm]["prompt_sha256"]
            raw = json.loads(z.read("response_" + arm + ".raw.json"))
            completion = z.read("completion_" + arm + ".txt").decode()
            assert raw["choices"][0]["message"]["content"] == completion
            assert sha(completion.encode()) == COMPLETION
            assert json.loads(z.read("inference_" + arm + ".json"))["compiler"] == "accepted"
            completions.add(completion)
            payload = json.loads(completion.removeprefix("```json\n").removesuffix("\n```"))
            assert len(payload["edits"]) == 2
            traces = json.loads(z.read("compiler_trace_" + arm + ".json"))
            assert len(traces) == 2
            for edit, trace in zip(payload["edits"], traces):
                assert edit["path"] == trace["path"]
                assert edit["old"] == trace["old"] and edit["new"] == trace["new"]
                assert edit["source_sha256"] == trace["source_sha256"]
                ast.parse(edit["new"])
            patch_hashes.add(tuple(t["result_sha256"] for t in traces))
            for phase, expected in (("public", 8), ("heldout", 4)):
                cases = json.loads(z.read("oracle_" + arm + "_" + phase + ".json"))["cases"]
                assert len(cases) == expected
                assert all(c["passed"] and c["expected"] == c["observed"] for c in cases)
        assert len(completions) == 1 and len(patch_hashes) == 1
        assert [sum(c["passed"] for c in json.loads(z.read("oracle_BASE_" + p + ".json"))["cases"]) for p in ("public", "heldout")] == [6, 2]
        print(json.dumps({"manifest_verified": len(manifest), "genuine_completions": 4,
                          "identical_completions": True, "identical_compiled_sources": True,
                          "IR_successes": 2, "Python_AST_successes": 2,
                          "per_arm_public": "8/8", "per_arm_heldout": "4/4",
                          "distinct_issues": 1, "representation_superiority": "not established"}, indent=2))

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
