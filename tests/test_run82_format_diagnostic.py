"""Run82 post-hoc diagnostic tests; all outputs are synthetic, no model calls."""
import json
import pytest
from research.run79.independent_scoring import load_tasks
from research.run82.format_diagnostic import diagnose, reanalyze


def test_format_only_error_is_separable_from_semantic_error():
    for task in load_tasks():
        name = task["allowed"][0]
        expr = task["target"][name]
        ir_text = name + " = " + expr
        result = diagnose(task, "python", ir_text)
        assert not result["native"]["ok"]
        assert result["normalized"]["ok"]
        assert result["format_only_failure"]
        assert diagnose(task, "ir", ir_text)["native"]["ok"]


def test_wrong_semantics_and_scope_fail_both_formats():
    task = load_tasks()[0]
    wrong = diagnose(task, "ir", "read = False")
    assert not wrong["native"]["ok"]
    assert not wrong["normalized"]["ok"]
    scope = diagnose(task, "ir", "audit = True")
    assert not scope["normalized"]["ok"]
    assert scope["normalized"]["error"] == "scope"


def test_synthetic_transcript_reanalysis(tmp_path):
    rows = []
    for task in load_tasks():
        name = task["allowed"][0]
        text = name + " = " + task["target"][name]
        for arm in ("python", "ir"):
            rows.append({"task": task["id"], "arm": arm,
                         "attempts": [{"raw_text": text}]})
    path = tmp_path / "synthetic.json"
    path.write_text(json.dumps({"rows": rows}))
    report = reanalyze(path)
    assert len(report["rows"]) == 12
    assert sum(row["native_success"] for row in report["rows"] if row["arm"] == "python") == 0
    assert sum(row["native_success"] for row in report["rows"] if row["arm"] == "ir") == 6
    assert all(row["normalized_success"] for row in report["rows"])


def test_incomplete_transcript_is_rejected(tmp_path):
    path = tmp_path / "empty.json"
    path.write_text(json.dumps({"rows": []}))
    with pytest.raises(ValueError, match="incomplete"):
        reanalyze(path)
