#!/usr/bin/env python3
"""Run423 minimal isolation counterexample (trusted local installed urllib3 only).

This intentionally preimports urllib3 to reproduce the failure on any Python
installation with urllib3. It does not execute model-generated code.
"""
import pathlib
import shutil
import sys
import tempfile

import urllib3

original = pathlib.Path(urllib3.__file__).parent
with tempfile.TemporaryDirectory(prefix="lattice-run423-") as root:
    destination = pathlib.Path(root) / "urllib3"
    shutil.copytree(original, destination)
    source = destination / "util" / "url.py"
    data = source.read_text()
    old = "if self.port:"
    new = "if self.port is not None:"
    assert data.count(old) == 1
    source.write_text(data.replace(old, new))
    for cache in destination.rglob("__pycache__"):
        shutil.rmtree(cache)

    sys.path.insert(0, root)
    from urllib3.util import Url
    naive_path = urllib3.__file__
    naive = Url(scheme="http", host="example.com", port=0).netloc
    assert naive == "example.com"

    for name in list(sys.modules):
        if name == "urllib3" or name.startswith("urllib3."):
            del sys.modules[name]
    import urllib3 as isolated
    from urllib3.util import Url as IsolatedUrl
    assert pathlib.Path(isolated.__file__).resolve().is_relative_to(
        destination.resolve()
    )
    repaired = IsolatedUrl(scheme="http", host="example.com", port=0).netloc
    assert repaired == "example.com:0"
    print({"naive_import": naive_path, "naive": naive,
           "isolated_import": isolated.__file__, "repaired": repaired})
