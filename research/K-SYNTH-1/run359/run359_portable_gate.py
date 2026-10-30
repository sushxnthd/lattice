#!/usr/bin/env python3
"""Run359 portable read-only audit. Never execute model-generated source.

Usage: python run359_portable_gate.py original_run358_cloud.zip baseline_dir
baseline_dir contains httpcore/_sync/http11.py and httpcore/_async/http11.py
"""
import ast
import hashlib
import json
import pathlib
import re
import sys
import zipfile

PINS = {
    "httpcore/_sync/http11.py": "e108f88b124043b05258f6d98363119b79f92d88",
    "httpcore/_async/http11.py": "a5eb480840dd4eae73bc8285c9d374a09a0bd44c",
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def gitblob(source):
    b = source.encode()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def stage(source, actions):
    lines = source.splitlines(keepends=True)
    intervals = []
    for a in actions:
        assert set(a) == {"path", "start_line", "end_line", "new"}
        left, right = a["start_line"] - 1, a["end_line"]
        assert 0 <= left <= right <= len(lines)
        assert a["new"] == "" or a["new"].endswith("\n")
        for lo, hi in intervals:
            assert not (left < hi and lo < right or
                        lo == hi and left <= lo < right or
                        left == right and lo <= left < hi or
                        left == right == lo == hi)
        intervals.append((left, right))
    for a in sorted(actions, key=lambda a: (a["start_line"], a["end_line"]), reverse=True):
        lines[a["start_line"] - 1:a["end_line"]] = [a["new"]]
    return "".join(lines)

def main(zip_path, base_dir):
    with zipfile.ZipFile(zip_path) as z:
        assert len(z.namelist()) == len(set(z.namelist()))
        manifest = json.loads(z.read("SHA256_MANIFEST.json"))
        assert set(z.namelist()) == set(manifest) | {"SHA256_MANIFEST.json"}
        for name, expected in manifest.items():
            assert sha(z.read(name)) == expected, name
        get = lambda name: json.loads(z.read(name))
        freeze = get("RUN357_FREEZE.json")
        assert sha(canon(get("RUN357_FACTS.json")).encode()) == freeze["fact_sha256"]
        sources = {p: (pathlib.Path(base_dir) / p).read_text() for p in PINS}
        for p, source in sources.items():
            assert gitblob(source) == PINS[p] == freeze["blobs"][p]
        result = {"original_zip_sha256": sha(pathlib.Path(zip_path).read_bytes()),
                  "original_manifest_entries": len(manifest), "arms": {}}
        for arm in ("IR", "PYTHON_AST"):
            request = get("request_" + arm + ".json")
            assert sha(canon(request).encode()) == freeze["requests"][arm]["request_sha256"]
            assert sha(request["messages"][0]["content"].encode()) == freeze["requests"][arm]["prompt_sha256"]
            raw = get("raw_" + arm + ".json")
            assert raw["choices"][0]["finish_reason"] == "stop"
            content = raw["choices"][0]["message"]["content"].strip()
            fence = chr(96) * 3
            content = re.sub(r"^" + fence + r"(?:json)?\s*", "", content)
            content = re.sub(r"\s*" + fence + r"$", "", content)
            edits = json.loads(content)["edits"]
            assert get("compile_" + arm + ".json")["error"] == "Reject:PYTHON_SYNTAX"
            by_file = {}
            for p, source in sources.items():
                chosen = [e for e in edits if e["path"] == p]
                valid = 0
                for mask in range(1 << len(chosen)):
                    candidate = stage(source, [e for i, e in enumerate(chosen) if mask & (1 << i)])
                    try:
                        ast.parse(candidate)
                        valid += 1
                    except SyntaxError:
                        pass
                try:
                    ast.parse(stage(source, chosen))
                    raise AssertionError("ORIGINAL_COMPILER_DISAGREEMENT")
                except SyntaxError:
                    pass
                by_file[p] = {"edits": len(chosen), "valid_subsets": valid,
                              "total_subsets": 1 << len(chosen)}
            result["arms"][arm] = {"edits": len(edits), "by_file": by_file,
                                   "completion_tokens": raw["usage"]["completion_tokens"]}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    assert len(sys.argv) == 3
    main(*sys.argv[1:])
