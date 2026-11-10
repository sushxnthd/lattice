import itertools,json
rows=[]
for bits in itertools.product((0,1),repeat=12):
    base,A,B,full=[bits[i:i+3] for i in range(0,12,3)]
    accepted=(full==(1,1,1) and base[2]==1 and base[:2]!=(1,1) and A[:2]!=(1,1) and B[:2]!=(1,1) and A[2]==1 and B[2]==1)
    witness=any(base[i]==0 and A[i]==0 and B[i]==0 and full[i]==1 for i in (0,1))
    if accepted: rows.append(dict(base=base,A=A,B=B,full=full,witness=witness))
assert len(rows)==27 and sum(not r["witness"] for r in rows)==12
print(json.dumps({"accepted":len(rows),"without_within_target_interaction":12,"rows":rows},indent=2))
