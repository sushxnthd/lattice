import itertools,json
keys=['t1','t2','c1','c2']
counts={'joint':0,'target':0,'joint_only':0,'neither':0}
for a,b in itertools.product(itertools.product((False,True),repeat=4),repeat=2):
    joint=all(not all(bits) for bits in (a,b))
    target=all(not all(bits[:2]) for bits in (a,b))
    counts['joint']+=joint
    counts['target']+=target
    counts['joint_only']+=joint and not target
    counts['neither']+=not joint and not target
assert counts=={'joint':225,'target':144,'joint_only':81,'neither':31}
print(json.dumps(counts,sort_keys=True))
