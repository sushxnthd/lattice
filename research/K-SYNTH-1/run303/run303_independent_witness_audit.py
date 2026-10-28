#!/usr/bin/env python3
"""Run303 independent replay. Never executes the model-generated candidate.

Inputs: original_run301_artifact.zip, original Run302 trusted-source ZIP,
both downloaded Run302 cloud witness ZIPs. Runs only the SHA-pinned trusted
upstream source locally; candidate outcomes are READ from original cloud JSON.
"""
import hashlib, json, subprocess, sys, tempfile, zipfile
from pathlib import Path

sha = lambda b: hashlib.sha256(b).hexdigest()
ORIGINAL = "d8feadc2c2328f76c1aaf4548871b490d2ded4abd3817d1848fe7345726a672a"
FAILED = "121ef6693d189d66fbc5ba996beec66dd97d568a185f6eb889cd40830d1e0fe6"
CORRECTED = "8b987a111822b9774bec9b191924d1c44d4b1971239480ff95fd7293ea90e7d8"
TRUSTED_READER = "05c760d59ecfb456d30075c053e2a65559d7c3260f7902339949f98dd6f18777"
MODEL_READER = "f1cec1f102fecd29a459a077b294ae5ace2f998200e42a78926051e20f38232e"

def checked_zip(path, expected):
    data = Path(path).read_bytes()
    assert sha(data) == expected, path
    z = zipfile.ZipFile(path)
    assert z.testzip() is None
    return z

def manifest(z):
    records = z.read("SHA256_MANIFEST.txt").decode().splitlines()
    for row in records:
        digest, name = row.split(maxsplit=1)
        assert sha(z.read(name.strip().lstrip("*"))) == digest
    return len(records)

PROBE = r'''
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import h11
assert Path(h11.__file__).resolve().is_relative_to(Path(sys.argv[1]).resolve())
cases = {
"CRLF_VALID": b"GET / HTTP/1.1\r\nHost: x\r\n\r\n",
"LF_ONLY": b"GET / HTTP/1.1\nHost: x\n\n",
"EXTRA_LF_REQUEST": b"GET / HTTP/1.1\n\r\nHost: x\r\n\r\n",
"EXTRA_CR_REQUEST": b"GET / HTTP/1.1\r\r\nHost: x\r\n\r\n",
"EXTRA_LF_HEADER": b"GET / HTTP/1.1\r\nHost: x\n\r\n\r\n",
"CRLF_EXTRA_VALID": b"GET / HTTP/1.1\r\nHost: x\r\nX-Tag: yes\r\n\r\n",
}
rows = []
for name, raw in cases.items():
    modes = {"whole": [raw],
             "split": [raw[:len(raw)//2], raw[len(raw)//2:]],
             "bytewise": [bytes([b]) for b in raw]}
    for mode, chunks in modes.items():
        conn = h11.Connection(h11.SERVER)
        events, error = [], None
        try:
            for chunk in chunks:
                conn.receive_data(chunk)
                for _ in range(10):
                    event = conn.next_event()
                    if event is h11.NEED_DATA or event is h11.PAUSED: break
                    events.append(type(event).__name__)
        except Exception as exc:
            error = type(exc).__name__
        rows.append({"case": name, "fragmentation": mode,
                     "events": events, "error": error,
                     "success": "Request" in events and
                     "EndOfMessage" in events and error is None})
print(json.dumps({"rows": rows}, sort_keys=True))
'''

def audit(original_path, trusted_zip_path, failed_path, corrected_path):
    original = checked_zip(original_path, ORIGINAL)
    trusted = zipfile.ZipFile(trusted_zip_path)
    failed = checked_zip(failed_path, FAILED)
    corrected = checked_zip(corrected_path, CORRECTED)
    originals = json.loads(original.read("SHA256_MANIFEST.json"))
    assert len(originals) == 84
    for name, digest in originals.items():
        assert sha(original.read(name)) == digest
    assert manifest(failed) == 1 and manifest(corrected) == 4
    assert failed.read("candidate_readers_sha.txt") == b""
    assert corrected.read("original_zip_sha.txt").decode().split()[0] == ORIGINAL
    assert corrected.read("candidate_readers_sha.txt").decode().split()[0] == MODEL_READER
    reader = trusted.read("trusted/h11/_readers.py")
    assert sha(reader) == TRUSTED_READER
    prefix = "stages/PYTHON_AST-python/ksynth1-stage-3vc0971q/h11/"
    assert sha(original.read(prefix + "_readers.py")) == MODEL_READER
    with tempfile.TemporaryDirectory(prefix="run303-trusted-") as tmp:
        root = Path(tmp)
        for name in original.namelist():
            if name.startswith(prefix) and name.endswith(".py"):
                rel = name[len(prefix):]
                if rel.startswith("tests/"): continue
                path = root / "h11" / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(reader if rel == "_readers.py" else original.read(name))
        assert sha((root/"h11"/"_readers.py").read_bytes()) == TRUSTED_READER
        process = subprocess.run([sys.executable, "-I", "-c", PROBE, str(root)],
                                 capture_output=True, text=True, check=True, timeout=30)
        baseline = json.loads(process.stdout)
    candidate = json.loads(corrected.read("candidate_probe.json"))
    assert candidate["import_path"] == "/candidate/h11/__init__.py"
    key = lambda row: (row["case"], row["fragmentation"])
    b = {key(row): row for row in baseline["rows"]}
    c = {key(row): row for row in candidate["rows"]}
    assert len(b) == len(c) == 18 and set(b) == set(c)
    fields = ("events", "error", "success")
    differences = [k for k in b if any(b[k][f] != c[k][f] for f in fields)]
    assert len(differences) == 3
    assert all(k[0] == "EXTRA_LF_REQUEST" and not b[k]["success"]
               and c[k]["success"] for k in differences)
    return {"trusted_cases": 18, "candidate_cases": 18,
            "differential_cases": len(differences),
            "trusted_successes": sum(r["success"] for r in b.values()),
            "candidate_successes": sum(r["success"] for r in c.values()),
            "differential_keys": sorted(differences),
            "model_candidate_executed_on_host": False}

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("usage: audit.py original_run301.zip run302_trusted.zip failed_witness.zip corrected_witness.zip")
    print(json.dumps(audit(*sys.argv[1:]), indent=2))
