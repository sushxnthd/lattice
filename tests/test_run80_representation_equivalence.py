"""Run80 development-only equivalence audit: format is not semantic IR.
This does not evaluate a model and must not be counted as representation superiority.
"""
import itertools
from lattice.semantic_edits import Program, parse_lattice_patch, parse_python_patch
from lattice.framed_edits import FramedProgram
from research.run79.independent_scoring import load_tasks, score


def candidate_expressions(inputs):
    a, b, c = inputs
    atoms = (a, b, c, "True", "False")
    expressions = list(atoms)
    expressions += ["not " + x for x in atoms]
    for x, y in itertools.product(atoms, repeat=2):
        expressions += ["(" + x + " and " + y + ")", "(" + x + " or " + y + ")"]
    expressions += [
        "(" + a + " or " + b + ") and not " + c,
        a + " and (" + b + " or " + c + ")",
        "not (" + a + " and " + b + ")",
        "(" + a + " or " + b + ") and (" + b + " or " + c + ")",
    ]
    return expressions


def test_same_semantics_for_matched_content():
    checked = 0
    for task in load_tasks():
        name = task["allowed"][0]
        before = FramedProgram.from_program(
            Program(tuple(task["inputs"]), tuple(task["rules"].items()))
        )
        for expr in candidate_expressions(task["inputs"]):
            python_text = "{" + repr(name) + ": " + expr + "}"
            ir_text = name + " = " + expr
            python_patch = parse_python_patch(python_text)
            ir_patch = parse_lattice_patch(ir_text)
            assert python_patch == ir_patch
            after_python = before.edit(python_patch, set(task["allowed"]))
            after_ir = before.edit(ir_patch, set(task["allowed"]))
            assert after_python == after_ir
            assert after_python.lower_python() == after_ir.lower_python()
            assert score(task, "python", python_text) == score(task, "ir", ir_text)
            checked += 1
    assert checked == 6 * 64


def test_format_rejection_is_distinct_from_semantic_content():
    task = load_tasks()[0]
    name = task["allowed"][0]
    expr = task["target"][name]
    assert score(task, "python", "{" + repr(name) + ": " + expr + "}")["ok"]
    assert score(task, "ir", name + " = " + expr)["ok"]
    assert not score(task, "python", name + " = " + expr)["ok"]
    assert not score(task, "ir", "{" + repr(name) + ": " + expr + "}")["ok"]
