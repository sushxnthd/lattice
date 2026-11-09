import itertools, math, json
def tail(k,n):
    return sum(math.comb(n,j) for j in range(k,n+1))/2**n
rows=[]
for weights in ([100,1,1,1],[20,20,1,1],[10]*8,[100]+[1]*15):
    R=len(weights); N=sum(weights); naive=repo=0
    for signs in itertools.product((-1,1),repeat=R):
        p=sum(w for w,s in zip(weights,signs) if s==1)
        q=sum(s==1 for s in signs)
        naive += 2*tail(max(p,N-p),N)<.05
        repo += 2*tail(max(q,R-q),R)<.05
    rows.append(dict(weights=weights,naive_rejections=naive,repo_rejections=repo,total=2**R))
print(json.dumps(rows,indent=2))
