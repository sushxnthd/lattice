#!/usr/bin/env python3
"""Read-only audit of Run366's unchanged historical HTTPcore oracle."""
import argparse
import json
from pathlib import Path

BASE_SYNC='9ccfa53e597a29ee387f9d16f3af4f695ac0d33a'
HEAD_SYNC='4b26f9c63032be5c6c932b9d1339c43d4029368e'
BASE_ASYNC='96e973d0ce223f6bed9be9e6a6a2f3c01622c611'
HEAD_ASYNC='5ef74e6497f1fe44b7be520f8e1502e8786e91fd'
ORACLE_SHA='1889d4e0b71610018b94fa87084199de280323cedf3133eeac7588025ff30797'
VARIANTS={
 'sync0_async0':(BASE_SYNC,BASE_ASYNC),
 'sync1_async0':(HEAD_SYNC,BASE_ASYNC),
 'sync0_async1':(BASE_SYNC,HEAD_ASYNC),
 'sync1_async1':(HEAD_SYNC,HEAD_ASYNC)}
TARGETS=('busy1_idle1_cap1','idle1_busy1_cap1','busy2_idle1_cap1','idle2_busy1_cap2',
         'idle2_busy1_cap1','idle3_busy1_cap2','idle2_busy2_cap2','busy2_idle2_cap1')
CONTROLS=('idle1_cap1','idle2_cap2','idle3_cap1','busy2_cap1','idle1_cap0',
          'closed_idle_cap1','expired_idle_cap1','closed_expired_busy','empty','busy_idle_closed')

def independent_expected(states,cap):
    live=[(str(i),s) for i,s in enumerate(states) if s not in 'CE']
    expired=[str(i) for i,s in enumerate(states) if s=='E']
    idle=[label for label,state in live if state=='I']
    remove=idle[:max(0,len(idle)-cap)]
    return [label for label,_ in live if label not in set(remove)],expired+remove

def audit(folder):
    folder=Path(folder)
    source=json.loads((folder/'source_shas.json').read_text())
    assert set(source)==set(VARIANTS),'source variants missing'
    for v,(s,a) in VARIANTS.items():
        assert source[v]=={'sync':s,'async':a},('source SHA',v)
    reports={}; rows={}
    for v in VARIANTS:
        status=json.loads((folder/f'{v}.status.json').read_text())
        assert status['variant']==v
        if status['exit_code']!=0:
            reports[v]={'status':'PREORACLE_FAILURE','exit_code':status['exit_code'],
                        'stderr_sha256':status['stderr_sha256']}
            continue
        doc=json.loads((folder/f'{v}.json').read_text())
        assert doc['label']==v and doc['oracle_sha256']==ORACLE_SHA
        assert len(doc['rows'])==36
        observed=set()
        counts={b:{'target':0,'control':0} for b in ('sync','async')}
        for r in doc['rows']:
            key=(r['backend'],r['case'])
            assert r['backend'] in ('sync','async') and r['case'] in TARGETS+CONTROLS
            assert key not in observed
            observed.add(key)
            assert r['group']==('target' if r['case'] in TARGETS else 'control')
            assert all(c in 'BICE' for c in r['states'])
            expected=independent_expected(r['states'],r['cap'])
            assert (r['expected_retained'],r['expected_closing'])==expected
            passed=(r['actual_retained'],r['actual_closing'])==expected and r['error'] is None
            assert r['pass_']==passed,(v,key)
            counts[r['backend']][r['group']]+=int(passed)
            rows[(v,)+key]=r
        assert observed=={(b,c) for b in ('sync','async') for c in TARGETS+CONTROLS}
        for b in ('sync','async'):
            for g,n in (('target',8),('control',10)):
                assert doc['summary'][b][g]=={'pass':counts[b][g],'total':n}
        reports[v]={'status':'EXECUTED','counts':counts,'httpcore_version':doc['httpcore_version']}
    all_executed=all(x['status']=='EXECUTED' for x in reports.values())
    clean_baseline=all_executed and all(reports['sync0_async0']['counts'][b]['control']==10 for b in ('sync','async'))
    full_pass=all_executed and all(reports['sync1_async1']['counts'][b][g]==n
                                   for b in ('sync','async') for g,n in (('target',8),('control',10)))
    joint_necessary=all_executed and all(
        any(reports[v]['counts'][b][g]<n for b in ('sync','async') for g,n in (('target',8),('control',10)))
        for v in ('sync1_async0','sync0_async1'))
    interactions={}
    if all_executed:
        for b in ('sync','async'):
            for c in TARGETS+CONTROLS:
                q=[int(rows[(v,b,c)]['pass_']) for v in
                   ('sync0_async0','sync1_async0','sync0_async1','sync1_async1')]
                interactions[f'{b}:{c}']=q[3]-q[1]-q[2]+q[0]
    return {'qualification':'PASS' if all_executed and clean_baseline and full_pass and joint_necessary else 'FAIL',
            'all_144_executed':all_executed,'baseline_controls_clean':clean_baseline,
            'full_reference_passes':full_pass,'joint_necessary':joint_necessary,
            'source_git_blob_ids_verified':True,'variants':reports,
            'case_level_interactions':interactions,
            'qualification_note':'Do not alter the original frozen controls.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--results',required=True);p.add_argument('--output',required=True)
    args=p.parse_args()
    result=audit(args.results)
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='case_level_interactions'},sort_keys=True))
