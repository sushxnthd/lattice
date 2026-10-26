# Run260 atomic editor restoration
The source is stored as zlib-compressed Base64 text in `atomic_span_editor.py.zlib.b64`. Restore with:
```python
from pathlib import Path
import base64,zlib,hashlib
p=Path("research/K-SYNTH-1/run260/atomic_span_editor.py.zlib.b64")
src=zlib.decompress(base64.b64decode(p.read_text().strip()))
assert hashlib.sha256(src).hexdigest()=="3d095f4efedd834611a0e07cc05911c6d442ac26eff81075efd3612a8a98f514"
Path("atomic_span_editor.py").write_bytes(src)
```
The complete 32-entry SHA256-verified local archive `/mnt/data/lattice_run260/lattice_run260_model_audit_atomic_editor.zip` (SHA256 `ddfdc046d3a189fbf5c9566f4f2eb7e4dbf82787a9a13548ab57b9017bb59202`) includes 16 passing unit tests, 512 rejected adversarial mutation trials, full independent cloud audit, original raw Qwen ZIP, and pinned Flask reference source. Test files and complete ZIP are not yet mirrored to GitHub. This is a prototype, not a general semantic IR or security proof.