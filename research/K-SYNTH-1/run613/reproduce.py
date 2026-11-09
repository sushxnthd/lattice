import itertools,json
rows=[]
for imported,rebound,called in itertools.product((False,True),repeat=3):
    original_calls=int(imported and not rebound and called)
    rows.append(dict(import_executed=imported,rebound=rebound,call_executed=called,static_import_edge=True,original_calls=original_calls))
assert len(rows)==8
assert sum(r['original_calls'] for r in rows)==1
assert sum(r['original_calls']==0 for r in rows if r['import_executed'])==3
out={'experiment':'finite dispatch counterexample','rows':rows,'static_edges':8,'actual_original_invocations':1,'executed_import_no_original_invocation':3}
open('raw.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True))
