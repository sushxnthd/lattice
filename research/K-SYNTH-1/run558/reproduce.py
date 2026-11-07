import itertools,json
base='abc'
edits=[(a,b,s) for a in range(4) for b in range(a,4) for s in ('','X')]
def atomic(es):
 if any(max(a,c)<min(b,d) or a==c for (a,b,_),(c,d,_) in itertools.combinations(es,2)): return None
 out=base
 for a,b,s in sorted(es,key=lambda e:e[0],reverse=True):out=out[:a]+s+out[b:]
 return out
def seq(es):
 out=base
 for a,b,s in es:out=out[:a]+s+out[b:]
 return out
records=[]
for x,y in itertools.product(edits,repeat=2):
 a=atomic([x,y]);f=seq([x,y]);r=seq([y,x])
 records.append((x,y,a,f,r))
valid=[z for z in records if z[2] is not None]
assert len(records)==400 and len(valid)==232
assert sum(f!=r for _,_,_,f,r in valid)==78
assert sum(a!=f for _,_,a,f,_ in valid)==39
assert all(a==atomic([y,x]) for x,y,a,_,_ in valid)
print(json.dumps({'total':400,'valid':232,'conflicts':168,'naive_order_sensitive':78,'naive_forward_mismatch':39}))
