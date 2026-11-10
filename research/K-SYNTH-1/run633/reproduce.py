"""Run633: fail-closed oracle completeness and provenance audit, synthetic only."""
import itertools,json,pathlib
OUT=pathlib.Path(__file__).parent
def verdict(v):
    if any(x is None for x in v): return 'UNKNOWN'
    b,a,c,f=[v[i:i+3] for i in range(0,12,3)]
    return 'PASS' if b[0]==0 and f==(1,1,1) and a[0]==0 and c[0]==0 and b[1:]==(1,1) else 'FAIL'
counts={'PASS':0,'FAIL':0,'UNKNOWN':0}
examples={}
for v in itertools.product((0,1,None),repeat=12):
    result=verdict(v);counts[result]+=1;examples.setdefault(result,v)
missing=(0,1,1,0,1,1,0,1,1,1,1,None)
complete=(0,1,1,0,1,1,0,1,1,1,1,1)
assert verdict(missing)=='UNKNOWN' and verdict(complete)=='PASS'
assert sum(counts.values())==3**12
for i in range(12):
    z=list(complete);z[i]=None;assert verdict(tuple(z))=='UNKNOWN'
report={'scope':'synthetic gate only; no real task qualification','total':3**12,'counts':counts,'examples':{k:list(v) for k,v in examples.items()},'counterexample':{'missing':list(missing),'missing_verdict':verdict(missing),'complete':list(complete),'complete_verdict':verdict(complete)},'deletion_tests':12}
(OUT/'raw.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'total':report['total'],'counts':counts,'deletion_tests':12}))
