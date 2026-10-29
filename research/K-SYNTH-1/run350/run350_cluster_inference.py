"""Exact paired cluster sign-flip inference and reproducible null calibration.

No scipy dependency. Run only on synthetic signs; no model output is fabricated.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
import json, math, random
from pathlib import Path

ALPHA = 0.05
SEED = 3502026

@lru_cache(maxsize=None)
def mcnemar_exact(ir_only: int, python_only: int) -> float:
    assert isinstance(ir_only, int) and isinstance(python_only, int)
    assert ir_only >= 0 and python_only >= 0
    n = ir_only + python_only
    if n == 0:
        return 1.0
    k = min(ir_only, python_only)
    return min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / (2**n))

def cluster_signflip_exact(scores: list[int]) -> float:
    """Exact two-sided p under independent repository-wise sign symmetry.

    A repository with score 0 is uninformative; removing it does not change p.
    """
    vals = [abs(int(s)) for s in scores if s]
    if not vals:
        return 1.0
    counts = Counter({0: 1})
    for s in vals:
        nxt = Counter()
        for total, multiplicity in counts.items():
            nxt[total+s] += multiplicity
            nxt[total-s] += multiplicity
        counts = nxt
    observed = abs(sum(scores))
    tail = sum(v for total, v in counts.items() if abs(total) >= observed)
    return tail / 2**len(vals)

def wilson95(k: int, n: int) -> list[float]:
    if not n: return [0.0, 1.0]
    z = 1.959963984540054
    p = k / n
    den = 1 + z*z/n
    mid = (p+z*z/(2*n))/den
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0.0,mid-half), min(1.0,mid+half)]

def one_trial(rng: random.Random, repos: int, issues_per_repo: int, rho: float):
    assert 0 <= rho <= 1
    scores = []
    for _ in range(repos):
        if rho == 0:
            p = 0.5
        elif rho == 1:
            p = float(rng.getrandbits(1))
        else:
            a = (1-rho)/(2*rho)
            p = rng.betavariate(a, a)
        wins = sum(rng.random() < p for _ in range(issues_per_repo))
        scores.append(2*wins - issues_per_repo)
    ir = (sum(scores)+repos*issues_per_repo)//2
    py = repos*issues_per_repo-ir
    return {'scores': scores, 'ir_only': ir, 'python_only': py,
            'issue_p': mcnemar_exact(ir, py), 'cluster_p': cluster_signflip_exact(scores)}

def enumerate_shared_signs(repos: int, issues_per_repo: int):
    assert repos <= 20
    tally = Counter()
    examples = []
    for signs in product((-1,1), repeat=repos):
        scores = [s*issues_per_repo for s in signs]
        ir = sum(s > 0 for s in signs)*issues_per_repo
        py = repos*issues_per_repo-ir
        issue_p = mcnemar_exact(ir, py)
        cluster_p = cluster_signflip_exact(scores)
        tally['n'] += 1
        tally['issue_reject'] += issue_p < ALPHA
        tally['cluster_reject'] += cluster_p < ALPHA
        if len(examples)<3 and issue_p<ALPHA and cluster_p>=ALPHA:
            examples.append({'scores':scores,'issue_p':issue_p,'cluster_p':cluster_p})
    return {'repos':repos,'issues_per_repo':issues_per_repo,
            'sign_vectors':tally['n'],'issue_reject':tally['issue_reject'],
            'cluster_reject':tally['cluster_reject'],
            'issue_type1':tally['issue_reject']/tally['n'],
            'cluster_type1':tally['cluster_reject']/tally['n'],
            'counterexamples':examples}

def run(outdir: Path, repetitions=2000):
    outdir.mkdir(parents=True, exist_ok=True)
    rng=random.Random(SEED)
    rows=[]
    summary=[]
    for repos in (8,16,32):
        for rho in (0.0,0.1,0.3,1.0):
            counts={'issue':0,'cluster':0}
            for trial in range(repetitions):
                x=one_trial(rng,repos,4,rho)
                counts['issue'] += x['issue_p'] < ALPHA
                counts['cluster'] += x['cluster_p'] < ALPHA
                rows.append({'repos':repos,'m':4,'rho':rho,'trial':trial,**x})
            summary.append({'repos':repos,'m':4,'rho':rho,'repetitions':repetitions,
                'issue_type1':counts['issue']/repetitions,
                'cluster_type1':counts['cluster']/repetitions,
                'issue_wilson95':wilson95(counts['issue'],repetitions),
                'cluster_wilson95':wilson95(counts['cluster'],repetitions)})
    (outdir/'RUN350_RAW_NULL_TRIALS.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in rows))
    exact=enumerate_shared_signs(8,4)
    (outdir/'RUN350_EXACT_ENUMERATION.json').write_text(json.dumps(exact,indent=2,sort_keys=True)+'\n')
    result={'seed':SEED,'alpha':ALPHA,'null':'symmetric beta-binomial repository effects',
            'total_trials':len(rows),'cells':summary,'exact_fully_correlated':exact,
            'one_repository_counterexample':{'issue_p':mcnemar_exact(8,0),
                                            'cluster_p':cluster_signflip_exact([8])},
            'minimum_two_sided_cluster_p_for_k_informative_repos':
                {str(k):2**(1-k) for k in range(1,9)}}
    (outdir/'RUN350_SUMMARY.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--outdir',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--repetitions',type=int,default=2000)
    a=p.parse_args()
    r=run(a.outdir,a.repetitions)
    print(json.dumps({'trials':r['total_trials'],'exact':r['exact_fully_correlated'],
                      'cells':r['cells']},indent=2))
