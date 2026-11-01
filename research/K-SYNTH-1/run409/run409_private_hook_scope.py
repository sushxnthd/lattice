#!/usr/bin/env python3
"""Run409 post-outcome scope diagnostic. Not a new qualification endpoint."""
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path
from importlib.metadata import version
HERE=Path(__file__).resolve().parent
def sha(x):return hashlib.sha256(x.encode()).hexdigest()
def sources(hook, expected):
    conf='''import pytest
order=[]
@pytest.fixture
def precondition():
    order.append("precondition")
@pytest.fixture
def subject_deps(precondition):
    order.append("subject_deps")
@pytest.fixture(autouse=True)
def subject(subject_deps):
    order.append("subject")
@pytest.fixture
def guard():
    order.append("guard")
'''
    if hook:
        conf+='''def pytest_generate_tests(metafunc):
    names=metafunc.fixturenames
    if "subject" in names:
        names.remove("subject")
        names.append("subject")
'''
    test='''import pytest
from conftest import order
@pytest.mark.usefixtures("guard")
class TestOrdering:
    def test_order(self):
        assert order == EXPECTED, order
'''.replace('EXPECTED',repr(expected))
    return conf,test
def main():
    ver=version('pytest')
    if not (ver.startswith('9.0.') or ver.startswith('9.1.')):raise RuntimeError('Unsupported diagnostic version')
    old=ver.startswith('9.0.')
    default=['precondition','subject_deps','subject','guard']
    reordered=(['guard','precondition','subject_deps','subject'] if old
               else ['precondition','subject_deps','guard','subject'])
    rows=[]
    for hook,expected in [(False,default),(True,reordered)]:
        conf,test=sources(hook,expected)
        with tempfile.TemporaryDirectory(prefix='lattice409_') as td:
            p=Path(td);(p/'conftest.py').write_text(conf);(p/'test_order.py').write_text(test)
            env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1')
            cp=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_order.py'],
                              cwd=td,env=env,capture_output=True,text=True,timeout=20)
            rows.append({'hook':hook,'expected':expected,'returncode':cp.returncode,
                         'stdout':cp.stdout,'stderr':cp.stderr,'conftest_sha256':sha(conf),
                         'test_sha256':sha(test),'passed':cp.returncode==0})
    out={'version':ver,'status':'POST_OUTCOME_DIAGNOSTIC','rows':rows,
         'scope':'Private metafunc.fixturenames mutation, not a supported public API contract.'}
    (HERE/('run409_hook_scope_'+ver.replace('.','_')+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    assert all(x['passed'] for x in rows),out
    print(json.dumps({'version':ver,'passed':len(rows),'orders':[x['expected'] for x in rows]},indent=2))
if __name__=='__main__':main()
