"""Exact paired McNemar power integrated over random discordant-pair count.

This model assumes independent issue pairs. An illustrative design effect is
reported separately; it is NOT a substitute for cluster-aware simulation.
"""
from scipy.stats import binom
import numpy as np
import json
import math

MAX_N = 2000
D = np.arange(MAX_N + 1)
k = binom.ppf(.025, D, .5).astype(int)
k = np.where(2 * binom.cdf(k, D, .5) > .05, k - 1, k)

def power(n, d, q):
    m, v = k[:n+1], D[:n+1]
    reject = np.where(m >= 0, binom.cdf(m, v, q) + binom.sf(v-m-1, v, q), 0)
    return float(np.dot(binom.pmf(v, n, d), reject))

def min_n(d, q):
    lo, hi = 1, MAX_N
    while lo < hi:
        mid = (lo + hi) // 2
        if power(mid, d, q) >= .8:
            hi = mid
        else:
            lo = mid + 1
    return lo if power(lo, d, q) >= .8 else None

if __name__ == '__main__':
    rows = []
    for d, q in ((.30, .65), (.20, .65), (.30, .60), (.20, .60)):
        n = min_n(d, q)
        rows.append({
            'discordance': d, 'conditional_IR_win': q,
            'independent_pairs_for_80pct': n,
            'power_258': round(power(258, d, q), 4),
            'power_686_independent': round(power(686, d, q), 4),
            'cluster_adjusted_example_4_issues_rho_0.10': math.ceil(n*1.3) if n else None,
        })
    print(json.dumps({
        'method': 'exact two-sided conditional binomial McNemar, integrated over binomial discordances; illustrative design effect only',
        'rows': rows,
    }, indent=2))
