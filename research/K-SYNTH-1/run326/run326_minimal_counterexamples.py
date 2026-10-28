#!/usr/bin/env python3
"""Run326 minimal executable semantic counterexamples; trusted expressions only.

This is a proof-by-counterexample artifact, not a whole-program analyzer.
"""
import ast
import json

def lexical_names(source):
    return sorted({node.id for node in ast.walk(ast.parse(source, mode="eval"))
                   if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)})

def main():
    events = []
    class Truth:
        def __bool__(self):
            events.append("HIDDEN_STATE_WRITE")
            return True
    x = Truth()
    assert bool(x) is True
    dynamic = {"source": "x", "lexical_names": lexical_names("x"),
               "runtime_effects": list(events)}
    assert dynamic["lexical_names"] == ["x"]
    assert dynamic["runtime_effects"] == ["HIDDEN_STATE_WRITE"]

    records = []
    for left in (False, True):
        for right in (False, True):
            reads = []
            def tap(name, value):
                reads.append(name)
                return value
            outcome = tap("x", left) and tap("y", right)
            records.append({"x": left, "y": right, "reads": reads,
                            "value": outcome})
    assert lexical_names("x and y") == ["x", "y"]
    assert sum(row["reads"] == ["x"] for row in records) == 2

    hidden = True
    result = eval("hidden", {"__builtins__": {}}, {"hidden": hidden})
    assert result is True and lexical_names("eval('hidden')") == ["eval"]

    output = {
        "scope": "DIRECT_LEXICAL_READS_ONLY",
        "dynamic_truthiness": dynamic,
        "short_circuit": records,
        "dynamic_eval": {"source": "eval('hidden')",
                         "lexical_names": lexical_names("eval('hidden')"),
                         "runtime_hidden_read": True},
        "claim": "A lexical Name graph cannot certify transitive effects; UNKNOWN required."
    }
    print(json.dumps(output, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
