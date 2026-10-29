"""Run341: exhaustive binary 2x2 factorial theorem and cancellation test.

This does not establish semantic dataflow or model superiority.
"""
from itertools import product
import json

def contrast(f):
    f00, f10, f01, f11 = f
    return f11 - f10 - f01 + f00

def monotone(f):
    a, b, c, d = f
    return a <= b <= d and a <= c <= d

def main():
    rows = []
    for f in product((0, 1), repeat=4):
        rows.append({"outcomes": f, "contrast": contrast(f), "monotone": monotone(f)})
    m = [r for r in rows if r["monotone"]]
    assert len(rows) == 16 and len(m) == 6
    assert all(r["contrast"] in (-1, 0, 1) for r in m)
    assert sum(r["contrast"] == 1 for r in m) == 1
    assert sum(r["contrast"] == -1 for r in m) == 1
    assert all(r["contrast"] == 0 for r in m if r["outcomes"] not in ((0,0,0,1),(0,1,1,1)))
    a, b = (0,0,0,1), (0,1,1,1)
    assert contrast(a) == 1 and contrast(b) == -1
    print(json.dumps({"functions": rows, "monotone_count": len(m),
                      "cancellation_counterexample": {"cases": [a,b],
                        "aggregate": contrast(a)+contrast(b),
                        "sum_absolute": abs(contrast(a))+abs(contrast(b)}},
                     indent=2))
if __name__ == "__main__":
    main()
