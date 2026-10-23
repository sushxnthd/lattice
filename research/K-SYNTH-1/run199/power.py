"""Outcome-blind power sensitivity for 120 independent repositories x 4 paired issues.

Not observed model results. Assumes 30% discordance, beta-distributed
repository directional ICC 0.5, and a repository-level two-sided t test.
"""
import json
import numpy as np
from scipy.stats import t

REPS=20000
NREPOS=120
ISSUES_PER_REPO=4
DISCORDANCE=.30
ICC=.50
SEED=1991023

def simulate(q, seed):
    rng=np.random.default_rng(seed)
    concentration=1/ICC-1
    repo_q=rng.beta(q*concentration,(1-q)*concentration,size=(REPS,NREPOS,1))
    discordant=rng.random((REPS,NREPOS,ISSUES_PER_REPO))<DISCORDANCE
    signs=np.where(rng.random((REPS,NREPOS,ISSUES_PER_REPO))<repo_q,1.,-1.)
    d=(discordant*signs).mean(axis=2)
    avg=d.mean(axis=1)
    std=d.std(axis=1,ddof=1)
    stat=np.divide(avg,std/np.sqrt(NREPOS),out=np.zeros_like(avg),where=std>0)
    p=2*t.sf(np.abs(stat),NREPOS-1)
    rate=float((p<.05).mean())
    return dict(rejection_rate=rate,mc_se=float(np.sqrt(rate*(1-rate)/REPS)),
                mean_paired_difference=float(avg.mean()),replications=REPS)

if __name__=="__main__":
    result=dict(seed=SEED,design="120 independent repositories x 4 independent paired issues",
        statistical_test="two-sided repository-level signed-difference t test, alpha=.05",
        assumptions=dict(discordance=DISCORDANCE,directional_icc=ICC,repo_heterogeneity="beta"),
        null=simulate(.5,SEED),large_effect=simulate(.65,SEED+1),
        moderate_effect=simulate(.60,SEED+2),
        caveat="Hypothetical power sensitivity, not observed inference. Recompute if eligible repositories or dependence differ.")
    print(json.dumps(result,indent=2))
