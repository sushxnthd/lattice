"""Run456: exact conditional two-sided McNemar power, independent-issue planning only."""
from scipy.stats import binom
def threshold(d,alpha=.05):
    return next((k for k in range(d//2+1,d+1) if 2*binom.sf(k-1,d,.5)<=alpha),d+1)
def power(n,q,p):
    return sum(binom.pmf(d,n,q)*binom.sf(threshold(d)-1,d,p) for d in range(n+1))
def design_effect(m,rho): return 1+(m-1)*rho
if __name__=="__main__":
    for n in (306,400,681,800):
        for p in (.60,.65):
            print(n,p,round(power(n,.30,p),8))
    for d in range(1,41):
        k=threshold(d)
        if k<=d: assert 2*binom.sf(k-1,d,.5)<=.050000000001
        if k>d//2+1: assert 2*binom.sf(k-2,d,.5)>.049999999999
    assert design_effect(5,.25)==2
