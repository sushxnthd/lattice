"""Run323 prospective repository-cluster sensitivity. Synthetic design evidence only."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
from scipy.stats import binom, t

HERE=Path(__file__).resolve().parent
SEED=3232026
REPS=1200
ALPHA=.05
DESIGNS=[('optimistic',306,102,.65),('moderate',681,170,.60),('expanded',800,200,.60)]
RHOS=(0.0,.10,.30)

def wilson(k,n):
    z=1.959963984540054
    p=k/n
    center=(p+z*z/(2*n))/(1+z*z/n)
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return [float(center-half),float(center+half)]

def run():
    rng=np.random.Generator(np.random.PCG64(SEED))
    summary=[]
    with (HERE/'run323_raw_replicates.jsonl').open('w') as f:
        for name,n,m,alt_q in DESIGNS:
            sizes=np.full(m,n//m,dtype=int)
            sizes[:n%m]+=1
            repo_ids=np.repeat(np.arange(m),sizes)
            starts=np.r_[0,np.cumsum(sizes)[:-1]]
            for rho in RHOS:
                for hypothesis,q in [('null',.5),('alternative',alt_q)]:
                    if rho==0:
                        qrepo=np.full((REPS,m),q,dtype=float)
                    else:
                        k=1/rho-1
                        qrepo=rng.beta(q*k,(1-q)*k,size=(REPS,m))
                    discordant=rng.random((REPS,n))<.30
                    ironly=rng.random((REPS,n))<qrepo[:,repo_ids]
                    d=np.where(discordant,np.where(ironly,1,-1),0).astype(np.int8)
                    scores=np.add.reduceat(d.astype(np.int16),starts,axis=1)
                    disccount=np.add.reduceat(discordant.astype(np.int16),starts,axis=1)
                    w=np.count_nonzero(d==1,axis=1)
                    l=np.count_nonzero(d==-1,axis=1)
                    mu=scores.sum(axis=1)/n
                    centered=scores-mu[:,None]*sizes[None,:]
                    se=np.sqrt(m/(m-1)*np.square(centered).sum(axis=1))/n
                    z=np.divide(np.abs(mu),se,out=np.full_like(mu,np.inf),where=se>0)
                    pc=np.minimum(1.0,2*t.sf(z,m-1))
                    pc[(se==0)&(mu==0)]=1.0
                    pm=np.minimum(1.0,2*binom.cdf(np.minimum(w,l),w+l,.5))
                    for i in range(REPS):
                        row={'design':name,'n':n,'m':m,'rho':rho,'q':q,'hypothesis':hypothesis,
                             'replicate':i,'seed':SEED,'scores':scores[i].tolist(),
                             'discordants_by_repo':disccount[i].tolist(),
                             'ir_only':int(w[i]),'python_only':int(l[i]),
                             'cluster_p':float(pc[i]),'mcnemar_p':float(pm[i])}
                        f.write(json.dumps(row,separators=(',',':'),sort_keys=True)+'\n')
                    a=int(np.count_nonzero(pc<ALPHA));b=int(np.count_nonzero(pm<ALPHA))
                    summary.append({'design':name,'n':n,'repos':m,'q':q,'rho':rho,'hypothesis':hypothesis,
                                    'replicates':REPS,'cluster_rejections':a,'cluster_rate':a/REPS,
                                    'cluster_wilson95':wilson(a,REPS),
                                    'mcnemar_rejections':b,'mcnemar_rate':b/REPS,
                                    'mcnemar_wilson95':wilson(b,REPS),
                                    'mean_discordants':float((w+l).mean()),
                                    'mean_issue_effect':float((w-l).mean()/n)})
    raw=HERE/'run323_raw_replicates.jsonl'
    result={'protocol_commit':'086c6cf59fdf197c718de5cdb196da4c3fe0ae5d',
            'seed':SEED,'replicates_per_cell':REPS,'total_replicates':len(summary)*REPS,
            'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
            'cells':summary,'model_inference':False,'real_repair_trials':0}
    (HERE/'run323_primary_summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'total_replicates':result['total_replicates'],'raw_sha256':result['raw_sha256'],
                      'cells':[{'design':s['design'],'rho':s['rho'],'hypothesis':s['hypothesis'],
                                'cluster_rate':s['cluster_rate'],'mcnemar_rate':s['mcnemar_rate']} for s in summary]},indent=2))
if __name__=='__main__':run()
