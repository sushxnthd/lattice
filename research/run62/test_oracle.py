"""Run62 independent oracle fault-injection tests."""
from pathlib import Path
import importlib.util
from unittest.mock import patch

from lattice.framed_edits import FramedProgram
from lattice.semantic_edits import Program

_PATH = Path(__file__).resolve().parent / "independent_oracle.py"
_SPEC = importlib.util.spec_from_file_location("run62_oracle", _PATH)
oracle = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(oracle)


def test_valid_edit_and_protected_frame():
    before = FramedProgram.from_program(Program(("a", "b"), (("read", "a"), ("edit", "read and b"))))
    after = before.edit({"read": "True"}, {"read"})
    report = oracle.audit_three_way(before, after, {"read"})
    assert report["ok"] is True
    assert report["cases"] == 4
    assert report["protected_pairs"] == 4


def test_independent_oracle_detects_protected_change():
    before = FramedProgram.from_program(Program(("a",), (("read", "a"), ("edit", "a"))))
    after = FramedProgram.from_program(Program(("a",), (("read", "a"), ("edit", "True"))))
    report = oracle.audit_three_way(before, after, {"read"})
    assert report["ok"] is False
    assert report["protected_regressions"] > 0


def test_independent_oracle_detects_production_corruption():
    before = FramedProgram.from_program(Program(("a",), (("read", "a"),)))
    with patch.object(FramedProgram, "run", lambda self, values: {"read": False}):
        report = oracle.audit_three_way(before, before, {"read"})
    assert report["ok"] is False
    assert report["production_before_mismatches"] > 0
    assert report["production_after_mismatches"] > 0


def test_independent_oracle_detects_lowering_corruption():
    before = FramedProgram.from_program(Program(("a",), (("read", "a"),)))
    original = FramedProgram.lower_python

    def corrupt(self):
        return original(self).replace(" = a", " = not a", 1)

    with patch.object(FramedProgram, "lower_python", corrupt):
        report = oracle.audit_three_way(before, before, {"read"})
    assert report["ok"] is False
    assert report["lowering_mismatches"] > 0


def test_independent_oracle_fails_closed_on_bound():
    before = FramedProgram.from_program(Program(("a", "b"), (("read", "a or b"),)))
    try:
        oracle.audit_three_way(before, before, {"read"}, max_inputs=1)
    except oracle.OracleError:
        pass
    else:
        raise AssertionError("expected bounded oracle rejection")
