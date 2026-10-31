#!/usr/bin/env python3
"""Independent-repository Hoeffding weak-null bound and exact null counterexample."""
from fractions import Fraction
from math import comb, exp, log, sqrt

def weak_null_bound(cluster_means, weights=None, alpha=.05):
    """Assumes independent bounded [-1,1] repository means and fixed weights.

    The null is the zero weighted average of expected repository effects,
    not conditional sign exchangeability. No guarantee for handpicked tasks.
    """
    n=len(cluster_means)
    if not n or any(not -1<=x<=1 for x in cluster_means):
        raise ValueError('invalid bounded repository means')
    w=weights if weights is not None else [1/n]*n
    if len(w)!=n or any(x<0 for x in w) or abs(sum(w)-1)>1e-12:
        raise ValueError('weights must be nonnegative, fixed, sum to one')
    if not 0<alpha<1:raise ValueError('invalid alpha')
    mu=sum(x*y for x,y in zip(cluster_means,w))
    v=sum(x*x for x in w)
    p=min(1.,2*exp(-mu*mu/(2*v)))
    radius=sqrt(2*v*log(2/alpha))
    return {'estimate':mu,'p_upper':p,'ci':[max(-1.,mu-radius),min(1.,mu+radius)],
            'effective_repositories':1/v,'reject':p<=alpha}

def exact_signflip_p(totals):
    """Exact signflip orbit, valid for sharp sign-exchangeability only."""
    dist={0:1}
    for x in totals:
        if not x:continue
        a=abs(x);nxt={}
        for s,k in dist.items():
            nxt[s+a]=nxt.get(s+a,0)+k
            nxt[s-a]=nxt.get(s-a,0)+k
        dist=nxt
    extreme=sum(k for s,k in dist.items() if abs(s)>=abs(sum(totals)))
    return Fraction(extreme,sum(dist.values()))

def exact_weak_null_failure(n=20):
    """X=+1 with p=1/6, X=-1/5 with p=5/6; E[X]=0 exactly."""
    if not 1<=n<=50:raise ValueError('n outside supported range')
    signflip=hoeffding=0
    for j in range(n+1):
        mass=comb(n,j)*5**(n-j)
        totals=[5]*j+[-1]*(n-j)
        if exact_signflip_p(totals)<=Fraction(1,20):signflip+=mass
        mu=(6*j-n)/(5*n)
        if min(1.,2*exp(-n*mu*mu/2))<=.05:hoeffding+=mass
    return {'n':n,'sharp_signflip_false_positive':str(Fraction(signflip,6**n)),
            'weak_null_hoeffding_false_positive':str(Fraction(hoeffding,6**n))}

if __name__=='__main__':
    print(exact_weak_null_failure())
    for n in (60,135,500,1000):
        print('repos',n,'95pct_weak_null_halfwidth',round(sqrt(2*log(40)/n),6))
