#!/usr/bin/env python3
"""Run310 trusted CPython 3.13 counterexample. Not model-generated code."""
import ast
import sys

assert sys.version_info[:2] == (3, 13), "Run310 requires eager CPython 3.13 annotations"
source = """from builtins import len as saved_len
len = lambda xs: -777
def f(x: (len := saved_len)): pass
observed = len([1, 2, 3])
assert observed == 3 and len is saved_len
"""
tree = ast.parse(source)
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
annotation = function.args.args[0].annotation
assert any(isinstance(n, ast.NamedExpr) for n in ast.walk(annotation))
assert not any(isinstance(n, ast.Call) for n in ast.walk(annotation))
namespace = {"__name__": "__main__"}
exec(compile(tree, "<trusted-run310-witness>", "exec"), namespace)
assert namespace["observed"] == 3
print("PASS: eager annotation NamedExpr restored builtins.len; Run309 ast.Call-only test misses this effect")
