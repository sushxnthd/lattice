#!/usr/bin/env python3
"""Independent functional necessary-condition witness for genuine Run234 pipx IR edit.

Reconstructs original pinned source by reversing model patch, verifies SHA,
executes only the target function with mocked external launcher, and checks
whether --python python3.11 and --python 3.11 are normalized equivalently.
"""
import ast
import hashlib
import json
import pathlib
import subprocess
import tempfile
import types
import typing


def check(root):
    root = pathlib.Path(root)
    issue = 'pypa__pipx-1186'
    arm = 'semantic_ir_json'
    stem = root/'raw'/f'{issue}-{arm}'
    rec = json.loads(pathlib.Path(str(stem)+'-verifier.json').read_text())
    after = json.loads(pathlib.Path(str(stem)+'-after.json').read_text())
    patch = pathlib.Path(str(stem)+'-patch.diff').read_text()
    with tempfile.TemporaryDirectory() as d:
        base = pathlib.Path(d)
        for path,src in after.items():
            f = base/path
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_text(src)
        subprocess.run(['git','apply','--reverse','-'],cwd=base,
                       input=patch,text=True,capture_output=True,check=True)
        before = {path:(base/path).read_text() for path in after}
    for path,src in before.items():
        assert hashlib.sha256(src.encode()).hexdigest() == rec['before'][path]
    path = 'src/pipx/interpreter.py'

    def exercise(source,version):
        fn = next(n for n in ast.parse(source).body
                  if isinstance(n,ast.FunctionDef) and n.name=='find_py_launcher_python')
        calls = []
        def fake_run(argv,**kwargs):
            calls.append(argv)
            return types.SimpleNamespace(stdout='/usr/bin/python3.11\n')
        ns = {'Optional':typing.Optional,
              'shutil':types.SimpleNamespace(which=lambda name:'/usr/bin/py'),
              'subprocess':types.SimpleNamespace(run=fake_run)}
        module = ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]))
        exec(compile(module,'<isolated-pipx>','exec'),ns)
        value = ns['find_py_launcher_python'](version)
        return {'returned':value,'argv':calls[0]}

    outcome = {label:{v:exercise(src,v) for v in ('3.11','python3.11')}
               for label,src in [('baseline',before[path]),('model_edit',after[path])]}
    outcome['behavior_unchanged'] = outcome['baseline'] == outcome['model_edit']
    outcome['python_name_normalized'] = (outcome['model_edit']['3.11']['argv'] ==
                                          outcome['model_edit']['python3.11']['argv'])
    return outcome


if __name__ == '__main__':
    import sys
    print(json.dumps(check(sys.argv[1]),indent=2,sort_keys=True))
