"""Rebuild pinned Run213, independently replay Run214 witnesses, apply safety patch."""
from __future__ import annotations
import base64
import importlib.util
import io
import json
import pathlib
import subprocess
import sys
import tarfile
import tempfile
import zlib

here=pathlib.Path(__file__).resolve().parent
parent=here.parent
archive=base64.b64decode((parent/'run211/run211_source.tar.gz.b64').read_bytes())
backend=zlib.decompress(base64.b64decode((parent/'run207/repo_transaction.py.zlib.b64').read_bytes()))
with tempfile.TemporaryDirectory(prefix="lattice-run214-") as td:
    work=pathlib.Path(td)
    (work/'repo_transaction.py').write_bytes(backend)
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as tf:
        expected={'semantic_refactor.py','test_semantic_refactor.py','run211_differential.py'}
        assert {m.name for m in tf.getmembers()}==expected
        for member in tf.getmembers():
            assert member.isfile()
            (work/member.name).write_bytes(tf.extractfile(member).read())
    (work/'test_run212_adversarial.py').write_bytes((parent/'run212/test_run212_adversarial.py').read_bytes())
    (work/'test_run213_escape_safety.py').write_bytes(zlib.decompress(base64.b64decode(
        (parent/'run213/test_run213_escape_safety.py.zlib.b64').read_bytes())))
    (work/'test_run214_observability.py').write_bytes((here/'test_run214_observability.py').read_bytes())
    subprocess.run(['patch','--batch','--forward','-p1','-i',
        str(parent/'run212/semantic_refactor.patch')],cwd=work,check=True)
    prior_patch=zlib.decompress(base64.b64decode(
        (parent/'run213/run212_to_run213.patch.zlib.b64').read_bytes()))
    (work/'run213.patch').write_bytes(prior_patch)
    subprocess.run(['patch','--batch','--forward','-p1','-i',
        str(work/'run213.patch')],cwd=work,check=True)

    sys.path.insert(0,str(work))
    import semantic_refactor as previous
    spec=importlib.util.spec_from_file_location('run214_tests',(here/'test_run214_observability.py'))
    tests=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=tests
    spec.loader.exec_module(tests)
    def observe(source):
        with tempfile.TemporaryDirectory(prefix='run214-observe-') as d:
            pathlib.Path(d,'target.py').write_text(source,encoding='utf-8')
            p=subprocess.run([sys.executable,'-c',
                'import target,json;print(json.dumps(target.probe(),sort_keys=True))'],
                cwd=d,capture_output=True,text=True,timeout=10)
            return {'exit_code':p.returncode,'stdout':p.stdout.strip(),
                    'stderr_tail':p.stderr.strip().splitlines()[-1:]}
    rows=[]
    for name,source in tests.CASES.items():
        snapshot={'target.py':source.encode('utf-8')}
        tx,_=previous.compile_semantic_rename(snapshot,set(snapshot),
            module_map={'target.py':'target'},target_path='target.py',
            old='old',new='new',closed_world=True)
        before=observe(source)
        after=observe(tx.changes['target.py'].decode('utf-8'))
        assert before['exit_code']==after['exit_code']==0,(name,before,after)
        assert before['stdout']!=after['stdout'],(name,before,after)
        rows.append({'case':name,'previous_accepted':True,'before':before,
                     'previous_after':after,'compiler_trace':list(tx.trace)})
    (here/'run214_ci_witnesses.json').write_text(json.dumps(rows,indent=2)+'\n')
    subprocess.run(['patch','--batch','--forward','-p1','-i',
        str(here/'run213_to_run214.patch')],cwd=work,check=True)
    subprocess.run([sys.executable,'-m','unittest','-q',
        'test_semantic_refactor','test_run212_adversarial',
        'test_run213_escape_safety','test_run214_observability'],cwd=work,check=True)
    print(json.dumps({'previous_accepted_behavior_changing':len(rows),
                      'corrected_rejected':len(rows),'total_tests':35}))
