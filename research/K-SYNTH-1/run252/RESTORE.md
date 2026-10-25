# Run252 executable restore

The two `.zlib.b64` files in this folder contain the exact locally tested source and ten regression tests. They are stored compressed to preserve transport integrity and reduce connector payload size.

From the repository root:

```bash
python - <<'PY'
import base64, zlib, hashlib, pathlib
root=pathlib.Path('research/K-SYNTH-1/run252')
for name, expected in [
    ('semantic_cfg_v2.py','51af4a1cc3d9c351acfb2afd3a4c45446d82455dea73c7442aafae67288975fe'),
    ('test_semantic_cfg_v2.py','1a37104eb7dee408c7818d006e513c59be05e048c5b662c198d31b15725fe82f'),
]:
    raw=zlib.decompress(base64.b64decode((root/(name+'.zlib.b64')).read_text().strip()))
    assert hashlib.sha256(raw).hexdigest()==expected, name
    (root/name).write_bytes(raw)
PY
cd research/K-SYNTH-1/run252
python -m unittest -v test_semantic_cfg_v2.py
```

The complete local Run252 archive includes the independent execution witness, 250-case stress harness, frozen 269-target replay, and Run251 baseline extractor. The GitHub mirror currently includes the new fixed-point implementation and its tests, not the entire 31-entry evidence archive.

**Construct validity:** bounded intraprocedural CFG and reaching definitions only. No claim of sound general Python semantics or model performance.
