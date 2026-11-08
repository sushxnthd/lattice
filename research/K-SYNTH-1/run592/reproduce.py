import math
from fractions import Fraction
for R in (1,2,4,8,16,32):
 n=100*R
 rejected=[]
 for k in range(R+1):
  m=max(100*k,n-100*k)
  tail=sum(Fraction(math.comb(n,j),2**n) for j in range(m,n+1))
  if min(Fraction(1),2*tail)<=Fraction(1,20):rejected.append(k)
 rate=sum(Fraction(math.comb(R,k),2**R) for k in rejected)
 print(R,str(rate),float(rate),rejected)
