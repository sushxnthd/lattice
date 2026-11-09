from itertools import product
from fractions import Fraction
import json

def signflip_p(values):
    observed = abs(sum(values))
    n = len(values)
    count = sum(abs(sum(s*x for s,x in zip(signs, values))) >= observed
                for signs in product((-1,1), repeat=n))
    return Fraction(count, 2**n)

def run(n=8):
    rejected = Fraction(0)
    rows = []
    for bits in product((0,1), repeat=n):
        vals = [1 if b else -9 for b in bits]
        prob = Fraction(9**sum(bits), 10**n)
        p = signflip_p(vals)
        if p <= Fraction(1,20):
            rejected += prob
        rows.append({"bits":bits, "p":str(p), "prob":str(prob)})
    return {"rejection_probability":str(rejected),
            "rejection_float":float(rejected), "rows":rows}

if __name__ == "__main__":
    result=run()
    assert result["rejection_probability"]=="21524531/50000000"
    print(json.dumps(result, indent=2))
