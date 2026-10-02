import ast
import importlib.util
import random
from pathlib import Path

import pytest

from lattice.semantic_edits import (Program, InvalidProgram, admit, cases,
    parse_lattice_patch, parse_python_patch, verify)

SPEC = importlib.util.spec_from_file_location("exp002", Path(__file__).parents[1] / "experiments/exp002/sequential_edits.py")
EXP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXP)


def base():
    return Program(("auth", "owner", "blocked"),
                   (("read", "auth and not blocked"), ("edit", "read and owner")))


def test_dependency_trap_returns_reproducible_witness_and_rolls_back():
    old = base()
    proposed = old.patched({"read": "not blocked"})
    target = old.patched({"read": "not blocked", "edit": "auth and not blocked and owner"})
    committed, result = admit(old, proposed, target, {"read"})
    assert committed is old and not result["ok"]
    w = result["witness"]
    assert w["kind"] == "regression" and w["output"] == "edit"
    assert proposed.run(w["input"])["edit"] != old.run(w["input"])["edit"]
    assert admit(old, target, target, {"read"})[1]["ok"]


def test_frame_detects_weakened_trusted_target():
    old = base()
    proposed = old.patched({"edit": "True"})
    assert not verify(old, proposed, proposed, {"read"})["ok"]


def test_python_patch_and_lattice_patch_have_identical_semantics():
    old = base()
    one = old.patched(parse_lattice_patch("read = not blocked\nedit = auth and owner and not blocked"))
    two = old.patched(parse_python_patch('{"read": not blocked, "edit": auth and owner and not blocked}'))
    for values in cases(old.inputs):
        assert one.run(values) == two.run(values)


@pytest.mark.parametrize("patch", ["read = read", "read = edit\nedit = read", "read = missing"])
def test_cycles_and_unknown_references_are_rejected(patch):
    with pytest.raises(InvalidProgram):
        base().patched(parse_lattice_patch(patch))


@pytest.mark.parametrize("patch", ["read = open('secret')", "read = auth.__class__", "read = 1",
    "read = True\nread = False", "import os", "read = [auth]", "read = auth + owner"])
def test_unsupported_code_is_never_executed(patch):
    with pytest.raises(InvalidProgram): parse_lattice_patch(patch)


def test_declared_inputs_and_outputs_are_checked():
    with pytest.raises(InvalidProgram): base().run({"auth": True})
    with pytest.raises(InvalidProgram): base().run({"auth": 1, "owner": True, "blocked": False})
    with pytest.raises(InvalidProgram): base().patched({"unknown": "True"})
    with pytest.raises(InvalidProgram): parse_python_patch('{"read": True, "read": False}')
    with pytest.raises(InvalidProgram): Program(("auth", "auth"), (("read", "True"),))


def test_independent_oracle_all_frozen_checkpoints():
    EXP.validate_oracles()


def test_full_python_lowering_and_nested_if():
    policy = EXP.PythonPolicy("def policy(a):\n    if a:\n        return (True, False, True)\n    else:\n        return (False, True, False)\n", ("a",))
    assert tuple(policy.run({"a": True}).values()) == (True, False, True)
    with pytest.raises(InvalidProgram):
        EXP.PythonPolicy("def policy(a):\n    import os\n    return (a, a, a)", ("a",))


def test_cumulative_requirement_can_be_repaired_after_rejection():
    _, _, initial, steps, family = EXP.scenario(EXP.ALIASES[0])
    stage_two = initial.patched(steps[0][1]).patched(steps[1][1])
    assert EXP.check(initial, stage_two, family, 2, steps[1][2])["ok"]


def test_random_graphs_agree_with_independent_native_python_lowering():
    rng = random.Random(2042)
    for _ in range(100):
        inputs = ("a", "b", "c", "d")
        names = list(inputs)
        rules = []
        for i in range(5):
            x, y = rng.choice(names), rng.choice(names)
            s = f"({x} {rng.choice(['and', 'or'])} {y})"
            if rng.choice([False, True]): s = f"not {s}"
            name = f"rule{i}"
            rules.append((name, s)); names.append(name)
        program = Program(inputs, tuple(rules))
        # Only trusted generated code from the validated compiler is executed.
        scope = {"__builtins__": {}}
        exec(compile(program.lower_python(), "<trusted-lowering>", "exec"), scope)
        for values in cases(inputs):
            assert tuple(program.run(values).values()) == scope["policy"](**values)
