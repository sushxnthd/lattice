# Run315 postfreeze adversarial counterexample

This test was conducted **after** the prospective primary experiment. It is exploratory and does not retroactively modify the frozen criteria.

## Finding
The prototype snapshot publisher checks `dst.is_symlink()` but does not reject symlinks in ancestor directories. In a controlled temporary directory, an attacker who pre-created `snapshots/<predictable-content-id>/nested` as a symlink to a directory outside the store caused `publish({'nested/victim.py': b'x = 1\\n'})` to write `victim.py` outside the store. The functional witness reported `outside_write=true`. No user files were touched.

This is a **real path-confinement failure in the prototype**, not a deployed security vulnerability, remote-code-execution claim or Python semantic breakthrough. The adversary needs the ability to modify the snapshot directory or its parent.

## Required mitigation
Use a fresh private staging directory; reject symlinks in all existing ancestors; use descriptor-relative no-follow operations where available; publish only fully verified snapshots; test concurrent writers and crash consistency. An explicit filesystem threat model remains necessary.

The frozen primary results remain valid for their nonadversarial test scope, but the publisher must **not** be treated as safe against hostile filesystem state.

Original local postfreeze witness archive SHA-256: `d12ad51358f302ed235d9c674f864ad113eb146320b3c82dd317a671c3262788`. Its GitHub ZIP mirror is not yet available.