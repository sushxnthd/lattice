#!/usr/bin/env python3
"""Reconstruct eight SHA-pinned historical Flask source combinations."""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

BASE = "7b0088693ece1bd3a9238a6fdf56ed8df7a4d43b"
MERGE = "c34d6e81fd8e405e6d4178bf24b364918811ef17"
FILES = {
    "src/flask/app.py": ("9a6fdd40d2edb1b7575bed5c68655706e18c4d35", "652b9bbf719b626c6b66cb545b27264a46453fc9"),
    "src/flask/ctx.py": ("8876efd04f0552fb5db315701abfcbcedcfeb447", "dbd62e7505382954cd61a59bff317ca3d27d6f1a"),
    "src/flask/helpers.py": ("3b65664afe9510c40b63f8f05e0adb9c6a3addd8", "8befe719695e12bd6374605c9a90e88f36e5c494"),
}

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def git_file(repo: Path, ref: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{ref}:{path}"], timeout=40)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--oracle", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    repo, oracle, out = args.repo.resolve(), args.oracle.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    assert sys.version_info[:2] == (3, 11), sys.version
    subprocess.run(["git", "-C", str(repo), "checkout", "--detach", BASE], check=True, timeout=60)
    pinned = {}
    for path, pair in FILES.items():
        old, new = git_file(repo, BASE, path), git_file(repo, MERGE, path)
        if (blob_sha(old), blob_sha(new)) != pair:
            raise RuntimeError(f"PINNED_SOURCE_MISMATCH {path} {(blob_sha(old), blob_sha(new))}")
        pinned[path] = (old, new)
    (out / "source_provenance.json").write_text(json.dumps({
        "baseline_commit": BASE, "transport_commit": MERGE,
        "blobs": {p: list(v) for p, v in FILES.items()}, "python": sys.version
    }, indent=2, sort_keys=True))
    matrix = {"schema": "run363.flask.matrix.v1", "variants": {}}
    failures = []
    try:
        for mask in range(8):
            selected = {}
            for bit, (path, pair) in enumerate(FILES.items()):
                index = (mask >> bit) & 1
                (repo / path).write_bytes(pinned[path][index])
                selected[path] = blob_sha((repo / path).read_bytes())
                if selected[path] != pair[index]:
                    raise RuntimeError(f"RECONSTRUCTION_MISMATCH mask={mask} {path}")
            env = os.environ.copy()
            env["PYTHONPATH"] = str(repo / "src")
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            p = subprocess.run([sys.executable, str(oracle)], cwd=repo, env=env,
                               capture_output=True, text=True, timeout=360)
            (out / f"variant_{mask}_stdout.txt").write_text(p.stdout)
            (out / f"variant_{mask}_stderr.txt").write_text(p.stderr)
            if p.returncode:
                failures.append({"mask": mask, "type": "ORACLE_EXIT", "returncode": p.returncode})
                continue
            try:
                row = json.loads(p.stdout)
                if row.get("schema") != "run363.flask.oracle.v1":
                    raise ValueError("oracle schema")
                row.update({"mask": mask, "blobs": selected})
                matrix["variants"][str(mask)] = row
            except (ValueError, TypeError) as exc:
                failures.append({"mask": mask, "type": "ORACLE_PARSE", "detail": str(exc)})
    finally:
        (out / "run363_matrix.json").write_text(json.dumps(matrix, indent=2, sort_keys=True))
        (out / "run363_failures.json").write_text(json.dumps(failures, indent=2, sort_keys=True))
        sha = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.iterdir())
               if f.is_file() and f.name != "sha256_manifest.json"}
        (out / "sha256_manifest.json").write_text(json.dumps(sha, indent=2, sort_keys=True))
    if failures or len(matrix["variants"]) != 8:
        raise RuntimeError(f"INCOMPLETE_ORACLE: {failures}")
    print(json.dumps({"variants": len(matrix["variants"]),
                      "cases": sum(len(x["results"]) for x in matrix["variants"].values()),
                      "artifact": str(out)}, sort_keys=True))

if __name__ == "__main__":
    main()
