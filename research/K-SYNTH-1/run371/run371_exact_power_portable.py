#!/usr/bin/env python3
"""Independent-issue McNemar power, not a clustered-power guarantee."""
from functools import lru_cache
from scipy.stats import binom

@lru_cache(None)
def lower_critical(d, alpha=0.05):
    if d == 0:
        return -1
    c = int(binom.ppf(alpha / 2, d, 0.5))
    return c - int(binom.cdf(c, d, 0.5) > alpha / 2 + 1e-14)

def exact_power(n, p, q, alpha=0.05):
    """D~Bin(n,p), W|D~Bin(D,q), two-sided exact conditional test."""
    total = 0.0
    for d in range(1, n + 1):
        c = lower_critical(d, alpha)
        if c < 0:
            continue
        rejection = binom.cdf(c, d, q) + binom.sf(d - c - 1, d, q)
        total += binom.pmf(d, n, p) * rejection
    return total

def null_cluster_design_effect(m, p, rho):
    """Equal-sized repositories; signed discordant scores; null q=.5."""
    return 1 + (m - 1) * p * rho

if __name__ == '__main__':
    for n, p, q in ((306,.3,.65),(681,.3,.6),(400,.3,.6),
                    (800,.3,.6),(681,.2,.6),(681,.4,.6)):
        print(n, p, q, round(exact_power(n,p,q), 9))
    print('null design effect', null_cluster_design_effect(8,.3,.35))
