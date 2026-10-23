"""Outcome-blind discovery/boundary power correction for K-SYNTH-1 Run203.

Input: frozen Run199/Run202 public.json. No gold patches, model outputs, or
held-out issue contents are used; only repository IDs and split labels.
"""
import argparse, collections, hashlib, json, math
from pathlib import Path
import numpy as np
from scipy.stats import t

def simulate(sizes, win, reps, seed, discordance=.30, rho=.50):
    rng=np.random.default_rng(seed)
    n=len(sizes)
    q=rng.beta(win*(1/rho-1),(1-win)*(1/rho-1),size=(reps,n))
    cluster=np.zeros((reps,n))
    for i,m in enumerate(sizes):
        active=rng.random((reps,m))<discordance
        signs=np.where(rng.random((reps,m))<q[:,i,None],1.,-1.)
        cluster[:,i]=(active*signs).mean(axis=1)
    avg=cluster.mean(axis=1)
    sd=cluster.std(axis=1,ddof=1)
    stat=np.divide(avg,sd/np.sqrt(n),out=np.zeros_like(avg),where=sd>0)
    reject=2*t.sf(np.abs(stat),n-1)<.05
    rate=float(reject.mean())
    return {'rejection_rate':rate,
            'monte_carlo_se':math.sqrt(rate*(1-rate)/reps),
            'expected_cluster_mean_difference':float(avg.mean())}

def audit(raw,reps=20000):
    data=json.loads(raw)
    groups={}
    for label in ('discovery','boundary','all'):
        rows=data if label=='all' else [x for x in data if x['split']==label]
        counts=collections.Counter(x['repo'] for x in rows)
        sizes=sorted(counts.values())
        assert sum(sizes)==len(rows)
        groups[label]={'issues':len(rows),'repositories':len(counts),
            'cluster_size_histogram':dict(collections.Counter(sizes)),
            'null':simulate(sizes,.5,reps,203000+len(rows)),
            'moderate_effect':simulate(sizes,.6,reps,203100+len(rows)),
            'large_effect':simulate(sizes,.65,reps,203200+len(rows))}
    return {'dataset_sha256':hashlib.sha256(raw).hexdigest(),
        'assumptions':{'discordance':.30,'conditional_ir_win_large':.65,
            'conditional_ir_win_moderate':.60,'repository_direction_icc':.50,
            'alpha_two_sided':.05,'reps':reps,
            'test':'two-sided repository-level t test'},
        'groups':groups,
        'warning':'Hypothetical power sensitivities only; do not use boundary issues in discovery primary analysis.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--public',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--reps',type=int,default=20000)
    args=ap.parse_args()
    result=audit(args.public.read_bytes(),args.reps)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,indent=2))
