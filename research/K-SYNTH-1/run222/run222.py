"""Run222: prospectively remove Run220's false exact-call-name preflight gate.

Frozen eight-repo discovery cohort; run only three previously excluded issues.
Same model, seeds, retrieval, facts, representations, compiler, schema, authority.
New model-generated matched format/functional controls precede inference.
This is feasibility science, NOT a scored functional repair comparison.
"""
import argparse, json, pathlib
import run220, paired_repo_pilot as prior, run217_matched_pilot as view
from repo_transaction import digest, tracked_authority

PROTOCOL='K-SYNTH-1/run222-preflight-falsification-v1'
INDICES=(2,6,7)

def control(endpoint,out,arm):
    issue={'instance_id':'lattice-run222-control','problem_statement':
           'In sample.py change scale(x) to return x + 2, keeping its signature.'}
    files={'sample.py':b'def scale(x):\n    return x + 1\n'}
    facts=run220.facts(files,issue)
    assert len([t for t in facts['sample.py']['targets'] if t['name']=='scale'])==1
    folder=out/'control'/arm;folder.mkdir(parents=True,exist_ok=True)
    record=run220.invoke(endpoint,folder,issue,facts,files,{'sample.py'},arm)
    passed=False
    if record.get('accepted'):
        try:
            response=json.loads(next(folder.glob('*-response.json')).read_bytes())
            patch=json.loads(response['choices'][0]['message']['content'])
            tx=prior.compile_arm(files,patch,{'sample.py'},'python_short_id')
            ns={};exec(compile(tx.changes['sample.py'],'sample.py','exec'),ns)
            passed=[ns['scale'](x) for x in (-3,0,2)]==[-1,2,4]
        except Exception as e:record['functional_error']=repr(e)
    record['independent_functional_control']=passed
    (folder/'control-result.json').write_bytes(prior.canonical(record))
    return record

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cohort',required=True);p.add_argument('--out',required=True)
    p.add_argument('--task-index',type=int,choices=INDICES,required=True)
    p.add_argument('--freeze-only',action='store_true')
    p.add_argument('--endpoint',default='http://127.0.0.1:8080/v1/chat/completions')
    a=p.parse_args();cohort_bytes=pathlib.Path(a.cohort).read_bytes()
    assert digest(cohort_bytes)==run220.COHORT_SHA
    cohort=json.loads(cohort_bytes);issue=cohort[a.task_index]
    assert tuple(x['instance_id'] for x in cohort)==run220.COHORT_IDS
    assert issue['split']=='discovery'
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    freeze={'protocol':PROTOCOL,'cohort_sha256':run220.COHORT_SHA,
      'issue':issue['instance_id'],'base_commit':issue['base_commit'],
      'run220_exclusion':'PREFLIGHT_MISSING_NAMED_TARGET',
      'only_design_change':'remove exact-call-name preflight; add symmetric format controls',
      'model':prior.MODEL,'model_sha256':prior.MODEL_SHA,
      'seed':int(digest((run220.PROTOCOL+issue['instance_id']).encode())[:8],16),
      'schema_sha256':digest(prior.canonical(prior.response_format('python_short_id'))),
      'arms':run220.ARMS,'same_compiler_and_authority':True,
      'functional_issue_resolution':'NOT_EVALUATED','boundary_untouched':True}
    (out/'freeze.json').write_bytes(prior.canonical(freeze))
    if a.freeze_only:return
    try:
        root=pathlib.Path('/tmp')/('lattice-run222-'+str(a.task_index))
        prior.clone_issue(issue,root);authority=tracked_authority(root)
        files=prior.retrieve(issue,root,authority,out,a.endpoint)
        facts=run220.facts(files,issue)
        assert json.loads(json.dumps(facts))==view.parse_python_view(view.python_view(facts))
        names=run220.issue_names(issue)
        matches=[(path,t['name'],t['target_id']) for path,d in facts.items()
                 for t in d['targets'] if t['name'] in names]
        (out/'target_coverage.json').write_bytes(prior.canonical({
          'named_matches':matches,'all_candidate_count':sum(len(d['targets']) for d in facts.values()),
          'retrieved_paths':sorted(files),'facts_sha256':digest(prior.canonical(facts)),
          'same_information_both_arms':True,'preflight_gate_removed':True}))
        controls={arm:control(a.endpoint,out,arm) for arm in run220.ARMS}
        (out/'control_gate.json').write_bytes(prior.canonical({
          arm:bool(r['independent_functional_control']) for arm,r in controls.items()}))
        raw=out/'raw';raw.mkdir(exist_ok=True)
        records=[]
        for arm in (run220.ARMS if a.task_index%2==0 else tuple(reversed(run220.ARMS))):
            record=run220.invoke(a.endpoint,raw,issue,facts,files,authority,arm)
            record['control_passed']=bool(controls[arm]['independent_functional_control'])
            record['functional_resolution']='NOT_EVALUATED'
            records.append(record)
            (out/'records.json').write_bytes(prior.canonical(records))
    except Exception as e:
        (out/'run_failure.json').write_bytes(prior.canonical({
          'issue':issue['instance_id'],'error':repr(e),'partial_artifacts_retained':True}))
        raise

if __name__=='__main__':main()
