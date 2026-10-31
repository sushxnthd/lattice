#!/usr/bin/env python3
"""Exact two-sided repository sign-flip test for paired repair comparisons.

Conditional validity requires independent fair *repository-level* arm-label
swaps, not merely E[IR-Python]=0. The algorithm is exact integer subset-sum
counting and never treats issues within a repository as independent.
"""
from collections import Counter
from fractions import Fraction
from itertools import product


def exact_cluster_signflip(sums):
    """Return exact rational p, extreme assignment count, nonzero repo count.

    Each repository contributes its sum of paired issue outcomes (+1/-1/0).
    Under the sharp exchangeability null, each nonzero repository sign may be
    independently flipped with probability 1/2.
    """
    values = [abs(int(s)) for s in sums if int(s) != 0]
    k = len(values)
    if k == 0:
        return Fraction(1), 1, 0
    # Distribution of S=sum +/- abs(s_r) via subset sums: S=2*T-A.
    counts = [1] + [0] * sum(values)
    used = 0
    for v in values:
        for j in range(used, -1, -1):
            if counts[j]:
                counts[j + v] += counts[j]
        used += v
    observed = abs(sum(int(s) for s in sums))
    extreme = sum(c for t, c in enumerate(counts) if abs(2*t-used) >= observed)
    assert sum(counts) == 1 << k
    return Fraction(extreme, 1 << k), extreme, k


def brute_force(sums):
    v = [int(x) for x in sums if x]
    if not v:
        return Fraction(1)
    observed = abs(sum(v))
    extreme = sum(abs(sum(a*x for a,x in zip(signs,v))) >= observed
                  for signs in product((-1,1),repeat=len(v)))
    return Fraction(extreme, 2**len(v))


def mcnemar_issue_p(wins, losses):
    from math import comb
    n = wins + losses
    if not n:
        return Fraction(1)
    lo = min(wins,losses)
    return min(Fraction(1), Fraction(2*sum(comb(n,j) for j in range(lo+1)), 2**n))
