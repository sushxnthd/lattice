#!/usr/bin/env python3
"""Run405 issue-first frozen black-box qualification probe for pytest #14997.
No reference patch, fix localization, or model inference. Do not retune.
"""
import hashlib,json,os,platform,subprocess,sys,tempfile,time
from pathlib import Path

FILES={
"tests/__init__.py":"",
"tests/conftest.py":"",
"tests/test_top.py":"def test_top():\n    assert True\n",
"tests/test_top2.py":"def test_top2():\n    assert True\n",
"tests/pkg/__init__.py":"",
"tests/pkg/conftest.py":"import pytest\n@pytest.fixture\ndef widget():\n    return 31\n",
"tests/pkg/test_a.py":"def test_a(widget):\n    assert widget == 31\n",
"tests/pkg/test_b.py":"def test_b(widget):\n    assert widget == 31\n",
"tests/pkg/test_c.py":"def test_c(widget):\n    assert widget == 31\n",
"tests/pkg2/__init__.py":"",
"tests/pkg2/conftest.py":"import pytest\n@pytest.fixture\ndef gadget():\n    return 47\n",
"tests/pkg2/test_a.py":"def test_a(gadget):\n    assert gadget == 47\n",
"tests/pkg2/test_b.py":"def test_b(gadget):\n    assert gadget == 47\n",
"tests/pkg2/test_c.py":"def test_c(gadget):\n    assert gadget == 47\n"}
CASES=[
("P1","public_target",["tests/pkg/test_a.py","tests/test_top.py","tests/pkg/test_b.py"]),
("P2","public_target",["tests/pkg2/test_a.py","tests/test_top.py","tests/pkg2/test_b.py"]),
("P3","public_target",["tests/pkg/test_a.py","tests/test_top2.py","tests/pkg/test_c.py"]),
("H1","heldout_target",["tests/pkg2/test_b.py","tests/test_top2.py","tests/pkg2/test_c.py"]),
("H2","heldout_target",["tests/pkg/test_b.py","tests/test_top.py","tests/pkg/test_c.py"]),
("H3","heldout_target",["tests/pkg2/test_a.py","tests/test_top2.py","tests/pkg2/test_c.py"]),
("C1","control",["tests/test_top.py","tests/pkg/test_a.py","tests/pkg/test_b.py"]),
("C2","control",["tests/pkg/test_a.py","tests/pkg/test_b.py","tests/test_top.py"]),
("C3","control",["tests/pkg/test_a.py","tests/pkg/test_b.py"]),
("C4","control",["tests/pkg2/test_a.py","tests/pkg2/test_b.py"]),
("C5","control",["tests/test_top2.py","tests/pkg2/test_b.py","tests/pkg2/test_c.py"]),
("C6","control",["tests/test_top.py","tests/test_top2.py"])]
REQUIREMENTS={"baseline_public_target_failures_min":2,"baseline_heldout_target_failures_min":2,"baseline_controls_success":6,"reference_all_targets_success":6,"reference_all_controls_success":6,"single_source_ablation_joint_behavioral_necessity":True,"neutral_shim_verified_independently":True,"no_requalification_after_outcome":True}
def main():
    out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lattice405_") as tmp:
        root=Path(tmp)
        for name,src in FILES.items():
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(src,encoding="utf-8")
        env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONHASHSEED="0",PYTHONDONTWRITEBYTECODE="1")
        env.pop("PYTHONPATH",None)
        version=subprocess.run([sys.executable,"-c","import pytest;print(pytest.__version__);print(pytest.__file__)"],text=True,capture_output=True,timeout=30,env=env)
        rows=[]
        for cid,kind,args in CASES:
            cmd=[sys.executable,"-m","pytest","-q","-p","no:cacheprovider","--disable-warnings",*args]
            start=time.monotonic()
            try:
                p=subprocess.run(cmd,cwd=root,env=env,text=True,capture_output=True,timeout=45)
                status="PASS" if p.returncode==0 else "FAIL"
                result=dict(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
            except subprocess.TimeoutExpired as e:
                status="TIMEOUT";result=dict(returncode=None,stdout=str(e.stdout),stderr=str(e.stderr))
            rows.append(dict(id=cid,kind=kind,argv=args,status=status,elapsed_sec=round(time.monotonic()-start,5),**result))
        record=dict(schema="lattice.run405.pytest14997.v1",issue="pytest-dev/pytest#14997",version_stdout=version.stdout,version_stderr=version.stderr,version_rc=version.returncode,python=platform.python_version(),platform=platform.platform(),source_sha256={k:hashlib.sha256(v.encode()).hexdigest() for k,v in sorted(FILES.items())},requirements=REQUIREMENTS,rows=rows)
        (out/"raw_oracle.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
        s={k:sum(r["status"]=="PASS" for r in rows if r["kind"]==k) for k in ["public_target","heldout_target","control"]}
        s.update(all_cases=len(rows),baseline_eligible=s["public_target"]<=1 and s["heldout_target"]<=1 and s["control"]==6,version_stdout=version.stdout.strip())
        (out/"summary.json").write_text(json.dumps(s,indent=2,sort_keys=True)+"\n")
        print(json.dumps(s,sort_keys=True))
if __name__=="__main__":main()
