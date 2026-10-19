"""Run118 exact finite multi-file import-identity counterexample."""
import json
from lattice.module_ir import ModuleGraph, Version, exact_frame

def function(name, x, y):
    return {'x': x, 'not x': not x, 'y': y, 'not y': not y}[name]

def graph(left, right, target):
    selected = 0 if target == 'left:helper' else 1
    return ModuleGraph(
        ('x', 'y'), ('left:helper', 'right:helper', 'api:serve', 'api:audit'),
        (('api', 'helper', target), ('api', 'other', 'right:helper')),
        (Version('left:helper', left, ()), Version('right:helper', right, ()),
         Version('api:serve', 'helper', (('helper', selected),)),
         Version('api:audit', 'other', (('other', 1),))),
        (('left:helper', 0), ('right:helper', 1), ('api:serve', 2), ('api:audit', 3)),
        ('api:serve', 'api:audit'))

def main():
    expressions = ('x', 'not x', 'y', 'not y')
    inputs = [(False, False), (False, True), (True, False), (True, True)]
    checks = 0
    collision_pairs = 0
    counterexamples = []
    for left in expressions:
        for right in expressions:
            g_left, g_right = graph(left, right, 'left:helper'), graph(left, right, 'right:helper')
            assert [v.source for v in g_left.versions] == [v.source for v in g_right.versions]
            assert g_left.public == g_right.public
            different = []
            for x, y in inputs:
                for target, g in (('left:helper', g_left), ('right:helper', g_right)):
                    expected = (function(left if target == 'left:helper' else right, x, y), function(right, x, y))
                    observed = tuple(g.run({'x': x, 'y': y}).values())
                    assert observed == expected
                    for lowered in (g.lower_python(), g.python_view()):
                        env = {}
                        exec(lowered, env)
                        assert env['policy'](x, y) == expected
                        checks += 1
                if g_left.run({'x': x, 'y': y}) != g_right.run({'x': x, 'y': y}):
                    different.append({'x': x, 'y': y})
            if different:
                collision_pairs += 1
                counterexamples.append({'left_source': left, 'right_source': right, 'witness': different[0]})
    g = graph('x', 'not x', 'left:helper')
    edited = g.edit({'left:helper': {'source': 'not x', 'captures': {}}}, {'left:helper'}, {})
    frame = exact_frame(g, edited, set())
    assert frame['ok']
    return {
        'status': 'EXACT_BOUNDED_SEMANTIC_COUNTEREXAMPLE',
        'model_inference': False,
        'breakthrough': False,
        'candidate_module_import_pairs': 16,
        'source_only_ambiguous_pairs': collision_pairs,
        'independent_semantics_and_python_lowering_checks': checks,
        'independent_oracle_mismatches': 0,
        'protected_public_frame': frame,
        'smallest_supported_claim': 'Unqualified local names plus source expressions do not uniquely identify cross-module captures when two modules export the same name.',
        'system_consequence': 'Stable module-qualified symbol identity, explicit import resolution, separate editable definitions/public outputs, and immutable captures are required in this bounded multi-file semantic compiler.',
        'counterexamples': counterexamples,
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
