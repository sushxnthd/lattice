"""Read-only casewise 2x2 interaction diagnostic for immutable Run340 records.

Does not infer source-level semantic interaction from Boolean outcomes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ARMS=("base_base","ref_sync","ref_async","ref_ref")
REQUIRED=("mode","kind","trailing","ok","expected","got","trace")
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def case_key(r):
    return (r["mode"],r["kind"],r["trailing"])
def check(r):
    if not isinstance(r,dict) or any(k not in r for k in REQUIRED):
        raise ValueError("missing required record fields")
    if type(r["trailing"]) is not bool or type(r["ok"]) is not bool:
        raise ValueError("invalid Boolean field")
    if r["mode"] not in ("sync","async") or r["kind"] not in ("connect","upgrade","ordinary"):
        raise ValueError("unexpected case")
    if not isinstance(r["got"],list) or not isinstance(r["expected"],list) or not isinstance(r["trace"],list):
        raise ValueError("invalid record structure")
    for value in r["got"]+r["expected"]:
        if not isinstance(value,str) or len(value)%2:
            raise ValueError("invalid hex")
        try: bytes.fromhex(value)
        except ValueError as exc: raise ValueError("invalid hex") from exc
    expected_status={"connect":200,"upgrade":101,"ordinary":200}[r["kind"]]
    if r["ok"] != (r["got"]==r["expected"] and r.get("status")==expected_status):
        raise ValueError("outcome mismatch")
def load(directory):
    directory=Path(directory)
    arms={};manifest={}
    for arm in ARMS:
        path=directory/(arm+".json")
        data=json.loads(path.read_text())
        if data.get("arm")!=arm or data.get("scope")!="HISTORICAL_PINN":
            raise ValueError("arm/scope mismatch")
        records=data.get("records")
        if not isinstance(records,list) or len(records)!=10:
            raise ValueError("unexpected record count")
        indexed={}
        for r in records:
            check(r)
            k=case_key(r)
            if k in indexed:raise ValueError("duplicate case")
            indexed[k]=r
        arms[arm]=indexed
        manifest[arm]={"sha256":sha(path),"records":len(records)}
    keys=set(arms[ARMS[0]])
    if any(set(arms[a])!=keys for a in ARMS):
        raise ValueError("case mismatch")
    for k in keys:
        if len({tuple(arms[a][k]["expected"]) for a in ARMS})!=1:
            raise ValueError("expected output drift")
    return arms,manifest
def analyze(arms):
    rows=[]
    keys=sorted(arms[ARMS[0]],key=lambda k:(k[1],k[2],k[0]))
    for k in keys:
        a,b,c,d=(int(arms[arm][k]["ok"]) for arm in ARMS)
        delta=d-b-c+a
        if delta>0:label="POSITIVE_OUTCOME_INTERACTION"
        elif delta<0:label="NEGATIVE_OUTCOME_INTERACTION"
        elif (a,b,c,d)==(0,1,0,1):label="SYNC_ONLY_OBSERVED"
        elif (a,b,c,d)==(0,0,1,1):label="ASYNC_ONLY_OBSERVED"
        elif len({a,b,c,d})==1:label="NO_OUTCOME_CHANGE"
        else:label="ZERO_CONTRAST_OTHER"
        rows.append({"case":{"mode":k[0],"kind":k[1],"trailing":k[2]},
                     "outcomes":dict(zip(ARMS,(a,b,c,d))),
                     "interaction":delta,"class":label,
                     "semantic_interaction":"UNKNOWN","abi_compatibility":"UNKNOWN"})
    return {"rows":rows,"aggregate_interaction":sum(r["interaction"] for r in rows),
            "sum_absolute_casewise_interaction":sum(abs(r["interaction"]) for r in rows),
            "nonzero_casewise":sum(r["interaction"]!=0 for r in rows),
            "counts":{arm:sum(arms[arm][k]["ok"] for k in keys) for arm in ARMS},
            "semantic_mechanism_certified":False}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    arms,manifest=load(args.input)
    result={"scope":"POST_OUTCOME_READ_ONLY","input_manifest":manifest,
            "diagnostic":analyze(arms),
            "limits":["finite observed cases only","ABI status UNKNOWN",
                      "Boolean outcome interaction does not prove semantic dataflow",
                      "no new model inference"]}
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"cases":len(result["diagnostic"]["rows"]),
                      "aggregate":result["diagnostic"]["aggregate_interaction"],
                      "casewise_nonzero":result["diagnostic"]["nonzero_casewise"]}))
if __name__=="__main__":
    main()
