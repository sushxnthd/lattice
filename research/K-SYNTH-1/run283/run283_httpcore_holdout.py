#!/usr/bin/env python3
"""Run283 post-qualification prospectively frozen HTTPcore mechanism holdout.
Executes only trusted pinned upstream source in isolated network-disabled subprocesses.
No model patches, no new independent benchmark issue, no retrofitting.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile,importlib.util
RUN279=pathlib.Path(__file__).resolve().parent.parent/"run279"/"run279_httpcore_1000_qualify.py"
_spec=importlib.util.spec_from_file_location("_run279_pinned",RUN279)
_mod=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
ORACLE,FILES,BASE=_mod.ORACLE,_mod.FILES,_mod.BASE
REF_ALIAS='10a658221deb38a4c5b16db55ab554b0bf731707'
ORIGINAL_ORACLE_SHA='6d1fbb5d18aa7b58da802fb34f43ec6a5efcfc7a3842049df2fb02f18d2e2e96'
CASE_NAMES=('H_sync_limit1_active1','H_sync_limit3_active3','H_async_limit1_active1','H_async_limit3_active3',
            'N_sync_limit4_active2','N_sync_limit10_active1','N_async_limit4_active2','N_async_limit10_active1')
HOLDOUT='''
# Frozen after Run279 qualification. Cases are disjoint from original 10.
CASES=[('H_sync_limit1_active1',lambda:sync_target(1,1)),
       ('H_sync_limit3_active3',lambda:sync_target(3,3)),
       ('H_async_limit1_active1',lambda:asyncio.run(async_target(1,1))),
       ('H_async_limit3_active3',lambda:asyncio.run(async_target(3,3))),
       ('N_sync_limit4_active2',lambda:sync_target(4,2)),
       ('N_sync_limit10_active1',lambda:sync_target(10,1)),
       ('N_async_limit4_active2',lambda:asyncio.run(async_target(4,2))),
       ('N_async_limit10_active1',lambda:asyncio.run(async_target(10,1)))]
rows=[]
for name,fn in CASES:
    try:
        observation=fn();error=None;passed=observation['pass']
    except Exception as exc:
        observation=None;error=type(exc).__name__+': '+str(exc);passed=False
    rows.append({'case':name,'observed':observation,'error':error,'pass':passed})
print(json.dumps({'rows':rows},sort_keys=True,separators=(',',':')))
'''
def sha(b):return hashlib.sha256(b).hexdigest()
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
def build_oracle():
    assert sha(ORACLE.encode())==ORIGINAL_ORACLE_SHA
    assert ORACLE.count('CASES=[')==1
    text=ORACLE.split('CASES=[',1)[0]+HOLDOUT
    compile(text,'<frozen-run283-holdout>','exec')
    return text
def run(base,ref,out,frozen):
    assert git(base,'rev-parse','HEAD')==BASE
    assert git(ref,'rev-parse','HEAD')==REF_ALIAS
    assert git(ref,'rev-parse','HEAD^')==BASE
    oracle=build_oracle()
    assert sha(oracle.encode())==frozen['holdout_oracle_sha256']
    assert list(CASE_NAMES)==frozen['cases']
    assert frozen['expected_pass_counts']=={'baseline':{'target':0,'control':4},
      'sync_only':{'target':2,'control':4},'async_only':{'target':2,'control':4},
      'full_reference':{'target':4,'control':4}}
    out.mkdir(parents=True,exist_ok=True)
    (out/'holdout_oracle.py').write_text(oracle)
    source_hashes={}
    for f in FILES:
        source_hashes[f]={'base':sha((base/f).read_bytes()),'ref':sha((ref/f).read_bytes())}
    assert source_hashes==frozen['source_sha256'],source_hashes
    configs={'baseline':(0,0),'sync_only':(1,0),'async_only':(0,1),'full_reference':(1,1)}
    records=[]
    with tempfile.TemporaryDirectory(prefix='lattice_run283_holdout_') as d:
        for name,flags in configs.items():
            root=pathlib.Path(d)/name
            shutil.copytree(base,root,ignore=shutil.ignore_patterns('.git'))
            for f,flag in zip(FILES,flags):
                if flag:shutil.copy2(ref/f,root/f)
            proc=subprocess.run([sys.executable,'-I',str(out/'holdout_oracle.py'),str(root)],cwd=root,
                 stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=180)
            try:
                rows=json.loads(proc.stdout)['rows'] if proc.returncode==0 else []
            except Exception:rows=[]
            if not rows:rows=[{'case':x,'observed':None,'error':'ORACLE_CENSORED','pass':False} for x in CASE_NAMES]
            records.append({'configuration':name,'rows':rows,'returncode':proc.returncode,'stderr':proc.stderr[-4000:],
              'source_sha256':{f:sha((root/f).read_bytes()) for f in FILES}})
    counts={}
    for rec in records:
        rows=rec['rows'];name=rec['configuration']
        counts[name]={'target':sum(bool(r['pass']) for r in rows if r['case'].startswith('H_')),
                      'control':sum(bool(r['pass']) for r in rows if r['case'].startswith('N_'))}
    passed=(all(rec['returncode']==0 and len(rec['rows'])==8 for rec in records) and
            counts==frozen['expected_pass_counts'])
    result={'schema':'lattice-run283-httpcore1000-frozen-holdout-v1','qualified_original_issue':True,
      'holdout_pass':passed,'counts':counts,'records':records,'frozen_sha256':sha(json.dumps(frozen,sort_keys=True).encode()),
      'oracle_sha256':sha(oracle.encode()),'original_frozen_criteria_unchanged':True}
    (out/'raw_holdout.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('base','ref','out','frozen'):p.add_argument('--'+k,required=True,type=pathlib.Path)
    a=p.parse_args();result=run(a.base,a.ref,a.out,json.loads(a.frozen.read_text()))
    print(json.dumps({'holdout_pass':result['holdout_pass'],'counts':result['counts']},sort_keys=True))
