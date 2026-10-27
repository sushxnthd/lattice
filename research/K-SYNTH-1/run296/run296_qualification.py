#!/usr/bin/env python3
"""Run296 prospectively frozen independent Click PR2956 functional qualification.

Only trusted public upstream reference sources are executed on an ephemeral CI runner.
No model-generated code is executed. No installed click distribution is imported.
Four base/reference source configurations receive identical public-API tests.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = '5c1239b0116b66492cdd0848144ab3c78a04495a'
HEAD = '9caedb9206103dfb5465e1916bc2f13b9c10c0e4'
BLOBS = {
    'base': {'src/click/core.py': 'f57ada62b195fa533387b5d06b366b17edb7d2f4',
             'src/click/types.py': '684cb3b1e6107bada194d18968de69a7f383a2a0'},
    'head': {'src/click/core.py': '445460bc5880f9f62df097f20996b80420b4f424',
             'src/click/types.py': 'e71c1c21e4c2e1f954ceeed228507478f138993a'},
}

# Frozen target/control cases are NOT derived from the upstream test suite.
# The expected results are public API contracts, not model-generated repairs.
CASES = [
    {'id':'T1_default_true_present','kind':'bool_default_true','args':['--enabled'], 'env':{}, 'expected':['ok','True']},
    {'id':'T2_nonbool_env_off','kind':'choice_env','args':[], 'env':{'CHOICE':'0'}, 'expected':['ok',"'False'"]},
    {'id':'T3_nonbool_env_on','kind':'choice_env','args':[], 'env':{'CHOICE':'1'}, 'expected':['ok',"'upper'"]},
    {'id':'C1_bool_env_on','kind':'bool_env','args':[], 'env':{'ENABLED':'true'}, 'expected':['ok','True']},
    {'id':'C2_bool_env_off','kind':'bool_env','args':[], 'env':{'ENABLED':'false'}, 'expected':['ok','False']},
    {'id':'C3_bool_default_off','kind':'bool_default_off','args':[], 'env':{}, 'expected':['ok','False']},
    {'id':'C4_bool_cli_on','kind':'bool_default_off','args':['--enabled'], 'env':{}, 'expected':['ok','True']},
    {'id':'C5_nonbool_cli_on','kind':'choice_env','args':['--choice'], 'env':{}, 'expected':['ok',"'upper'"]},
    {'id':'C6_invalid_bool_env','kind':'bool_env','args':[], 'env':{'ENABLED':'notabool'}, 'expected':['exit',2]},
    {'id':'C7_int_env_argument','kind':'int_env','args':[], 'env':{'COUNT':'42'}, 'expected':['ok','42']},
]

# A separate Python process imports a clean copy of Click for each configuration.
ORACLE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import click
from click.testing import CliRunner
from pathlib import Path
assert Path(click.__file__).resolve().is_relative_to(Path(sys.argv[1]).resolve())
cases=json.loads(sys.argv[2]); rows=[]
for c in cases:
    try:
        if c['kind']=='bool_default_true':
            @click.command()
            @click.option('--enabled', is_flag=True, default=True)
            def command(enabled): return enabled
        elif c['kind']=='choice_env':
            @click.command()
            @click.option('--choice', is_flag=True, flag_value='upper', envvar='CHOICE')
            def command(choice): return choice
        elif c['kind']=='bool_env':
            @click.command()
            @click.option('--enabled/--no-enabled', envvar='ENABLED')
            def command(enabled): return enabled
        elif c['kind']=='bool_default_off':
            @click.command()
            @click.option('--enabled', is_flag=True)
            def command(enabled): return enabled
        elif c['kind']=='int_env':
            @click.command()
            @click.argument('count', type=int, envvar='COUNT')
            def command(count): return count
        else: raise AssertionError('unknown kind')
        r=CliRunner().invoke(command, c['args'], env=c['env'], standalone_mode=False)
        if r.exit_code == 0:
            got=['ok',repr(r.return_value)]
        else:
            got=['exit',r.exit_code]
        rows.append({'id':c['id'],'got':got,'expected':c['expected'],
                     'pass':got==c['expected'],'exception_type':type(r.exception).__name__ if r.exception else None,
                     'stdout':r.output[:400]})
    except BaseException as e:
        rows.append({'id':c['id'],'got':['exception',type(e).__name__],
                     'expected':c['expected'],'pass':False,
                     'exception_type':type(e).__name__,'stdout':str(e)[:400]})
print(json.dumps({'click_path':click.__file__,'rows':rows},sort_keys=True))
'''

def git(repo: Path, *args: str) -> bytes:
    p=subprocess.run(['git','-C',str(repo),*args],capture_output=True,check=True)
    return p.stdout.strip() if args[0]=='rev-parse' else p.stdout

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def blob_sha(b:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def main():
    if len(sys.argv)!=3:
        raise SystemExit('usage: run296_qualification.py UPSTREAM_BASE_CHECKOUT OUTPUT_JSON')
    repo=Path(sys.argv[1]).resolve(); output=Path(sys.argv[2]).resolve()
    assert git(repo,'rev-parse','HEAD').decode()==BASE, 'upstream checkout not pinned to base'
    sources={}
    for name,ref in [('base',BASE),('head',HEAD)]:
        sources[name]={}
        for path,expected_blob in BLOBS[name].items():
            b=git(repo,'show',f'{ref}:{path}')
            assert blob_sha(b)==expected_blob,(name,path,'blob SHA mismatch')
            sources[name][path]=b
    variants={'base':set(), 'core_only':{'src/click/core.py'},
              'types_only':{'src/click/types.py'},'full':set(BLOBS['head'])}
    results={}
    with tempfile.TemporaryDirectory(prefix='lattice-run296-') as t:
        for name,updated in variants.items():
            root=Path(t)/name
            shutil.copytree(repo/'src',root/'src')
            for path in updated:
                (root/path).write_bytes(sources['head'][path])
            env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'
            env['PYTHONNOUSERSITE']='1'; env['PYTHONHASHSEED']='0'
            # Only the frozen trusted upstream source is imported, not model output.
            proc=subprocess.run([sys.executable,'-B','-c',ORACLE,str(root/'src'),json.dumps(CASES)],
                                cwd=root,env=env,text=True,capture_output=True,timeout=90)
            result={'returncode':proc.returncode,'stderr':proc.stderr[:2000],
                    'source_sha256':{path:sha((root/path).read_bytes()) for path in BLOBS['base']},
                    'oracle_stdout':proc.stdout}
            if proc.returncode==0:
                data=json.loads(proc.stdout)
                assert [x['id'] for x in data['rows']]==[x['id'] for x in CASES]
                result['rows']=data['rows']
                result['pass_count']=sum(x['pass'] for x in data['rows'])
            results[name]=result
    target=[x['id'] for x in CASES if x['id'].startswith('T')]
    controls=[x['id'] for x in CASES if x['id'].startswith('C')]
    def all_pass(name,ids):
        return all(r['pass'] for r in results[name].get('rows',[]) if r['id'] in ids) and len(results[name].get('rows',[]))==len(CASES)
    qualified=(all_pass('full',target+controls) and all_pass('base',controls)
               and not all_pass('base',target)
               and not all_pass('core_only',target+controls)
               and not all_pass('types_only',target+controls))
    payload={'protocol':'RUN296_CLICK_PR2956_V1','base':BASE,'head':HEAD,
             'source_git_blobs':BLOBS,'cases':CASES,'results':results,
             'prospective_qualified':qualified,
             'qualification_rule':'full passes targets+controls; base passes controls and fails target; each single-file ablation fails >=1 combined check',
             'note':'One PR only; candidate selected after reading upstream PR patch; not a gold-blind model benchmark.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'qualified':qualified,'pass_counts':{k:v.get('pass_count') for k,v in results.items()},
                      'raw_sha256':sha(output.read_bytes())},sort_keys=True))
    if any(v['returncode']!=0 for v in results.values()): raise SystemExit(3)

if __name__=='__main__': main()
