import itertools,json,collections
rows=[]
for bits in itertools.product((0,1),repeat=6):
    target=sum(bits[:3]); control=sum(bits[3:])
    joint=(target<3 or control<3)
    necessary=target<3
    rows.append({'mask':''.join(map(str,bits)),'target_pass':target,'control_pass':control,'joint_gate':joint,'target_necessary':necessary,'control_only':joint and not necessary})
counts=dict(collections.Counter('target_necessary' if r['target_necessary'] else 'control_only' if r['control_only'] else 'neither' for r in rows))
assert counts=={'target_necessary':56,'control_only':7,'neither':1},counts
print(json.dumps({'scope':'exhaustive synthetic 3 target x 3 control ablation outcome patterns','counts':counts,'rows':rows},indent=2))
