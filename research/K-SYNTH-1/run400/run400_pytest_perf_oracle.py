#!/usr/bin/env python3
"""Frozen issue-first pytest #14942 benchmark; self-authored workloads only."""
import argparse,hashlib,json,os,pathlib,platform,statistics,subprocess,sys,tempfile,time

def make_workload(root,modules,classes_per_module=10):
    root.mkdir(parents=True,exist_ok=True)
    (root/'pytest.ini').write_text('[pytest]\naddopts = -p no:cacheprovider\nfilterwarnings =\n    ignore:.*Class-scoped fixture defined as instance method.*:pytest.PytestRemovedIn10Warning\n')
    (root/'conftest.py').write_text('import pytest\n@pytest.fixture(scope="session")\ndef session_token():\n    return 7\n')
    for m in range(modules):
        lines=['import pytest','']
        for c in range(classes_per_module):
            lines += [f'class TestM{m:03d}C{c:02d}:','    @pytest.fixture(scope="class")',
                '    def item(self, session_token):','        return session_token + 1',
                '    def test_one(self, item):','        assert item == 8',
                '    def test_two(self, item):','        assert item > 0','']
        (root/f'test_module_{m:04d}.py').write_text('\n'.join(lines))
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*')) if p.is_file()}
    return {'modules':modules,'classes_per_module':classes_per_module,
        'expected_cases':modules*classes_per_module*2,'source_sha256':hashes}

def bench_one(root,repeat=3,timeout=240):
    env=os.environ.copy();env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1';env['PYTHONHASHSEED']='0'
    rows=[]
    for r in range(repeat):
        start=time.perf_counter()
        try:
            p=subprocess.run([sys.executable,'-m','pytest','--collect-only','-q',str(root)],
                cwd=str(root),env=env,text=True,capture_output=True,timeout=timeout)
            row={'repeat':r,'seconds':time.perf_counter()-start,'exit_code':p.returncode,
                'stdout':p.stdout,'stderr':p.stderr}
        except subprocess.TimeoutExpired as e:
            row={'repeat':r,'seconds':time.perf_counter()-start,'exit_code':None,
                'timed_out':True,'stdout':str(e.stdout),'stderr':str(e.stderr)}
        rows.append(row)
    return {'median_seconds':statistics.median(x['seconds'] for x in rows),
        'repetitions':rows,'all_collection_success':all(x['exit_code']==0 for x in rows)}

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',required=True)
    a.add_argument('--modules',nargs='+',type=int,default=[8,32,128])
    a.add_argument('--repeat',type=int,default=3);a.add_argument('--timeout',type=int,default=240)
    args=a.parse_args()
    import pytest
    result={'python':sys.version,'platform':platform.platform(),'pytest':pytest.__version__,
        'protocol':'issue-first Run400 pytest #14942','runs':[]}
    with tempfile.TemporaryDirectory(prefix='lattice_run400_pytest_') as td:
        for n in args.modules:
            root=pathlib.Path(td)/f'workload_{n}'
            meta=make_workload(root,n);out=bench_one(root,args.repeat,args.timeout)
            result['runs'].append({'workload':meta,'outcome':out})
            print(json.dumps({'pytest':pytest.__version__,'modules':n,
                'cases':meta['expected_cases'],'median_s':out['median_seconds'],
                'collection_success':out['all_collection_success']}),flush=True)
    pathlib.Path(args.output).write_text(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
