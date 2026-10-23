"""Representation-agnostic post-compile safety diagnostics for code-repair studies.

These are optional research guards, not proofs of functional correctness.
For comment-only tasks, disable the AST-delta requirement. Existing legal
notices must be preserved unless explicitly reviewed and authorized.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Mapping

LEGAL_MARKERS = (
    "copyright", "spdx-license-identifier", "licensed under",
    "all rights reserved", "permission is hereby granted",
    "apache license", "mit license", "gnu general public license",
)

@dataclass(frozen=True)
class FileEvidence:
    path: str
    before_sha256: str
    after_sha256: str
    text_changed: bool
    ast_changed: bool | None
    legal_header_present: bool
    legal_header_preserved: bool
    syntax_valid: bool | None

def legal_header(source: str) -> str:
    """Find the leading comment block when it contains a legal notice."""
    prefix = []
    for line in source.splitlines(keepends=True):
        stripped = line.lstrip("\ufeff \t")
        if stripped.startswith("#") or not stripped.strip():
            prefix.append(line)
        else:
            break
    header = "".join(prefix)
    return header if any(marker in header.lower() for marker in LEGAL_MARKERS) else ""

def evidence(before: Mapping[str, bytes], after: Mapping[str, bytes]) -> list[FileEvidence]:
    if not set(after).issubset(before):
        raise ValueError("new files require separate edit authority")
    results = []
    for path, data in sorted(after.items()):
        old = before[path]
        is_python = Path(path).suffix == ".py"
        old_source = old.decode("utf-8") if is_python else None
        new_source = data.decode("utf-8") if is_python else None
        header = legal_header(old_source) if old_source is not None else ""
        preserved = not header or new_source.startswith(header)
        ast_changed = syntax_valid = None
        if is_python:
            try:
                a = ast.dump(ast.parse(old_source, type_comments=True), include_attributes=False)
                b = ast.dump(ast.parse(new_source, type_comments=True), include_attributes=False)
                ast_changed, syntax_valid = a != b, True
            except SyntaxError:
                syntax_valid = False
        results.append(FileEvidence(
            path, sha256(old).hexdigest(), sha256(data).hexdigest(),
            old != data, ast_changed, bool(header), preserved, syntax_valid
        ))
    return results

def enforce(
    before: Mapping[str, bytes],
    after: Mapping[str, bytes],
    *,
    require_python_ast_delta: bool = False,
    preserve_legal_headers: bool = True,
) -> list[FileEvidence]:
    """Apply the same optional diagnostics to all representation conditions."""
    rows = evidence(before, after)
    if preserve_legal_headers:
        removed = [r.path for r in rows if not r.legal_header_preserved]
        if removed:
            raise ValueError("legal-header removal: " + ", ".join(removed))
    if any(r.syntax_valid is False for r in rows):
        raise ValueError("invalid Python syntax")
    if require_python_ast_delta:
        py = [r for r in rows if r.ast_changed is not None]
        if py and not any(r.ast_changed for r in py):
            raise ValueError("no Python AST delta (functional outcome untested)")
    return rows
