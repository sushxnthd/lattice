"""Soundness-scoped exact semantic transfer for two literal slash regexes.

NOT a general Python dataflow analyzer. Open-world patterns, flags, callbacks,
bytes, replacement escapes, and non-string inputs are explicitly UNKNOWN.
"""
from __future__ import annotations
from dataclasses import dataclass
import ast

@dataclass(frozen=True)
class Result:
    kind: str
    value: str | None
    reason: str

LITERAL_PATTERNS = {'/{2,}?': 'lazy_pair', '/{2,}': 'greedy_run'}

def transfer(pattern: object, replacement: object, source: object, *, flags: int = 0) -> Result:
    if type(pattern) is not str or pattern not in LITERAL_PATTERNS:
        return Result('UNKNOWN', None, 'pattern not one of two certified slash literals')
    if type(replacement) is not str or replacement != '/':
        return Result('UNKNOWN', None, 'replacement not literal slash')
    if type(source) is not str:
        return Result('UNKNOWN', None, 'source not exact str')
    if flags != 0:
        return Result('UNKNOWN', None, 'nonzero regex flags outside certified scope')
    out = []
    i = 0
    while i < len(source):
        if source[i] != '/':
            out.append(source[i])
            i += 1
            continue
        j = i
        while j < len(source) and source[j] == '/':
            j += 1
        k = j - i
        if pattern == '/{2,}?':
            out.append('/' * ((k + 1) // 2))
        else:
            out.append('/')
        i = j
    return Result('EXACT', ''.join(out), 'literal slash-run transducer')

def classify_call(node: ast.AST) -> str:
    """Source-only syntactic scope; binding of name re is NOT certified."""
    if not isinstance(node, ast.Call) or len(node.args) != 3 or node.keywords:
        return 'UNKNOWN'
    fn = node.func
    if not (isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name)
            and fn.value.id == 're' and fn.attr == 'sub'):
        return 'UNKNOWN'
    p, r, s = node.args
    if not (isinstance(p, ast.Constant) and isinstance(p.value, str)
            and p.value in LITERAL_PATTERNS):
        return 'UNKNOWN'
    if not (isinstance(r, ast.Constant) and r.value == '/'):
        return 'UNKNOWN'
    if not isinstance(s, (ast.Constant, ast.Name, ast.Attribute)):
        return 'UNKNOWN'
    return 'MAY_LITERAL_RE_SUB_UNRESOLVED_BINDING'
