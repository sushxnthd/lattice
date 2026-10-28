"""Run319: explicit, bounded decorator-aware structural edit adapter.

Pure in-memory atomic snapshot; never executes model-generated code.
Preserves Run317's fail-closed behavior for ordinary decorated-node edits.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass
from hashlib import sha256
from typing import Mapping, Sequence
from run315_multifile_compiler import PatchRejected, checked_path, node_digest
from run317_structural_compiler import Action, compile_structural

DECORATED_OPS = frozenset({'delete_decorated_stmt','replace_decorated_stmt'})

def _offset(lines: list[bytes], lineno: int, col: int) -> int:
    if not (1 <= lineno <= len(lines) and 0 <= col <= len(lines[lineno - 1])):
        raise PatchRejected('invalid byte span')
    return sum(map(len, lines[:lineno - 1])) + col

def _decorator_start(lines: list[bytes], node: ast.AST) -> int:
    decorators = getattr(node, 'decorator_list', None)
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) or not decorators:
        raise PatchRejected('explicit decorated action requires decorated declaration')
    indent = lines[node.lineno - 1][:node.col_offset]
    if indent.strip() or any(c not in (32, 9) for c in indent):
        raise PatchRejected('nonstandalone declaration')
    last_end = None
    for dec in decorators:
        if dec.col_offset != node.col_offset + 1 or dec.lineno >= node.lineno:
            raise PatchRejected('unsupported decorator location')
        line = lines[dec.lineno - 1]
        if line[:node.col_offset] != indent or line[node.col_offset:node.col_offset + 1] != b'@':
            raise PatchRejected('decorator is not line anchored')
        if last_end is not None and dec.lineno != last_end + 1:
            raise PatchRejected('gap between decorators')
        last_end = dec.end_lineno
    if node.lineno != last_end + 1:
        raise PatchRejected('gap between decorator and declaration')
    return _offset(lines, decorators[0].lineno, 0)

def _replacement(text: str, node: ast.AST, indent: bytes, newline: bytes) -> bytes:
    if not text or '\x00' in text or len(text.encode('utf-8')) > 32768 or text.endswith(('\n','\r')):
        raise PatchRejected('invalid replacement')
    if text[:1] in (' ', '\t'):
        raise PatchRejected('replacement must start dedented')
    try:
        parsed = ast.parse(text)
    except (SyntaxError, ValueError, UnicodeError) as exc:
        raise PatchRejected('invalid replacement syntax') from exc
    if len(parsed.body) != 1 or type(parsed.body[0]) is not type(node):
        raise PatchRejected('replacement must be one same-kind declaration')
    if parsed.body[0].name != node.name:
        raise PatchRejected('replacement declaration name differs')
    return indent + text.encode('utf-8').replace(b'\n', newline + indent)

def compile_decorator_transaction(sources: Mapping[str, bytes], actions: Sequence[Action], *,
                                  allowed_paths: frozenset[str]) -> dict[str, bytes]:
    """Explicit decorated-node edits plus unchanged Run317 operations, one atomic snapshot.

    For mixed actions we independently reproduce Run317 span selection for ordinary
    actions by compiling them alone and deriving diffs only when exactly one contiguous
    edit is observed; reject ambiguous diffs. This deliberately conservative adapter
    does not claim a general mixed-edit compiler.
    """
    if not actions or len(actions) > 64 or len(sources) > 64:
        raise PatchRejected('invalid transaction size')
    if any(checked_path(p) != p for p in allowed_paths):
        raise PatchRejected('invalid authority')
    trees = {}
    for path, data in sources.items():
        if checked_path(path) != path or type(data) is not bytes or len(data) > 1000000:
            raise PatchRejected('invalid source')
        try:
            trees[path] = ast.parse(data.decode('utf-8'))
        except (UnicodeError, SyntaxError, ValueError) as exc:
            raise PatchRejected('invalid source') from exc
    edits = {}
    for a in actions:
        if not isinstance(a, Action) or a.path not in allowed_paths or a.path not in sources:
            raise PatchRejected('unauthorized action')
        data = sources[a.path]
        if sha256(data).hexdigest() != a.source_sha256:
            raise PatchRejected('stale source SHA')
        if a.operation not in DECORATED_OPS:
            # Deliberately only allow standalone Run317 transactions; no guessing
            # byte spans for arbitrary mixed operations.
            if len(actions) != 1:
                raise PatchRejected('mixed ordinary/decorated actions unsupported')
            return compile_structural(sources, actions, allowed_paths=allowed_paths)
        hits = [n for n in ast.walk(trees[a.path]) if type(n).__name__ == a.node_type
                and hasattr(n,'lineno')
                and (n.lineno,n.col_offset,n.end_lineno,n.end_col_offset) ==
                (a.lineno,a.col_offset,a.end_lineno,a.end_col_offset)
                and node_digest(n) == a.node_sha256]
        if len(hits) != 1:
            raise PatchRejected('missing or ambiguous node')
        node = hits[0]
        lines = data.splitlines(keepends=True)
        start = _decorator_start(lines, node)
        end = _offset(lines, node.end_lineno, node.end_col_offset)
        if not 0 <= start < end <= len(data):
            raise PatchRejected('invalid declaration span')
        if lines[node.end_lineno-1][node.end_col_offset:].strip():
            raise PatchRejected('trailing content')
        if a.operation == 'delete_decorated_stmt':
            if a.replacement:
                raise PatchRejected('delete with replacement')
            end = _offset(lines, node.end_lineno, len(lines[node.end_lineno - 1]))
            repl = b''
        else:
            newline = b'\r\n' if b'\r\n' in data and b'\n' not in data.replace(b'\r\n',b'') else b'\n'
            indent = lines[node.lineno-1][:node.col_offset]
            repl = _replacement(a.replacement, node, indent, newline)
        edits.setdefault(a.path,[]).append((start,end,repl))
    out = dict(sources)
    for path, chunks in edits.items():
        chunks.sort(key=lambda t:(t[0],t[1]))
        if any(b[0] < a[1] or b[0] == a[0] for a,b in zip(chunks,chunks[1:])):
            raise PatchRejected('colliding edits')
        buf = out[path]
        for start,end,repl in reversed(chunks):
            buf = buf[:start] + repl + buf[end:]
        try:
            tree = ast.parse(buf.decode('utf-8'))
            compile(tree,path,'exec',dont_inherit=True)
        except (SyntaxError,UnicodeError,ValueError,TypeError) as exc:
            raise PatchRejected('invalid compiled Python') from exc
        out[path] = buf
    return out
