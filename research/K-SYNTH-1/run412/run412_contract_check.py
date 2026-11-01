#!/usr/bin/env python3
"""Run412 independent raw TLS-contract checker (no execution of untrusted code).

Usage: python run412_contract_check.py evidence_directory
The complete 3-arm raw JSON and source trees are in the Run412 SHA-verified ZIP.
"""
import hashlib
import json
from pathlib import Path
import sys

ARMS = ("baseline", "one_file_fix", "one_file_two_paths")

def verify(root: Path) -> dict:
    results = {}
    sources = {}
    for arm in ARMS:
        package = root / "sandbox" / arm / "urllib3"
        data = json.loads((root / f"run412_{arm}_raw.json").read_text())
        assert data["version"] == "2.7.0"
        assert data["total"] == len(data["cases"]) == 16
        sources[arm] = {
            str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in package.rglob("*.py")
        }
        assert len(sources[arm]) >= 20
        for name in ("connection.py", "poolmanager.py"):
            assert sources[arm][name] == data["source_sha256"][name]
        seen = set()
        false_accept = false_reject = correct = 0
        for row in data["cases"]:
            p, t, ca, host = (row[k] for k in (
                "proxy_verify", "target_verify", "ca_trusted", "proxy_host"
            ))
            key = (p, t, ca, host)
            assert key not in seen
            seen.add(key)
            assert host in ("localhost", "127.0.0.1")
            expected = (not p) or (ca and host == "localhost")
            accepted = row["status"] == 200 and row["error"] is None
            assert row["expected_accept"] == expected
            assert row["accepted"] == accepted
            assert row["correct_acceptance"] == (expected == accepted)
            if accepted:
                assert row["proxy_events"] == [{
                    "request_line": "GET https://target.invalid/run412 HTTP/1.1"
                }]
            else:
                assert row["status"] is None and row["error"]
                assert all("request_line" not in ev for ev in row["proxy_events"])
                if not expected:
                    assert "CERTIFICATE_VERIFY_FAILED" in row["error"]["message"]
            correct += (accepted == expected)
            false_accept += accepted and not expected
            false_reject += (not accepted) and expected
        assert len(seen) == 16 and correct == data["passed"]
        results[arm] = dict(correct=correct, false_accept=false_accept,
                            false_reject=false_reject)
    baseline = sources["baseline"]
    for arm in ARMS[1:]:
        assert baseline.keys() == sources[arm].keys()
        assert all(baseline[p] == sources[arm][p]
                   for p in baseline if p != "connection.py")
    assert results["baseline"] == results["one_file_fix"] == dict(
        correct=8, false_accept=3, false_reject=5
    )
    assert results["one_file_two_paths"] == dict(
        correct=16, false_accept=0, false_reject=0
    )
    return results

if __name__ == "__main__":
    print(json.dumps(verify(Path(sys.argv[1])), indent=2, sort_keys=True))
