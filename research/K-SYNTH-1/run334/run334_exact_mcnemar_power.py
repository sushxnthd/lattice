#!/usr/bin/env python3
"""Exact unconditional McNemar power (iid) and repository clustering sensitivity."""
import json,math
from scipy.stats import binom
def power(n,q,p,alpha=.05):
    total=0.
    for m in range(1,n+1):
        lo=int(binom.ppf(alpha/2,m,.5))
        while lo>=0 and 2*binom.cdf(lo,m,.5)>alpha:lo-=1
        if lo<0:continue
        total+=binom.pmf(m,n,q)*(binom.cdf(lo,m,p)+binom.sf(m-lo-1,m,p))
    return total
rows=[{'n':n,'discordance_probability':.30,'conditional_ir_win_probability':p,
       'exact_unconditional_power_iid':round(power(n,.30,p),5)}
      for n in (306,681) for p in (.60,.65)]
cluster=[{'issues_per_repo':m,'icc':icc,'design_effect':round(1+(m-1)*icc,3),
          'issues_for_306_effective':math.ceil(306*(1+(m-1)*icc)),
          'issues_for_681_effective':math.ceil(681*(1+(m-1)*icc))}
         for m in (2,4,6,8) for icc in (.05,.10,.15)]
print(json.dumps({'schema':'run334-mcnemar-exact-power-v1','alpha_two_sided':.05,
 'method':'exact conditional binomial test integrated over binomial discordant count',
 'power_iid':rows,'cluster_design_effect_sensitivity':cluster,
 'caveats':['iid power invalid under correlated repository clusters',
 'ICC and equal cluster sizes hypothetical, not estimated',
 'design effect is a planning approximation, not exact clustered McNemar power',
 'no effect-size estimate from three qualified historical tasks']},indent=2))
