#!/usr/bin/env python3
"""Finite repository-clustering counterexample; no model code executed."""
from itertools import product
from scipy.stats import binomtest

def main():
    independent_repository_sums = [8, 8]
    issue_level_p = binomtest(16, 16, p=.5, alternative="two-sided").pvalue
    null_distribution = [
        sum(sign * count for sign, count in zip(signs, independent_repository_sums))
        for signs in product((-1, 1), repeat=2)
    ]
    observed = sum(independent_repository_sums)
    repository_randomization_p = sum(
        abs(s) >= abs(observed) for s in null_distribution
    ) / len(null_distribution)
    assert issue_level_p == 2 / (2 ** 16)
    assert repository_randomization_p == .5
    print("issue-level exact McNemar p:", issue_level_p)
    print("repository-level exact sign-flip p:", repository_randomization_p)
    print("null distribution:", null_distribution)

if __name__ == "__main__":
    main()
