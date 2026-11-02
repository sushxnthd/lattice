"""Five real CPython imports falsify 'reference ablations prove 2-file minimality'."""
import json
import pathlib
import subprocess
import sys
import tempfile

old = 'def f(x): return x\n'
new = 'def h(x): return x + 1\n'
bridge_old = 'from core import f\ndef evaluate(x): return f(x)\n'
bridge_new = 'from core import h\ndef evaluate(x): return h(x)\n'
variants = {
    'base': (old, bridge_old),
    'reference': (new, bridge_new),
    'reference_without_core': (old, bridge_new),
    'reference_without_bridge': (new, bridge_old),
    'one_file_alternative': ('def f(x): return x + 1\n', bridge_old),
}
results = {}
with tempfile.TemporaryDirectory() as td:
    for name, (core, bridge) in variants.items():
        folder = pathlib.Path(td) / name
        folder.mkdir()
        (folder / 'core.py').write_text(core)
        (folder / 'bridge.py').write_text(bridge)
        program = ('import sys;sys.path.insert(0,sys.argv[1]);'
                   'from bridge import evaluate;print(evaluate(41))')
        p = subprocess.run([sys.executable, '-I', '-c', program, str(folder)],
                           capture_output=True, text=True, timeout=15)
        results[name] = {'returncode': p.returncode,
                         'stdout': p.stdout.strip(),
                         'error_type': 'ImportError' if 'ImportError' in p.stderr else None}
assert results['base']['stdout'] == '41'
assert results['reference']['stdout'] == '42'
assert results['one_file_alternative']['stdout'] == '42'
assert results['reference_without_core']['error_type'] == 'ImportError'
assert results['reference_without_bridge']['error_type'] == 'ImportError'
print(json.dumps(results, sort_keys=True))
