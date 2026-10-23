"""Outcome-blind power simulation for observed unequal repository cluster sizes."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.stats import t

def simulate(sizes, conditional_ir_win, seed, reps=20000, discordance=.30, rho=.50):
    rng=np.random.default_rng(seed)
    n=len(sizes)
    q=rng.beta(conditional_ir_win*(1/rho-1),(1-conditional_ir_win)*(1/rho-1),size=(reps,n))
    cluster=np.zeros((reps,n))
    for i,m in enumerate(sizes):
        active=rng.random((reps,m))<discordance
        signs=np.where(rng.random((reps,m))<q[:,i,None],1.,-1.)
        cluster[:,i]=(active*signs).mean(axis=1)
    means=cluster.mean(axis=1)
    sd=cluster.std(axis=1,ddof=1)
    tstat=np.divide(means,sd/np.sqrt(n),out=np.zeros_like(means),where=sd>0)
    rejected=2*t.sf(np.abs(tstat),n-1)<.05
    rate=float(rejected.mean())
    return dict(rejection_rate=rate,mc_se=float(np.sqrt(rate*(1-rate)/reps)),
                mean_difference=float(means.mean()))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("manifest",type=Path)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    manifest=json.loads(a.manifest.read_text())
    hist={int(k):int(v) for k,v in manifest["cluster_size_histogram"].items()}
    sizes=[size for size,count in sorted(hist.items()) for _ in range(count)]
    assert sum(sizes)==manifest["selected_issues"]
    out=dict(manifest_sha256=hashlib.sha256(a.manifest.read_bytes()).hexdigest(),
        issues=sum(sizes),repositories=len(sizes),cluster_size_histogram=hist,
        assumptions="20k reps, 30% discordance, beta repository direction ICC 0.5, two-sided repo-level t test alpha=.05",
        null=simulate(sizes,.5,1991990),large_effect=simulate(sizes,.65,1991991),
        moderate_effect=simulate(sizes,.60,1991992),
        caveat="Prospective power sensitivity only; no model inference. Real heterogeneity may differ.")
    a.out.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=="__main__":main()
