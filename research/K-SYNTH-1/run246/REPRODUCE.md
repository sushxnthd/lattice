# Run246 reproducibility and persistence

Full run-local archive: `lattice_run246_original_span_science.zip`, SHA-256 `6a9539a2fc297b572fb8607bb97b952b1086afb170c8d0ac8d1d96174e502253`. The archive contains 269-target audit rows, immutable Run237 and Run242 source archives, v1/v2/v3 source, independent auditor, 38 regression tests and checksums. The complete archive is **not mirrored to GitHub**.

The v3 source is also stored in this branch as `typed_representation_v3.py.zlib.b64`, a UTF-8 text file containing zlib-compressed Python source encoded in base64. Its Git blob SHA is `59b38f3dd7cd84ff8f3f888e0ca1edc551e19d9f`. Decode with:

```bash
python - <<'PY'
from pathlib import Path
import base64, zlib, hashlib
p=Path('typed_representation_v3.py.zlib.b64')
raw=zlib.decompress(base64.b64decode(p.read_text().strip()))
assert hashlib.sha256(raw).hexdigest()=='d259f5a8eeda32209d217dcc6d8ab5572ca422b7c344e916f0eb05cb2dc21eb2'
Path('typed_representation_v3.py').write_bytes(raw)
PY
```

The v3 module imports `typed_representation.py` and `typed_representation_v2.py` from the complete local archive; those dependencies and the independent test/audit sources have not yet been mirrored here. Do not claim this GitHub directory alone is sufficient to reproduce the audit. The local archive is the authoritative complete evidence until mirroring succeeds.

The Run247 protocol requires a *new capable-model functional comparison*, not another representation-only audit.