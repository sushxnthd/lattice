#!/usr/bin/env python3
"""Frozen issue-first pytest #14992 fixture-order oracle. No reference patch used."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def make_case(i):
    target = i < 6
    p,d,s,g = (("precondition","subject_deps","subject","guard")
               if i%2==0 else ("ready","dependency","autouse","shield"))
    conftest = f'''import pytest
order=[]
@pytest.fixture
def {p}():
    order.append("{p}")
@pytest.fixture
def {d}({p}):
    order.append("{d}")
@pytest.fixture(autouse=True)
def {s}({d}):
    order.append("{s}")
@pytest.fixture
def {g}():
    order.append("{g}")
def pytest_generate_tests(metafunc):
    names=metafunc.fixturenames
    if "{s}" in names:
        names.remove("{s}")
        names.append("{s}")
'''
    if target:
        test = f'''import pytest
from conftest import order
@pytest.mark.usefixtures("{g}")
class TestOrdering:
    def test_guard_precedes_dependency(self):
        assert order[0] == "{g}", order
'''
    else:
        test = f'''import pytest
from conftest import order
@pytest.mark.usefixtures("{g}")
class TestPresence:
    def test_guard_is_present(self):
        assert "{g}" in order, order
'''
    return conftest,test

def run_case(i):
    conftest,test = make_case(i)
    with tempfile.TemporaryDirectory(prefix="lattice408_issue14992_") as td:
        p=Path(td)
        (p/"conftest.py").write_text(conftest)
        (p/"test_order.py").write_text(test)
        env=os.environ.copy()
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"]="1"
        env["PYTHONDONTWRITEBYTECODE"]="1"
        cp=subprocess.run([sys.executable,"-m","pytest","-q","-p",
                           "no:cacheprovider","test_order.py"],
                          cwd=td,env=env,text=True,capture_output=True,timeout=15)
        return {"case":i,"group":"target_public" if i<3 else
                "target_heldout" if i<6 else "control",
                "conftest_sha256":sha(conftest),"test_sha256":sha(test),
                "command":["python","-m","pytest","-q","-p","no:cacheprovider","test_order.py"],
                "returncode":cp.returncode,"stdout":cp.stdout,
                "stderr":cp.stderr,"passed":cp.returncode==0}

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default=".")
    args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    raw=out/"run408_pytest14992_raw.jsonl"
    with raw.open("w") as f:
        for i in range(12):
            f.write(json.dumps(run_case(i),sort_keys=True)+"\n")
    rows=[json.loads(x) for x in raw.read_text().splitlines()]
    summary={"cases":12,"targets_pass":sum(x["passed"] for x in rows[:6]),
             "controls_pass":sum(x["passed"] for x in rows[6:]),
             "raw_sha256":hashlib.sha256(raw.read_bytes()).hexdigest()}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":
    main()
