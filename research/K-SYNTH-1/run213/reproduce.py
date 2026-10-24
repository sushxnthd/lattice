"""Rebuild Run213 from pinned repository archives and execute 32 tests."""
from __future__ import annotations
import base64
import io
import pathlib
import subprocess
import sys
import tarfile
import tempfile
import zlib

here = pathlib.Path(__file__).resolve().parent
parent = here.parent
archive = base64.b64decode((parent / 'run211/run211_source.tar.gz.b64').read_bytes())
backend = zlib.decompress(base64.b64decode((parent / 'run207/repo_transaction.py.zlib.b64').read_bytes()))
with tempfile.TemporaryDirectory(prefix='lattice-run213-') as tmp:
    work = pathlib.Path(tmp)
    (work / 'repo_transaction.py').write_bytes(backend)
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tf:
        expected = {'semantic_refactor.py', 'test_semantic_refactor.py', 'run211_differential.py'}
        if {m.name for m in tf.getmembers()} != expected or not all(m.isfile() for m in tf.getmembers()):
            raise RuntimeError('unexpected Run211 source archive members')
        for member in tf.getmembers():
            (work / member.name).write_bytes(tf.extractfile(member).read())
    (work / 'test_run212_adversarial.py').write_bytes((parent / 'run212/test_run212_adversarial.py').read_bytes())
    (work / 'test_run213_escape_safety.py').write_bytes(zlib.decompress(base64.b64decode(
        (here / 'test_run213_escape_safety.py.zlib.b64').read_bytes())))
    subprocess.run(['patch', '--batch', '--forward', '-p1', '-i',
                    str(parent / 'run212/semantic_refactor.patch')], cwd=work, check=True)
    patch = zlib.decompress(base64.b64decode((here / 'run212_to_run213.patch.zlib.b64').read_bytes()))
    patch_path = work / 'run213.patch'
    patch_path.write_bytes(patch)
    subprocess.run(['patch', '--batch', '--forward', '-p1', '-i', str(patch_path)],
                   cwd=work, check=True)
    subprocess.run([sys.executable, '-m', 'unittest', '-q',
                    'test_semantic_refactor', 'test_run212_adversarial',
                    'test_run213_escape_safety'], cwd=work, check=True)
