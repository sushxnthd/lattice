#!/usr/bin/env python3
"""Post-reference finite factorial theorem; input is original Run424 cloud raw JSON.

Download original artifact from GitHub Actions run 41368162492.
No source execution, oracle modification, or task requalification.
"""
import itertools,json,sys
raw=json.load(open(sys.argv[1],encoding='utf-8'))
flags=list(itertools.product((0,1),repeat=3))
a={tuple(v['flags']):v['observations'] for v in raw['arms']}
assert len(a)==8 and set(a)==set(flags)
keys=sorted(a[(0,0,0)])
assert len(keys)==70 and all(set(a[f])==set(keys) for f in flags)
deps={}
for k in keys:
 deps[k]=tuple(i for i in range(3) if any(
  a[f][k]!=a[tuple(1-v if j==i else v for j,v in enumerate(f))][k]
  for f in flags))
counts={d:sum(x==d for x in deps.values()) for d in ((),(0,),(1,),(2,))}
assert counts=={():60,(0,):2,(1,):6,(2,):2}
assert not any(len(d)>1 for d in deps.values())
def sig(f,rows):return tuple(json.dumps(a[f][k],sort_keys=True) for k in rows)
for n in (1,2):
 for rows in itertools.combinations(keys,n):
  assert len({sig(f,rows) for f in flags})<8
witness=['samehost_http_80','proxy_http_0','netloc_http_0']
assert [deps[k] for k in witness]==[(0,),(1,),(2,)]
assert len({sig(f,witness) for f in flags})==8
base=a[(0,0,0)];full=a[(1,1,1)]
assert sum(base[k]!=full[k] for k in keys)==10
assert [k for k in keys if k.startswith('samehost_') and base[k]!=full[k]]==['samehost_http_80','samehost_https_443']
print(json.dumps({'status':'PASS','rows':70,'arms':8,'constant':60,'component_only':[2,6,2],
                  'interaction_rows':0,'minimum_separating_rows':3,'post_outcome_witness':witness,
                  'original_frozen_gate':'FAILED','new_qualified_task':False},sort_keys=True))
