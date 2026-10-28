#!/usr/bin/env python3
"""Independent read-only audit of the original Run325 v3 GitHub Actions ZIP."""
import hashlib, json, pathlib, sys, zipfile
archive = pathlib.Path(sys.argv[1])
sha = lambda b: hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(archive) as z:
    names = z.namelist()
    assert len(names) == len(set(names))
    data = {name: z.read(name) for name in names}
manifest = json.loads(data["SHA256_MANIFEST.json"])
assert set(manifest) == set(data) - {"SHA256_MANIFEST.json"}
assert all(sha(data[n]) == digest for n, digest in manifest.items())
base = json.loads(data["oracle_BASE.json"])
ref = json.loads(data["oracle_REFERENCE.json"])
qualification = json.loads(data["qualification.json"])
assert qualification["oracle_qualified"] is True
assert qualification["base"] == base and qualification["reference"] == ref
names = ["explicit_pool_port_zero", "url_pool_port_zero", "url_object_port_zero", "missing_pool_port", "explicit_pool_port_80", "explicit_pool_port_8080", "https_default_port", "url_parse_zero", "url_without_port"]
for arm in (base, ref):
    assert [row["name"] for row in arm["rows"]] == names
    assert [row["kind"] for row in arm["rows"]] == ["target"] * 3 + ["control"] * 6
    assert arm["targets"] == sum(row["passed"] for row in arm["rows"][:3])
    assert arm["controls"] == sum(row["passed"] for row in arm["rows"][3:])
    assert arm["all_pass"] == all(row["passed"] for row in arm["rows"])
    assert all(row["error"] is None for row in arm["rows"])
assert [row["passed"] for row in base["rows"]] == [False, False, True] + [True] * 6
assert all(row["passed"] for row in ref["rows"])
assert data["upstream_commits.txt"].decode().splitlines() == ["f4e4bc31f40f8c94c6a1f1685df28f97ff48c305", "8b6b36f57e139755356074908abbcb0b07732d6d"]
shim = data["bootstrap_sha256.txt"].decode().splitlines()
assert len(shim) == 2 and shim[0].split()[0] == shim[1].split()[0]
assert data["oracle_BASE.stderr"] == data["oracle_REFERENCE.stderr"] == b""
print(json.dumps({"original_zip_sha256": sha(archive.read_bytes()), "manifest_verified": len(manifest), "base_targets": base["targets"], "base_controls": base["controls"], "reference_targets": ref["targets"], "reference_controls": ref["controls"], "audited_rows": 18, "discrepancies": 0}, sort_keys=True))
