#!/usr/bin/env python3
"""Run338 prospectively frozen Rich #3180 qualification.

Protocol: research/K-SYNTH-1/run337/PROTOCOL_RUN338_RICH3180.md
NO REFERENCE DIFF was inspected before this source was committed.
Source-informed minimal public API oracle; no model inference.
"""
import argparse
import hashlib
import importlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = "e76f3c3ea78481342e21a7b3328075462ab69c2b"
HEAD = "05c5dfc8fcbb1c967490540cc080c3d534a91a12"
PATHS = ("rich/_wrap.py", "rich/cells.py")
EXPECTED_BASE_BLOBS = {
    "rich/_wrap.py": "c45f193f74ad7385c84f3b935663198415cfaa4b",
    "rich/cells.py": "9354f9e3140999702ec8c140636c511d71c340b2",
}
CASES = (
    [("public", "アプリケーションは1670万色を使用でき", 20),
     ("public", "TextualはPythonの高速アプリケーション開発フレームワークです", 20)]
    + [("heldout", text, width)
       for text, widths in (
           ("東京大阪京都123456789", (6, 8, 10)),
           ("AB日本語CD東京EF", (5, 7, 9)),
           ("漢字123ABC仮名456", (4, 6, 8)))
       for width in widths]
    + [("control", text, width)
       for text, widths in (
           ("hello world", (5, 10, 20)),
           ("abc 123 def", (5, 8, 12)),
           ("日本語", (6, 8)),
           ("", (5,)))
       for width in widths]
)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()

def git_show(repo, commit, path):
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{commit}:{path}"])

def evaluate(root, label):
    sys.path.insert(0, str(root))
    for name in tuple(sys.modules):
        if name == "rich" or name.startswith("rich."):
            del sys.modules[name]
    try:
        wrap = importlib.import_module("rich._wrap")
        cells = importlib.import_module("rich.cells")
        rows = []
        for stratum, source, width in CASES:
            row = {"arm": label, "stratum": stratum, "text": source, "width": width}
            try:
                cuts = wrap.divide_line(source, width, fold=True)
                boundaries = [0] + list(cuts) + [len(source)]
                segments = [source[a:b] for a, b in zip(boundaries, boundaries[1:])]
                widths = [cells.cell_len(s) for s in segments]
                row.update({"cuts": cuts, "segments": segments, "cell_widths": widths,
                            "preserved": "".join(segments) == source,
                            "width_ok": all(n <= width for n in widths),
                            "ok": "".join(segments) == source and all(n <= width for n in widths)})
            except Exception as exc:
                row.update({"ok": False, "error_type": type(exc).__name__,
                            "error": str(exc)})
            rows.append(row)
        return rows
    except Exception as exc:
        return [{"arm": label, "import_error": type(exc).__name__,
                 "detail": str(exc), "ok": False}]
    finally:
        sys.path.remove(str(root))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    repo = pathlib.Path(args.repo).resolve()
    output = pathlib.Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    # Explicitly verify historical baseline before any reference source is accessed.
    base_bytes = {p: git_show(repo, BASE, p) for p in PATHS}
    base_blobs = {p: git_blob(data) for p, data in base_bytes.items()}
    assert base_blobs == EXPECTED_BASE_BLOBS, base_blobs
    # Historical HEAD read only after frozen oracle and baseline SHA verification.
    ref_bytes = {p: git_show(repo, HEAD, p) for p in PATHS}
    source_sha = {"base": {p: sha256(v) for p, v in base_bytes.items()},
                  "ref": {p: sha256(v) for p, v in ref_bytes.items()}}
    records = []
    with tempfile.TemporaryDirectory(prefix="lattice-run338-") as temp:
        for use_wrap, use_cells in ((0,0),(1,0),(0,1),(1,1)):
            arm = f"wrap{use_wrap}_cells{use_cells}"
            root = pathlib.Path(temp) / arm
            shutil.copytree(repo / "rich", root / "rich")
            for path, use_ref in zip(PATHS, (use_wrap, use_cells)):
                (root / path).write_bytes(ref_bytes[path] if use_ref else base_bytes[path])
            records.extend(evaluate(root, arm))
    summaries = {}
    for arm in ("wrap0_cells0", "wrap1_cells0", "wrap0_cells1", "wrap1_cells1"):
        rr = [r for r in records if r["arm"] == arm]
        summaries[arm] = {
            "targets": sum(r["ok"] for r in rr if r.get("stratum") in ("public", "heldout")),
            "controls": sum(r["ok"] for r in rr if r.get("stratum") == "control"),
            "errors": sum("error_type" in r or "import_error" in r for r in rr),
            "total_rows": len(rr)}
    total_targets = sum(s in ("public", "heldout") for s, _, _ in CASES)
    total_controls = len(CASES) - total_targets
    base = summaries["wrap0_cells0"]
    full = summaries["wrap1_cells1"]
    singles = [summaries["wrap1_cells0"], summaries["wrap0_cells1"]]
    qualified = (
        base["targets"] < total_targets
        and full["targets"] == total_targets and full["controls"] == total_controls
        and all(x["targets"] < total_targets or x["controls"] < total_controls for x in singles)
        and all(x["total_rows"] == len(CASES) for x in summaries.values())
    )
    report = {"candidate": "Textualize/rich#3180", "base": BASE, "head": HEAD,
              "source_sha256": source_sha, "baseline_git_blobs": base_blobs,
              "oracle_case_count": len(CASES), "targets": total_targets,
              "controls": total_controls, "summaries": summaries,
              "qualified": qualified, "records": records,
              "scope": "direct historical rich._wrap.divide_line API, not Console integration"}
    raw = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2).encode()
    (output / "raw_results.json").write_bytes(raw)
    (output / "raw_results.sha256").write_text(sha256(raw) + "  raw_results.json\\n")
    print(json.dumps({"qualified": qualified, "summaries": summaries,
                      "cases": len(CASES), "sha256": sha256(raw)}, indent=2))
if __name__ == "__main__":
    main()
