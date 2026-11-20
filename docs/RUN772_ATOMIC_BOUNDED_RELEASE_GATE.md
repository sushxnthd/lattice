# Run772 — atomic bounded release-gate candidate (2026-11-20 UTC)

Local Python 3.13.5 reproducibility archive SHA-256: `304dc7038de1e528c7badb6170da8d507b8f2365445125953f82e3b1af53b678`.

Seven deterministic local tests passed: clean pinned wheel; wrong pin; malformed pin; caller path swapped after immutable snapshot; subsequent changed-path rejection; highly compressed wheel rejected even with matching pin; 257-entry archive rejected even with matching pin.

Mechanism: read at most MAX_WHEEL_BYTES+1 bytes once; validate external pin and ZIP resource bounds on that same in-memory snapshot; write snapshot to private temporary wheel; run RECORD verifier on private snapshot. This removes the prior two-open caller-path race between resource checks and pinned RECORD verification. Does not authenticate publisher, prevent malicious authenticated wheels, or constitute a public release. Full executable code, traces, fixture, manifest are in local SHA-verified Run772 archive; not yet mirrored. No model inference or real-task qualification. No superiority claim. PR #9 stays draft/unmerged; 89 reserved issues untouched.