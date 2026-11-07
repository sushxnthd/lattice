import itertools,json
base=(1,1,0)
records=[]
for full in itertools.product((0,1),repeat=3):
 aggregate_ok=sum(full)>=sum(base)
 identity_ok=all(not b or f for b,f in zip(base,full))
 records.append(dict(full=full,aggregate_ok=aggregate_ok,identity_ok=identity_ok))
false_accept=[r for r in records if r['aggregate_ok'] and not r['identity_ok']]
assert len(records)==8 and len(false_accept)==2
assert {tuple(r['full']) for r in false_accept}=={(1,0,1),(0,1,1)}
print(json.dumps({'base':base,'records':records,'false_accept_count':len(false_accept)},indent=2))