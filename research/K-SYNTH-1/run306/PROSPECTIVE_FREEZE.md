# K-SYNTH-1 Run306 prospective freeze (before functional outcomes)

Research question: Does Run305's source-only alias transfer unsoundly rule out builtins.len after an unknown definition-time call mutates a module-level name? Bounded no-unmodeled-mutation assumption is deliberately violated; this is an adversarial scope test, not evidence of general soundness.

Original reference: Run305 annotation transfer, exact source as archived in Run305. Run306 may only strengthen uncertainty; it may not retroactively alter Run305 results.

Trusted generator: fixed 3 sites (annotation, positional default, decorator expression) x 2 effects (mutating restore of builtins.len, no-op) x 2 annotation modes (eager vs future) x 32 source variants = 384 records. Variant i uses argument length 1 + (i % 13). No randomized filtering. Eager annotation and default/decorator expressions are definition-time effects; postponed annotation is not. The mutating helper sets globals()['len'] = builtins.len. Initial len is a local lambda returning -777. After definition, len(list(range(k))) is the observation. A no-op helper returns a valid annotation/default/decorator without mutating len. No user/model code runs; trusted fixed source executes in subprocesses. Python version, source SHA256, runtime observation, static classification, and raw traces must be preserved.

Expected before observing:
- Mutating eager annotation, default, decorator => runtime builtins.len, hence MUST NOT be classified NOT_KNOWN_TARGET; old Run305 expected to fail this.
- Mutating postponed annotation => no effect, runtime local lambda; a conservative UNKNOWN is permitted.
- No-op => runtime local lambda; conservative UNKNOWN is permitted.
- Default and decorator still execute under postponed annotations.
- New transfer must invalidate all known module-level alias bindings after any unmodeled executed Call, while not claiming precision or global Python soundness. Deferred function-body calls must not mutate outer env during analysis.
- Independently audit raw functional records and source hashes using separate trusted CPython replay. No statistical independence claim for correlated variants.

Go/no-go: count pre-correction false-negative MAY cases, corrected false negatives, runtime mismatches, and source/trace hash discrepancies. Preserve all failures. Do not promote a sixth real task or make an IR-superiority claim.

Repository constraints: only sushxnthd/lattice, branch research/exp003-context-order, draft PR #9 open/unmerged; all 89 boundary issues SEALED. Preserve SHA-256 local artifacts and publish protocol, code, raw traces, independent audit, and limitations.
