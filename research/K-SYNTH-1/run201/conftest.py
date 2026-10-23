"""Restore the pinned Run200 compiler for Run201 research regression tests."""
import base64
import sys
import types
import zlib
from pathlib import Path

source_file = Path(__file__).parents[1] / 'run200' / 'multifile_editor.py.zlib.b64'
module = types.ModuleType('multifile_editor')
module.__file__ = str(source_file)
sys.modules[module.__name__] = module
source = zlib.decompress(base64.b64decode(source_file.read_text())).decode('utf-8')
exec(compile(source, str(source_file), 'exec'), module.__dict__)
