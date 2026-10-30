"""Read-only independent auditor: never imports historical Jinja source."""
import argparse
import hashlib
import json
from pathlib import Path

BASE={"compiler":"df6fa372e60182cbadabd437a538f3c3997d102e","runtime":"a05b196118bc355c10f1cfff245a958c1089e968"}
REF={"compiler":"50f98f1a9c064e3f270eed5ae547b1138584bce0","runtime":"4a3c36eeaf5a480b824e6c01f4ac6034e4d9e65a"}
VARIANTS={"base":BASE,"compiler_only":{"compiler":REF["compiler"],"runtime":BASE["runtime"]},"runtime_only":{"compiler":BASE["compiler"],"runtime":REF["runtime"]},"full":REF}

def audit(results,shas):
    assert set(results)==set(VARIANTS) and set(shas)==set(VARIANTS)
    rows={}
    for variant,expected_shas in VARIANTS.items():
        assert shas[variant]==expected_shas,("source SHA mismatch",variant)
        d=results[variant]
        assert d["variant"]==variant
        assert len(d["records"])==12
        assert len(set(x["name"] for x in d["records"]))==12
        for r in d["records"]:
            assert r["kind"] in ("target_public","target_heldout","control")
            assert len(r["template_sha256"])==64
            assert r["status"] in ("PASS","FAIL","ERROR")
            if r["status"]=="PASS":assert r["actual"]==r["expected"] and r["error"] is None
            if r["status"]=="FAIL":assert r["actual"]!=r["expected"] and r["error"] is None
            if r["status"]=="ERROR":assert r["actual"] is None and r["error"] is not None
        assert d["counts"]=={s:sum(r["status"]==s for r in d["records"]) for s in ("PASS","FAIL","ERROR")}
        rows[variant]={r["name"]:r for r in d["records"]}
    names=set(rows["base"])
    assert all(set(rows[v])==names for v in VARIANTS)
    matrix=[]
    for name in sorted(names):
        samples=[rows[v][name] for v in VARIANTS]
        assert len({r["template_sha256"] for r in samples})==1
        assert len({r["expected"] for r in samples})==1
        assert len({r["kind"] for r in samples})==1
        row={"name":name,"kind":samples[0]["kind"]}
        for v in VARIANTS:row[v]=int(rows[v][name]["status"]=="PASS")
        row["interaction"]=row["full"]-row["compiler_only"]-row["runtime_only"]+row["base"]
        matrix.append(row)
    targets=[r for r in matrix if r["kind"].startswith("target")]
    controls=[r for r in matrix if r["kind"]=="control"]
    assert len(targets)==6 and len(controls)==6
    def all_pass(v,group):return all(r[v] for r in group)
    full=all_pass("full",matrix)
    baseline=not all_pass("base",targets) and all_pass("base",controls)
    partials=all(not all_pass(v,matrix) for v in ("compiler_only","runtime_only"))
    return {"matrix":matrix,"counts":{v:sum(r[v] for r in matrix) for v in VARIANTS},"reference_full_pass":full,"baseline_targets_fail_controls_pass":baseline,"partials_not_full":partials,"qualified_joint_target_control":full and baseline and partials,"target_interaction_sum":sum(r["interaction"] for r in targets),"control_interaction_sum":sum(r["interaction"] for r in controls)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--results-dir",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    d=Path(a.results_dir)
    results={v:json.loads((d/(v+".json")).read_text()) for v in VARIANTS}
    shas=json.loads((d/"source_shas.json").read_text())
    report=audit(results,shas)
    report["sha256_inputs"]={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.glob("*.json"))}
    Path(a.output).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("matrix","sha256_inputs")},sort_keys=True))

if __name__=="__main__":main()
