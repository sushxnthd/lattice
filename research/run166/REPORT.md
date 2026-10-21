# Run166 — package identity counterexample

The previous editor treats `pkg.py` and `pkg/__init__.py` as different module identities, whereas CPython resolves `pkg` to the package. In a three-file fixture, the old oracle accepts `from pkg import fn` while CPython raises ImportError. The corrected local editor canonicalizes `pkg/__init__.py` to `pkg` and rejects duplicate module identity.

48 local tests passed. No capable-model inference was performed. This does not establish representation advantage over Python.

Full executable evidence is available in the local Run166 archive pending repository integration.
