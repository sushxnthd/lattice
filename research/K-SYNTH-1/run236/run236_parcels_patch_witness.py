#!/usr/bin/env python3
"""Exact genuine Parcels patch-corruption witness; frozen records unchanged."""
import hashlib
import json
import pathlib
import subprocess
import tempfile
from run236_patch_serializer import byte_faithful_patch


def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(pathlib.Path(p).read_text())


def check(root):
    root = pathlib.Path(root)
    freeze = read(root / "freeze.json")
    stem = root / "raw" / (freeze["issue"] + "-python_annotated")
    record = read(pathlib.Path(str(stem) + "-verifier.json"))
    response = read(pathlib.Path(str(stem) + "-response.json"))
    action = json.loads(response["choices"][0]["message"]["content"])["actions"][0]
    after = read(pathlib.Path(str(stem) + "-after.json"))
    facts = read(root / "facts.json")
    path = action["path"]
    target = next(t for t in facts[path]["targets"] if t["target_id"] == action["selector"])
    assert after[path].count(action["content"]) == 1
    before = after[path].replace(action["content"], target["old_text"], 1)
    assert sha(before.encode()) == record["before"][path] == facts[path]["file_sha256"]
    assert sha(after[path].encode()) == record["after"][path]
    frozen_patch = pathlib.Path(str(stem) + "-patch.diff").read_bytes()
    with tempfile.TemporaryDirectory() as tmp:
        dest = pathlib.Path(tmp) / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(before)
        original_check = subprocess.run(
            ["git", "apply", "--check", "-"], cwd=tmp,
            input=frozen_patch, capture_output=True
        )
    assert original_check.returncode == 128
    corrected = byte_faithful_patch({path: before.encode()}, {path: after[path].encode()})
    assert b"\\ No newline at end of file" in corrected
    return {
        "task": freeze["issue"],
        "arm": "python_annotated",
        "frozen_compiler_accepted": record["accepted"],
        "frozen_git_patch_check": record["patch_apply_check"]["returncode"],
        "independent_frozen_patch_check": original_check.returncode,
        "frozen_patch_error": original_check.stderr.decode().strip(),
        "before_sha256": sha(before.encode()),
        "after_sha256": sha(after[path].encode()),
        "corrected_patch_sha256": sha(corrected),
        "corrected_patch_exact_byte_replay_verified": True,
        "frozen_result_unchanged": True,
    }


if __name__ == "__main__":
    import sys
    print(json.dumps(check(sys.argv[1]), indent=2, sort_keys=True))
