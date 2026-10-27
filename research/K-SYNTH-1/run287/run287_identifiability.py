#!/usr/bin/env python3
"""Run287 expression-only identifiability witness. Trusted test code only."""
import ast, builtins, hashlib, json, random

OLD = "len([connection.is_idle() for connection in connections]) > threshold"
NEW = "sum(connection.is_idle() for connection in connections) > threshold"

class Connection:
    def __init__(self, value): self.value = value
    def is_idle(self): return self.value

def evaluate(values, threshold, shadow_len=False):
    namespace = {
        "connections": [Connection(v) for v in values],
        "threshold": threshold,
        "__builtins__": builtins.__dict__,
    }
    if shadow_len:
        namespace["len"] = lambda xs: 0
    old = eval(compile(ast.parse(OLD, mode="eval"), "<trusted-old>", "eval"), namespace)
    new = eval(compile(ast.parse(NEW, mode="eval"), "<trusted-new>", "eval"), namespace)
    i = sum(bool(v) for v in values)
    return {"old": old, "new": new, "disagree": old != new,
            "naive_boolean_prediction": i <= threshold < len(values),
            "scope_attested": not shadow_len and all(type(v) is bool for v in values)}

def run():
    a = evaluate([True, True], 1)
    b = evaluate([True, True], 1, shadow_len=True)
    c = evaluate([2, 2], 3)
    assert (a["old"], a["new"]) == (True, True)
    assert (b["old"], b["new"]) == (False, True)
    assert (c["old"], c["new"]) == (False, True)
    assert a["disagree"] != b["disagree"]
    rng = random.Random(287)
    errors = 0
    for _ in range(5000):
        vals = [bool(rng.randrange(2)) for _ in range(rng.randrange(1, 12))]
        k = rng.randrange(-1, 13)
        x = evaluate(vals, k)
        errors += x["disagree"] != x["naive_boolean_prediction"]
    assert errors == 0
    return {"schema": "lattice-run287-expression-identifiability-v1",
            "fixed_expression_ast_hashes": [
                hashlib.sha256(ast.dump(ast.parse(s, mode="eval")).encode()).hexdigest()
                for s in (OLD, NEW)],
            "exact_boolean_trials": 5000, "theorem_mismatches": errors,
            "ordinary_builtins": a, "shadowed_len": b,
            "non_boolean_predicate": c,
            "conclusion": "EXPRESSION_ONLY_RUNTIME_CLASSIFICATION_UNIDENTIFIABLE",
            "limitation": "does not rule out verified whole-program analysis"}

if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
