#!/usr/bin/env python3
"""K-SYNTH-1 Run289: executable bounded lexical counterexample.
Only fixed trusted fixtures are compiled/executed; no model code is run.
"""
import ast
import builtins
import dis
import json
import symtable

FIXTURES = {
    "global": "def f(xs):\n    return len(xs)\n",
    "parameter": "def f(xs, len):\n    return len(xs)\n",
    "unbound": "def f(xs):\n    out = len(xs)\n    len = 0\n    return out\n",
    "closure": "def outer():\n    len = lambda xs: 0\n    def f(xs):\n        return len(xs)\n    return f\n",
}

def inspect(source):
    root = symtable.symtable(source, "<fixed>", "exec")
    target = root.get_children()[0]
    if target.get_name() == "outer":
        target = target.get_children()[0]
    symbol = target.lookup("len")
    if symbol.is_parameter():
        kind = "PARAMETER_LOCAL"
    elif symbol.is_free():
        kind = "FREE_CLOSURE"
    elif symbol.is_local():
        kind = "LOCAL_BINDING"
    else:
        kind = "GLOBAL_OR_BUILTIN_UNKNOWN"
    return {"lexical_kind": kind, "runtime_identity": "UNKNOWN"}

def main():
    result = {}
    for name, source in FIXTURES.items():
        ast.parse(source)
        scope = inspect(source)
        env = {"__builtins__": dict(vars(builtins))}
        exec(compile(source, "<trusted_fixed_fixture>", "exec"), env)
        fn = env["outer"]() if name == "closure" else env["f"]
        try:
            value = fn([1, 2, 3]) if name != "parameter" else fn([1, 2, 3], lambda xs: 0)
            observed = {"return": value}
        except Exception as error:
            observed = {"exception": type(error).__name__}
        result[name] = {"scope": scope, "observed": observed}
    assert result["global"]["observed"] == {"return": 3}
    assert result["parameter"]["observed"] == {"return": 0}
    assert result["unbound"]["observed"] == {"exception": "UnboundLocalError"}
    assert result["closure"]["observed"] == {"return": 0}
    assert all(row["scope"]["runtime_identity"] == "UNKNOWN" for row in result.values())
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
