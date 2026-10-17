"""Development-only Run79 task manifest and independent semantic oracle."""
import ast
import itertools
import json
from pathlib import Path
from lattice.semantic_edits import Program, parse_python_patch, parse_lattice_patch
from lattice.framed_edits import FramedProgram
from research.run62.independent_oracle import audit_three_way, bound_values, eval_bool

TASKS = Path(__file__).with_name("tasks.json")

def load_tasks():
    manifest = json.loads(TASKS.read_text())
    assert manifest["schema"] == "lattice-run79-development-v1"
    return manifest["tasks"]

def score(task, arm, response):
    before = FramedProgram.from_program(Program(tuple(task["inputs"]), tuple(task["rules"].items())))
    parser = parse_python_patch if arm == "python" else parse_lattice_patch
    try:
        patch = parser(response)
        if set(patch) != set(task["allowed"]):
            return {"ok": False, "error": "scope"}
        after = before.edit(patch, set(task["allowed"]))
        audit = audit_three_way(before, after, set(task["allowed"]))
        if not audit["ok"]:
            return {"ok": False, "error": "oracle", "audit": audit}
        for bits in itertools.product((False, True), repeat=len(task["inputs"])):
            values = dict(zip(task["inputs"], bits))
            old = bound_values(before, values)
            got = bound_values(after, values)
            for name in old:
                expected = (eval_bool(ast.parse(task["target"][name], mode="eval").body, values)
                            if name in task["allowed"] else old[name])
                if got[name] != expected:
                    return {"ok": False, "error": "semantic", "input": values,
                            "output": name, "expected": expected, "got": got[name]}
        return {"ok": True, "cases": 2 ** len(task["inputs"])}
    except (ValueError, SyntaxError, TypeError) as exc:
        return {"ok": False, "error": type(exc).__name__}
