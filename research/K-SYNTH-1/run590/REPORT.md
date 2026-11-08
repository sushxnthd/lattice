# K-SYNTH-1 Run590 — isolated Python execution-phase traces

Executed 12 deterministic synthetic Python programs in separate `python -I` child processes. All 12 matched prespecified event sequences after correcting a harness-only error: an initial `import json` was inserted ahead of `from __future__ import annotations`, producing a SyntaxError and initial 11/12 pass. After fixing import ordering, 12/12 passed. This was not a model/IR failure.

Cases: definition-time default arguments and decorators; deferred and invoked lambdas; deferred and consumed generators; boolean short-circuit; conditional expression; comprehension iteration; eager and postponed annotations. Per-case source SHA256, observed events, process status and stderr are preserved in local SHA-verified archive `lattice_run590.zip` (ZIP SHA256 `26e10a0a353b2f19688a2c9bdfbc18c439457482804970155ae30c5d5815dcad`).

Bounded synthetic functional traces only. No real production repair or coding-model inference; no IR superiority claim. Two real tasks remain qualified; 89 reserved boundary issues sealed. Full executable/raw GitHub mirroring outstanding.
