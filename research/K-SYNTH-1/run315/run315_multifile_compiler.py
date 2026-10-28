"""K-SYNTH-1 Run315: bounded multi-file, all-or-nothing Python constant editor.

This compiler returns a complete immutable snapshot. It never runs generated code
and does not claim that overwriting multiple filesystem paths is atomic.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass
from hashlib import sha256
from pathlib import PurePosixPath
from typing import Mapping, Sequence

class PatchRejected(ValueError):
    pass

def digest(data: bytes) -> str:
    return sha256(data).hexdigest()

@dataclass(frozen=True)
class Edit:
    path: str
    source_sha256: str
    node_sha256: str
    line: int
    col: int
    end_line: int
    end_col: int
    old: int
    new: int

def node_digest(node: ast.AST) -> str:
    return digest(ast.dump(node, include_attributes=False).encode('utf-8'))

def checked_path(path: str) -> str:
    if not isinstance(path, str) or not path or '\\' in path or '\x00' in path:
        raise PatchRejected('invalid path')
    p = PurePosixPath(path)
    if p.is_absolute() or any(x in ('.', '..') for x in path.split('/')) or p.suffix != '.py':
        raise PatchRejected('path outside edit authority')
    return str(p)

def python_ast_constructor(value: str) -> int:
    """Parse a literal AST constructor, not Python eval/exec."""
    try:
        n = ast.parse(value, mode='eval').body
    except (SyntaxError, ValueError, TypeError) as exc:
        raise PatchRejected('invalid AST action') from exc
    if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and isinstance(n.func.value, ast.Name) and n.func.value.id == 'ast'
            and n.func.attr == 'Constant' and not n.args and len(n.keywords) == 1
            and n.keywords[0].arg == 'value' and isinstance(n.keywords[0].value, ast.Constant)
            and type(n.keywords[0].value.value) is int):
        raise PatchRejected('unsupported AST constructor')
    return n.keywords[0].value.value

def normalize_ir(base: Edit, new: int) -> Edit:
    if type(new) is not int:
        raise PatchRejected('invalid IR value')
    return Edit(**{**vars(base), 'new': new})

def normalize_python_ast(base: Edit, expression: str) -> Edit:
    return normalize_ir(base, python_ast_constructor(expression))

def compile_transaction(sources: Mapping[str, bytes], edits: Sequence[Edit], *,
                        allowed_paths: frozenset[str]) -> dict[str, bytes]:
    """Pure all-or-nothing edit: no source mutated; reject entire transaction on any failure.

    Input facts and edit authority are identical for IR and AST-action frontends.
    Spans are UTF-8 byte offsets per CPython's AST contract. A multi-file
    filesystem overwrite is NOT atomic; callers must publish one snapshot pointer.
    """
    if not edits:
        raise PatchRejected('empty transaction')
    if len(edits) > 64 or len(sources) > 64:
        raise PatchRejected('bounded transaction exceeded')
    normalized_sources: dict[str, bytes] = {}
    for path, source in sources.items():
        cp = checked_path(path)
        if cp != path or cp in normalized_sources or type(source) is not bytes:
            raise PatchRejected('invalid source mapping')
        normalized_sources[cp] = source
    if any(checked_path(path) != path for path in allowed_paths):
        raise PatchRejected('invalid authority path')
    per_path: dict[str, list[tuple[int,int,bytes]]] = {}
    for edit in edits:
        if not isinstance(edit, Edit):
            raise PatchRejected('invalid edit')
        path = checked_path(edit.path)
        if path not in allowed_paths or path not in normalized_sources:
            raise PatchRejected('unauthorized path')
        source = normalized_sources[path]
        if digest(source) != edit.source_sha256:
            raise PatchRejected('stale source precondition')
        if type(edit.old) is not int or type(edit.new) is not int or not (0 <= edit.new < 1000000):
            raise PatchRejected('unsupported value')
        try:
            tree = ast.parse(source.decode('utf-8'))
        except (UnicodeError, SyntaxError) as exc:
            raise PatchRejected('invalid source') from exc
        hits = [n for n in ast.walk(tree) if isinstance(n, ast.Constant)
                and type(n.value) is int and n.value == edit.old
                and (n.lineno,n.col_offset,n.end_lineno,n.end_col_offset) ==
                (edit.line,edit.col,edit.end_line,edit.end_col)
                and node_digest(n) == edit.node_sha256]
        if len(hits) != 1 or edit.line != edit.end_line:
            raise PatchRejected('ambiguous, stale or multiline node')
        lines = source.splitlines(keepends=True)
        start = sum(len(x) for x in lines[:edit.line-1]) + edit.col
        stop = sum(len(x) for x in lines[:edit.end_line-1]) + edit.end_col
        if source[start:stop] != str(edit.old).encode('ascii'):
            raise PatchRejected('noncanonical integer literal')
        per_path.setdefault(path, []).append((start,stop,str(edit.new).encode('ascii')))
    out = dict(normalized_sources)
    for path, spans in per_path.items():
        spans.sort(key=lambda x: x[0])
        if any(b[0] < a[1] for a,b in zip(spans, spans[1:])):
            raise PatchRejected('overlapping edits')
        buf = out[path]
        for start, stop, replacement in reversed(spans):
            buf = buf[:start] + replacement + buf[stop:]
        try:
            ast.parse(buf.decode('utf-8'))
        except (UnicodeError, SyntaxError) as exc:
            raise PatchRejected('invalid compiled patch') from exc
        out[path] = buf
    return out
