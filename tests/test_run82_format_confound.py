"""Run82: synthetic format-confound test. Not model inference."""
from research.run79.independent_scoring import load_tasks, score

def test_format_confound_is_not_semantic_representation_evidence():
    for task in load_tasks():
        name = task["allowed"][0]
        expr = task["target"][name]
        assignment = name + " = " + expr
        dictionary = "{" + repr(name) + ": " + expr + "}"
        assert score(task, "ir", assignment)["ok"]
        assert score(task, "python", dictionary)["ok"]
        assert not score(task, "python", assignment)["ok"]
        assert not score(task, "ir", dictionary)["ok"]

def test_native_parser_rejection_is_not_a_compiler_disagreement():
    task = load_tasks()[0]
    name = task["allowed"][0]
    expr = task["target"][name]
    assignment = name + " = " + expr
    rejected = score(task, "python", assignment)
    accepted = score(task, "ir", assignment)
    assert rejected["error"] == "InvalidProgram"
    assert accepted["ok"]
