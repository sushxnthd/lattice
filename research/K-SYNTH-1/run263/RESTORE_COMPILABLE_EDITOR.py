#!/usr/bin/env python3
"""Restore Run263 compiler-validating editor from the SHA-pinned Run261 v2 source."""
import base64, hashlib, pathlib, zlib

source = pathlib.Path("research/K-SYNTH-1/run261/atomic_span_editor_v2.py.zlib.b64")
raw = zlib.decompress(base64.b64decode(source.read_text().strip()))
assert hashlib.sha256(raw).hexdigest() == "9eea3daebc3bc9aa80b09ccce92e21db54481664150054b6a6245e6bf9d0c1b8"
text = raw.decode()
text = text.replace(
    '"""Lattice K-SYNTH-1 Run261 (hardened Run260): fail-closed, atomic byte-span editing core.',
    '"""Lattice K-SYNTH-1 Run263: compilability-checked atomic byte-span editor.',
).replace(
    "* no edit can commit if any file fails AST syntax validation;",
    "* no edit can commit if any file fails CPython compile-time validation;",
)
old = """        try:
            ast.parse(b.decode('utf-8'), filename=p)
        except (UnicodeError,SyntaxError) as exc:
            raise ValueError('edited Python is invalid') from exc"""
new = """        try:
            # ast.parse accepts code that Python cannot compile, e.g. module-level
            # return/break/continue, duplicate arguments and illegal nonlocal.
            # compile() validates CPython compile-time restrictions without running code.
            compile(b.decode('utf-8'), p, 'exec', dont_inherit=True)
        except (UnicodeError, SyntaxError, ValueError, OverflowError) as exc:
            raise ValueError('edited Python is not compilable') from exc"""
assert text.count(old) == 1
text = text.replace(old, new)
assert hashlib.sha256(text.encode()).hexdigest() == "987785d5ffcbb2386a4af9bb71aa808db10140124b24ad84a6d8f62ad6a126bb"
pathlib.Path("atomic_span_editor_v3.py").write_text(text)
print("RESTORED_SHA256", hashlib.sha256(text.encode()).hexdigest())
