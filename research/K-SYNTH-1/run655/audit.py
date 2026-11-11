import itertools, json, math
def exact_tail(weights, observed):
    counts={0:1}
    for w in weights:
        nxt={}
        for s,c in counts.items():
            for t in (-w,w): nxt[s+t]=nxt.get(s+t,0)+c
        counts=nxt
    return sum(c for s,c in counts.items() if abs(s)>=abs(observed))/2**len(weights)
def mcnemar(w,l):
    n=w+l
    return min(1.,2*sum(math.comb(n,k) for k in range(min(w,l)+1))/2**n)
R,m=12,4
issue=cluster=0
for signs in itertools.product((-1,1),repeat=R):
    w=m*sum(s==1 for s in signs); l=m*R-w
    issue+=mcnemar(w,l)<=.05
    cluster+=exact_tail([m]*R,m*sum(signs))<=.05
print(json.dumps(dict(assignments=2**R,issue_rejections=issue,cluster_rejections=cluster,issue_rate=issue/2**R,cluster_rate=cluster/2**R),indent=2))
assert (issue,cluster)==(1588,158)