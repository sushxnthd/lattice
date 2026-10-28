"""Run321 fail-closed whole-module AST congruence guard for expression edits.

Engineering guarantee: accepted patches have AST identical to substitution of the
specified node. Not a semantic-equivalence proof or a security boundary.
"""
from __future__ import annotations
import ast, copy
from hashlib import sha256
from typing import Mapping, Sequence
from run315_multifile_compiler import PatchRejected, node_digest
from run320_hardened_compiler import Action, compile_structural


def expected_tree(source: bytes, action: Action) -> ast.AST:
    if action.operation != 'replace_expr':
        raise PatchRejected('AST congruence guard currently supports only expression replacement')
    try:
        tree = ast.parse(source.decode('utf-8'))
        new_expr = ast.parse(action.replacement, mode='eval').body
    except (UnicodeError, SyntaxError, ValueError, TypeError) as exc:
        raise PatchRejected('unparseable expected AST') from exc
    hits = [n for n in ast.walk(tree) if isinstance(n, ast.expr)
            and type(n).__name__ == action.node_type
            and getattr(n, 'lineno', None) == action.lineno
            and getattr(n, 'col_offset', None) == action.col_offset
            and getattr(n, 'end_lineno', None) == action.end_lineno
            and getattr(n, 'end_col_offset', None) == action.end_col_offset
            and node_digest(n) == action.node_sha256]
    if len(hits) != 1:
        raise PatchRejected('nonunique target AST node')
    target = hits[0]
    class Replace(ast.NodeTransformer):
        def visit(self, node):
            if node is target:
                return ast.copy_location(copy.deepcopy(new_expr), node)
            return super().visit(node)
    return ast.fix_missing_locations(Replace().visit(tree))


def compile_ast_congruent(sources: Mapping[str, bytes], actions: Sequence[Action], *,
                          allowed_paths: frozenset[str]) -> dict[str, bytes]:
    if not actions or any(not isinstance(a, Action) or a.operation != 'replace_expr' for a in actions):
        raise PatchRejected('unsupported action for AST congruence')
    expected = {p: ast.parse(v.decode('utf-8')) for p, v in sources.items()}
    for a in actions:
        if a.path not in sources or a.path not in allowed_paths:
            raise PatchRejected('unauthorized source')
        if sha256(sources[a.path]).hexdigest() != a.source_sha256:
            raise PatchRejected('stale source')
        if sum(x.path == a.path for x in actions) != 1:
            raise PatchRejected('multiple actions per file unsupported by congruence guard')
        expected[a.path] = expected_tree(sources[a.path], a)
    result = compile_structural(sources, actions, allowed_paths=allowed_paths)
    for path, expected_ast in expected.items():
        try:
            actual_ast = ast.parse(result[path].decode('utf-8'))
        except (UnicodeError, SyntaxError, ValueError, TypeError) as exc:
            raise PatchRejected('invalid patched AST') from exc
        if ast.dump(actual_ast, include_attributes=False) != ast.dump(expected_ast, include_attributes=False):
            raise PatchRejected('AST congruence mismatch')
    return result
