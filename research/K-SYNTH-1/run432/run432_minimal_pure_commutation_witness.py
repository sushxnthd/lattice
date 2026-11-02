#!/usr/bin/env python3
"""Run432 executable restricted-Python commutation witness. No model-generated code."""
import ast

def names(expr):
    if isinstance(expr, ast.Name) and isinstance(expr.ctx, ast.Load):
        return {expr.id}
    if isinstance(expr, ast.Constant) and type(expr.value) is int:
        return set()
    if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, (ast.UAdd, ast.USub)):
        return names(expr.operand)
    if isinstance(expr, ast.BinOp) and isinstance(expr.op, (ast.Add, ast.Sub, ast.Mult)):
        return names(expr.left) | names(expr.right)
    raise ValueError("UNKNOWN_DYNAMIC_EXPRESSION")

def swap(source):
    tree = ast.parse(source)
    assert len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
    f = tree.body[0]
    assert len(f.body) == 3 and isinstance(f.body[2], ast.Return)
    a, b = f.body[:2]
    assert all(isinstance(x, ast.Assign) and len(x.targets) == 1 and
               isinstance(x.targets[0], ast.Name) for x in (a, b))
    wa, wb = a.targets[0].id, b.targets[0].id
    assert wa != wb and wa not in names(b.value) and wb not in names(a.value)
    f.body[:2] = [b, a]
    ast.fix_missing_locations(tree)
    return ast.unparse(tree) + "\n"

def execute(source, arg):
    namespace = {}
    exec(compile(source, "<trusted-witness>", "exec"), namespace)
    return namespace["f"](arg)

def main():
    source = "def f(x):\n    a = x + 1\n    b = x + 2\n    return a * b\n"
    modified = swap(source)
    for x in range(-100, 101):
        assert type(x) is int
        assert execute(source, x) == execute(modified, x)
    events = []
    class Spy:
        def __add__(self, other):
            events.append(other)
            return other
    execute(source, Spy())
    original_trace = events[:]
    events.clear()
    execute(modified, Spy())
    swapped_trace = events[:]
    assert original_trace == [1, 2] and swapped_trace == [2, 1]
    print({"exact_int_checks": 201, "disagreements": 0,
           "dynamic_counterexample": [original_trace, swapped_trace],
           "scope": "exact-int, pure expressions only"})

if __name__ == "__main__":
    main()
