import itertools,json,math
def exact_cluster_p(margins):
    observed=abs(sum(margins)); n=len(margins)
    extreme=sum(abs(sum(s*x for s,x in zip(signs,margins)))>=observed for signs in itertools.product((-1,1),repeat=n))
    return extreme/(2**n)
def exact_mcnemar(a,b):
    n=a+b
    return min(1,2*sum(math.comb(n,k) for k in range(min(a,b)+1))/2**n) if n else 1
margins=[10]*7+[-10]
result={'design':'synthetic, not model observations','repo_margins':margins,'issues':80,'repos':8,'ir_only':70,'python_only':10,'mcnemar_exact_two_sided':exact_mcnemar(70,10),'cluster_signflip_exact_two_sided':exact_cluster_p(margins),'signflip_assignments':256}
assert result['mcnemar_exact_two_sided']<0.05
assert result['cluster_signflip_exact_two_sided']>0.05
assert all(exact_cluster_p(list(p))==result['cluster_signflip_exact_two_sided'] for p in itertools.permutations(margins))
assert exact_cluster_p([-x for x in margins])==result['cluster_signflip_exact_two_sided']
print(json.dumps(result,sort_keys=True,indent=2))
