#!/usr/bin/env python3
"""Trusted minimal witness: direct-name inventory misses aliased target calls."""
import ast
import builtins

source = '''
f = len
g = f
result = g([1, 2, 3])
'''
tree = ast.parse(source)
direct = [(c.lineno, c.col_offset) for c in ast.walk(tree)
          if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
          and c.func.id in {'len', 'sum'}]
aliased = [(c.lineno, c.col_offset) for c in ast.walk(tree)
           if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
           and c.func.id == 'g']
assert direct == [] and len(aliased) == 1
namespace = {'len': builtins.len}
exec(compile(tree, '<trusted_fixed_witness>', 'exec'), namespace)
assert namespace['result'] == 3
print({'direct_target_calls': len(direct), 'aliased_target_calls': len(aliased),
       'observed_result': namespace['result'], 'runtime_identity_proven': False})
