"""Run316 prospectively frozen bounded adversarial snapshot-store experiment.

Trusted fixture bytes only. No untrusted code is run. All paths confined to a
TemporaryDirectory, including the intentionally redirected parent-symlink case.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from run315_multifile_compiler import PatchRejected
from run315_snapshot_store_hardened import publish as original
from run316_snapshot_store_v2 import publish as corrected


def expect_rejected(call):
    try:
        call()
    except PatchRejected:
        return True
    raise AssertionError('expected PatchRejected')


def check_snapshot(store: Path, sid: str, files: dict[str, bytes]):
    snap = store/'snapshots'/sid
    manifest = json.loads((snap/'MANIFEST.json').read_bytes())
    assert manifest == {p:sha256(b).hexdigest() for p,b in files.items()}
    for path, data in files.items():
        assert (snap/path).read_bytes() == data


def main():
    result = {'original_parent_symlink_escape':0, 'corrected_parent_symlink_rejections':0,
              'same_id_concurrent_publishes':0, 'distinct_id_concurrent_publishes':0,
              'verified_concurrent_snapshots':0, 'failure_rollbacks':0,
              'symlink_snapshots_rejections':0, 'symlink_final_rejections':0}
    with tempfile.TemporaryDirectory(prefix='lattice_run316_') as root_name:
        root=Path(root_name)
        for i in range(32):
            outer=root/f'parent{i}'
            outer.mkdir()
            outside=outer/'outside'
            outside.mkdir()
            (outer/'alias').symlink_to(outside,target_is_directory=True)
            store=outer/'alias'/'store'
            files={'pkg/value.py':f'VALUE = {i}\n'.encode()}
            sid=original(store,files)
            check_snapshot(outside/'store',sid,files)
            result['original_parent_symlink_escape']+=1
            assert expect_rejected(lambda: corrected(store,files))
            result['corrected_parent_symlink_rejections']+=1
        store=root/'honest_store'
        for i in range(128):
            files={'pkg/value.py':f'VALUE = {i}\n'.encode(), 'other.py':b'OTHER = 1\n'}
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures=[pool.submit(corrected,store,files) for _ in range(2)]
                sids=[f.result() for f in futures]
            assert sids[0]==sids[1]
            check_snapshot(store,sids[0],files)
            result['same_id_concurrent_publishes']+=1
            result['verified_concurrent_snapshots']+=1
        for i in range(128):
            left={'pkg/value.py':f'VALUE = {i}\n'.encode()}
            right={'pkg/value.py':f'VALUE = {-i-1}\n'.encode()}
            with ThreadPoolExecutor(max_workers=2) as pool:
                f1=pool.submit(corrected,store,left)
                f2=pool.submit(corrected,store,right)
                s1,s2=f1.result(),f2.result()
            assert s1!=s2
            check_snapshot(store,s1,left)
            check_snapshot(store,s2,right)
            assert (store/'CURRENT').read_text().strip() in (s1,s2)
            result['distinct_id_concurrent_publishes']+=1
            result['verified_concurrent_snapshots']+=2
        for i in range(128):
            previous=(store/'CURRENT').read_bytes()
            files={'pkg/value.py':f'VALUE = {i+1000}\n'.encode()}
            try:corrected(store,files,fail_before_pointer=True)
            except OSError:pass
            else:raise AssertionError('expected injected failure')
            assert (store/'CURRENT').read_bytes()==previous
            result['failure_rollbacks']+=1
        for i in range(16):
            out=root/f'outside-snap-{i}'
            out.mkdir()
            bad=root/f'bad-snap-{i}'
            bad.mkdir()
            (bad/'snapshots').symlink_to(out,target_is_directory=True)
            assert expect_rejected(lambda: corrected(bad,{'a.py':b'x=1\n'}))
            result['symlink_snapshots_rejections']+=1
        for i in range(16):
            bad=root/f'bad-final-{i}'
            bad.mkdir()
            files={'a.py':f'x={i}\n'.encode()}
            manifest=json.dumps({p:sha256(b).hexdigest() for p,b in files.items()},sort_keys=True,separators=(',',':')).encode()
            sid=sha256(manifest).hexdigest()
            (bad/'snapshots').mkdir()
            out=root/f'outside-final-{i}'
            out.mkdir()
            (bad/'snapshots'/sid).symlink_to(out,target_is_directory=True)
            assert expect_rejected(lambda: corrected(bad,files))
            result['symlink_final_rejections']+=1
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
