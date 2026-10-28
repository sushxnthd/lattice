#!/usr/bin/env python3
"""Independent read-only audit of original Run311 raw repo-score vectors."""
import gzip,json,math,collections,hashlib
from pathlib import Path
from scipy.stats import norm,t
R=Path(__file__).resolve().parent
summary=json.loads((R/'RUN311_SUMMARY.json').read_text())
bykey={(x['J'],x['m'],x['p'],x['rho']):x for x in summary['cells']}
acc=collections.defaultdict(lambda:{'count':0,'naive':0,'cluster':0,'sum':0.,'sum2':0.,'discordant':0})
checked=0
zcut=norm.ppf(.975)
tcut={j:t.ppf(.975,j-1) for j,m in [(102,3),(227,3),(100,4),(100,8),(200,4),(200,6),(200,8)]}
with gzip.open(R/'RUN311_RAW_REPLICATES.jsonl.gz','rt') as f:
    for line in f:
        row=json.loads(line);key=(row['J'],row['m'],row['p'],row['rho'])
        assert key in bykey
        J,m,p,rho=key
        scores=row['repo_scores']
        assert len(scores)==J and all(isinstance(v,int) and -m<=v<=m for v in scores)
        wins,losses=row['wins'],row['losses']
        total=sum(scores); n=wins+losses
        assert total==wins-losses and 0<=n<=J*m
        assert (n-total)%2==0
        z=total/math.sqrt(n) if n else 0.
        naive=abs(z)>zcut
        avg=total/J
        variance=J/(J-1)*sum((u-avg)**2 for u in scores)
        tc=total/math.sqrt(variance) if variance>0 else 0.
        cluster=variance>0 and abs(tc)>tcut[J]
        assert naive==row['naive_reject'] and cluster==row['cluster_reject']
        a=acc[key];a['count']+=1;a['naive']+=naive;a['cluster']+=cluster
        a['sum']+=total;a['sum2']+=total*total;a['discordant']+=n
        checked+=1
assert checked==63*4000
for key,original in bykey.items():
    a=acc[key]; assert a['count']==4000
    assert a['naive']==original['naive']['rejections']
    assert a['cluster']==original['cluster']['rejections']
    assert math.isclose(a['discordant']/4000,original['mean_discordant'],rel_tol=0,abs_tol=1e-12)
    var=(a['sum2']-a['sum']**2/4000)/3999
    assert math.isclose(var,original['observed_total_score_variance'],rel_tol=1e-12)
    J,m,p,rho=key
    q=.3
    mean=q*(2*p-1)
    one_var=q-mean**2
    pair_cov=q*q*4*p*(1-p)*rho
    theory=J*m*one_var+J*m*(m-1)*pair_cov
    assert math.isclose(theory,original['theory_total_score_variance'],rel_tol=1e-12)
result={'schema':'run311-independent-audit-v1','checked_replicates':checked,
        'checked_cells':len(bykey),'all_naive_decisions_match':True,
        'all_cluster_decisions_match':True,'all_variances_match':True,
        'all_theory_variances_match':True,
        'raw_sha256':hashlib.sha256((R/'RUN311_RAW_REPLICATES.jsonl.gz').read_bytes()).hexdigest(),
        'summary_sha256':hashlib.sha256((R/'RUN311_SUMMARY.json').read_bytes()).hexdigest()}
(R/'RUN311_INDEPENDENT_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
