"""Exhaustive target-necessity vs control-regression gate audit; not a real repair oracle."""
import itertools, json
rows=[]
for ta,tb,ca,cb in itertools.product((False,True),repeat=4):
    joint=(ta or ca) and (tb or cb)
    target=ta and tb
    rows.append(dict(target_loss_a=ta,target_loss_b=tb,control_regression_a=ca,control_regression_b=cb,joint=joint,target_necessity=target,control_only_joint=joint and not target))
assert len(rows)==16
assert sum(r["joint"] for r in rows)==9
assert sum(r["target_necessity"] for r in rows)==4
assert sum(r["control_only_joint"] for r in rows)==5
print(json.dumps(rows,indent=2))
