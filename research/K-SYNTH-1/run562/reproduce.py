import itertools,math,json
clusters=[(30,1)]*7+[(2,-1)]
n=sum(w for w,s in clusters)
margin=sum(w*s for w,s in clusters)
issue_p=2*sum(math.comb(n,k) for k in range((n+abs(margin))//2,n+1))/2**n
flips=list(itertools.product((-1,1),repeat=len(clusters)))
weighted_p=sum(abs(sum(w*s for (w,_),s in zip(clusters,f)))>=abs(margin) for f in flips)/len(flips)
repo_p=sum(abs(sum(f))>=6 for f in flips)/len(flips)
reversal=[(1,1)]*7+[(30,-1)]
assert n==212 and margin==208 and sum(w*s for w,s in reversal)==-23
print(json.dumps(dict(n=n,margin=margin,issue_p=issue_p,weighted_cluster_p=weighted_p,equal_repo_p=repo_p,reversal_issue_margin=-23,reversal_repo_margin=6),indent=2))
