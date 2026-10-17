"""Exact paired binary test audit for frozen Run79 six-task pilot."""
from math import comb

N = 6

def two_sided_p(ir_only, python_only):
    n = ir_only + python_only
    if n == 0:
        return 1.0
    k = min(ir_only, python_only)
    return min(1.0, 2 * sum(comb(n, j) for j in range(k + 1)) / 2**n)

def exact_power(p_ir_only, p_python_only):
    tie = 1 - p_ir_only - p_python_only
    assert 0 <= tie <= 1
    return sum(comb(N, a) * comb(N-a, b) * p_ir_only**a
               * p_python_only**b * tie**(N-a-b)
               for a in range(N+1) for b in range(N-a+1)
               if two_sided_p(a, b) < 0.05)

if __name__ == "__main__":
    significant = [(a, b) for a in range(N+1) for b in range(N-a+1)
                   if two_sided_p(a, b) < 0.05]
    assert significant == [(0, 6), (6, 0)]
    print("significant outcomes:", significant)
    for a, b in ((0.1, 0), (0.3, 0.2), (0.5, 0)):
        print("true paired difference", a-b, "power", exact_power(a, b))
