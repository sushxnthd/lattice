import json, math
from pathlib import Path

def exact_p(k,n):
    return min(1.0, 2*sum(math.comb(n,j) for j in range(min(k,n-k)+1))/2**n)

def power(ps):
    n=len(ps); dp=[1.0]+[0.0]*n
    for i,p in enumerate(ps):
        nd=[0.0]*(n+1)
        for k in range(i+1):
            nd[k]+=dp[k]*(1-p); nd[k+1]+=dp[k]*p
        dp=nd
    return sum(v for k,v in enumerate(dp) if exact_p(k,n)<=.05),sum(k*v for k,v in enumerate(dp)),sum(dp)

rows=[]
for n in (6,12,20,40,80,120,200):
    for label,ps in [('homogeneous_0.65',[.65]*n),('heterogeneous_balanced',[.8 if i%2==0 else .5 for i in range(n)]),('heterogeneous_reversed',[.95 if i%2==0 else .35 for i in range(n)])]:
        p,mean,total=power(ps)
        assert abs(total-1)<1e-10
        rows.append(dict(repositories=n,scenario=label,average_win_probability=sum(ps)/n,exact_two_sided_power=p,expected_IR_wins=mean))
assert exact_p(6,6)==.03125
assert exact_p(5,5)==.0625
out={'method':'exact Poisson-binomial distribution for independent repository signs; exact two-sided binomial sign-test rejection','alpha':.05,'rows':rows,'limitations':['synthetic independent repository signs, not observed repair data','no zero-discordance clusters','heterogeneous probabilities do not imply exchangeability of sign flips','not a power analysis for issue-weighted McNemar or correlated multi-issue repo effects']}
Path(__file__).with_name('raw.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:print(r)
