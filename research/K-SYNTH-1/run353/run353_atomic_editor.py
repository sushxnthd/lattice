"""K-SYNTH-1 Run353: bounded, fail-closed, two-file literal-default editor.

A patch transaction is *data*, never executed. It may change only declared
function-parameter default literals at independently pinned source identities.
The compiler makes a fresh stage only after validating every requested edit.
This is not a general-purpose Python patch language or runtime verifier.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


class EditError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def _literal(node: ast.AST) -> Any:
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        raise EditError('NON_LITERAL_OR_UNSUPPORTED') from None
    if type(value) not in (bool, type(None), int, float, str):
        raise EditError('UNSUPPORTED_LITERAL_TYPE')
    return value


def _node_span(data: bytes, node: ast.AST) -> tuple[int, int]:
    lines = data.splitlines(keepends=True)
    if not all(hasattr(node, k) for k in ('lineno', 'col_offset', 'end_lineno', 'end_col_offset')):
        raise EditError('MISSING_AST_LOCATION')
    if not (1 <= node.lineno <= node.end_lineno <= len(lines)):
        raise EditError('BAD_AST_LOCATION')
    begin = sum(map(len, lines[:node.lineno-1])) + node.col_offset
    end = sum(map(len, lines[:node.end_lineno-1])) + node.end_col_offset
    if not (0 <= begin < end <= len(data)):
        raise EditError('BAD_AST_LOCATION')
    return begin, end


def _functions(tree: ast.AST):
    def walk(nodes, parents):
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield '.'.join((*parents, node.name)), node
            elif isinstance(node, ast.ClassDef):
                yield from walk(node.body, (*parents, node.name))
    yield from walk(tree.body, ())


def _default_slot(tree: ast.AST, function: str, parameter: str) -> ast.AST:
    matches = [n for name, n in _functions(tree) if name == function]
    if len(matches) != 1:
        raise EditError('FUNCTION_NOT_UNIQUE_OR_MISSING')
    args = matches[0].args
    positional = [*args.posonlyargs, *args.args]
    defaults: list[tuple[str, ast.AST]] = []
    for param, default in zip(positional[len(positional)-len(args.defaults):], args.defaults):
        defaults.append((param.arg, default))
    for param, default in zip(args.kwonlyargs, args.kw_defaults):
        if default is not None:
            defaults.append((param.arg, default))
    matched = [n for p, n in defaults if p == parameter]
    if len(matched) != 1:
        raise EditError('DEFAULT_NOT_UNIQUE_OR_MISSING')
    return matched[0]


def inspect_slot(data: bytes, function: str, parameter: str) -> dict:
    try:
        tree = ast.parse(data, type_comments=True)
    except (SyntaxError, ValueError, UnicodeDecodeError):
        raise EditError('INVALID_SOURCE') from None
    node = _default_slot(tree, function, parameter)
    start, end = _node_span(data, node)
    return {'start': start, 'end': end, 'value': _literal(node),
            'anchor_sha256': sha(data[start:end]), 'text': data[start:end].decode('utf-8')}


def compile_transaction(sources: dict[str, bytes], authority: dict,
                        actions: list[dict]) -> tuple[dict[str, bytes], dict]:
    """No filesystem writes; validate every source and action before output."""
    if not isinstance(actions, list) or not actions:
        raise EditError('EMPTY_OR_INVALID_TRANSACTION')
    allowed = authority.get('files', {})
    if set(sources) != set(allowed):
        raise EditError('SOURCE_AUTHORITY_SET_MISMATCH')
    for path, data in sources.items():
        if (not isinstance(path, str) or path.startswith('/') or
            '..' in Path(path).parts or '\\' in path or path.startswith('.')):
            raise EditError('UNSAFE_SOURCE_PATH')
        if not isinstance(data, bytes) or sha(data) != allowed[path]['sha256']:
            raise EditError('SOURCE_SHA_MISMATCH')
    patches: dict[str, list[tuple[int, int, bytes, dict]]] = {p: [] for p in sources}
    targets = set()
    records = []
    for action in actions:
        if not isinstance(action, dict) or set(action) != {
            'path', 'function', 'parameter', 'expected', 'replacement', 'anchor_sha256'}:
            raise EditError('BAD_ACTION_SCHEMA')
        path = action['path']
        if path not in allowed:
            raise EditError('UNAUTHORIZED_PATH')
        f, p = action['function'], action['parameter']
        if not isinstance(f, str) or not isinstance(p, str):
            raise EditError('BAD_SELECTOR')
        target = (path, f, p)
        if target in targets:
            raise EditError('DUPLICATE_TARGET')
        targets.add(target)
        if [f, p] not in allowed[path]['slots']:
            raise EditError('UNAUTHORIZED_SLOT')
        slot = inspect_slot(sources[path], f, p)
        if type(action['expected']) is not type(slot['value']) or action['expected'] != slot['value']:
            raise EditError('STALE_EXPECTED_VALUE')
        if action['anchor_sha256'] != slot['anchor_sha256']:
            raise EditError('STALE_AST_ANCHOR')
        replacement = action['replacement']
        if type(replacement) not in (bool, type(None), int, float, str):
            raise EditError('UNSUPPORTED_REPLACEMENT')
        text = repr(replacement).encode('utf-8')
        try:
            parsed = ast.parse(text, mode='eval')
            if type(_literal(parsed.body)) is not type(replacement) or _literal(parsed.body) != replacement:
                raise EditError('REPLACEMENT_ROUNDTRIP')
        except (SyntaxError, ValueError, UnicodeDecodeError):
            raise EditError('REPLACEMENT_ROUNDTRIP') from None
        effective = sources[path][slot['start']:slot['end']] != text
        # Comments are not AST nodes. Flag potential stale documentation, do not
        # claim to decide its meaning or silently rewrite it.
        line_end = sources[path].find(b'\n', slot['end'])
        if line_end < 0:
            line_end = len(sources[path])
        tail = sources[path][slot['end']:line_end].decode('utf-8', errors='replace')
        review = ['ADJACENT_DEFAULT_COMMENT'] if effective and '#' in tail and 'default' in tail.lower() else []
        rec = {'path': path, 'function': f, 'parameter': p,
               'before_sha256': slot['anchor_sha256'], 'after_sha256': sha(text),
               'effective': effective, 'start': slot['start'], 'end': slot['end'], 'review_flags': review}
        patches[path].append((slot['start'], slot['end'], text, rec))
        records.append(rec)
    result = dict(sources)
    for path, entries in patches.items():
        sorted_entries = sorted(entries, key=lambda x: x[0])
        if any(a[1] > b[0] for a, b in zip(sorted_entries, sorted_entries[1:])):
            raise EditError('OVERLAPPING_SPANS')
        data = sources[path]
        for start, end, new, _ in reversed(sorted_entries):
            data = data[:start] + new + data[end:]
        try:
            ast.parse(data, type_comments=True)
        except (SyntaxError, ValueError, UnicodeDecodeError):
            raise EditError('PATCH_INVALID_SYNTAX') from None
        result[path] = data
    receipt = {'schema': 'ksynth1-run353-literal-default-transaction-v1',
               'source_sha256': {p: sha(sources[p]) for p in sorted(sources)},
               'stage_sha256': {p: sha(result[p]) for p in sorted(result)},
               'effective_edits': sum(r['effective'] for r in records),
               'no_op_edits': sum(not r['effective'] for r in records),
               'records': records, 'review_flags': sum((r['review_flags'] for r in records), []), 'authority_sha256': sha(canonical(authority)),
               'transaction_sha256': sha(canonical(actions))}
    return result, receipt


def stage_transaction(sources: dict[str, bytes], authority: dict,
                      actions: list[dict], destination: Path) -> dict:
    """All-or-nothing stage in a new directory; single-writer assumption."""
    output, receipt = compile_transaction(sources, authority, actions)
    destination = Path(destination)
    if destination.exists():
        raise EditError('DESTINATION_EXISTS')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.ksynth1-stage-', dir=destination.parent) as td:
        temp = Path(td) / 'tree'
        temp.mkdir()
        for path, data in output.items():
            file = temp / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(data)
        (temp / 'TRANSACTION_RECEIPT.json').write_bytes(canonical(receipt) + b'\n')
        if destination.exists():
            raise EditError('DESTINATION_EXISTS')
        os.rename(temp, destination)
    return receipt
