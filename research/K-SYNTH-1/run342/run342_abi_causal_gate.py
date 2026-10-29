#!/usr/bin/env python3
"""Read-only casewise ABI-confounding diagnostic for frozen Run342 traces."""
import argparse
import json
from pathlib import Path

ORIGINAL=('base_base','ref_A','ref_B','ref_ref')
ADAPTED=('base_base','ref_A_plus_abi','ref_B_plus_abi','ref_ref')

def load(path):
    payload=json.loads(Path(path).read_text())
    records=payload.get('records')
    if not isinstance(records,list) or len(records)!=10:raise ValueError('record count')
    result={}
    for r in records:
        k=r['id']
        if k in result:raise ValueError('duplicate case')
        if type(r['ok']) is not bool or r['ok']!=(r['got']==r['expected']):raise ValueError('outcome mismatch')
        result[k]=r
    return result

def diagnose(original,adapted):
    old={a:load(original/(a+'.json')) for a in ORIGINAL}
    new={a:load((adapted if a.endswith('_plus_abi') else original)/(a+'.json')) for a in ADAPTED}
    ids=set(old['base_base'])
    if len(ids)!=10:raise ValueError('case count')
    rows=[]
    for case in sorted(ids):
        all_records=[arm[case] for arm in list(old.values())+list(new.values())]
        if any(set(arm)!=ids for arm in list(old.values())+list(new.values())):raise ValueError('case set drift')
        if len({json.dumps((r['expected'],r['input_chunks_hex'],r['group']),sort_keys=True) for r in all_records})!=1:
            raise ValueError('oracle drift')
        before=[int(old[a][case]['ok']) for a in ORIGINAL]
        after=[int(new[a][case]['ok']) for a in ADAPTED]
        contrast=lambda x:x[3]-x[1]-x[2]+x[0]
        rows.append({'case':case,'group':old['base_base'][case]['group'],
                     'original':before,'abi_corrected':after,
                     'original_interaction':contrast(before),'corrected_interaction':contrast(after)})
    return {'scope':'POST_OUTCOME_ABI_DIAGNOSTIC_NOT_QUALIFICATION',
      'cases':rows,'original_nonzero':sum(r['original_interaction']!=0 for r in rows),
      'corrected_nonzero':sum(r['corrected_interaction']!=0 for r in rows),
      'original_sum_absolute':sum(abs(r['original_interaction']) for r in rows),
      'corrected_sum_absolute':sum(abs(r['corrected_interaction']) for r in rows),
      'new_repository_qualification':False,'semantic_global_proof':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--original',type=Path,required=True);p.add_argument('--adapted',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=diagnose(args.original,args.adapted)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('original_nonzero','corrected_nonzero','original_sum_absolute','corrected_sum_absolute')}))
if __name__=='__main__':main()
