"""Exact repository-cluster sign-flip enumeration; constructed counterexample, not model evidence."""
from fractions import Fraction
from itertools import product
from math import comb

def p_cluster(margins):
    observed=sum(margins)
    return Fraction(sum(sum(s*x for s,x in zip(signs,margins))>=observed for signs in product((-1,1),repeat=len(margins))),2**len(margins))

def p_issue(wins,losses):
    n=wins+losses
    return Fraction(sum(comb(n,k) for k in range(wins,n+1)),2**n)

A=[10,10,10,10,-10,-10]
B=[5]*8+[-5]*4
assert sum(x for x in A if x>0)==sum(x for x in B if x>0)==40
assert -sum(x for x in A if x<0)==-sum(x for x in B if x<0)==20
assert p_cluster(A)==Fraction(11,32)
assert p_cluster(B)==Fraction(397,2048)
assert p_cluster(A)!=p_cluster(B)
assert p_issue(40,20)<Fraction(1,100)
assert p_cluster([0,0,1])==Fraction(1,2)
print('A',p_cluster(A),'B',p_cluster(B),'naive',p_issue(40,20))
print('PASS: exact rational enumeration and nonidentifiability witness')
