# K-SYNTH-1 Run362: prospectively frozen new AnyIO PR #595 qualification

**Freeze precedes the first historical 2x2 execution.** This is a NEW candidate task in repository `agronholm/anyio`, not one of the eight Run344 qualified PRs. Do not count it as qualified until the original frozen test passes and an independent verifier confirms the original artifact.

- PR: https://github.com/agronholm/anyio/pull/595, merged 2023-07-25.
- Pinned baseline commit: `6307392c6e590c130e57e991472633c0ceb6af0d`.
- Pinned reference PR head: `3f2f1f2f2c8b3b84c133e257af80b4ac4bb18466`.
- Component A: `src/anyio/_backends/_asyncio.py`, base Git blob `dd1f09c7998e45c496b4b6501f7a46225caaa964`, head blob `f8ed75609c0249ddae5273f589e2df6c7194d63f`.
- Component B: `src/anyio/streams/memory.py`, base blob `f74f8b8f123d69c345827565c018e268f2e83ae7`, head blob `530c60679d98a43e7ae5bdb158473f2b43d0c66e`.
- Four variants: `base`, `backend_only`, `memory_only`, `full`. Build each from the **same base source tree**, substituting only the SHA-verified head file for the selected component.
- Oracle: `run362_anyio_oracle.py`, 6 predeclared targets and 6 controls, Python 3.11 `asyncio` backend. Each case has a 3-second deadline; run all 12 independently, preserve failures, and never alter expectations after seeing outcomes.
- Target IDs: T1 event set then cancel; T2 nested event set then cancel; T3 shielded event set then cancel; T4/T5/T6 memory send then cancel at capacity 0/1/2.
- Control IDs: C1 ordinary event; C2 buffered memory; C3 rendezvous; C4 canceled blocked receive; C5 end of stream; C6 cancellation checkpoint.
- Qualify only if `full` passes all 12, `base` fails >=1 target while passing all six controls, and each partial variant fails >=1 target OR >=1 control. Require that **at least one target/control failure in the two partials is genuinely different**; this guards against trivial duplicated edits. Otherwise `NOT_QUALIFIED`, even if some cases improve. Report exact per-case factorial interactions; 12 tests are NOT 12 independent samples.
- Qualification is a finite historical functional certificate, NOT proof of causal mechanism, model success or IR superiority. The PR was selected with reference patch inspection for qualification; never pass that patch, changed lines, or this oracle's outcomes to the model. No post-outcome retuning or retroactive criteria changes.
- Isolation: no untrusted historical source or model code on the host. Historical source executes only in a no-network Docker container with read-only source, tmpfs, resource limits and dropped capabilities. Build/install dependencies before sandbox, record versions.
- Failure taxonomy: SOURCE_HASH_MISMATCH, BUILD_FAILURE, ORACLE_RUNTIME_FAILURE, NOT_QUALIFIED, QUALIFIED. Do not confuse infrastructure failures with failed repair.
- Preserve original workflow artifact, raw outputs, source Git blobs, oracle SHA, dependency versions and complete SHA256 manifest. Independently verify original evidence before counting. All 89 reserved boundary issues remain sealed; PR #9 stays draft/unmerged.
