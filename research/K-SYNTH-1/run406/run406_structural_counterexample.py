#!/usr/bin/env python3
"""Read-only structural-holdout audit of the unmodified Run405 frozen oracle."""
import ast
import collections
import pathlib

ORACLE = pathlib.Path(__file__).resolve().parents[1] / "run405" / "run405_issue14997_oracle.py"

def frozen_cases():
    tree = ast.parse(ORACLE.read_text(encoding="utf-8"))
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            if isinstance(stmt.targets[0], ast.Name) and stmt.targets[0].id == "CASES":
                return ast.literal_eval(stmt.value)
    raise RuntimeError("Frozen CASES not found")

def pattern(paths):
    result = []
    packages = []
    for name in paths:
        parts = pathlib.PurePosixPath(name).parts
        if len(parts) == 2:
            result.append("TOP")
        elif len(parts) == 3:
            result.append("PACKAGE")
            packages.append(parts[1])
        else:
            result.append("UNKNOWN")
    if len(set(packages)) > 1:
        result.append("CROSS_PACKAGE")
    return tuple(result)

if __name__ == "__main__":
    cases = frozen_cases()
    target = {case_id: pattern(paths) for case_id, kind, paths in cases if kind != "control"}
    controls = {case_id: pattern(paths) for case_id, kind, paths in cases if kind == "control"}
    assert len(target) == 6 and len(controls) == 6
    assert set(target.values()) == {("PACKAGE", "TOP", "PACKAGE")}
    print("Six disjoint target argument sequences, ONE abstract structural class")
    print("Target classes:", dict(collections.Counter(target.values())))
    print("Control classes:", dict(collections.Counter(controls.values())))
    print("This is NOT a claim of semantic equivalence under all pytest implementations.")
