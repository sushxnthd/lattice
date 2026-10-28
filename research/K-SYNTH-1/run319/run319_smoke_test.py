"""Small deterministic regression for canonical GitHub checkout; full traces in archive."""
import ast, hashlib
from run319_decorator_compiler import compile_decorator_transaction, Action
from run315_multifile_compiler import PatchRejected, node_digest

def action(source, op, replacement=''):
    node=next(n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.FunctionDef) and n.name=='disposable')
    return Action('m.py',hashlib.sha256(source).hexdigest(),node_digest(node),type(node).__name__,node.lineno,node.col_offset,node.end_lineno,node.end_col_offset,op,replacement)

source=b'''def mark(f):
    f.tainted = True
    return f

@mark
def disposable(): return 1

def protected(): return 42
'''
allow=frozenset({'m.py'})
deleted=compile_decorator_transaction({'m.py':source},[action(source,'delete_decorated_stmt')],allowed_paths=allow)['m.py']
replaced=compile_decorator_transaction({'m.py':source},[action(source,'replace_decorated_stmt','def disposable(): return 99')],allowed_paths=allow)['m.py']
assert b'@mark\n' not in deleted and b'@mark\n' not in replaced
for out in (deleted,replaced):
    assert b'def protected(): return 42' in out
    assert ast.parse(out)
for op in ('delete_stmt','replace_stmt'):
    try:compile_decorator_transaction({'m.py':source},[action(source,op,'def disposable(): pass' if op=='replace_stmt' else '')],allowed_paths=allow)
    except PatchRejected:pass
    else:raise AssertionError('unsafe ordinary edit accepted')
print('Run319 smoke: 4/4 checks PASS')
