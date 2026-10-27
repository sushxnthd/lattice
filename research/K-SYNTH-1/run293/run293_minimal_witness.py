#!/usr/bin/env python3
"""Executable counterexample: a Boolean expression preserves a callable alias.
Trusted fixture only; does not infer runtime identity from source in general.
"""
import ast
import json
src = "f = len\ng = f or sum\nresult = g([1, 2, 3])\n"
tree = ast.parse(src)
assign = tree.body[1]
assert isinstance(assign, ast.Assign)
assert isinstance(assign.value, ast.BoolOp)
# The prior transfer returned an empty, non-UNKNOWN candidate set for BoolOp.
prior_candidates = []
prior_unknown = False
log = []
def tracked_len(xs):
    log.append('len')
    return len(xs)
def tracked_sum(xs):
    log.append('sum')
    return sum(xs)
ns = {'len': tracked_len, 'sum': tracked_sum}
exec(compile(src, '<trusted_run293_witness>', 'exec'), ns)
assert ns['result'] == 3 and log == ['len']
assert not prior_candidates and not prior_unknown
print(json.dumps({'source': src, 'old_candidates': prior_candidates,
                  'old_unknown': prior_unknown, 'observed_calls': log,
                  'result': ns['result'], 'false_negative': True}, sort_keys=True))
