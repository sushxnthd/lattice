import math, json
alpha = 0.05
rows = []
for n in [20,100,200,400,800,2000,5000,10000]:
    fixed = math.sqrt(2*math.log(2/alpha)/n)
    alpha_n = alpha*6/(math.pi**2*n*n)
    anytime = math.sqrt(2*math.log(2/alpha_n)/n)
    rows.append(dict(repositories=n, fixed_halfwidth=fixed, anytime_halfwidth=anytime, alpha_spent=alpha_n, ratio=anytime/fixed))
assert sum(alpha*6/(math.pi**2*n*n) for n in range(1,100001)) < alpha
print(json.dumps({"method":"Bonferroni-Hoeffding anytime confidence sequence","alpha":alpha,"rows":rows},indent=2))
