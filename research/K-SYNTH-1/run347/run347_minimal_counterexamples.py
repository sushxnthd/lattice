"""Run347 executable CPython counterexamples and bytecode-local-binding witness.

This file executes only self-authored synthetic code, never model completions or
historical repository code. Run: python run347_minimal_counterexamples.py
"""
from __future__ import annotations
import ast
import dis
import json
import subprocess
import sys

SOURCE = """def f(x, y):
    a = x + y
    b = a * 3
    return b
"""

CHILD = r"""
import json, sys
def callee(x): return x + 1
def target(x): return callee(x)
before = target(10)
def callee(x): return x - 1
after = target(10)
def f():
    x = 1
    y = 2
    return x + y
read_line = f.__code__.co_firstlineno + 3
def tracer(frame, event, arg):
    if frame.f_code.co_name == 'f' and event == 'line' and frame.f_lineno == read_line:
        frame.f_locals['x'] = 99
    return tracer
normal = f()
sys.settrace(tracer)
try:
    mutated = f()
finally:
    sys.settrace(None)
print(json.dumps(dict(before=before, after=after, normal=normal, mutated=mutated,
                      python=sys.version.split()[0])))
"""

def run():
    tree = ast.parse(SOURCE)
    fn = tree.body[0]
    assert isinstance(fn, ast.FunctionDef)
    code = compile(SOURCE, "<synthetic>", "exec")
    nested = next(c for c in code.co_consts if hasattr(c, "co_code") and c.co_name == "f")
    ops = list(dis.get_instructions(nested))
    # Python 3.13 can fuse the two argument reads into one superinstruction.
    assert any(i.opname == "LOAD_FAST_LOAD_FAST" and i.argval == ("x", "y")
               for i in ops) or all(any(i.opname in ("LOAD_FAST", "LOAD_FAST_CHECK")
               and i.argval == name for i in ops) for name in ("x", "y"))
    assert any(i.opname == "STORE_FAST" and i.argval == "a" for i in ops)
    assert any(i.opname == "LOAD_FAST" and i.argval == "b" for i in ops)
    p = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD],
                       capture_output=True, text=True, check=True, timeout=10)
    outcome = json.loads(p.stdout)
    assert (outcome["before"], outcome["after"]) == (11, 9)
    assert outcome["normal"] == 3
    # CPython frame mutation is implementation/version sensitive; record the
    # actual observation and require a change on this tested runtime.
    assert outcome["mutated"] == 101, outcome
    outcome["runtime_callee_MUST"] = "FALSIFIED"
    outcome["unconditional_local_binding_MUST"] = "FALSIFIED"
    outcome["conditional_on_reach_no_frame_mutation"] = "NOT_FALSIFIED"
    outcome["production_source_executed"] = False
    print(json.dumps(outcome, sort_keys=True, indent=2))
    return outcome

if __name__ == "__main__":
    run()
