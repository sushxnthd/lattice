import math,json
alpha=.05
rows=[]
for n in [20,40,80,100,120,200,400,800,1000,2000,5000]:
    half=min(1.0,math.sqrt(2*math.log(2/alpha)/n))
    rows.append({'repositories':n,'halfwidth_95':half})
for effect in [.05,.1,.15,.2,.3]:
    n=math.floor(2*math.log(2/alpha)/(effect**2))+1
    assert math.sqrt(2*math.log(2/alpha)/n)<effect
    rows.append({'observed_effect':effect,'minimum_repositories':n})
assert (100-1)/101>0.98 and (1-1)/2==0
print(json.dumps(rows,indent=2))
