"""Run444 minimal excerpt-only cross-file dataflow counterexample (trusted code)."""
import json, subprocess, sys, tempfile
from pathlib import Path

excerpt_a = "def f(x):\n    return helper(x)\n"
excerpt_b = "def helper(x):\n    return x + 1\n"
values = list(range(-64, 64))
for imported in ("b", "c"):
    outputs = {}
    for edit in (False, True):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.py").write_text(f"from {imported} import helper\n" + excerpt_a)
            (root / "b.py").write_text("def helper(x):\n    return x + " + ("11" if edit else "1") + "\n")
            (root / "c.py").write_text("def helper(x):\n    return x + 100\n")
            script = "import sys,json;sys.path.insert(0,sys.argv[1]);import a;print(json.dumps([a.f(x) for x in range(-64,64)]))"
            p = subprocess.run([sys.executable, "-I", "-c", script, d],
                               check=True, capture_output=True, text=True, timeout=15)
            outputs[edit] = json.loads(p.stdout)
    delta = [b-a for a,b in zip(outputs[False],outputs[True])]
    assert delta == ([10]*128 if imported == "b" else [0]*128)
    print(imported, "edit b.py delta:", delta[0], "on", len(delta), "inputs")
print("Published a.py and b.py excerpts identical; dependency unidentifiable.")
