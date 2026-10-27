#!/usr/bin/env python3
"""Run287 independent audit of original Run285 Actions artifact, no code execution."""
import hashlib, json, pathlib, sys, zipfile

ARTIFACT_SHA = "8486f65cf7731a73a08a6a09c190ef5b39fbcfd6cfe09ea09279ef5090b215c7"
FROZEN_SHA = "811e33423dc734ab5d0fbe72de4e9c5277b68bed86315b9e7373c01b157be571"
ARMS = {"baseline", "sync_only", "async_only", "full_reference"}

def sha(data): return hashlib.sha256(data).hexdigest()

def audit(artifact, frozen_path):
    artifact = pathlib.Path(artifact)
    frozen_path = pathlib.Path(frozen_path)
    assert sha(artifact.read_bytes()) == ARTIFACT_SHA
    assert sha(frozen_path.read_bytes()) == FROZEN_SHA
    freeze = json.loads(frozen_path.read_text())
    assert freeze["status"] == "FROZEN_BEFORE_ORACLE"
    cases = {c["id"]: c for c in freeze["cases"]}
    assert len(cases) == 30
    assert set(freeze["expected"]) == ARMS
    with zipfile.ZipFile(artifact) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == 4
        manifest = z.read("ARTIFACT_SHA256SUMS").decode().splitlines()
        verified = []
        for entry in manifest:
            digest, name = entry.split("  ", 1)
            assert name in names and sha(z.read(name)) == digest
            verified.append(name)
        assert len(verified) == 3
        raw = json.loads(z.read("raw_results.json"))
        commitment = z.read("FROZEN_RUN285_COMMITMENT.md").decode()
    assert FROZEN_SHA in commitment
    assert raw["frozen_local_json_sha256"] == FROZEN_SHA
    assert raw["cases"] == freeze["cases"]
    assert raw["source_sha256"] == {
        p: [v["base"], v["ref"]] for p, v in freeze["source_sha256"].items()
    }
    assert len(raw["records"]) == 4
    assert {r["arm"] for r in raw["records"]} == ARMS
    censored, mismatches, n = [], [], 0
    for record in raw["records"]:
        arm = record["arm"]
        if record["returncode"] != 0 or len(record["rows"]) != 30:
            censored.append([arm, "missing/nonzero"]); continue
        seen = set()
        for row in record["rows"]:
            key = row["id"]
            if key in seen or key not in cases or row["error"] is not None:
                censored.append([arm, key]); continue
            seen.add(key)
            actual = row["observation"]
            if not isinstance(actual, dict) or set(actual) != {"before", "during"}:
                censored.append([arm, key]); continue
            if any(type(v) is not int for v in actual.values()):
                censored.append([arm, key]); continue
            n += 1
            expected = freeze["expected"][arm][key]
            if actual != expected:
                mismatches.append([arm, key, expected, actual])
        if seen != set(cases): censored.append([arm, "incomplete"])
    assert n == 120 and not censored and not mismatches
    return {"schema": "lattice-run287-original-artifact-audit-v1",
            "artifact_sha256": ARTIFACT_SHA, "frozen_sha256": FROZEN_SHA,
            "manifest_entries_verified": 3, "functional_observations": n,
            "censored": censored, "mismatches": mismatches,
            "independent_source_bytes_rehashed": False,
            "new_independent_issue": False, "model_repair": False}

if __name__ == "__main__":
    print(json.dumps(audit(sys.argv[1], sys.argv[2]), indent=2, sort_keys=True))
