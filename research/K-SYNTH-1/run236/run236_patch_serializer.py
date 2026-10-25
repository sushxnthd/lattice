#!/usr/bin/env python3
"""Byte-faithful Git patch serializer for a trusted, already-authorized transaction.

Git records missing terminal newlines with a valid `\\ No newline at end of file`
marker. Verify that each patch applies and reproduces EXACT output bytes.
Prospective fix only; frozen Run234 records remain unchanged.
"""
from __future__ import annotations
import pathlib
import subprocess
import tempfile


def run(root, *args, input=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        input=input, capture_output=True, check=False
    )
    if proc.returncode:
        raise RuntimeError(
            f"git {args} failed ({proc.returncode}): "
            + proc.stderr.decode(errors="replace")
        )
    return proc.stdout


def safe_path(path):
    p = pathlib.PurePosixPath(path)
    if not path or p.is_absolute() or ".." in p.parts or "\\" in path or str(p) != path:
        raise ValueError(f"unsafe path {path!r}")


def put(root, path, data):
    dest = root / path
    if data is None:
        if dest.exists():
            dest.unlink()
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)


def byte_faithful_patch(before: dict[str, bytes | None], after: dict[str, bytes | None]):
    if set(before) != set(after):
        raise ValueError("before and after must cover identical path sets")
    for path in before:
        safe_path(path)
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp) / "work"
        root.mkdir()
        run(root, "init", "-q")
        for path, data in before.items():
            put(root, path, data)
        run(root, "add", "-A")
        for path, data in after.items():
            put(root, path, data)
        for path in after:
            if before[path] is None and after[path] is not None:
                run(root, "add", "-N", "--", path)
        patch = run(root, "diff", "--binary", "--no-ext-diff", "--no-color", "--full-index")
        check = pathlib.Path(tmp) / "check"
        check.mkdir()
        for path, data in before.items():
            put(check, path, data)
        run(check, "apply", "--check", "-", input=patch)
        run(check, "apply", "-", input=patch)
        for path, expected in after.items():
            dest = check / path
            observed = dest.read_bytes() if dest.exists() else None
            if observed != expected:
                raise AssertionError(f"patch replay differs for {path}")
        return patch
