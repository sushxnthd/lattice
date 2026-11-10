import math
from statistics import NormalDist
# Approximate cluster sensitivity; rho is hypothetical, not measured.
for n in (306,681,800):
 for repos in (50,100,200):
  for rho in (0,.05,.10,.20):
   deff=1+(n/repos-1)*rho
   neff=n/deff
   for p in (.60,.65):
    delta=2*p-1
    z=delta*math.sqrt(neff*.30)/math.sqrt(1-delta*delta)
    power=NormalDist().cdf(z-1.95996398454)+NormalDist().cdf(-z-1.95996398454)
    print(n,repos,rho,p,round(neff,3),round(power,6))
