#!/usr/bin/env python3
"""Prospectively frozen clustered McNemar design audit (NOT model evidence).

GitHub protocol commit 24934720d333918ae57cb6b34a763a385cf767af.
All 63 cells and every replicate's repository score vector are retained.
"""
import gzip, json, math, platform, hashlib
from pathlib import Path
import numpy as np
from scipy.stats import norm, t

ROOT = Path(__file__).resolve().parent
SEED = 31120261028
R = 4000
Q = .30
DESIGNS = [(102,3),(227,3),(100,4),(100,8),(200,4),(200,6),(200,8)]
PS = [.50,.60,.65]
RHOS = [0.,.05,.15]

def simulate():
    rng=np.random.default_rng(SEED)
    zcut=float(norm.ppf(.975))
    summary=[]
    with gzip.open(ROOT/'RUN311_RAW_REPLICATES.jsonl.gz','wt',encoding='utf8',compresslevel=6) as out:
        for J,m in DESIGNS:
            for p in PS:
                for rho in RHOS:
                    if rho:
                        concentration=1/rho-1
                        prob=rng.beta(p*concentration,(1-p)*concentration,size=(R,J,1))
                    else:
                        prob=p
                    discordant=rng.random((R,J,m))<Q
                    winner=rng.random((R,J,m))<prob
                    signs=np.where(discordant,np.where(winner,1,-1),0).astype(np.int8)
                    repo=signs.sum(axis=2,dtype=np.int16)
                    total=repo.sum(axis=1,dtype=np.int32)
                    nd=discordant.sum(axis=(1,2),dtype=np.int32)
                    wins=((nd+total)//2).astype(np.int32)
                    losses=((nd-total)//2).astype(np.int32)
                    assert np.array_equal(wins+losses,nd)
                    naive=np.divide(total,np.sqrt(nd),out=np.zeros(R),where=nd>0)
                    mean=repo.mean(axis=1)
                    varsum=(J/(J-1))*np.sum((repo-mean[:,None])**2,axis=1)
                    cluster=np.divide(total,np.sqrt(varsum),out=np.zeros(R),where=varsum>0)
                    nreject=(np.abs(naive)>zcut)
                    creject=(varsum>0)&(np.abs(cluster)>t.ppf(.975,J-1))
                    for i in range(R):
                        out.write(json.dumps({'J':J,'m':m,'p':p,'rho':rho,'rep':i,
                           'wins':int(wins[i]),'losses':int(losses[i]),
                           'repo_scores':repo[i].tolist(),
                           'naive_reject':bool(nreject[i]),
                           'cluster_reject':bool(creject[i])},separators=(',',':'))+'\n')
                    var_theory=J*m*(Q-Q*Q*(2*p-1)**2)+J*m*(m-1)*(4*Q*Q*p*(1-p)*rho)
                    obsvar=float(np.var(total,ddof=1))
                    def est(x):
                        k=int(np.count_nonzero(x)); rate=k/R
                        se=math.sqrt(rate*(1-rate)/R)
                        return {'rejections':k,'rate':rate,'mc_se':se,
                                'mc_ci95':[max(0,rate-1.96*se),min(1,rate+1.96*se)]}
                    summary.append({'J':J,'m':m,'n':J*m,'p':p,'rho':rho,
                        'naive':est(nreject),'cluster':est(creject),
                        'mean_discordant':float(nd.mean()),
                        'theory_total_score_variance':var_theory,
                        'observed_total_score_variance':obsvar,
                        'variance_ratio':obsvar/var_theory,
                        'mean_total_score':float(total.mean())})
    meta={'schema':'run311-cluster-power-v1','protocol_commit':'24934720d333918ae57cb6b34a763a385cf767af',
        'seed':SEED,'replicates_per_cell':R,'q':Q,'designs':DESIGNS,'ps':PS,'rhos':RHOS,
        'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__,
        'null_type1_vs_alternative_power':'p=0.5 is null',
        'limitations':['independent discordance indicators within and across repos',
           'equal cluster sizes per design','beta-binomial sign correlation only',
           'no actual model inference or repository qualification'],
        'cells':summary}
    (ROOT/'RUN311_SUMMARY.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta

if __name__=='__main__':
    meta=simulate()
    for p in [.5,.6,.65]:
        print('p',p)
        for d in meta['cells']:
            if d['p']==p and d['rho']==.15:
                print(f"J={d['J']} m={d['m']} n={d['n']}: naive={d['naive']['rate']:.3f} cluster={d['cluster']['rate']:.3f} var_ratio={d['variance_ratio']:.3f}")
