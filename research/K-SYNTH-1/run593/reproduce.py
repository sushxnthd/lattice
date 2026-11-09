"""Exact optional-stopping audit of fixed-n Hoeffding intervals under a fair null."""
import json
import math
from fractions import Fraction

ALPHA = 0.05
CHECKPOINTS = tuple(range(20, 2001, 20))
states = {0: 1}
results = []
for n in range(1, max(CHECKPOINTS) + 1):
    nxt = {}
    for k, count in states.items():
        nxt[k] = nxt.get(k, 0) + count
        nxt[k + 1] = nxt.get(k + 1, 0) + count
    states = nxt
    if n in CHECKPOINTS:
        radius = math.sqrt(2 * math.log(2 / ALPHA) / n)
        rejected = {k: v for k, v in states.items() if abs((2*k-n)/n) > radius}
        newly = sum(rejected.values())
        prob = Fraction(newly, 2**n)
        prior = Fraction(results[-1]["cumulative_numerator"], results[-1]["cumulative_denominator"]) if results else Fraction(0)
        cumulative = prior + prob
        states = {k: v for k, v in states.items() if k not in rejected}
        results.append({"n": n, "radius": radius, "newly_reject_probability": float(prob),
                        "cumulative_false_positive": float(cumulative),
                        "cumulative_numerator": cumulative.numerator,
                        "cumulative_denominator": cumulative.denominator,
                        "survivor_states": len(states)})
print(json.dumps({"null": "independent fair Rademacher repository effects, true mean zero",
                  "method": "exact absorbing binomial dynamic program; fixed-n Hoeffding radius reused at 100 looks",
                  "alpha": ALPHA, "checkpoints": results}, indent=2))
