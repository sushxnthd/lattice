"""Conditional Boolean-cardinality proof; never infers Python purity."""
import ast
import itertools

OLD = 'len([x.is_idle() for x in self._connections]) > self._max_keepalive_connections'
NEW = 'sum(x.is_idle() for x in self._connections) > self._max_keepalive_connections'
REQUIRED = ('finite','stable','pure','boolean','integer_threshold')

def classify(assumptions):
    if any(assumptions.get(k) is not True for k in REQUIRED):
        return 'UNKNOWN'
    old = ast.parse(OLD, mode='eval').body
    new = ast.parse(NEW, mode='eval').body
    assert isinstance(old.left.args[0], ast.ListComp)
    assert isinstance(new.left.args[0], ast.GeneratorExp)
    assert ast.dump(old.left.args[0].elt) == ast.dump(new.left.args[0].elt)
    assert ast.dump(old.left.args[0].generators[0]) == ast.dump(new.left.args[0].generators[0])
    assert ast.dump(old.comparators[0]) == ast.dump(new.comparators[0])
    return 'VERIFIED_CONDITIONAL'

def verify(max_n=11):
    assert classify({}) == 'UNKNOWN'
    assert classify({k: True for k in REQUIRED}) == 'VERIFIED_CONDITIONAL'
    checks = discordances = 0
    for n in range(max_n + 1):
        for bits in itertools.product((False, True), repeat=n):
            true_count = sum(bits)
            for k in range(-1, n + 2):
                original = len([v for v in bits]) > k
                corrected = sum(v for v in bits) > k
                predicted = true_count <= k < n
                assert (original != corrected) == predicted
                assert not (corrected and not original)
                checks += 1
                discordances += predicted
    assert (len([2, 2]) > 3) is False and (sum([2, 2]) > 3) is True
    return {'evaluations': checks, 'discordances': discordances, 'mismatches': 0,
            'non_boolean_counterexample': [2, 2], 'scope': 'conditional_only'}

if __name__ == '__main__':
    import json
    print(json.dumps(verify(), sort_keys=True))
