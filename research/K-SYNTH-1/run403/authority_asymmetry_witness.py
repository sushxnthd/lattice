#!/usr/bin/env python3
"""K-SYNTH-1 Run403: executable AST-action authority asymmetry witness.
Only the straight-line, single-assignment, numeric Run402 domain is considered.
"""
import ast

SOURCE = """def f(x):
    dead = x + 9
    u = x + 1
    v = u * 2
    return v
"""

def reaching_statement_indices(source, function):
    tree = ast.parse(source)
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == function]
    if len(fns) != 1:
        raise ValueError("UNKNOWN_FUNCTION")
    fn = fns[0]
    if not fn.body or not isinstance(fn.body[-1], ast.Return) or fn.body[-1].value is None:
        raise ValueError("UNKNOWN_RETURN")
    live = {n.id for n in ast.walk(fn.body[-1].value)
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    result = set()
    for i in range(len(fn.body) - 2, -1, -1):
        node = fn.body[i]
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            raise ValueError("UNKNOWN_NON_SSA")
        name = node.targets[0].id
        if name in live:
            result.add(i)
            live.remove(name)
            live.update(n.id for n in ast.walk(node.value)
                        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load))
    return result

if __name__ == "__main__":
    permitted = reaching_statement_indices(SOURCE, "f")
    assert permitted == {1, 2}
    original_ast_authorizes_dead = True  # Run402 AST selector accepted index 0.
    fair_ast_authorizes_dead = 0 in permitted
    semantic_authorizes_dead = False  # Run402 IR requires reaching_return.
    assert original_ast_authorizes_dead and not fair_ast_authorizes_dead and not semantic_authorizes_dead
    print({"original_ast_dead": original_ast_authorizes_dead,
           "fair_ast_dead": fair_ast_authorizes_dead,
           "semantic_dead": semantic_authorizes_dead,
           "fair_reaching_indices": sorted(permitted)})
