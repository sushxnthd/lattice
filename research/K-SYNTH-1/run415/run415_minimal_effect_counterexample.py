#!/usr/bin/env python3
"""Run415 minimal executable counterexample to syntactic dead-definition pruning.

The definition 'dead' does not syntactically reach the return. Nevertheless,
editing its expression changes the return via overloaded __add__.
"""
import subprocess
import sys

prefix = """state=[0]
class X:
    def __add__(self, value):
        state[0] += value
        return state[0]
"""
base = """def f(x):
    dead = x + 1
    live = x + 2
    return live
"""
edited = base.replace("dead = x + 1", "dead = x + 101")

def execute(source):
    cp = subprocess.run(
        [sys.executable, "-I", "-S", "-c", prefix + source + "print(f(X()))"],
        capture_output=True, text=True, timeout=5, check=True
    )
    return int(cp.stdout.strip())

if __name__ == "__main__":
    before, after = execute(base), execute(edited)
    assert (before, after) == (3, 103), (before, after)
    print({"before": before, "after": after, "changed": before != after})
