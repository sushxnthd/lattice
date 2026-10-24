"""Reconstruct patched Run212 editor from archived Run207/Run211 sources and run 27 tests."""
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
archive = base64.b64decode((parent / "run211/run211_source.tar.gz.b64").read_bytes())
backend = zlib.decompress(base64.b64decode((parent / "run207/repo_transaction.py.zlib.b64").read_bytes()))
with tempfile.TemporaryDirectory(prefix="lattice-run212-") as tmp:
    work = pathlib.Path(tmp)
    (work / "repo_transaction.py").write_bytes(backend)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tf:
        allowed = {"semantic_refactor.py", "test_semantic_refactor.py", "run211_differential.py"}
        if {m.name for m in tf.getmembers()} != allowed or not all(m.isfile() for m in tf.getmembers()):
            raise RuntimeError("unexpected Run211 source archive members")
        for member in tf.getmembers():
            (work / member.name).write_bytes(tf.extractfile(member).read())
    (work / "test_run212_adversarial.py").write_bytes((here / "test_run212_adversarial.py").read_bytes())
    subprocess.run(["patch", "--batch", "--forward", "-p1", "-i", str(here / "semantic_refactor.patch")],
                   cwd=work, check=True)
    subprocess.run([sys.executable, "-m", "unittest", "-q",
                    "test_semantic_refactor", "test_run212_adversarial"], cwd=work, check=True)
