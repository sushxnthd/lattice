# Run439 prospectively frozen urllib3 #3352 wire-level oracle

**Frozen before inspecting any fixing PR/diff**.

- Issue: https://github.com/urllib3/urllib3/issues/3352
- Historical baseline: upstream urllib3 2.2.1, resolve immutable tag commit and source hashes before execution.
- Fixing reference: earliest merged upstream PR explicitly resolving #3352, immutable commit SHA pinned before historical oracle outcomes.
- Full frozen executable oracle: `run439_urllib3_3352_wire_oracle.py` SHA-256 `71863379e91c5e5eca24ae34193ca52dbc80fa93a5bf6f96229f65ef876497db`.
- Detailed local freeze: `RUN439_URLLIB3_3352_FREEZE.md` SHA-256 `221655ba8796d2b839490f70bab103d4308ebc5cee9c09c3fde6c1f8ecb0ad2d`.

Eight actual isolated-loopback request-target cases, all frozen: targets `//v:h`, `///v:h`, `//v:h?x=1`, `//user:pass@x`; controls `/v:h`, `//plain`, `/a//b`, `/?q=v:h`. All require HTTP 200 and byte-identical raw request-targets. A modern **non-historical** urllib3 2.7.0 exploratory execution passed 8/8, but does not qualify the historical repair.

Qualification: baseline fails >=1 target while preserving all controls; full reference passes all eight; >=2 production Python sources changed; deleting each of >=2 distinct reference source components breaks >=1 frozen target or control; any one-file reference alternative passing all eight disqualifies. Same isolated oracle, dependency closure, SHA verification, raw traces. No retuning after reference inspection. A wire-changing upstream fix fails this *strict benchmark contract*, not necessarily upstream's intended contract.

All 89 reserved boundary issues SEALED. No model inference on this issue until qualified. One K-SYNTH-1 kernel, canonical branch, one draft/unmerged PR #9.
