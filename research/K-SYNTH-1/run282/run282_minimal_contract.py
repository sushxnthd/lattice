"""Run282 minimal independently executable interval-certificate checker.

Only valid for finite stable pure Boolean-returning predicates and integer k.
It does not infer those assumptions from Python source.
"""
from itertools import product

ASSUMPTIONS = ('finite', 'stable', 'pure', 'boolean_return', 'integer_threshold')

def certify(n, lo, hi, k, assumptions):
    if any(assumptions.get(a) is not True for a in ASSUMPTIONS):
        return 'UNKNOWN'
    if any(type(x) is not int for x in (n, lo, hi, k)) or not 0 <= lo <= hi <= n:
        return 'UNKNOWN'
    if n <= k or lo > k:
        return 'MUST_AGREE'
    if hi <= k:
        return 'MUST_DIVERGE'
    return 'MAY_DIVERGE'

def replay(max_n=12):
    a = dict.fromkeys(ASSUMPTIONS, True)
    cases = evaluations = 0
    for n in range(max_n + 1):
        for lo in range(n + 1):
            for hi in range(lo, n + 1):
                for k in range(-2, n + 3):
                    observed = []
                    for i in range(lo, hi + 1):
                        bits = tuple([True] * i + [False] * (n - i))
                        observed.append((len([x for x in bits]) > k) !=
                                        (sum(x for x in bits) > k))
                        evaluations += 1
                    expected = ('MUST_DIVERGE' if all(observed) else
                                'MUST_AGREE' if not any(observed) else 'MAY_DIVERGE')
                    assert certify(n, lo, hi, k, a) == expected
                    cases += 1
    assert certify(3, 0, 2, 1, {}) == 'UNKNOWN'
    assert (len([2, 2]) > 3) is False and (sum([2, 2]) > 3) is True
    return {'cases': cases, 'evaluations': evaluations, 'mismatches': 0}

if __name__ == '__main__':
    import json
    print(json.dumps(replay(), sort_keys=True))
