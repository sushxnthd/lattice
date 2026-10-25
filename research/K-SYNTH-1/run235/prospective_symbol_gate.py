#!/usr/bin/env python3
"""Prospective semantic-editor contract: retain named AST declaration in same scope.

A necessary, not sufficient, safety invariant for a whole-AST-node replace.
This is NOT wired into the frozen Run234 experiment.
"""
from __future__ import annotations
import ast

DECL = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


class DeclarationContractError(ValueError):
    pass


def declaration_paths(source: str):
    tree = ast.parse(source)
    found = []

    def visit(node, scope):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, DECL):
                first = min([child.lineno] + [d.lineno for d in getattr(child, 'decorator_list', [])])
                path = scope + ((type(child).__name__, child.name),)
                found.append({'path': path, 'start_line': first,
                              'end_line': child.end_lineno, 'node': child})
                visit(child, path)
            else:
                visit(child, scope)
    visit(tree, ())
    return found


def validate_replacement(target: dict, before: str, after: str):
    """Reject deletion/movement/renaming of the selected declaration.

    The caller must independently verify file hashes, selector authority,
    and transactionality. Explicit rename/delete operations are out of scope.
    """
    kind = target['kind']
    if kind not in ('FunctionDef', 'AsyncFunctionDef', 'ClassDef'):
        return {'applies': False, 'passes': True}
    originals = [x for x in declaration_paths(before)
                 if x['path'][-1] == (kind, target['name'])
                 and x['start_line'] == target['start_line']
                 and x['end_line'] == target['end_line']]
    if len(originals) != 1:
        raise DeclarationContractError('target not uniquely located in baseline AST')
    path = originals[0]['path']
    survivors = [x for x in declaration_paths(after) if x['path'] == path]
    if not survivors:
        raise DeclarationContractError('AST declaration erased, renamed or moved: ' + repr(path))
    return {'applies': True, 'passes': True, 'path': path, 'matches': len(survivors)}
