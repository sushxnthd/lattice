#!/usr/bin/env python3
"""K-SYNTH-1: trusted two-source, POSIX snapshot-publication experiment.

NOT an arbitrary Python editor, not a general-purpose filesystem transaction,
not safe against malicious concurrent writers or hostile filesystem metadata.
Readers MUST use read_snapshot() (one HEAD read) rather than open mutable paths.
Only the HEAD pointer is atomically replaced. A multi-file POSIX rename is not
claimed. Durability needs fsync and remains OS/filesystem dependent.
"""
from __future__ import annotations
import hashlib
import fcntl
import json
import os
from pathlib import Path
import shutil
import uuid
from run437_lossless_transaction import transact_lossless
from run436_dual_view_compiler import Unknown, sha

FILES=('provider.py','consumer.py')
POINTS=('after_provider_write','after_consumer_write','after_manifest_write',
        'after_generation_publish','after_head_tmp_write',
        'after_head_replace','after_head_dirsync')

class InjectedFailure(RuntimeError):
    pass

def _fsync_dir(path:Path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)

def _write_sync(path:Path,data:bytes):
    with open(path,'xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

def _manifest(gen:str, parent:str|None, sources:dict[str,bytes]):
    return {'schema':'K-SYNTH-1/SNAPSHOT-v1','generation':gen,
            'parent':parent,'source_sha256':{name:sha(sources[name]) for name in FILES}}

def _verify_generation(root:Path,gen:str)->dict[str,bytes]:
    if not (gen and len(gen)==64 and all(c in '0123456789abcdef' for c in gen)):
        raise Unknown('UNKNOWN_HEAD_ID')
    path=root/'generations'/gen
    if not path.is_dir() or path.is_symlink():
        raise Unknown('UNKNOWN_GENERATION_DIR')
    try:
        manifest=json.loads((path/'manifest.json').read_bytes())
        if manifest['schema']!='K-SYNTH-1/SNAPSHOT-v1' or manifest['generation']!=gen or set(manifest['source_sha256'])!=set(FILES):
            raise ValueError('bad manifest')
        sources={name:(path/name).read_bytes() for name in FILES}
        if any((path/name).is_symlink() for name in FILES):
            raise ValueError('symlink')
        if manifest['source_sha256']!={name:sha(sources[name]) for name in FILES}:
            raise ValueError('bad source digest')
        expected=_generation_id(manifest['parent'],sources)
        if expected!=gen:
            raise ValueError('bad generation commitment')
        return sources
    except (OSError,KeyError,ValueError,TypeError,json.JSONDecodeError) as e:
        raise Unknown('UNKNOWN_SNAPSHOT_INTEGRITY') from e

def _generation_id(parent:str|None,sources:dict[str,bytes]):
    payload=json.dumps({'parent':parent,'source_sha256':{k:sha(sources[k]) for k in FILES}},sort_keys=True,separators=(',',':')).encode()
    return sha(payload)

def read_snapshot(root:Path)->tuple[str,dict[str,bytes]]:
    root=Path(root)
    head=(root/'HEAD').read_text(encoding='ascii').strip()
    return head,_verify_generation(root,head)

def init_store(root:Path,sources:dict[str,bytes]):
    root=Path(root)
    if root.exists(): raise Unknown('UNKNOWN_ALREADY_INITIALIZED')
    root.mkdir(parents=True)
    (root/'generations').mkdir()
    (root/'staging').mkdir()
    _write_sync(root/'LOCK',b'K-SYNTH-1 single-writer lock\n')
    gen=_generation_id(None,sources)
    d=root/'generations'/gen
    d.mkdir()
    for name in FILES:_write_sync(d/name,sources[name])
    _write_sync(d/'manifest.json',(json.dumps(_manifest(gen,None,sources),sort_keys=True)+'\n').encode())
    _fsync_dir(d);_fsync_dir(root/'generations')
    _write_sync(root/'HEAD',(gen+'\n').encode())
    _fsync_dir(root)
    assert read_snapshot(root)==(gen,sources)
    return gen

def commit(root:Path,action:dict,mode:str,fail_at:str|None=None)->dict:
    """Single trusted writer; inject failure after any named checkpoint.

    On exception after HEAD replacement, operation may have COMMITTED. Caller
    MUST reconcile via read_snapshot rather than treating exception as rollback.
    """
    root=Path(root)
    if fail_at is not None and fail_at not in POINTS: raise ValueError('bad injection point')
    parent,sources=read_snapshot(root)
    outputs,receipt=transact_lossless(sources,action,mode)
    gen=_generation_id(parent,outputs)
    stage=root/'staging'/uuid.uuid4().hex
    stage.mkdir()
    def point(name):
        if fail_at==name: raise InjectedFailure(name)
    for name,checkpoint in [('provider.py','after_provider_write'),('consumer.py','after_consumer_write')]:
        _write_sync(stage/name,outputs[name]);point(checkpoint)
    _write_sync(stage/'manifest.json',(json.dumps(_manifest(gen,parent,outputs),sort_keys=True)+'\n').encode())
    point('after_manifest_write')
    _fsync_dir(stage)
    dest=root/'generations'/gen
    if dest.exists():
        if _verify_generation(root,gen)!=outputs:raise Unknown('UNKNOWN_GENERATION_COLLISION')
        shutil.rmtree(stage)
    else:
        os.replace(stage,dest)
        _fsync_dir(root/'generations')
    point('after_generation_publish')
    head_tmp=root/('HEAD.tmp.'+uuid.uuid4().hex)
    _write_sync(head_tmp,(gen+'\n').encode())
    point('after_head_tmp_write')
    os.replace(head_tmp,root/'HEAD')
    point('after_head_replace')
    _fsync_dir(root)
    point('after_head_dirsync')
    actual,check=read_snapshot(root)
    assert actual==gen and check==outputs
    return {'parent':parent,'generation':gen,'compiler':receipt,
            'atomic_visibility_scope':'snapshot readers, single writer, same filesystem',
            'durability_scope':'fsync on files, generation directory, HEAD directory; no simulated power-loss guarantee'}

def recover(root:Path):
    """Validate HEAD then clean incomplete stage dirs; retain all generations."""
    root=Path(root)
    head,sources=read_snapshot(root)
    stale=[]
    for child in (root/'staging').iterdir():
        if child.is_symlink() or not child.is_dir():
            raise Unknown('UNKNOWN_STAGING_ENTRY')
        shutil.rmtree(child);stale.append(child.name)
    for child in root.glob('HEAD.tmp.*'):
        if child.is_symlink() or not child.is_file():
            raise Unknown('UNKNOWN_TEMP_ENTRY')
        child.unlink();stale.append(child.name)
    _fsync_dir(root/'staging');_fsync_dir(root)
    return {'head':head,'source_sha256':{k:sha(v) for k,v in sources.items()},'cleaned':len(stale)}

def commit_locked(root:Path,action:dict,mode:str,fail_at:str|None=None):
    """POSIX advisory single-writer serialization; readers remain lock-free."""
    root=Path(root)
    with open(root/'LOCK','rb') as lock:
        fcntl.flock(lock.fileno(),fcntl.LOCK_EX)
        try: return commit(root,action,mode,fail_at)
        finally: fcntl.flock(lock.fileno(),fcntl.LOCK_UN)
