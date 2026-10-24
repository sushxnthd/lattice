#!/usr/bin/env python3
"""Cluster-aware paired power sensitivity for Lattice representation experiments.

D = +1 (IR-only functional success), -1 (Python-only success), or 0.
Within-repository beta-distributed win probabilities model heterogeneity.
The endpoint is a two-sided t-test on repository-level paired differences.
This is planning, NOT measured model performance.
"""
from __future__ import annotations
import argparse, json
import numpy as np
from scipy.stats import t as student_t

SEED=22620261024

def simulate(n_repos:int,k:int,discordance:float,ir_win:float,latent_rho:float,
             replicates:int,seed:int)->dict:
    if not (0<discordance<1 and 0.5<=ir_win<1 and 0<=latent_rho<1):
        raise ValueError("invalid probability")
    rng=np.random.default_rng(seed)
    if latent_rho:
        concentration=1/latent_rho-1
        repo_win=rng.beta(ir_win*concentration,(1-ir_win)*concentration,
                          size=(replicates,n_repos,1))
    else:
        repo_win=np.full((replicates,n_repos,1),ir_win)
    is_disc=rng.random((replicates,n_repos,k))<discordance
    ir_only=rng.random((replicates,n_repos,k))<repo_win
    d=np.where(is_disc,np.where(ir_only,1,-1),0).astype(np.float64)
    means=d.mean(axis=2)
    avg=means.mean(axis=1)
    sd=means.std(axis=1,ddof=1)
    t_stat=np.divide(avg,sd/np.sqrt(n_repos),out=np.zeros_like(avg),where=sd>0)
    rejected=np.abs(t_stat)>student_t.ppf(0.975,n_repos-1)
    power=float(rejected.mean())
    se_mc=float(np.sqrt(power*(1-power)/replicates))
    q,p=discordance,ir_win
    variance=q-(q*(2*p-1))**2
    cov=4*q*q*p*(1-p)*latent_rho
    rho_issue=cov/variance
    return dict(repositories=n_repos,issues_per_repository=k,total_issues=n_repos*k,
        discordance=q,ir_win_given_discordance=p,latent_beta_rho=latent_rho,
        induced_issue_ICC=round(rho_issue,5),
        design_effect=round(1+(k-1)*rho_issue,5),
        power=round(power,5),mc_se=round(se_mc,5),
        replicates=replicates,seed=seed,
        test="two-sided repository-level paired difference t-test")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--replicates",type=int,default=5000)
    ap.add_argument("--output",default="cluster_power_results.json")
    args=ap.parse_args()
    rows=[]
    for q,p in ((0.3,0.6),(0.2,0.6),(0.3,0.65)):
        for latent in (0,0.1,0.3,0.6):
            for n_repos in (65,172,256,375):
                seed=SEED+int(q*10000)+int(p*100000)+int(latent*1000)+n_repos
                rows.append(simulate(n_repos,4,q,p,latent,args.replicates,seed))
    data={"protocol":"K-SYNTH-1/run226-cluster-power-v1",
          "interpretation":"planning sensitivity only; no observed model performance",
          "rows":rows}
    with open(args.output,"w") as f:json.dump(data,f,indent=2)
    for r in rows:
        if r["discordance"]==0.3 and r["ir_win_given_discordance"]==0.6:
            print(f"n={r['total_issues']:4} latent={r['latent_beta_rho']:.1f} "
                  f"issueICC={r['induced_issue_ICC']:.3f} power={r['power']:.3f}")

if __name__=="__main__":main()
