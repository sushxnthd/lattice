#!/usr/bin/env python3
"""Run413 finite-grid audit. Pure read-only JSON; does not execute model code.

Usage: python run413_finite_grid_check.py baseline_connect.json baseline_identity.json
The full real-TLS oracle, independent auditor, raw traces and source roots are in
the SHA-verified Run413 reproducibility archive referenced in RUN413_RESULT.md.
"""
import itertools
import json
import sys

def verify(connect, identity):
    assert len(connect["rows"]) == connect["total"] == 16
    assert len(identity["rows"]) == identity["total"] == 4
    seen = set()
    correct = false_accept = false_reject = 0
    for r in connect["rows"]:
        k = tuple(r[x] for x in ("proxy_verify", "target_verify", "proxy_trust", "target_trust"))
        assert all(type(x) is bool for x in k)
        assert k not in seen
        seen.add(k)
        expected = (not k[0] or k[2]) and (not k[1] or k[3])
        assert r["expected_accept"] is expected
        accepted = r["status"] == 200 and any(
            e.get("request") == "GET /run413 HTTP/1.1" for e in r["origin_events"]
        )
        assert r["accepted"] is accepted
        assert r["correct"] is (accepted == expected)
        correct += accepted == expected
        false_accept += accepted and not expected
        false_reject += not accepted and expected
    assert seen == set(itertools.product((False, True), repeat=4))
    assert (correct, false_accept, false_reject) == (
        connect["correct"], connect["false_accept"], connect["false_reject"]
    )
    identity_names = {
        "control", "target_assert_hostname", "target_assert_fingerprint",
        "target_missing_client_certificate",
    }
    seen_identity = set()
    accepted_count = 0
    for r in identity["rows"]:
        assert r["case"] in identity_names and r["case"] not in seen_identity
        seen_identity.add(r["case"])
        accepted = r["status"] == 200 and any(
            e.get("request_line", "").startswith("GET https://target.invalid/run413")
            for e in r["proxy_events"]
        )
        assert r["expected_accept"] is True
        assert r["accepted"] is accepted and r["correct"] is accepted
        accepted_count += accepted
    assert seen_identity == identity_names and identity["correct"] == accepted_count
    return {"connect_correct": correct, "false_accept": false_accept,
            "false_reject": false_reject, "identity_correct": accepted_count}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: run413_finite_grid_check.py CONNECT.json IDENTITY.json")
    with open(sys.argv[1], encoding="utf8") as f:
        connect = json.load(f)
    with open(sys.argv[2], encoding="utf8") as f:
        identity = json.load(f)
    print(json.dumps(verify(connect, identity), sort_keys=True))
