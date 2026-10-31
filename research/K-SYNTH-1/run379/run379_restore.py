"""Restore the exact tested Run379 AST-span editor from its SHA-verified payload.

The complete 22-payload reproducibility ZIP (including raw stress traces, independent
auditor and tests) is distributed separately; this restores only the core editor.
"""
import base64
import hashlib
import pathlib
import zlib

ROOT = pathlib.Path(__file__).resolve().parent
encoded = (ROOT / "run379_atomic_ast_editor.py.zlib.b64").read_text().strip()
source = zlib.decompress(base64.b64decode(encoded, validate=True))
expected = "a2c6228f46dd5f570ad2eeec4057e0e9f6b713f9eb4c7289c6ecd6146af2c46c"
assert hashlib.sha256(source).hexdigest() == expected, "source SHA mismatch"
out = ROOT / "run379_atomic_ast_editor.py"
if out.exists():
    assert out.read_bytes() == source, "refusing to overwrite different source"
else:
    out.write_bytes(source)
print("SHA-256 verified:", expected)
