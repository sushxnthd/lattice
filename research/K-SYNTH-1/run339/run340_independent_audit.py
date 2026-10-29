"""Independent read-only auditor for frozen HTTPcore #882 public API experiment.

Runs after all four historical arms complete. A failed qualification is a
scientific negative result, not a reason to modify frozen cases.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ARMS=("base_base","ref_sync","ref_async","ref_ref")
CASES={(mode,kind,trailing)
       for mode in ("sync","async")
       for kind in ("connect","upgrade","ordinary")
       for trailing in ((True,False) if kind!="ordinary" else (True,))}
assert len(CASES)==10

def main():
    results={}
    errors=[]
    for arm in ARMS:
        p=ROOT / "raw" / (arm+".json")
        obj=json.loads(p.read_text())
        if obj.get("arm")!=arm or obj.get("scope")!="HISTORICAL_PINNED":
            errors.append("invalid metadata "+arm)
        records=obj["records"]
        if len(records)!=10: errors.append("case count "+arm)
        seen=set()
        for r in records:
            key=(r["mode"],r["kind"],r["trailing"])
            if key not in CASES or key in seen: errors.append("case identity "+arm+" "+str(key))
            seen.add(key)
            expected=([b"HELLO"] if r["kind"]=="ordinary" else
                      [b"HELLO",b"WORLD"] if r["trailing"] else [b"WORLD"])
            expected_hex=[v.hex() for v in expected]
            if r.get("expected") is not None and r["expected"]!=expected_hex:
                errors.append("expected mutated "+arm+" "+str(key))
            status={"connect":200,"upgrade":101,"ordinary":200}[r["kind"]]
            computed=r.get("status")==status and r.get("got")==expected_hex
            if bool(r["ok"])!=bool(computed): errors.append("fabricated pass "+arm+" "+str(key))
            if not isinstance(r.get("trace"),list): errors.append("trace missing "+arm+" "+str(key))
            if r.get("exception") and r["ok"]: errors.append("exception pass "+arm+" "+str(key))
            if "got" in r:
                reads=[t for t in r["trace"] if t[0]=="read"]
                if not reads: errors.append("no reads "+arm+" "+str(key))
                elif r["trailing"] and not bytes.fromhex(reads[0][2]).endswith(b"HELLO"):
                    errors.append("first raw chunk missing trailing bytes "+arm+" "+str(key))
        if seen!=CASES: errors.append("missing cases "+arm)
        results[arm]=records
    if errors: raise AssertionError(errors)
    def target(r):return r["kind"]!="ordinary" and r["trailing"]
    def control(r):return not target(r)
    def counts(arm):
        rows=results[arm]
        return {"targets":sum(r["ok"] for r in rows if target(r)),
                "controls":sum(r["ok"] for r in rows if control(r)),
                "exceptions":[{"mode":r["mode"],"kind":r["kind"],"type":r.get("exception")}
                              for r in rows if "exception" in r]}
    c={a:counts(a) for a in ARMS}
    reasons=[]
    if c["base_base"]["targets"]>=4:reasons.append("baseline did not fail a target")
    if c["base_base"]["controls"]!=6:reasons.append("baseline control regression")
    if c["ref_ref"]["targets"]!=4 or c["ref_ref"]["controls"]!=6:
        reasons.append("full reference not all target+control correct")
    for arm,unrepaired in (("ref_sync","async"),("ref_async","sync")):
        if c[arm]["controls"]!=6:reasons.append(arm+" control regression")
        missing=[r for r in results[arm] if target(r) and r["mode"]==unrepaired and not r["ok"]]
        if not missing:reasons.append(arm+" lacks necessary unrepaired target failure")
        if any(e["type"]=="TypeError" for e in c[arm]["exceptions"]):
            reasons.append(arm+" ABI_CONFOUNDED: TypeError")
    decision={"qualified":not reasons,"reasons":reasons,"counts":c,
              "scope":"exact frozen 10-case public API only, no model inference"}
    (ROOT/"raw"/"decision.json").write_text(json.dumps(decision,indent=2)+"\n")
    print(json.dumps(decision,indent=2))
if __name__=="__main__":main()
