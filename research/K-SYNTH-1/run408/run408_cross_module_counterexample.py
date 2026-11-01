#!/usr/bin/env python3
"""Executable closed-module counterexample: import-path facts do not fix runtime targets."""
import json,subprocess,sys,tempfile
from pathlib import Path

def run(rebind):
    with tempfile.TemporaryDirectory(prefix='lattice408_alias_') as td:
        root=Path(td)/'pkg';root.mkdir()
        (root/'__init__.py').write_text('')
        (root/'b.py').write_text('def helper(x):\n    return x * 2\n')
        (root/'a.py').write_text('from . import b\n'+('b.helper = lambda x: 123\n' if rebind else '')+'def entry(x):\n    return b.helper(x + 3)\n')
        script=f'import sys,json\nsys.path.insert(0,{td!r})\nfrom pkg.a import entry\nprint(json.dumps([entry(x) for x in range(-3,4)]))\n'
        cp=subprocess.run([sys.executable,'-I','-S','-c',script],capture_output=True,text=True,timeout=5)
        assert cp.returncode==0,cp.stderr
        return json.loads(cp.stdout)

if __name__=='__main__':
    base=run(False);mutated=run(True)
    assert base==[(x+3)*2 for x in range(-3,4)]
    assert mutated==[123]*7
    print(json.dumps({'base':base,'rebound':mutated,'different':base!=mutated},indent=2))
