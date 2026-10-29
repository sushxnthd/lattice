"""Executable exact-null counterexample to issue-level McNemar under clustering."""
from itertools import product
from math import comb
import json

def mcnemar(b,c):
    n=b+c
    return min(1.,2*sum(comb(n,j) for j in range(min(b,c)+1))/2**n) if n else 1.

def cluster_p(scores):
    target=abs(sum(scores))
    return sum(abs(sum(a*s for a,s in zip(signs,scores)))>=target
               for signs in product((-1,1),repeat=len(scores)))/2**len(scores)

def exact_null(repos=8,issues_per_repo=4):
    issue_reject=cluster_reject=0
    for signs in product((-1,1),repeat=repos):
        scores=[issues_per_repo*s for s in signs]
        b=issues_per_repo*sum(s>0 for s in signs)
        c=issues_per_repo*sum(s<0 for s in signs)
        issue_reject+=mcnemar(b,c)<.05
        cluster_reject+=cluster_p(scores)<.05
    n=2**repos
    return {'repos':repos,'issues_per_repo':issues_per_repo,
            'null_sign_vectors':n,'issue_rejections':issue_reject,
            'cluster_rejections':cluster_reject,
            'issue_type1':issue_reject/n,'cluster_type1':cluster_reject/n}

if __name__=='__main__':
    result=exact_null()
    assert (result['issue_rejections'],result['cluster_rejections'])==(74,2)
    print(json.dumps(result,indent=2))
