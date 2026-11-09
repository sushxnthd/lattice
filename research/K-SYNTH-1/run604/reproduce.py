import itertools,json
def gate(base,a,b,full,targets,controls):
 n=len(base)
 assert all(len(x)==n for x in (a,b,full))
 assert not(set(targets)&set(controls)) and set(targets)|set(controls)==set(range(n))
 return all(full) and all(not base[i] and full[i] for i in targets) and all(base[i] and full[i] for i in controls) and not all(a) and not all(b)
base=(0,0,1,1); full=(1,1,1,1)
pairs=list(itertools.product(itertools.product((0,1),repeat=4),repeat=2))
discord=[(a,b) for a,b in pairs if gate(base,a,b,full,[0,1],[2,3]) and not (not all(a[i] for i in (0,1)) and not all(b[i] for i in (0,1)))]
assert len(discord)==81
print(json.dumps({"ablation_pairs":len(pairs),"joint_qualifies_but_target_only_rejects":len(discord),"first_counterexample":discord[0],"scope":"synthetic gate validation; not production qualification"},indent=2))
