#!/usr/bin/env python3
"""Genuine Parcels IR edit erases @property; independent behavior witness."""
import ast
import hashlib
import json
import pathlib
import subprocess
import tempfile
import textwrap
import functools


def read(p): return json.loads(pathlib.Path(p).read_text())
def sha(b): return hashlib.sha256(b).hexdigest()


def check(root):
    root = pathlib.Path(root)
    freeze = read(root / "freeze.json")
    stem = root / "raw" / (freeze["issue"] + "-semantic_ir_json")
    record = read(pathlib.Path(str(stem) + "-verifier.json"))
    response = read(pathlib.Path(str(stem) + "-response.json"))
    action = json.loads(response["choices"][0]["message"]["content"])["actions"][0]
    facts = read(root / "facts.json")
    target = next(t for t in facts[action["path"]]["targets"]
                  if t["target_id"] == action["selector"])
    after = read(pathlib.Path(str(stem) + "-after.json"))
    patch = pathlib.Path(str(stem) + "-patch.diff").read_text()
    with tempfile.TemporaryDirectory() as tmp:
        dest = pathlib.Path(tmp) / action["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(after[action["path"]])
        subprocess.run(["git", "apply", "--reverse", "-"], cwd=tmp,
                       input=patch, text=True, capture_output=True, check=True)
        before = dest.read_text()
    assert sha(before.encode()) == record["before"][action["path"]]
    assert sha(after[action["path"]].encode()) == record["after"][action["path"]]
    old = ast.parse(textwrap.dedent(target["old_text"])).body[0]
    new = ast.parse(textwrap.dedent(action["content"])).body[0]
    assert isinstance(old, ast.FunctionDef) and isinstance(new, ast.FunctionDef)
    assert any(isinstance(d, ast.Name) and d.id == "property" for d in old.decorator_list)
    assert not any(isinstance(d, ast.Name) and d.id == "property" for d in new.decorator_list)

    def exercise(method):
        stub = ast.ClassDef(name="Stub", bases=[], keywords=[],
                            body=[method], decorator_list=[])
        module = ast.fix_missing_locations(ast.Module(body=[stub], type_ignores=[]))
        ns = {"functools": functools}
        exec(compile(module, "<isolated-parcels>", "exec"), ns)
        obj = ns["Stub"]()
        obj.fields = {}
        value = obj.time_interval
        return {"is_none": value is None, "callable": callable(value),
                "descriptor_type": type(ns["Stub"].__dict__["time_interval"]).__name__}

    before_result = exercise(old)
    edited_result = exercise(new)
    assert before_result["is_none"] and edited_result["callable"]
    return {
        "task": freeze["issue"], "arm": "semantic_ir_json",
        "frozen_compiler_accepted": record["accepted"],
        "before_sha256": sha(before.encode()),
        "after_sha256": sha(after[action["path"]].encode()),
        "before": before_result, "model_edit": edited_result,
        "property_contract_broken": True,
        "frozen_result_unchanged": True,
    }


if __name__ == "__main__":
    import sys
    print(json.dumps(check(sys.argv[1]), indent=2, sort_keys=True))
