"""Run351 independently verifiable historical-source identity and default audit.
Read-only; no model code is executed. Invoke with path to pinned HTTPX checkout.
"""
from __future__ import annotations
import ast, hashlib, json, pathlib, sys

EXPECTED = {
    "_api.py": ("bd646bd7bfddd75eba6687bef45b52f5c9e1b7634d680fbcbfaf16304b618f5d",
                "a300f633e7ace1d0876a39735bf9af0c7ac64336"),
    "_client.py": ("6b223a7a32afcbaf4e1a9a83f6d34caf8f66a31d740a1ac511df678463ecd8a2",
                   "e3b2f5b31913f210491a6c5fc2bff1c454833440"),
}
CONTAMINATED_API_SHA256 = "81bf91fe16e23a93c5d128e243aca4ef66591e2d61bb3e2baaf4a1b8285dfabe"

def inspect_source(root):
    results = []
    for name, (expected_sha256, expected_blob) in EXPECTED.items():
        source = (pathlib.Path(root) / name).read_bytes()
        sha256 = hashlib.sha256(source).hexdigest()
        blob = hashlib.sha1(b"blob " + str(len(source)).encode() + b"\\0" + source).hexdigest()
        if sha256 != expected_sha256 or blob != expected_blob:
            raise ValueError(f"wrong historical baseline {name}: {sha256} {blob}")
        tree = ast.parse(source.decode())
        defaults = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            args = node.args
            slots = list(zip(args.kwonlyargs, args.kw_defaults))
            positional = args.posonlyargs + args.args
            if args.defaults:
                slots.extend(zip(positional[-len(args.defaults):], args.defaults))
            for arg, default in slots:
                if arg.arg == "allow_redirects" and isinstance(default, ast.Constant) and type(default.value) is bool:
                    defaults.append((node.name, node.lineno, default.value))
        results.append({"file": name, "sha256": sha256, "git_blob": blob, "defaults": defaults})
    all_defaults = [v for item in results for v in item["defaults"]]
    assert len(all_defaults) == 31, len(all_defaults)
    assert sum(not value for _, _, value in all_defaults) == 3
    return {"baseline_verified": True, "default_count": 31, "false_defaults": 3,
            "run348_contaminated_api_sha256": CONTAMINATED_API_SHA256, "files": results}

if __name__ == "__main__":
    print(json.dumps(inspect_source(sys.argv[1]), indent=2))
