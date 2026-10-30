#!/usr/bin/env python3
"""Independent read-only verifier for four HTTPX #1532 historical arms."""
import json
import sys
from pathlib import Path

EXPECTED={
 "P01":("public","url","/somewhere-else"),
 "P02":("public","url","/path/to/somewhere-else"),
 "P03":("public","client","https://example.org/some/path/sub:path"),
 "H01":("heldout","url","/path/somewhere-else"),
 "H02":("heldout","url","/somewhere-else"),
 "H03":("heldout","client","https://example.org/some/path/testing:123"),
 "C01":("control","url","https://example.org/c"),
 "C02":("control","url","https://example.org/c"),
 "C03":("control","client","https://example.org/a/b/c"),
 "C04":("control","client","https://example.org/a/b/c"),
 "C05":("control","client","https://other.org/x"),
 "C06":("control","url","https://other.org/x"),
 "C07":("control","url","https://example.org/a/b#frag"),
}
ARMS=("client0_models0","client1_models0","client0_models1","client1_models1")
def audit(paths):
 if set(paths)!=set(ARMS):raise ValueError("missing or extra arm")
 observed={}
 for arm in ARMS:
  d=json.loads(Path(paths[arm]).read_text())
  if d.get("schema")!="lattice.run368.oracle.v1" or d.get("arm")!=arm or "fatal" in d:raise ValueError("bad schema/arm/fatal "+arm)
  rows=d.get("rows")
  if not isinstance(rows,list) or len(rows)!=len(EXPECTED):raise ValueError("bad row count "+arm)
  m={}
  for r in rows:
   ident=r["id"]
   if ident not in EXPECTED or ident in m:raise ValueError("duplicate or unknown id")
   group,kind,expected=EXPECTED[ident]
   if (r["group"],r["kind"],r["expected"])!=(group,kind,expected):raise ValueError("oracle contract changed")
   calc=r.get("error") is None and r.get("actual")==expected
   if r.get("passed") is not calc:raise ValueError("incorrect pass flag")
   m[ident]=calc
  if set(m)!=set(EXPECTED):raise ValueError("missing case")
  observed[arm]=m
 matrix={a:{g:sum(observed[a][i] for i,(group,_,_) in EXPECTED.items() if group==g) for g in ("public","heldout","control")} for a in ARMS}
 interaction={i:int(observed[ARMS[3]][i])-int(observed[ARMS[1]][i])-int(observed[ARMS[2]][i])+int(observed[ARMS[0]][i]) for i in EXPECTED}
 base=matrix[ARMS[0]];full=matrix[ARMS[3]]
 qualified=(base["control"]==7 and base["public"]+base["heldout"]<6 and full=={"public":3,"heldout":3,"control":7} and all(matrix[a]["public"]+matrix[a]["heldout"]<6 for a in ARMS[1:3]) and all(matrix[a]["control"]==7 for a in ARMS))
 return dict(schema="lattice.run368.audit.v1",matrix=matrix,case_interactions=interaction,casewise_nonzero=sum(x!=0 for x in interaction.values()),historical_reference_qualified=qualified,reference_blind=False,number_observations=52,model_completions=0)
if __name__=="__main__":
 paths={a:sys.argv[i+1] for i,a in enumerate(ARMS)}
 print(json.dumps(audit(paths),sort_keys=True,indent=2))
