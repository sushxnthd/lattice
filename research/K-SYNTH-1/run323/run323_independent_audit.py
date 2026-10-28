"""Independent, read-only Run323 audit; does not import primary simulator."""
from __future__ import annotations
import hashlib,json,math,collections
from pathlib import Path
from scipy.special import stdtr
from scipy.stats import binomtest

HERE=Path(__file__).resolve().parent
expected={('optimistic',306,102,.65),('moderate',681,170,.60),('expanded',800,200,.60)}
raw=HERE/'run323_raw_replicates.jsonl'
summary=json.loads((HERE/'run323_primary_summary.json').read_text())
assert hashlib.sha256(raw.read_bytes()).hexdigest()==summary['raw_sha256']
counts=collections.defaultdict(lambda:[0,0,0])
errors=[]
seen=set()
with raw.open() as f:
    for line_no,line in enumerate(f,1):
        row=json.loads(line)
        name,n,m,q=row['design'],row['n'],row['m'],row['q']
        hypothesis=row['hypothesis'];rho=row['rho'];rep=row['replicate']
        if hypothesis=='alternative': assert (name,n,m,q) in expected
        else: assert q==.5 and (name,n,m) in {(a,b,c) for a,b,c,_ in expected}
        assert rho in (0.0,.1,.3) and 0<=rep<1200
        key=(name,rho,hypothesis,rep)
        assert key not in seen
        seen.add(key)
        sizes=[n//m+int(j<n%m) for j in range(m)]
        s=row['scores'];d=row['discordants_by_repo']
        assert len(s)==len(d)==m
        assert all(0<=di<=ni and abs(si)<=di and (di-si)%2==0 for si,di,ni in zip(s,d,sizes))
        ir=sum((di+si)//2 for si,di in zip(s,d))
        py=sum((di-si)//2 for si,di in zip(s,d))
        assert (ir,py)==(row['ir_only'],row['python_only'])
        effect=sum(s)/n
        sq=0.
        for sr,nr in zip(s,sizes):
            residual=sr-nr*effect
            sq+=residual*residual
        se=math.sqrt((m/(m-1))*sq)/n
        if se==0: pcluster=0.0 if effect else 1.0
        else: pcluster=min(1.,2*float(stdtr(m-1,-abs(effect/se))))
        pmcnemar=float(binomtest(ir,ir+py,p=.5,alternative='two-sided').pvalue) if ir+py else 1.
        if abs(pcluster-row['cluster_p'])>1e-11 or abs(pmcnemar-row['mcnemar_p'])>1e-11:
            errors.append({'line':line_no,'cluster_delta':pcluster-row['cluster_p'],
                           'mcnemar_delta':pmcnemar-row['mcnemar_p']})
        c=counts[(name,rho,hypothesis)];c[0]+=1;c[1]+=pcluster<.05;c[2]+=pmcnemar<.05
assert len(seen)==21600
for cell in summary['cells']:
    k=(cell['design'],cell['rho'],cell['hypothesis'])
    assert counts[k]==[cell['replicates'],cell['cluster_rejections'],cell['mcnemar_rejections']],(k,counts[k])
report={'records':len(seen),'cells':len(counts),'discrepancies':len(errors),'first_errors':errors[:5],
        'raw_sha256':summary['raw_sha256'],
        'independent_test':'scipy.special.stdtr + scipy.stats.binomtest, explicit repository sums',
        'all_aggregate_counts_match':True}
(HERE/'run323_independent_audit.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2))
assert not errors
