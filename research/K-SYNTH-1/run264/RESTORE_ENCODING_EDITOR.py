#!/usr/bin/env python3
"""Restore Run264 encoding-coherent editor from immutable Run263 v3, with SHA verification."""
from pathlib import Path
import runpy,hashlib
runpy.run_path("research/K-SYNTH-1/run263/RESTORE_COMPILABLE_EDITOR.py",run_name="__main__")
p=Path("atomic_span_editor_v3.py")
s=p.read_text()
assert hashlib.sha256(s.encode()).hexdigest()=="987785d5ffcbb2386a4af9bb71aa808db10140124b24ad84a6d8f62ad6a126bb"
s=s.replace('"""Lattice K-SYNTH-1 Run263: compilability-checked atomic byte-span editor.', '"""Lattice K-SYNTH-1 Run264: encoding-coherent compilability-checked atomic editor.')
s=s.replace('import json\n','import json\nimport io\nimport tokenize\n')
marker='\ndef apply_transaction(raw: str, originals: Mapping[str, bytes], authorized: set[str]):'
assert s.count(marker)==1
helper='''\ndef require_utf8_source(source: bytes, path: str) -> None:
    """Fail closed when CPython's source-file decoding differs from UTF-8.

    The edit language uses UTF-8 codepoint boundaries, so a latin-1 coding
    cookie makes compile(text) and actual compile(source_bytes) disagree.
    Source files with non-UTF8 declared encoding are outside this editor's
    explicitly supported language, even if their bytes happen to be UTF-8.
    """
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(source).readline)
        # Canonical Python tokenizer values for UTF-8 and UTF-8 BOM.
        if encoding.lower().replace('_', '-') not in ('utf-8', 'utf-8-sig'):
            raise ValueError('unsupported source encoding: ' + encoding)
        source.decode('utf-8-sig')
        # Byte-mode compile is what CPython uses for source files. It checks
        # coding cookies, BOM, parser restrictions, and code-object validity.
        compile(source, path, 'exec', dont_inherit=True)
    except (SyntaxError, UnicodeError, LookupError, OverflowError) as exc:
        raise ValueError('invalid UTF-8 Python source') from exc

'''
s=s.replace(marker,'\n'+helper+marker)
s=s.replace("        b.decode('utf-8')\n", "        require_utf8_source(b, p)\n")
old="""        try:
            # ast.parse accepts code that Python cannot compile, e.g. module-level
            # return/break/continue, duplicate arguments and illegal nonlocal.
            # compile() validates CPython compile-time restrictions without running code.
            compile(b.decode('utf-8'), p, 'exec', dont_inherit=True)
        except (UnicodeError, SyntaxError, ValueError, OverflowError) as exc:
            raise ValueError('edited Python is not compilable') from exc
"""
new="""        # Preserve the exact source-file decoding and compile-time semantics.
        # This rejects non-UTF8 coding cookies even if the raw bytes are UTF-8.
        require_utf8_source(b, p)
"""
assert s.count(old)==1
s=s.replace(old,new)
assert hashlib.sha256(s.encode()).hexdigest()=="6244f0ce779c5bda0d7c062343f44844a9c1ee7cb1550c0c76fb06d75a31b229"
Path("atomic_span_editor_v4.py").write_text(s)
print("RESTORED_SHA256",hashlib.sha256(s.encode()).hexdigest())
