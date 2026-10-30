#!/usr/bin/env python3
"""Four-arm exact-source replay; PR #680 inspected only after prospective freeze."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();UPSTREAM=ROOT/'upstream';OUT=ROOT/'run376-factorial-results'
ORACLE=ROOT/'research/K-SYNTH-1/run376/run376_historical_oracle.py'
PATHS={'async':'httpcore/_async/connection_pool.py','sync':'httpcore/_sync/connection_pool.py'}
BASE_BLOBS={'async':'e6c4ef66312d4d6f31fcbfc417905ae329ef5885','sync':'53536d05e8c3d127b466e44dcf20e9f028aadab0'}
REF_BLOBS={'async':'10b7a55a4d0cc89b18247bde06724a561b5f4e7d','sync':'1a7025e1724d933e1dffc1bcdf28bac5328d5435'}
OLD='                    self._requests.remove(status)\n                    raise exc\n'
NEW='                    # Ensure only remove when task exists.\n                    if status in self._requests:\n                        self._requests.remove(status)\n                    raise exc\n'
ARMS={'none':(),'async_only':('async',),'sync_only':('sync',),'full':('async','sync')}

def gitblob(path):return subprocess.check_output(['git','hash-object',str(path)],text=True).strip()

def prepare_arm(name,repaired):
    arm=ROOT/f'run376-arm-{name}'
    if arm.exists():shutil.rmtree(arm)
    shutil.copytree(UPSTREAM,arm,ignore=shutil.ignore_patterns('.git'))
    for key,path in PATHS.items():
        dest=arm/path
        assert gitblob(dest)==BASE_BLOBS[key],f'baseline source mismatch {key}'
        if key in repaired:
            s=dest.read_text()
            assert s.count(OLD)==1,f'patch applicability mismatch {key}'
            dest.write_text(s.replace(OLD,NEW,1))
        assert gitblob(dest)==(REF_BLOBS[key] if key in repaired else BASE_BLOBS[key]),f'exact reference blob mismatch {key}'
    return arm

def run_phase(name,arm,phase):
    env=dict(os.environ,PYTHONPATH=str(arm))
    probe=subprocess.run([sys.executable,'-c','import httpcore;print(httpcore.__file__)'],env=env,text=True,capture_output=True,timeout=20,check=True)
    assert Path(probe.stdout.strip()).resolve().is_relative_to(arm.resolve()),f'wrong import {probe.stdout}'
    output=OUT/f'{name}_{phase}.json'
    p=subprocess.run([sys.executable,str(ORACLE),'--upstream',str(UPSTREAM),'--phase',phase,'--out',str(output)],env=env,text=True,capture_output=True,timeout=35)
    if p.returncode!=0:raise RuntimeError(f'{name} {phase} rc={p.returncode}: {p.stderr}')
    data=json.loads(output.read_text())
    return {'phase':phase,'cases':data['cases'],'stdout':p.stdout.strip(),'import_path':probe.stdout.strip(),'raw_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}

def main():
    OUT.mkdir(exist_ok=True)
    result={'issue':'encode/httpcore#670','reference':'https://github.com/encode/httpcore/pull/680',
            'baseline':'5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e','arms':{}}
    for name,keys in ARMS.items():
        arm=prepare_arm(name,keys)
        item={'repaired':list(keys),'blobs':{k:gitblob(arm/p) for k,p in PATHS.items()},'phases':{}}
        for phase in ['public','heldout']:item['phases'][phase]=run_phase(name,arm,phase)
        result['arms'][name]=item
    matrix={name:{x['case']:x['passed'] for phase in arm['phases'].values() for x in phase['cases']} for name,arm in result['arms'].items()}
    cases=sorted(matrix['none'])
    assert all(set(cases)==set(d) for d in matrix.values())
    interaction={case:int(matrix['full'][case])-int(matrix['async_only'][case])-int(matrix['sync_only'][case])+int(matrix['none'][case]) for case in cases}
    result['casewise_interaction']=interaction
    result['summary']={name:{'pass':sum(vals.values()),'total':len(vals)} for name,vals in matrix.items()}
    result['qualification_gates']={
      'baseline_public_targets_fail':all(not matrix['none'][c] for c in ('T1','T2')),
      'baseline_public_controls_pass':all(matrix['none'][c] for c in ('C1','C2','C3','C4','C5','C6')),
      'full_public_and_heldout_pass':all(matrix['full'].values()),
      'each_partial_fails_some_target_or_control':all(not all(matrix[name].values()) for name in ('async_only','sync_only')),
      'exact_two_production_file_reference':True,'source_blobs_match_reference':True}
    (OUT/'factorial_summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'summary':result['summary'],'gates':result['qualification_gates'],'interactions':interaction},sort_keys=True))

if __name__=='__main__':main()
