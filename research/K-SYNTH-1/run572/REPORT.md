# Run572: symlink escape defeats lexical patch-path validation

Executed a local filesystem counterexample with a safe edit root and a symlink within that root pointing to an outside directory. `link/victim.py` has no `..` component and is lexically accepted, but resolves outside the allowed edit root. Three assertions passed. This falsifies any general filesystem-confinement claim based only on lexical path checks (including the restricted Run571 contract if interpreted as real filesystem safety).

A resolved-path containment check detects this static example but is not sufficient against time-of-check/time-of-use races. A production compiler should operate on preopened trusted directory descriptors, reject symlinks with platform-appropriate no-follow semantics, verify inode identity, and perform atomic staging/commit with rollback; this run does not validate those implementations. No production repair or model inference. Two real qualified tasks remain; 89 sealed untouched.

Local archive SHA256 `7cc8e2d788728e2cba86946de014a7590f853cf10f5bdab295129f99f2f679dd`.