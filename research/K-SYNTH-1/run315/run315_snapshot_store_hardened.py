"""Postfreeze bounded hardening against pre-existing symlink ancestors.

Uses private random staging + atomic directory rename + single CURRENT pointer.
Not proven secure against an adversary with concurrent write access to store,
network filesystem semantics, power loss, or other crash-consistency hazards.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from run315_multifile_compiler import PatchRejected, checked_path


def _check_store(store: Path) -> None:
    for parent in [store, store / 'snapshots']:
        if parent.is_symlink():
            raise PatchRejected('symlink in store ancestry')
        if parent.exists() and not parent.is_dir():
            raise PatchRejected('non-directory store component')


def _verify(snap: Path, manifest: bytes, mapping: dict[str, str]) -> None:
    if snap.is_symlink() or not snap.is_dir():
        raise PatchRejected('snapshot path is not a directory')
    manifest_path=snap/'MANIFEST.json'
    if manifest_path.is_symlink() or not manifest_path.is_file() or manifest_path.read_bytes()!=manifest:
        raise PatchRejected('snapshot manifest mismatch')
    for rel, expected in mapping.items():
        target=snap
        for part in Path(rel).parts:
            target=target/part
            if target.is_symlink():
                raise PatchRejected('snapshot symlink ancestor')
        if hashlib.sha256(target.read_bytes()).hexdigest()!=expected:
            raise PatchRejected('snapshot file mismatch')


def publish(store: Path, files: dict[str, bytes], *, fail_before_pointer=False) -> str:
    _check_store(store)
    store.mkdir(parents=True,exist_ok=True)
    snaps=store/'snapshots'
    snaps.mkdir(exist_ok=True)
    _check_store(store)
    if not files or len(files)>64:
        raise PatchRejected('empty or oversized snapshot')
    mapping={}
    for rel,data in files.items():
        if checked_path(rel)!=rel or type(data) is not bytes:
            raise PatchRejected('invalid snapshot member')
        mapping[rel]=hashlib.sha256(data).hexdigest()
    manifest=json.dumps(mapping,sort_keys=True,separators=(',',':')).encode()
    sid=hashlib.sha256(manifest).hexdigest()
    final=snaps/sid
    stage=Path(tempfile.mkdtemp(prefix='.staging-',dir=snaps))
    try:
        for rel,data in files.items():
            dst=stage/rel
            dst.parent.mkdir(parents=True,exist_ok=True)
            fd=os.open(dst,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
            with os.fdopen(fd,'wb') as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
        (stage/'MANIFEST.json').write_bytes(manifest)
        _verify(stage,manifest,mapping)
        if final.is_symlink():
            raise PatchRejected('preexisting symlink at snapshot destination')
        if final.exists():
            _verify(final,manifest,mapping)
        else:
            try:
                os.rename(stage,final)
            except OSError as exc:
                if not final.exists() or final.is_symlink():
                    raise PatchRejected('snapshot publication conflict') from exc
                _verify(final,manifest,mapping)
        _verify(final,manifest,mapping)
        if fail_before_pointer:
            raise OSError('injected prepublication failure')
        fd,tmp=tempfile.mkstemp(prefix='.current-',dir=store)
        try:
            with os.fdopen(fd,'w',encoding='ascii') as f:
                f.write(sid+'\n')
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp,store/'CURRENT')
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
        return sid
    finally:
        if stage.exists():shutil.rmtree(stage)
