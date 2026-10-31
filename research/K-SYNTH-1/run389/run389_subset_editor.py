#!/usr/bin/env python3
"""K-SYNTH-1 Run389: source-pinned optional-subset AST transaction compiler.
Never executes model-generated Python on host.
"""
import ast
import hashlib
from dataclasses import dataclass

class Reject(Exception):
    pass

def sha(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def functions(source):
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise Reject("INVALID_BASE") from exc
    found = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found.setdefault(node.name, []).append(node)
    return found

@dataclass(frozen=True)
class Edit:
    path: str
    function: str
    replacement: str

def compile_transaction(sources, frozen_sha, edits, allowed, max_edits=2):
    """Return new source map or reject atomically; supports 0, 1 or 2 edits."""
    if set(sources) != set(allowed) or set(frozen_sha) != set(allowed):
        raise Reject("SOURCE_AUTHORITY_MISMATCH")
    if any(sha(sources[p]) != frozen_sha[p] for p in allowed):
        raise Reject("STALE_SOURCE")
    if not isinstance(edits, list) or len(edits) > max_edits:
        raise Reject("EDIT_COUNT")
    if len({e.path for e in edits}) != len(edits):
        raise Reject("DUPLICATE_PATH")
    if any(e.path not in allowed for e in edits):
        raise Reject("UNAUTHORIZED_PATH")
    proposed = dict(sources)
    for e in edits:
        if not isinstance(e.function, str) or not isinstance(e.replacement, str):
            raise Reject("EDIT_SCHEMA")
        if len(e.replacement.encode()) > 30000:
            raise Reject("OVERSIZE")
        source = sources[e.path]
        matches = functions(source).get(e.function, [])
        if len(matches) != 1:
            raise Reject("FUNCTION_NOT_UNIQUE")
        fn = matches[0]
        if fn.decorator_list:
            raise Reject("DECORATED_FUNCTION_UNKNOWN")
        try:
            replacement_tree = ast.parse(e.replacement)
        except (SyntaxError, ValueError) as exc:
            raise Reject("REPLACEMENT_SYNTAX") from exc
        if len(replacement_tree.body) != 1 or type(replacement_tree.body[0]) is not type(fn):
            raise Reject("REPLACEMENT_NOT_ONE_SAME_KIND_FUNCTION")
        new_fn = replacement_tree.body[0]
        if new_fn.name != e.function or new_fn.decorator_list or new_fn.col_offset != 0:
            raise Reject("FUNCTION_IDENTITY_CHANGED")
        lines = source.splitlines(keepends=True)
        if fn.col_offset != 0 or not (1 <= fn.lineno <= fn.end_lineno <= len(lines)):
            raise Reject("INVALID_SPAN")
        patch = "".join(lines[:fn.lineno-1]) + e.replacement.rstrip("\r\n") + "\n" + "".join(lines[fn.end_lineno:])
        try:
            ast.parse(patch)
            compile(patch, e.path, "exec")
        except (SyntaxError, ValueError) as exc:
            raise Reject("PATCH_SYNTAX") from exc
        if patch == source:
            raise Reject("NO_CHANGE")
        proposed[e.path] = patch
    return proposed

def compile_json(sources, frozen_sha, payload, allowed):
    if not isinstance(payload, dict) or set(payload) != {"edits"} or not isinstance(payload["edits"], list):
        raise Reject("TRANSACTION_SCHEMA")
    edits = []
    for item in payload["edits"]:
        if not isinstance(item, dict) or set(item) != {"path", "function", "replacement"}:
            raise Reject("EDIT_SCHEMA")
        edits.append(Edit(**item))
    return compile_transaction(sources, frozen_sha, edits, allowed)
