#!/usr/bin/env python3
"""Minimal stdlib-only counterexample for Run225's PyBaMM positive control.

Upstream BatchStudy.solve sets self.sims=[] before iterating and appends each
simulation after its solve. Attribute existence is therefore not a sufficient
solved-state witness. This diagnostic does NOT modify the frozen Run225 endpoint.
"""
from types import SimpleNamespace

def old_guard(obj):
    return not hasattr(obj, "sims")

def corrected_guard(obj):
    return (not hasattr(obj, "sims") or not obj.sims
            or any(getattr(sim, "solution", None) is None for sim in obj.sims))

def main():
    solved = SimpleNamespace(solution=object())
    unsolved = SimpleNamespace(solution=None)
    cases = [
        ("absent", SimpleNamespace(), True),
        ("empty", SimpleNamespace(sims=[]), True),
        ("one_unsolved", SimpleNamespace(sims=[unsolved]), True),
        ("partial", SimpleNamespace(sims=[solved, unsolved]), True),
        ("solved", SimpleNamespace(sims=[solved]), False),
        ("multi_solved", SimpleNamespace(sims=[solved, solved]), False),
    ]
    old_passed = new_passed = 0
    for name, obj, expected_reject in cases:
        a, b = old_guard(obj), corrected_guard(obj)
        old_passed += (a == expected_reject)
        new_passed += (b == expected_reject)
        print(f"{name}: expected_reject={expected_reject} old={a} corrected={b}")
    assert old_passed == 3, old_passed
    assert new_passed == 6, new_passed
    print(f"old {old_passed}/6, corrected {new_passed}/6")
if __name__ == "__main__":
    main()
