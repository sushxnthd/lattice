"""Portable read-only gate for original Run360 Jinja factorial evidence.
No historical production code is imported or executed.
"""
import hashlib
import json
import sys
from pathlib import Path

BASE = ("df6fa372e60182cbadabd437a538f3c3997d102e", "a05b196118bc355c10f1cfff245a958c1089e968")
REF = ("50f98f1a9c064e3f270eed5ae547b1138584bce0", "4a3c36eeaf5a480b824e6c01f4ac6034e4d9e65a")
EXPECTED = {"base": BASE, "compiler_only": (REF[0], BASE[1]), "runtime_only": (BASE[0], REF[1]), "full": REF}
NAMES = {"target_scoped_loop", "target_loop_local_context", "target_block_local_context",
         "target_nested_scoped_context", "target_heldout_shadowed_assignment",
         "target_heldout_block_shadow", "control_plain_scope", "control_ordinary_loop_call",
         "control_ordinary_block_call", "control_context_top_level", "control_empty_loop",
         "control_scoped_block_no_loop"}

def check(directory):
    d = Path(directory)
    manifest = {}
    for line in (d / "sha256_manifest.txt").read_text().splitlines():
        sha, path = line.split()
        assert path.startswith("run360-results/")
        name = path.split("/", 1)[1]
        assert name not in manifest
        manifest[name] = sha
    assert set(manifest) == {v + ".json" for v in EXPECTED} | {
        "source_shas.json", "source_sha_lines.txt", "frozen_commits.txt", "INDEPENDENT_AUDIT.json"}
    for name, sha in manifest.items():
        assert hashlib.sha256((d / name).read_bytes()).hexdigest() == sha, name
    assert (d / "frozen_commits.txt").read_text().splitlines() == [
        "94ccd028ef1f3cd9eaec862d6a1d646d02a242bc",
        "f524bcce0cf295941fe665cbcb6846e7e9f39df5"]
    source = json.loads((d / "source_shas.json").read_text())
    assert {k: (v["compiler"], v["runtime"]) for k, v in source.items()} == EXPECTED
    rows = {}
    for variant in EXPECTED:
        data = json.loads((d / (variant + ".json")).read_text())
        assert data["variant"] == variant and data["jinja_version"] == "3.0.0a1"
        assert data["python"].startswith("3.9.")
        rs = data["records"]
        assert len(rs) == 12 and {r["name"] for r in rs} == NAMES
        assert data["counts"] == {s: sum(r["status"] == s for r in rs)
                                  for s in ("PASS", "FAIL", "ERROR")}
        for r in rs:
            s = r["status"]
            assert ((s == "PASS" and r["actual"] == r["expected"] and r["error"] is None)
                    or (s == "FAIL" and r["actual"] != r["expected"] and r["error"] is None)
                    or (s == "ERROR" and r["actual"] is None and isinstance(r["error"], dict)))
        rows[variant] = {r["name"]: r for r in rs}
    matrix = []
    for name in sorted(NAMES):
        identities = {(rows[v][name]["kind"], rows[v][name]["expected"],
                       rows[v][name]["template_sha256"]) for v in EXPECTED}
        assert len(identities) == 1
        bits = {v: int(rows[v][name]["status"] == "PASS") for v in EXPECTED}
        matrix.append((name, rows["base"][name]["kind"], bits,
                       bits["full"] - bits["compiler_only"] - bits["runtime_only"] + bits["base"]))
    controls = [x for x in matrix if x[1] == "control"]
    targets = [x for x in matrix if x[1] != "control"]
    assert len(controls) == len(targets) == 6
    assert all(x[2]["base"] for x in controls)
    assert all(x[2]["full"] for x in matrix)
    assert any(not x[2]["base"] for x in targets)
    assert any(not x[2]["compiler_only"] for x in matrix)
    assert any(not x[2]["runtime_only"] for x in matrix)
    counts = {v: sum(x[2][v] for x in matrix) for v in EXPECTED}
    assert counts == {"base": 7, "compiler_only": 5, "runtime_only": 7, "full": 12}
    assert sum(x[3] for x in targets) == 5
    assert sum(x[3] for x in controls) == 2
    original = json.loads((d / "INDEPENDENT_AUDIT.json").read_text())
    assert original["qualified_joint_target_control"] and original["counts"] == counts
    return {"status": "finite_joint_target_plus_control_qualified", "counts": counts,
            "target_interaction": 5, "control_interaction": 2,
            "manifest_entries": len(manifest)}

if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1]), sort_keys=True))
