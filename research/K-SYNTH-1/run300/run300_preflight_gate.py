#!/usr/bin/env python3
"""Fail-closed paired compiler contract gate. Run BEFORE model inference.

Usage: gate.py TRUSTED_COMPILER.py SOURCE_ROOT IR_EXAMPLE.json PYTHON_EXAMPLE.json
Never use this to retroactively reclassify historical model outcomes.
"""
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

def load_trusted_compiler(path):
    spec = importlib.util.spec_from_file_location('ksynth_trusted_compiler', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load trusted compiler')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def gate(compiler_path, root, ir_file, python_file):
    compiler = load_trusted_compiler(compiler_path)
    raw_ir = Path(ir_file).read_text()
    raw_python = Path(python_file).read_text()
    canonical_ir = compiler.canonicalize(raw_ir)
    canonical_python = compiler.canonicalize(raw_python)
    if canonical_ir != canonical_python:
        raise AssertionError('NON_EQUIVALENT_CANONICAL_TRANSACTIONS')
    before = {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in Path(root).rglob('*') if p.is_file()}
    with tempfile.TemporaryDirectory(prefix='ksynth-contract-gate-') as tmp:
        stages = [compiler.compile_to_isolated_stage(root, raw, tmp)
                  for raw in (raw_ir,raw_python)]
    after = {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
             for p in Path(root).rglob('*') if p.is_file()}
    if before != after:
        raise AssertionError('SOURCE_MUTATION')
    if stages[0]['canonical_sha256'] != stages[1]['canonical_sha256'] or stages[0]['files'] != stages[1]['files']:
        raise AssertionError('STAGE_PARITY')
    return {'gate':'PASS','canonical_sha256':stages[0]['canonical_sha256'],
            'staged_files':stages[0]['files'],'original_files_unchanged':True}

if __name__=='__main__':
    if len(sys.argv)!=5:
        raise SystemExit('usage: gate.py TRUSTED_COMPILER.py SOURCE_ROOT IR_EXAMPLE.json PYTHON_EXAMPLE.json')
    print(json.dumps(gate(*sys.argv[1:]),sort_keys=True))
