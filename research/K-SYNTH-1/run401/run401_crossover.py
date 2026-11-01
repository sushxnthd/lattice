#!/usr/bin/env python3
"""Prospective same-runner ABBA/BAAB crossover on the frozen pytest #14942 workload."""
import argparse, hashlib, json, os, pathlib, platform, re, statistics, subprocess, sys, tempfile, time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"run400"))
from run400_pytest_perf_oracle import make_workload

NODE=re.compile(r'^test_module_\d{4}\.py::TestM\d{3}C\d{2}::test_(?:one|two)$')

def command(py,root,expected,arm,phase,block,slot,timeout):
 env=os.environ.copy();env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1';env['PYTHONHASHSEED']='0'
 t=time.perf_counter()
 try:
  p=subprocess.run([py,'-m','pytest','--collect-only','-q',str(root)],cwd=str(root),
    env=env,text=True,capture_output=True,timeout=timeout)
  duration=time.perf_counter()-t
  stdout,stderr,rc=p.stdout,p.stderr,p.returncode
  timed_out=False
 except subprocess.TimeoutExpired as e:
  duration=time.perf_counter()-t
  stdout=str(e.stdout);stderr=str(e.stderr);rc=None;timed_out=True
 ids=[s.strip() for s in stdout.splitlines() if NODE.fullmatch(s.strip())]
 valid=(rc==0 and len(ids)==expected and len(set(ids))==expected
   and re.search(rf'\b{expected} tests? collected\b',stdout) is not None)
 return {'arm':arm,'phase':phase,'block':block,'slot':slot,'seconds':duration,
   'exit_code':rc,'timed_out':timed_out,'valid_collection':valid,
   'node_count':len(ids),'stdout':stdout,'stderr':stderr}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--python-a',required=True)
 ap.add_argument('--python-b',required=True);ap.add_argument('--output',required=True)
 ap.add_argument('--timeout',type=int,default=120);args=ap.parse_args()
 py={k:str(pathlib.Path(v).resolve()) for k,v in [('A',args.python_a),('B',args.python_b)]}
 versions={k:subprocess.check_output([v,'-c','import pytest;print(pytest.__version__)'],text=True).strip() for k,v in py.items()}
 assert versions=={'A':'9.0.3','B':'9.1.1'},versions
 record={'protocol':'RUN401_SEPARATE_PROSPECTIVE_SAME_HOST_CROSSOVER',
   'versions':versions,'interpreters':py,'host':platform.platform(),
   'host_python':sys.version,'cpu_count':os.cpu_count(),
   'orders':['ABBA','BAAB','ABBA','BAAB'],'warmup_order':'ABBA',
   'workloads':[]}
 with tempfile.TemporaryDirectory(prefix='lattice_run401_crossover_') as td:
  for n in (8,32,128):
   root=pathlib.Path(td)/f'w{n}';source=make_workload(root,n)
   observations=[]
   for slot,arm in enumerate('ABBA'):
    observations.append(command(py[arm],root,20*n,arm,'warmup',-1,slot,args.timeout))
   for block,order in enumerate(record['orders']):
    for slot,arm in enumerate(order):
     observations.append(command(py[arm],root,20*n,arm,'measured',block,slot,args.timeout))
   measured={arm:[x['seconds'] for x in observations if x['phase']=='measured' and x['arm']==arm] for arm in 'AB'}
   medians={arm:statistics.median(times) for arm,times in measured.items()}
   valid=all(x['valid_collection'] for x in observations)
   record['workloads'].append({'source':source,'observations':observations,
     'median_measured_seconds':medians,'ratio_B_over_A':medians['B']/medians['A'],
     'all_collections_success':valid})
   print(json.dumps({'modules':n,'ratio_B_over_A':medians['B']/medians['A'],
     'all_collections_success':valid}),flush=True)
 record['frozen_3x_both_larger']=(all(w['ratio_B_over_A']>=3 for w in record['workloads'][1:])
   and all(w['all_collections_success'] for w in record['workloads']))
 pathlib.Path(args.output).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
