#!/usr/bin/env python3
"""Prospectively frozen pytest #14992 candidate oracle, no reference patch used."""
import hashlib,json,os,platform,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(s):return hashlib.sha256(s.encode()).hexdigest()

def make_case(i):
 target=i<6
 names=('precondition','subject_deps','subject','guard') if i%2==0 else ('ready','dependency','autouse','shield')
 p,d,s,g=names
 # The source code is deliberately kept as a single structural class, not six tasks.
 conftest=f'''import pytest
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
  test=f'''import pytest
from conftest import order
@pytest.mark.usefixtures("{g}")
class TestOrdering:
    def test_guard_precedes_dependency(self):
        assert order[0] == "{g}", order
'''
 else:
  test=f'''import pytest
from conftest import order
@pytest.mark.usefixtures("{g}")
class TestPresence:
    def test_guard_is_present(self):
        assert "{g}" in order, order
'''
 return conftest,test

def run_case(i):
 conftest,test=make_case(i)
 with tempfile.TemporaryDirectory(prefix='lattice408_issue14992_') as td:
  p=Path(td);(p/'conftest.py').write_text(conftest);(p/'test_order.py').write_text(test)
  env=os.environ.copy();env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1';env['PYTHONDONTWRITEBYTECODE']='1'
  cp=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_order.py'],cwd=td,env=env,text=True,capture_output=True,timeout=15)
  return {'case':i,'group':'target_public' if i<3 else 'target_heldout' if i<6 else 'control',
    'conftest_sha256':sha(conftest),'test_sha256':sha(test),'command':['python','-m','pytest','-q','-p','no:cacheprovider','test_order.py'],
    'returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr,'passed':cp.returncode==0}

def main():
 out=HERE/'run408_pytest14992_raw.jsonl'
 with out.open('w') as f:
  for i in range(12):f.write(json.dumps(run_case(i),sort_keys=True)+'\n')
 rows=[json.loads(s) for s in out.read_text().splitlines()]
 summary={'candidate':'pytest-dev/pytest#14992','local_installed_pytest':'9.0.2',
 'control_preflight_pass':sum(r['passed'] for r in rows),'cases':12,
 'targets_pass':sum(r['passed'] for r in rows[:6]),'controls_pass':sum(r['passed'] for r in rows[6:]),
 'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'qualification':'NOT_QUALIFIED_REFERENCE_AND_REGRESSION_NOT_RUN'}
 (HERE/'run408_pytest14992_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
