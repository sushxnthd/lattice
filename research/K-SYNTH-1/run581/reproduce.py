import itertools, math
patterns={'concentrated':[20]*9+[0]*3,'balanced':[15]*12,'mixed':[20]*6+[10]*6}
assert all(len(x)==12 and sum(x)==180 for x in patterns.values())
for name,wins in patterns.items():
 d=[2*x-20 for x in wins]
 observed=abs(sum(d))
 extreme=sum(abs(sum(a*b for a,b in zip(signs,d)))>=observed for signs in itertools.product((-1,1),repeat=12))
 print(name,extreme,4096,extreme/4096)
print('issue_mcnemar',2*sum(math.comb(240,k) for k in range(180,241))/2**240)
for k in range(1,21): print('minimum_p',k,2/2**k)
