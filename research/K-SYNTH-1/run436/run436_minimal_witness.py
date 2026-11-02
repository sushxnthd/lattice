#!/usr/bin/env python3
"""Run436 minimal trusted two-file witness. No coding-model code executed."""
from __future__ import annotations
import ast
import hashlib
import json
import random
import sys
import types

def digest(x: bytes) -> str:
    return hashlib.sha256(x).hexdigest()

def sources(a, b, o):
    return {
        "provider.py": f"def core(x):\n    return x * {a} + {b}\n\ndef keep(x):\n    return x + 1\n".encode(),
        "consumer.py": f"from provider import core\n\ndef compute(x):\n    return core(x) + {o}\n\ndef keep(x):\n    return x - 1\n".encode(),
    }

def compile_transaction(src, new_b, new_o):
    if set(src) != {"provider.py", "consumer.py"}:
        raise ValueError("UNKNOWN_SOURCE_SET")
    p, c = (ast.parse(src[name]) for name in ("provider.py", "consumer.py"))
    if not (len(p.body) == 2 and len(c.body) == 3
            and isinstance(c.body[0], ast.ImportFrom)
            and c.body[0].module == "provider"
            and len(c.body[0].names) == 1
            and c.body[0].names[0].name == "core"):
        raise ValueError("UNKNOWN_IMPORT_OR_MODULE_SHAPE")
    if not (type(new_b) is int and type(new_o) is int):
        raise ValueError("UNKNOWN_EDIT_TYPE")
    p.body[0].body[0].value.right = ast.Constant(new_b)
    c.body[1].body[0].value.right = ast.Constant(new_o)
    return {"provider.py": (ast.unparse(p) + "\n").encode(),
            "consumer.py": (ast.unparse(c) + "\n").encode()}

def execute(src, x):
    p = types.ModuleType("provider")
    exec(compile(src["provider.py"], "provider.py", "exec"), p.__dict__)
    c = types.ModuleType("consumer")
    previous = sys.modules.get("provider")
    sys.modules["provider"] = p
    try:
        exec(compile(src["consumer.py"], "consumer.py", "exec"), c.__dict__)
    finally:
        if previous is None:
            sys.modules.pop("provider", None)
        else:
            sys.modules["provider"] = previous
    return (p.core(x), c.compute(x), p.keep(x), c.keep(x))

def main():
    rng = random.Random(4362026)
    observations = 0
    for _ in range(128):
        a, b, o = rng.randint(2, 9), rng.randint(-20, 20), rng.randint(-20, 20)
        db, do = rng.randint(1, 7), rng.randint(1, 7)
        original = sources(a, b, o)
        full = compile_transaction(original, b + db, o + do)
        assert all(digest(v) for v in full.values())
        variants = [original,
                    {"provider.py": full["provider.py"], "consumer.py": original["consumer.py"]},
                    {"provider.py": original["provider.py"], "consumer.py": full["consumer.py"]},
                    full]
        for _ in range(8):
            x = rng.randint(-1000, 1000)
            for index, variant in enumerate(variants):
                got = execute(variant, x)
                assert (got[:2] == (a*x+b+db, a*x+b+db+o+do)) == (index == 3)
                assert got[2:] == (x+1, x-1)
                observations += 4
        # Exhaustive finite grammar, 101^2 possible (b',o') edits.
        solutions = [(bb, oo) for bb in range(-50, 51) for oo in range(-50, 51)
                     if bb == b + db and bb + oo == b + db + o + do]
        assert solutions == [(b + db, o + do)]
        # If only consumer.compute is observed, one-file alternatives exist.
        assert b + db + do + o == b + db + o + do
        assert b + (o + db + do) == b + db + o + do
    print(json.dumps({"trusted_cases":128,"actual_function_calls":observations,
                      "finite_candidates_checked":128*101*101,
                      "dual_target_unique_solutions":128,
                      "qualified_real_repairs_added":0,
                      "model_completions":0}, sort_keys=True))

if __name__ == "__main__":
    main()
