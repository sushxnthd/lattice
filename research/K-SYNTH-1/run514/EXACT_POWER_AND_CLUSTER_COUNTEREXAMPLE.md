# Run514: Exact paired-power audit and cluster-identifiability counterexample

Date: 2026-11-05 UTC. Kernel: K-SYNTH-1. Status: methodological result, NOT production repair or model evidence.

## Exact calculations
For each issue, independent discordance D~Binomial(n,0.30); conditional on D=d, IR-only wins W~Binomial(d,p). Reject the two-sided exact McNemar test when 2 Pr[Binomial(d,0.5)>=max(W,d-W)] <=0.05. Sum the conditional rejection probability over D. This is **unclustered** power only.

| n | p=.60 | p=.65 |
|---:|---:|---:|
| 100 | 0.142708 | 0.303991 |
| 306 | 0.443642 | 0.800367 |
| 400 | 0.558530 | 0.898777 |
| 681 | 0.800498 | 0.989749 |
| 800 | 0.862140 | 0.996393 |

## New finite identifiability counterexample
Suppose there are 20 independent repositories, each contributing 10 perfectly correlated discordant issues, all ten with the same sign. A naive pooled McNemar calculation sees 200 discordant issue-level votes; in fact there are only 20 independent sign units. Under the sharp null, each repository's sign is an independent fair coin. A repository-aware exact two-sided sign test is the correct randomization distribution for this construction. Multiplying every repository's issues by ten does not add independent evidence. Any power forecast based solely on issue count, discordance and conditional win fraction is non-identifiable without a cluster dependence assumption.

## Protocol consequence
Pre-register repository as the randomization/inference unit or justify a cluster-aware method; do not treat 306/681 as guaranteed powered targets. Preserve repository IDs and within-repository paired outcomes. Do not use this synthetic construction to claim empirical IR performance.

## Executable reproduction
```javascript
function tail(n,k,p){
  if(k>n)return 0;
  let term=Math.pow(1-p,n), sum=0;
  for(let j=0;j<=n;j++){
    if(j>=k)sum+=term;
    if(j<n)term*=((n-j)/(j+1))*(p/(1-p));
  }
  return sum;
}
function critical(d){
  let k=Math.floor(d/2)+1;
  while(k<=d && 2*tail(d,k,0.5)>0.05)k++;
  return k;
}
function power(n,discord,win){
  let term=Math.pow(1-discord,n),total=0;
  for(let d=0;d<=n;d++){
    let k=critical(d);
    total+=term*(tail(d,k,win)+tail(d,k,1-win));
    if(d<n)term*=((n-d)/(d+1))*discord/(1-discord);
  }
  return total;
}
for(const n of [100,306,400,681,800])
  for(const p of [0.60,0.65])
    console.log(n,p,power(n,0.30,p));
```

No new real task qualified; two previously qualified tasks remain. No model inference. All 89 reserved issues sealed. No PR merge authorized.