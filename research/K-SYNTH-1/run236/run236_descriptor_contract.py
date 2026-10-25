#!/usr/bin/env python3
"""Prospective scoped AST declaration+decorator safety contract.

Preserve the original symbol and its descriptor/decorator semantics unless
the caller explicitly authorizes decorator changes. This is necessary, not
sufficient, for correctness. Do not apply retroactively to frozen Run234.
"""
import ast

DECL = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


class DeclarationContractError(ValueError):
    pass


def declaration_paths(source):
    tree = ast.parse(source)
    found = []

    def visit(node, scope):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, DECL):
                first = min([child.lineno] +
                            [d.lineno for d in getattr(child, "decorator_list", [])])
                path = scope + ((type(child).__name__, child.name),)
                found.append({"path": path, "start_line": first,
                              "end_line": child.end_lineno, "node": child})
                visit(child, path)
            else:
                visit(child, scope)
    visit(tree, ())
    return found


def validate_declaration_and_decorators(
    target, before, after, *, allow_decorator_change=False
):
    kind = target["kind"]
    if kind not in ("FunctionDef", "AsyncFunctionDef", "ClassDef"):
        return {"applies": False, "passes": True}
    originals = [
        x for x in declaration_paths(before)
        if x["path"][-1] == (kind, target["name"])
        and x["start_line"] == target["start_line"]
        and x["end_line"] == target["end_line"]
    ]
    if len(originals) != 1:
        raise DeclarationContractError("baseline target not uniquely identified")
    original = originals[0]
    survivors = [x for x in declaration_paths(after) if x["path"] == original["path"]]
    if len(survivors) != 1:
        raise DeclarationContractError("original declaration missing, moved or duplicated")

    def decorators(node):
        return [ast.dump(d, include_attributes=False) for d in node.decorator_list]

    old = decorators(original["node"])
    new = decorators(survivors[0]["node"])
    if old != new and not allow_decorator_change:
        raise DeclarationContractError("decorator/descriptor contract changed without authority")
    return {
        "applies": True, "passes": True, "path": original["path"],
        "decorators_preserved": old == new,
        "decorator_change_authorized": allow_decorator_change,
    }
