#!/usr/bin/env python3
"""Exact finite-grid Boolean mechanism for the Run412 TLS forwarding experiment."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
for arm in ("baseline", "one_file_fix", "one_file_two_paths"):
    data = json.loads((root / f"run412_{arm}_raw.json").read_text())
    table = {
        (r["proxy_verify"], r["target_verify"], r["ca_trusted"],
         r["proxy_host"] == "localhost"): r["accepted"]
        for r in data["cases"]
    }
    assert len(table) == 16
    if arm == "one_file_two_paths":
        expected = lambda p, t, ca, host: (not p) or (ca and host)
    else:
        expected = lambda p, t, ca, host: not t
    assert all(observed == expected(*key) for key, observed in table.items())
    target_contrasts = []
    for key in table:
        if key[1]:
            continue
        alternate = (key[0], True, key[2], key[3])
        target_contrasts.append(int(table[alternate]) - int(table[key]))
    assert len(target_contrasts) == 8
    print(json.dumps({
        "arm": arm, "exact_grid": 16,
        "target_verify_negative_contrasts": target_contrasts.count(-1),
        "target_verify_zero_contrasts": target_contrasts.count(0),
        "target_verify_positive_contrasts": target_contrasts.count(1)
    }, sort_keys=True))
