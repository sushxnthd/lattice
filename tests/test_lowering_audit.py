from lattice.lowering_audit import audit_framed_lowering
from lattice.framed_edits import FramedProgram
from lattice.semantic_edits import Program, InvalidProgram
import pytest


def test_exact_finite_semantics():
    before = FramedProgram.from_program(Program(("a", "b"), (("read", "a"), ("edit", "read and b"))))
    after = before.edit({"read": "True"}, {"read"})
    report = audit_framed_lowering(before, after, {"read"})
    assert report["ok"] is True
    assert report["cases"] == 4
    assert report["changed_pairs"]["edit"] == 0
    assert report["protected_pairs"] == 4


def test_protected_change_is_detected():
    before = FramedProgram.from_program(Program(("a",), (("read", "a"), ("edit", "read"))))
    changed = FramedProgram.from_program(Program(("a",), (("read", "a"), ("edit", "True"))))
    report = audit_framed_lowering(before, changed, {"read"})
    assert report["ok"] is False
    assert report["protected_regressions"] > 0


def test_bounded_audit():
    before = FramedProgram.from_program(Program(("a", "b"), (("read", "a or b"),)))
    with pytest.raises(InvalidProgram):
        audit_framed_lowering(before, before, {"read"}, max_inputs=1)
