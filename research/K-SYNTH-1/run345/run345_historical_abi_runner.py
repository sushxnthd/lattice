"""Run345 post-outcome ABI-only Jinja historical-source ablation.

This experiment does NOT alter or requalify Run344. Historical code is executed
in disposable GitHub Actions checkouts only. No untrusted code on the host.
"""
from __future__ import annotations
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# Run344 runner is restored by CI from its immutable SHA-pinned archive.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'run344'))
import run344_historical_runner as parent

HERE = Path(__file__).resolve().parent
OUT = HERE / 'cloud_raw'
ABI_ARMS = {'00A': (0, 0), '10A': (1, 0), '01A': (0, 1), '11A': (1, 1)}
ANCHOR = b'        try:\n            return __obj(*args, **kwargs)'
REPLACEMENT = (b'        kwargs.pop("_loop_vars", None)\n'
               b'        kwargs.pop("_block_vars", None)\n'
               b'        try:\n            return __obj(*args, **kwargs)')
EXPECTED = {'00A': (1,8), '10A': (2,8), '01A': (1,8), '11A': (6,8)}
TARGET_PASS_10A = {'T03', 'T04'}


def adapter(source: bytes) -> bytes:
    """Fail-closed exact baseline-blob edit; no semantic context derivation."""
    assert parent.blob_sha(source) == parent.BASE_BLOBS['runtime'], 'BASELINE_RUNTIME_BLOB_MISMATCH'
    assert source.count(ANCHOR) == 1, 'ANCHOR_NOT_UNIQUE'
    assert source.count(REPLACEMENT) == 0, 'ALREADY_PATCHED'
    modified = source.replace(ANCHOR, REPLACEMENT, 1)
    assert modified.count(REPLACEMENT) == 1
    compile(modified, 'historical_runtime_abi_adapter.py', 'exec')
    return modified


def prediction(rows: dict) -> dict:
    counts = {}
    for arm, record in rows.items():
        records = record['records']
        assert len(records) == 14 and len({r['id'] for r in records}) == 14
        counts[arm] = (sum(r['ok'] for r in records if r['kind']=='target'),
                       sum(r['ok'] for r in records if r['kind']=='control'))
    keys = {a:{r['id']:r for r in rows[a]['records']} for a in ABI_ARMS}
    assert len({tuple(sorted(k)) for k in keys.values()}) == 1
    pass_10a = {r['id'] for r in rows['10A']['records'] if r['kind']=='target' and r['ok']}
    interaction = {}
    for case_id in sorted(keys['00A']):
        y = [int(keys[a][case_id]['ok']) for a in ABI_ARMS]
        interaction[case_id] = {'outcomes':y,'delta':y[3]-y[1]-y[2]+y[0]}
    positive = {k for k,v in interaction.items() if v['delta']>0}
    negative = {k for k,v in interaction.items() if v['delta']<0}
    matched = counts == EXPECTED and pass_10a == TARGET_PASS_10A and positive == {'T01','T02','T05','T06'} and not negative
    return {'counts':{k:list(v) for k,v in counts.items()},'prediction_met':matched,
            'pass_10a':sorted(pass_10a),'positive_interactions':sorted(positive),
            'negative_interactions':sorted(negative),'casewise':interaction,
            'status':'POST_OUTCOME_MECHANISM_ONLY','source_qualification_unchanged':True,
            'semantic_mechanism':'FINITE_ABI_NORMALIZED_CASEWISE_INTERACTION_NOT_GLOBAL_PROOF'}


def main():
    parent.verify_oracle()
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='lattice-run345-jinja-') as td:
        td = Path(td)
        repo = td / 'jinja'
        parent.cmd('git','clone','--quiet','https://github.com/pallets/jinja.git',str(repo))
        for rev in (parent.BASE,parent.REF):
            parent.cmd('git','cat-file','-e',rev+'^{commit}',cwd=repo)
        source={}
        for version,rev,expected in [('base',parent.BASE,parent.BASE_BLOBS),('reference',parent.REF,parent.REF_BLOBS)]:
            source[version]={}
            for component,path in parent.SOURCES.items():
                b=subprocess.run(['git','show',f'{rev}:{path}'],cwd=repo,capture_output=True,check=True,timeout=120).stdout
                assert parent.blob_sha(b)==expected[component], (version,component,'SOURCE_HASH_MISMATCH')
                source[version][component]=b
        adapted = adapter(source['base']['runtime'])
        (OUT/'adapter.diff').write_text(''.join(difflib.unified_diff(
            source['base']['runtime'].decode().splitlines(keepends=True),
            adapted.decode().splitlines(keepends=True),
            fromfile='baseline/runtime.py',tofile='baseline/runtime.py+ABI-only')))
        (OUT/'adapter.sha256').write_text(parent.sha(adapted)+'\n')
        parent.cmd('git','checkout','--quiet',parent.BASE,cwd=repo)
        manifest={}
        rows={}
        for arm,(compiler_ref,runtime_ref) in ABI_ARMS.items():
            overlay=td/('arm_'+arm)
            shutil.copytree(repo/'src',overlay/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            used={}
            for component,is_ref in [('compiler',compiler_ref),('runtime',runtime_ref)]:
                b=source['reference' if is_ref else 'base'][component]
                if component=='runtime' and not is_ref:
                    b=adapted
                path=overlay/parent.SOURCES[component]
                path.write_bytes(b)
                used[component]={'sha256':parent.sha(b),'blob_sha1':parent.blob_sha(b),
                                 'version':'reference' if is_ref else ('baseline+ABI-only' if component=='runtime' else 'baseline')}
            env=os.environ.copy()
            env.update({'PYTHONPATH':str(overlay/'src'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1'})
            oracle_output=td/f'{arm}.json'
            p=subprocess.run([sys.executable,str(HERE.parent/'run344'/'run344_jinja_oracle.py'),
                              '--output',str(oracle_output)],cwd=overlay,env=env,
                              text=True,capture_output=True,timeout=45)
            try: records=json.loads(oracle_output.read_text())['records']
            except (OSError,ValueError,KeyError):records=[]
            rows[arm]={'arm':arm,'source':used,'returncode':p.returncode,
                       'stdout':p.stdout,'stderr':p.stderr,'records':records}
            target=OUT/f'{arm}.json'
            target.write_text(json.dumps(rows[arm],sort_keys=True,indent=2)+'\n')
            manifest[target.name]=parent.sha(target.read_bytes())
        decision=prediction(rows)
        (OUT/'decision.json').write_text(json.dumps(decision,sort_keys=True,indent=2)+'\n')
        manifest['decision.json']=parent.sha((OUT/'decision.json').read_bytes())
        for name in ('adapter.diff','adapter.sha256'):
            manifest[name]=parent.sha((OUT/name).read_bytes())
        (OUT/'manifest.json').write_text(json.dumps({'schema':'run345-v1',
            'freeze_commit':'15d8c2b0755200c4ffa27d9e2cc8c850da4853ef',
            'base':parent.BASE,'reference':parent.REF,'oracle_sha256':parent.ORACLE_SHA,
            'runner_sha256':parent.sha(Path(__file__).read_bytes()),
            'payload_sha256':manifest},sort_keys=True,indent=2)+'\n')
        print(json.dumps({'counts':decision['counts'],'prediction_met':decision['prediction_met'],
                          'positive_interactions':decision['positive_interactions']},sort_keys=True))


if __name__=='__main__':main()
