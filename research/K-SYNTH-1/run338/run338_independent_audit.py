#!/usr/bin/env python3
"""Independent read-only auditor of original Run338 Rich functional evidence."""
import hashlib
import json
import pathlib
import sys
import unicodedata

BASE = "e76f3c3ea78481342e21a7b3328075462ab69c2b"
HEAD = "05c5dfc8fcbb1c967490540cc080c3d534a91a12"
BLOBS = {"rich/_wrap.py": "c45f193f74ad7385c84f3b935663198415cfaa4b",
         "rich/cells.py": "9354f9e3140999702ec8c140636c511d71c340b2"}
ARMS = ("wrap0_cells0", "wrap1_cells0", "wrap0_cells1", "wrap1_cells1")
CASES = [("public", "アプリケーションは1670万色を使用でき", 20),
         ("public", "TextualはPythonの高速アプリケーション開発フレームワークです", 20)]
for s, widths in (("東京大阪京都123456789", (6,8,10)),
                  ("AB日本語CD東京EF", (5,7,9)),
                  ("漢字123ABC仮名456", (4,6,8))):
    CASES.extend(("heldout", s, w) for w in widths)
for s, widths in (("hello world", (5,10,20)),
                  ("abc 123 def", (5,8,12)),
                  ("日本語", (6,8)),
                  ("", (5,))):
    CASES.extend(("control", s, w) for w in widths)

def cell_width(s):
    # All frozen characters are noncombining; independent Unicode check.
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)

def audit(directory):
    directory = pathlib.Path(directory)
    raw = (directory / "raw_results.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == (directory / "raw_results.sha256").read_text().split()[0]
    data = json.loads(raw)
    assert data["base"] == BASE and data["head"] == HEAD
    assert data["baseline_git_blobs"] == BLOBS
    assert data["targets"] == 11 and data["controls"] == 9
    assert len(data["records"]) == 80 and len(CASES) == 20
    seen = set()
    summaries = {}
    for arm in ARMS:
        rows = [r for r in data["records"] if r["arm"] == arm]
        assert len(rows) == 20
        targets = controls = errors = 0
        for row, case in zip(rows, CASES):
            assert (row["stratum"], row["text"], row["width"]) == case
            key = (arm, *case)
            assert key not in seen
            seen.add(key)
            if "error_type" in row:
                assert row["ok"] is False and "segments" not in row
                errors += 1
                continue
            cuts = row["cuts"]
            assert cuts == sorted(cuts)
            assert all(0 <= n <= len(row["text"]) for n in cuts)
            parts = [row["text"][a:b] for a,b in
                     zip([0]+cuts, cuts+[len(row["text"])])]
            widths = [cell_width(s) for s in parts]
            assert parts == row["segments"] and widths == row["cell_widths"]
            preserved = "".join(parts) == row["text"]
            fits = all(n <= row["width"] for n in widths)
            assert row["preserved"] == preserved and row["width_ok"] == fits
            assert row["ok"] == (preserved and fits)
            if row["ok"]:
                if row["stratum"] == "control": controls += 1
                else: targets += 1
        summaries[arm] = dict(targets=targets, controls=controls,
                              errors=errors, total_rows=len(rows))
    assert summaries == data["summaries"]
    full = summaries["wrap1_cells1"]
    baseline = summaries["wrap0_cells0"]
    singles = (summaries["wrap1_cells0"], summaries["wrap0_cells1"])
    qualified = (baseline["targets"] < 11 and
                 full["targets"] == 11 and full["controls"] == 9 and
                 all(s["targets"] < 11 or s["controls"] < 9 for s in singles))
    assert data["qualified"] == qualified
    return {"verified": len(seen), "qualified": qualified,
            "sha256": digest, "summaries": summaries}

if __name__ == "__main__":
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
