import itertools,json
arms=((0,0),(1,0),(0,1),(1,1))
def gate(y): return y[(1,1)]==1 and all(y[k]==0 for k in arms[:3])
rows=[]
for env in itertools.product((0,1),repeat=4):
 y=dict(zip(arms,env)); rows.append({'environment':env,'false_qualification':gate(y)})
assert sum(r['false_qualification'] for r in rows)==1
for e in (0,1): assert not gate({k:e for k in arms})
print(json.dumps({'assignments':16,'false_qualifications':1,'rows':rows},indent=2))
