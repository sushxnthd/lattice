import itertools, math, json
def pbin(n,k):
    return min(1., 2*sum(math.comb(n,i) for i in range(min(k,n-k)+1))/2**n)
def cluster_p(weights):
    obs=abs(sum(weights))
    vals=[abs(sum(s*w for s,w in zip(signs,weights))) for signs in itertools.product((-1,1),repeat=len(weights))]
    return sum(v>=obs for v in vals)/len(vals)
rows=[]
for r in range(1,11):
    for issues in (1,2,4,8,16):
        w=[issues]*r
        rows.append(dict(repos=r,issues_per_repo=issues,total_issues=r*issues,naive_mcnemar=pbin(r*issues,r*issues),cluster_randomization=cluster_p(w)))
assert len(rows)==50
checks=0
for r in range(1,11):
    for weights in ([1]*r,list(range(1,r+1))):
        ps=[cluster_p([s*w for s,w in zip(signs,weights)]) for signs in itertools.product((-1,1),repeat=r)]
        for alpha in (.01,.05,.1,.2,.5,1.):
            assert sum(p<=alpha+1e-12 for p in ps)/len(ps)<=alpha+1e-12
            checks+=1
print(json.dumps({'rows':rows,'calibration_assertions':checks},indent=2))
