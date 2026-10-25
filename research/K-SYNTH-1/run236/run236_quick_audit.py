#!/usr/bin/env python3
"""Independent read-only audit of Run234 artifact directories, including truncated JSON."""
import ast
import hashlib
import json
import pathlib
import sys


def read(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def audit(root):
    root = pathlib.Path(root)
    expected = read(root / "SHA256_MANIFEST.json")
    actual = {str(p.relative_to(root)): sha(p.read_bytes()) for p in root.rglob("*")
              if p.is_file() and p.name != "SHA256_MANIFEST.json"}
    assert expected == actual, "artifact manifest mismatch"
    freeze = read(root / "freeze.json")
    facts = read(root / "facts.json")
    eq = read(root / "equivalence.json")
    records = read(root / "records.json")
    assert sha(canonical(facts)) == eq["facts_sha256"]
    assert len(records) == 2 and {r["arm"] for r in records} == set(freeze["arms"])
    results = []
    for rec in records:
        stem = root / "raw" / (freeze["issue"] + "-" + rec["arm"])
        req = read(pathlib.Path(str(stem) + "-request.json"))
        res = read(pathlib.Path(str(stem) + "-response.json"))
        assert read(pathlib.Path(str(stem) + "-verifier.json")) == rec
        assert sha(req["messages"][0]["content"].encode()) == rec["prompt_sha256"]
        assert req["model"] == rec["model"] == freeze["model"]
        assert req["seed"] == rec["seed"] == freeze["seed"]
        assert res["usage"] == rec["usage"] and rec["facts_sha256"] == eq["facts_sha256"]
        content = res["choices"][0]["message"]["content"]
        try:
            out = json.loads(content)
            valid_json = True
        except json.JSONDecodeError:
            out = {}
            valid_json = False
        if rec["accepted"]:
            assert valid_json
        erased = []
        vacuous = []
        if rec["accepted"]:
            after = read(pathlib.Path(str(stem) + "-after.json"))
            assert all(sha(s.encode()) == rec["after"][p] for p, s in after.items())
            for a in out.get("actions", []):
                if a.get("op") != "replace" or a["path"] not in after:
                    continue
                target = [t for t in facts[a["path"]]["targets"]
                          if t["target_id"] == a["selector"]]
                assert len(target) == 1
                t = target[0]
                if t["kind"] in ("FunctionDef", "AsyncFunctionDef", "ClassDef"):
                    tree = ast.parse(after[a["path"]])
                    if not any(type(n).__name__ == t["kind"]
                               and getattr(n, "name", None) == t["name"]
                               for n in ast.walk(tree)):
                        erased.append(t["name"])
            if freeze["issue"] == "tox-dev__sphinx-autodoc-typehints-422":
                src = after.get("tests/roots/test-dummy/conf.py", "")
                extension_lists = [ast.literal_eval(n.value) for n in ast.parse(src).body
                                   if isinstance(n, ast.Assign)
                                   and any(isinstance(t, ast.Name) and t.id == "extensions"
                                           for t in n.targets)]
                if extension_lists and "sphinx_autodoc_typehints" not in extension_lists[0]:
                    vacuous.append("extension_disabled")
        results.append({"arm": rec["arm"], "compiler_accepted": rec["accepted"],
                        "patch_check": rec.get("patch_apply_check", {}).get("returncode"),
                        "valid_json": valid_json, "erased_declarations": erased,
                        "vacuous_workarounds": vacuous,
                        "functional_resolution": rec["functional_resolution"]})
    return {"issue": freeze["issue"], "verified_files": len(actual), "arms": results}


if __name__ == "__main__":
    print(json.dumps([audit(pathlib.Path(p)) for p in sys.argv[1:]],
                     indent=2, sort_keys=True))
