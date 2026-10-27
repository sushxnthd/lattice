#!/usr/bin/env python3
"""Trusted CPython semantic witness. No model-generated code is executed."""
import ast, dis, json, sys
from builtins import len as original_len, sum as original_sum

log = []
def len(x):
    log.append("len")
    return original_len(x)
def sum(x):
    log.append("sum")
    return original_sum(x)

xs = [1, 2, 3]
a = [0] * 5
a[len(xs)]: int
assert log == ["len"], log
a[len(xs)]: int = 7
assert log == ["len", "len"], log
f = lambda x=len(xs): sum(xs) + x
assert log == ["len", "len", "len"], log
assert f() == 9
assert log == ["len", "len", "len", "sum"], log
g = (sum(xs) for i in range(len(xs)))
assert log == ["len", "len", "len", "sum", "len"], log
assert list(g) == [6, 6, 6]
assert log == ["len", "len", "len", "sum", "len", "sum", "sum", "sum"], log
cases = ["a[len(xs)]: int", "a[len(xs)]: int = 7", "a: int"]
bytecode = {s: any(x.opname == "CALL" for x in dis.get_instructions(compile(s, "<trusted>", "exec"))) for s in cases}
assert bytecode == {cases[0]: True, cases[1]: True, cases[2]: False}
print(json.dumps({"python": sys.version, "events": log, "bytecode_calls": bytecode, "status": "PASS"}, sort_keys=True))
