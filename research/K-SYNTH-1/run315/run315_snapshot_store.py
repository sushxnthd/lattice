"""Immutable snapshots with a single atomic pointer publication.

Readers MUST resolve CURRENT once then read files under that snapshot. This
avoids claiming impossible all-file atomicity for independent path overwrites.
This is a local prototype, not a crash-consistency proof on all filesystems.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from run315_multifile_compiler import checked_path, PatchRejected


def publish(store: Path, files: dict[str, bytes], *, fail_before_pointer=False) -> str:
    store.mkdir(parents=True, exist_ok=True)
    canonical = {checked_path(p): hashlib.sha256(data).hexdigest() for p,data in files.items()}
    if len(canonical) != len(files):
        raise PatchRejected('duplicate path')
    manifest = json.dumps(canonical, sort_keys=True, separators=(',',':')).encode()
    snapshot_id = hashlib.sha256(manifest).hexdigest()
    snap = store / 'snapshots' / snapshot_id
    snap.mkdir(parents=True, exist_ok=True)
    for rel, data in files.items():
        dst = snap / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_symlink():
            raise PatchRejected('symlink in snapshot')
        if dst.exists():
            if dst.read_bytes() != data:
                raise PatchRejected('snapshot hash collision or mutation')
            continue
        with NamedTemporaryFile(dir=dst.parent, delete=False) as f:
            tmp = Path(f.name)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, dst)
    (snap/'MANIFEST.json').write_bytes(manifest)
    if fail_before_pointer:
        raise OSError('injected prepublication failure')
    with NamedTemporaryFile(dir=store, delete=False, mode='w', encoding='ascii') as f:
        tmp = Path(f.name)
        f.write(snapshot_id+'\n')
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, store/'CURRENT')
    return snapshot_id

def read_current(store: Path) -> dict[str, bytes]:
    snapshot_id = (store/'CURRENT').read_text(encoding='ascii').strip()
    if len(snapshot_id) != 64 or any(x not in '0123456789abcdef' for x in snapshot_id):
        raise PatchRejected('invalid snapshot pointer')
    snap = store/'snapshots'/snapshot_id
    manifest = (snap/'MANIFEST.json').read_bytes()
    if hashlib.sha256(manifest).hexdigest() != snapshot_id:
        raise PatchRejected('invalid snapshot manifest')
    mapping = json.loads(manifest)
    result = {}
    for path, sha in mapping.items():
        checked_path(path)
        data = (snap/path).read_bytes()
        if hashlib.sha256(data).hexdigest() != sha:
            raise PatchRejected('snapshot content corrupted')
        result[path] = data
    return result
