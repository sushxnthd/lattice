#!/usr/bin/env python3
"""Run452: exact enumeration of pseudoreplication in paired repair evaluations.

No external dependencies, no model inference, no production repair claims.
A repo-level latent Bernoulli variable determines the outcome of two issues
from that repo. Null: each repo independently favors IR with probability 1/2.
"""
from itertools import product
from fractions import Fraction

def exact_null(num_repos=4, issues_per_repo=2):
    assert num_repos > 0 and issues_per_repo > 0
    distribution = {}
    for signs in product((0, 1), repeat=num_repos):
        ir_wins = sum(signs) * issues_per_repo
        distribution[ir_wins] = distribution.get(ir_wins, 0) + 1
    denominator = 2 ** num_repos
    assert sum(distribution.values()) == denominator
    return {k: Fraction(v, denominator) for k, v in sorted(distribution.items())}

def naive_all_wins_probability(num_repos=4, issues_per_repo=2):
    return Fraction(1, 2 ** (num_repos * issues_per_repo))

def cluster_all_wins_probability(num_repos=4):
    return Fraction(1, 2 ** num_repos)

def main():
    d = exact_null()
    assert d == {0: Fraction(1,16), 2: Fraction(4,16),
                 4: Fraction(6,16), 6: Fraction(4,16),
                 8: Fraction(1,16)}
    assert cluster_all_wins_probability() == Fraction(1,16)
    assert naive_all_wins_probability() == Fraction(1,256)
    assert cluster_all_wins_probability() / naive_all_wins_probability() == 16
    # General construction: m perfectly correlated issues per repo.
    for r in range(1, 9):
        for m in range(1, 5):
            dist = exact_null(r, m)
            assert sum(dist.values()) == 1
            assert dist[r*m] == cluster_all_wins_probability(r)
            assert dist[r*m] / naive_all_wins_probability(r,m) == 2**(r*(m-1))
    print("PASS: exact enumeration, 32 parameter checks")
    print("4 repos x 2 perfectly correlated issues: all 8 IR wins")
    print("Correct null tail P = 1/16 = 0.0625")
    print("Incorrect issue-IID tail P = 1/256 = 0.00390625")
    print("False significance inflation factor = 16")
    print("Scope: constructed repo-cluster null, not measured Lattice performance")

if __name__ == "__main__":
    main()
