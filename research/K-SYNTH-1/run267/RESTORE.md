# Run267 v3 provenance restorer

`bounded_provenance_ir_v3.py.zlib.b64` contains zlib-compressed, base64-encoded UTF-8 Python source. Restore with:

```python
import base64, hashlib, pathlib, zlib
src=zlib.decompress(base64.b64decode(pathlib.Path('bounded_provenance_ir_v3.py.zlib.b64').read_text().strip()))
assert hashlib.sha256(src).hexdigest()=='98fe3ed68113c44be5eba5c81834f2b46bc627fa460beec6bdb0fb1e8bb86874'
pathlib.Path('bounded_provenance_ir_v3.py').write_bytes(src)
```

The module requires the SHA-pinned Run266 `bounded_provenance_ir_v2.py` and its Run265/264 editor/index dependencies; those complete files and Run267 tests/raw witnesses remain in the SHA-verified local ZIP. The GitHub copy alone is **not** yet a standalone reproduction. The Run265 frozen prompts are immutable and cannot establish a semantic-IR-versus-Python causal effect because both arms share the same semantic graph facts. See RUN267_RESULT.md and PROTOCOL_RUN268.md.
