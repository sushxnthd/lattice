"""Run518: prospective 2x2 qualification gate. stdlib only. Execute: python3 run518_gate.py
No historical task is promoted by this script. Inputs must be frozen before oracle execution.
"""
import hashlib, json
from pathlib import Path

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def freeze(spec):
    assert set(spec)=={"repo","pr","base_sha","reference_sha","source_paths","targets","controls","oracle","holdout_commitment"}
    assert len(spec["source_paths"])>=2 and len(set(spec["source_paths"]))>=2
    assert spec["targets"] and spec["controls"] and not (set(spec["targets"])&set(spec["controls"]))
    assert all(len(spec[k])==40 for k in ("base_sha","reference_sha"))
    assert len(spec["holdout_commitment"])==64
    return digest(spec)

def qualify(spec, frozen_sha, observations):
    if digest(spec)!=frozen_sha: return "REJECT_FREEZE_MISMATCH"
    required={"base","component_a","component_b","full"}
    if set(observations)!=required: return "REJECT_MISSING_ARM"
    ids=set(spec["targets"])|set(spec["controls"])
    if any(set(v)!=ids or any(type(x) is not bool for x in v.values()) for v in observations.values()):
        return "REJECT_ORACLE_MATRIX"
    t,c=spec["targets"],spec["controls"]
    base,a,b,full=(observations[k] for k in ("base","component_a","component_b","full"))
    if not all(not base[x] and full[x] for x in t): return "REJECT_TARGET_REPAIR"
    if not all(base[x] and full[x] for x in c): return "REJECT_CONTROL_REGRESSION"
    # Necessity means each component's removal fails at least one target OR control.
    if all(a[x] for x in ids) or all(b[x] for x in ids): return "REJECT_COMPONENT_NOT_NECESSARY"
    # More stringent target-specific requirement: each removal must fail at least one TARGET.
    # This rejects the historical PR2535 control-only interaction confound.
    if all(a[x] for x in t) or all(b[x] for x in t): return "REJECT_TARGET_ONLY_NECESSITY"
    return "QUALIFIED_CONDITIONAL_ON_INDEPENDENT_ORACLE"

def selftest():
    s=dict(repo="example/repo",pr=123,base_sha="a"*40,reference_sha="b"*40,
           source_paths=["pkg/a.py","pkg/b.py"],targets=["t1","t2"],controls=["c1","c2"],
           oracle="isolated-immutable-v1",holdout_commitment="c"*64)
    f=freeze(s)
    good={"base":{"t1":False,"t2":False,"c1":True,"c2":True},
          "component_a":{"t1":True,"t2":False,"c1":True,"c2":True},
          "component_b":{"t1":False,"t2":True,"c1":True,"c2":True},
          "full":{"t1":True,"t2":True,"c1":True,"c2":True}}
    assert qualify(s,f,good)=="QUALIFIED_CONDITIONAL_ON_INDEPENDENT_ORACLE"
    # Both single-component arms can fail solely on controls: not enough.
    confounded={"base":good["base"],"component_a":{"t1":True,"t2":True,"c1":False,"c2":True},
                "component_b":{"t1":True,"t2":True,"c1":True,"c2":False},"full":good["full"]}
    assert qualify(s,f,confounded)=="REJECT_TARGET_ONLY_NECESSITY"
    assert qualify(dict(s,pr=124),f,good)=="REJECT_FREEZE_MISMATCH"
    assert qualify(s,f,{k:v for k,v in good.items() if k!="component_a"})=="REJECT_MISSING_ARM"
    print(json.dumps({"checks":4,"status":"PASS","freeze_sha256":f,"confounded":"REJECT_TARGET_ONLY_NECESSITY"},sort_keys=True))
if __name__=="__main__": selftest()
