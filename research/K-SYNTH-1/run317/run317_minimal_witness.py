"""Standalone trusted decorator reattachment witness; never executes model code."""
import ast
import hashlib
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'run315'))
sys.path.insert(0, str(HERE.parent / 'run316'))
sys.path.insert(0, str(HERE))
from run315_multifile_compiler import PatchRejected, node_digest
from run316_structural_compiler import Action as OldAction, compile_structural as old
from run317_structural_compiler import Action as NewAction, compile_structural as corrected

source = b'''def marker(fn):
    fn.tainted = True
    return fn

@marker
def disposable():
    return 1

def protected():
    return 42
'''
node = next(n for n in ast.walk(ast.parse(source))
            if isinstance(n, ast.FunctionDef) and n.name == 'disposable')
args = ('mod.py', hashlib.sha256(source).hexdigest(), node_digest(node),
        type(node).__name__, node.lineno, node.col_offset,
        node.end_lineno, node.end_col_offset, 'delete_stmt')
patch = old({'mod.py': source}, [OldAction(*args)], allowed_paths=frozenset({'mod.py'}))['mod.py']
original_scope = {}; exec(source, original_scope)
patched_scope = {}; exec(patch, patched_scope)
assert original_scope['protected']() == patched_scope['protected']() == 42
assert not hasattr(original_scope['protected'], 'tainted')
assert patched_scope['protected'].tainted is True
try:
    corrected({'mod.py': source}, [NewAction(*args)], allowed_paths=frozenset({'mod.py'}))
except PatchRejected as exc:
    assert 'decorated statement' in str(exc)
else:
    raise AssertionError('corrected compiler accepted orphaned decorator')
print('REPRODUCED: old accepted and silently tainted protected; corrected rejected')
