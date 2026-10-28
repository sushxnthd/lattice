"""K-SYNTH-1 Run322 bounded multi-action AST-congruence validator.

Checks exact intended AST transformation, not semantic equivalence, comments,
filesystem isolation, or correctness of model-authored edits.
"""
from __future__ import annotations
import ast
from hashlib import sha256
from typing import Mapping, Sequence
from run315_multifile_compiler import PatchRejected, checked_path, node_digest
from run320_hardened_compiler import Action, compile_structural

SUPPORTED = frozenset({'replace_expr', 'replace_stmt', 'delete_stmt', 'insert_before'})

def _key(node: ast.AST):
    return (type(node).__name__, getattr(node, 'lineno', None),
            getattr(node, 'col_offset', None), getattr(node, 'end_lineno', None),
            getattr(node, 'end_col_offset', None), node_digest(node))

def _action_key(a: Action):
    return (a.node_type, a.lineno, a.col_offset, a.end_lineno,
            a.end_col_offset, a.node_sha256)

def _parse_replacement(a: Action):
    try:
        if a.operation == 'replace_expr':
            return ast.parse(a.replacement, mode='eval').body
        if a.operation == 'delete_stmt':
            if a.replacement: raise PatchRejected('nonempty deletion')
            return None
        parsed = ast.parse(a.replacement, mode='exec')
        if len(parsed.body) != 1:
            raise PatchRejected('statement replacement must contain exactly one statement')
        return parsed.body[0]
    except (SyntaxError, UnicodeError, ValueError, TypeError) as exc:
        raise PatchRejected('invalid intended AST replacement') from exc

def _expected_ast(data: bytes, actions: Sequence[Action]) -> ast.Module:
    """Simultaneous AST edits against ORIGINAL tree; no reference patch read."""
    try: tree = ast.parse(data.decode('utf-8'))
    except (UnicodeError, SyntaxError, ValueError, TypeError) as exc:
        raise PatchRejected('invalid source AST') from exc
    by_id: dict[int, tuple[Action, ast.AST | None]] = {}
    spans: list[tuple[int,int,int,int,str]] = []
    for a in actions:
        hits = [n for n in ast.walk(tree) if _key(n) == _action_key(a)]
        if len(hits) != 1: raise PatchRejected('missing or ambiguous target')
        target = hits[0]
        if a.operation == 'replace_expr' and not isinstance(target, ast.expr):
            raise PatchRejected('expression operation on nonexpression')
        if a.operation != 'replace_expr' and not isinstance(target, ast.stmt):
            raise PatchRejected('statement operation on nonstatement')
        if id(target) in by_id: raise PatchRejected('duplicate target')
        by_id[id(target)] = (a, _parse_replacement(a))
        spans.append((a.lineno, a.col_offset, a.end_lineno, a.end_col_offset, a.operation))
    # Overlap by original AST span, including nested AST nodes. Insertions at
    # identical offsets also conflict; no order-dependent action composition.
    def overlap(x,y):
        x0=(x[0],x[1]); x1=(x[2],x[3]); y0=(y[0],y[1]); y1=(y[2],y[3])
        return x0 < y1 and y0 < x1 or x0 == y0
    if any(overlap(x,y) for i,x in enumerate(spans) for y in spans[i+1:]):
        raise PatchRejected('overlapping AST targets')

    def visit(node: ast.AST):
        hit = by_id.get(id(node))
        if hit is not None:
            a, repl = hit
            if a.operation == 'replace_expr' or a.operation == 'replace_stmt':
                assert repl is not None
                return repl
            if a.operation == 'delete_stmt': return None
            if a.operation == 'insert_before':
                assert repl is not None
                return [repl, node]
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                new=[]
                for item in value:
                    if isinstance(item, ast.AST):
                        changed=visit(item)
                        if isinstance(changed, list): new.extend(changed)
                        elif changed is not None: new.append(changed)
                    else: new.append(item)
                setattr(node, field, new)
            elif isinstance(value, ast.AST):
                changed=visit(value)
                if isinstance(changed, list):
                    raise PatchRejected('statement insertion outside statement list')
                if changed is None:
                    raise PatchRejected('statement deletion outside statement list')
                setattr(node, field, changed)
        return node
    transformed=visit(tree)
    if not isinstance(transformed, ast.Module):
        raise PatchRejected('invalid expected module')
    return transformed

def compile_multi_ast_congruent(sources: Mapping[str, bytes], actions: Sequence[Action], *,
                                allowed_paths: frozenset[str]) -> dict[str, bytes]:
    if not actions or len(actions) > 64 or len(sources) > 64:
        raise PatchRejected('invalid transaction size')
    if any(checked_path(p) != p for p in allowed_paths):
        raise PatchRejected('invalid authority')
    by_path: dict[str, list[Action]] = {}
    for a in actions:
        if not isinstance(a, Action) or a.operation not in SUPPORTED:
            raise PatchRejected('unsupported action')
        if a.path not in sources or a.path not in allowed_paths:
            raise PatchRejected('unauthorized source')
        if type(sources[a.path]) is not bytes or sha256(sources[a.path]).hexdigest() != a.source_sha256:
            raise PatchRejected('stale or invalid source SHA')
        by_path.setdefault(a.path, []).append(a)
    expected={p: _expected_ast(sources[p], group) for p,group in by_path.items()}
    patched=compile_structural(sources, actions, allowed_paths=allowed_paths)
    for p, want in expected.items():
        try: got=ast.parse(patched[p].decode('utf-8'))
        except (UnicodeError, SyntaxError, ValueError, TypeError) as exc:
            raise PatchRejected('invalid patched AST') from exc
        if ast.dump(got, include_attributes=False) != ast.dump(want, include_attributes=False):
            raise PatchRejected('whole-module AST mismatch')
    if any(patched[p] != sources[p] for p in sources if p not in by_path):
        raise PatchRejected('unauthorized mutation')
    return patched
