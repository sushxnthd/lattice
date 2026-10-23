"""Safe Boolean XOR/conditional grammar, shared by both edit interfaces.

These tests are prospective compiler regression checks. They do not rescore
or change the frozen Run196 experiment.
"""
import itertools
import pytest
from lattice.semantic_edits import Program, InvalidProgram, expression
from lattice.framed_edits import FramedProgram


def test_xor_and_conditional_match_native_python_on_all_boolean_inputs():
    program = Program(("a", "b", "c"), (
        ("xor", "a ^ b"),
        ("mux", "xor if c else a"),
        ("endpoint", "mux"),
    ))
    framed = FramedProgram.from_program(program)
    namespace = {}
    exec(framed.lower_python(), namespace)
    native = namespace["policy"]
    for a, b, c in itertools.product((False, True), repeat=3):
        env = {"a": a, "b": b, "c": c}
        expected = (a ^ b) if c else a
        assert program.run(env)["endpoint"] == expected
        assert framed.run(env)["endpoint"] == expected
        native_results = native(a, b, c)
        assert tuple(framed.run(env)[root] for root, _ in framed.roots) == native_results


def test_xor_patch_preserves_historical_protected_output():
    before = FramedProgram.from_program(Program(("a", "b"), (
        ("gate", "a and b"), ("audit", "gate"), ("endpoint", "gate"),
    )))
    after = before.edit({"gate": "a ^ b"}, {"gate", "endpoint"})
    for a, b in itertools.product((False, True), repeat=2):
        env = {"a": a, "b": b}
        assert after.run(env)["gate"] == (a ^ b)
        assert after.run(env)["endpoint"] == (a ^ b)
        assert after.run(env)["audit"] == before.run(env)["audit"]


@pytest.mark.parametrize("source", [
    "a + b", "a | b", "a & b", "a == b", "int(a)",
    "a[0]", "[a][0]", "lambda: a", "(a := b)", "a ** b",
])
def test_expanded_allowlist_still_rejects_unsafe_or_unrelated_python(source):
    with pytest.raises(InvalidProgram):
        expression(source)
