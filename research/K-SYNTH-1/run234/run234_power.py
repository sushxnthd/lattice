"""Prospective cluster-aware power planning; no observed model outcomes used.

For each planned repository, a latent probability of IR winning a discordant
pair is drawn from a beta distribution.  The simulation explicitly retains
within-repository dependence and uses a two-sided repository-level t test.
The empirical Run199 repository-size histogram is resampled as a template for
*new independent repositories*; it does not duplicate the actual benchmark.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.stats import t as tdist

HIST={1:77,2:45,3:27,4:11,5:28,6:8}
SIZES=np.array([k for k,v in HIST.items() for _ in range(v)],dtype=np.int64)
assert len(SIZES)==196 and SIZES.sum()==480

def power(repositories:int,p:float,*,discordance=.30,rho=.5,reps=5000,seed=234):
    if not (repositories>=3 and 0<p<1 and 0<discordance<=1 and 0<rho<1 and reps>=100):
        raise ValueError('invalid simulation parameters')
    rng=np.random.default_rng(seed)
    # Draw new independent repo sizes from the frozen, outcome-blind Run199 histogram.
    base=SIZES.copy()
    rng.shuffle(base)
    sizes=np.resize(base,repositories)
    alpha=p*(1/rho-1);beta=(1-p)*(1/rho-1)
    q=rng.beta(alpha,beta,size=(reps,repositories))
    delta=np.zeros((reps,repositories),dtype=np.float64)
    for i,m in enumerate(sizes):
        active=rng.random((reps,m))<discordance
        win=rng.random((reps,m))<q[:,i,None]
        delta[:,i]=(active*np.where(win,1.,-1.)).mean(axis=1)
    avg=delta.mean(axis=1)
    sd=delta.std(axis=1,ddof=1)
    z=np.divide(avg,sd/np.sqrt(repositories),out=np.zeros_like(avg),where=sd>0)
    rejected=2*tdist.sf(np.abs(z),repositories-1)<.05
    v=float(rejected.mean())
    return {'repositories':repositories,'issues':int(sizes.sum()),'p_ir_given_discordant':p,
            'power':v,'mc_se':math.sqrt(v*(1-v)/reps),'seed':seed,'reps':reps,
            'discordance':discordance,'rho':rho,'method':'two-sided repository-mean t test'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--reps',type=int,default=5000)
    a=p.parse_args()
    counts=[196,300,400,420,440,460,500,600]
    results=[]
    for prob in (.5,.60,.65):
        for n in counts:
            results.append(power(n,prob,reps=a.reps,seed=234000+int(prob*100)*1000+n))
    data={'design':'K-SYNTH-1/run234-cluster-power-v1','histogram':HIST,
          'scope':'hypothetical power planning only; not model performance',
          'assumptions':'new independent repositories with cluster sizes tiled from a shuffled Run199 empirical histogram; 30% paired discordance; beta repository-direction ICC 0.5; two-sided alpha 0.05',
          'results':results}
    a.out.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps(data,sort_keys=True,indent=2))

if __name__=='__main__':main()
