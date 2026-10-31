"""Run395: genuine two-module CPython witnesses, no untrusted model code."""
import json
import pathlib
import subprocess
import sys
import tempfile


def execute(a, b):
    with tempfile.TemporaryDirectory() as td:
        pathlib.Path(td, 'a.py').write_text(a)
        pathlib.Path(td, 'b.py').write_text(b)
        script = (f'import sys;sys.path.insert(0,{td!r});'
                  'from b import compute;print(json.dumps([compute(1),compute(99)]))')
        script = 'import json;' + script
        p = subprocess.run([sys.executable, '-I', '-S', '-c', script],
                           cwd=td, capture_output=True, text=True, timeout=5)
        if p.returncode:
            return {'status': 'ABORT', 'stderr': p.stderr[-250:]}
        return {'status': 'EXECUTED', 'values': json.loads(p.stdout)}


def main():
    a0 = 'def adjust(x): return x\n'
    a1 = 'def adjust(x): return x + (5 if x == 99 else 0)\n'
    b1 = 'from a import adjust\ndef compute(x): return adjust(x) + 3\n'
    invisible = execute(a0, b1)
    hidden = execute(a1, b1)
    assert invisible['values'][0] == hidden['values'][0] == 4
    assert invisible['values'][1] == 102 and hidden['values'][1] == 107
    base_a = 'def noop(): return 0\n'
    ref_a = 'TOKEN = 5\ndef noop(): return 0\n'
    ref_b = 'from a import TOKEN\ndef compute(x): return x + TOKEN\n'
    mechanical_abort = execute(base_a, ref_b)
    full = execute(ref_a, ref_b)
    shim = execute(base_a + 'TOKEN = 5\n', ref_b)
    assert mechanical_abort['status'] == 'ABORT'
    assert full == shim == {'status': 'EXECUTED', 'values': [6, 104]}
    print(json.dumps({'out_of_domain': {'frozen_view': invisible,
                                       'reference_view': hidden},
                      'mechanical': {'ablation': mechanical_abort,
                                     'full': full, 'shim': shim}}, sort_keys=True))


if __name__ == '__main__':
    main()
