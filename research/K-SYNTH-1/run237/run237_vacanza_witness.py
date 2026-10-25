#!/usr/bin/env python3
"""Pinned-source necessary-condition witness; not a full issue-level oracle."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ISSUE = 'vacanza__holidays-2197'
PATH = 'holidays/calendars/custom.py'
ARMS = ('semantic_ir_json', 'python_annotated')

def read(path):
    return json.loads(Path(path).read_text())

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def run_class_witness(source):
    tree = ast.parse(source)
    if not all(isinstance(n, ast.ClassDef) for n in tree.body):
        raise ValueError('unexpected top-level source; refusing execution')
    forbidden = (ast.Import, ast.ImportFrom, ast.Lambda, ast.With, ast.Try,
                 ast.Raise, ast.Global, ast.Nonlocal, ast.Await, ast.Yield)
    if any(isinstance(n, forbidden) for n in ast.walk(tree)):
        raise ValueError('unsafe source; refusing execution')
    harness = '''import json,sys
ns={'__name__':'lattice_witness'}
try:
    exec(compile(sys.stdin.read(),'<pinned>','exec'),ns)
    exec('class Child(_CustomCalendar):\\n    public = 7\\n',ns)
    obj=ns['Child']()
    assert type(obj).__name__=='Child'
    assert ns['Child'].public_CUSTOM_CALENDAR==7
    print(json.dumps({'passes':True,'renamed_attribute':7}))
except Exception as exc:
    print(json.dumps({'passes':False,'exception':type(exc).__name__,'message':str(exc)}))
'''
    process = subprocess.run([sys.executable, '-I', '-S', '-c', harness],
                             input=source, text=True, capture_output=True,
                             check=True, timeout=5)
    return json.loads(process.stdout)

def check(root):
    root = Path(root)
    assert read(root / 'freeze.json')['issue'] == ISSUE
    facts = read(root / 'facts.json')[PATH]
    old = next(t['old_text'] for t in facts['targets'] if t['kind']=='File')
    assert sha(old) == facts['file_sha256']
    baseline = run_class_witness(old)
    assert baseline['passes'], 'baseline control must pass'
    results = {'original_sha256': sha(old), 'baseline': baseline, 'arms': {}}
    for arm in ARMS:
        stem = root / 'raw' / (ISSUE + '-' + arm)
        record = read(str(stem) + '-verifier.json')
        assert record['accepted']
        after = read(str(stem) + '-after.json')[PATH]
        assert sha(after) == record['after'][PATH]
        names = [n.name for n in ast.parse(after).body if isinstance(n, ast.ClassDef)]
        observed = run_class_witness(after) if arm == 'python_annotated' else {
            'passes': False, 'exception': 'MissingClass' if '_CustomCalendar' not in names else 'UnexpectedClass'}
        results['arms'][arm] = {'after_sha256': sha(after), 'top_level_classes': names, **observed}
    assert all(not result['passes'] for result in results['arms'].values())
    return results

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: run237_vacanza_witness.py <extracted-run234-repo11-artifact>')
    print(json.dumps(check(sys.argv[1]), indent=2))
