# K-SYNTH-1 Run344 — eighth historical reference-qualified PR; ABI-confounded interaction

**2026-10-29 UTC.** One canonical branch, sole OPEN/DRAFT/UNMERGED PR #9, all 89 reserved boundary issues SEALED.

## Original prospectively frozen experiment

New independent repository [pallets/jinja PR #1242](https://github.com/pallets/jinja/pull/1242), merged 2021-03-26. The [freeze](PROSPECTIVE_FREEZE.md) was committed `32cadd2835bb7bc5a18a47dfd11cd422e0f61400` **before** reference source/patch inspection; exact oracle SHA256 `4d121eb18d8071eacbf5967c7fa62e458f3bcad140b85be1f2398c163e37d5f0` was separately committed `ba73788c2986984cfad81dd4480a77883cffe1d0`. Base `94ccd028ef1f3cd9eaec862d6a1d646d02a242bc`, reference merge `f71f5ebab2e76c5ee6f5f705a2703f3891e762bc`. GitHub comparison: 3 commits ahead, 0 behind, only `compiler.py` and `runtime.py` production changes (plus changelog and tests).

[Original Actions 40901730453](https://github.com/sushxnthd/lattice/actions/runs/40901730453) **SUCCESS**; original artifact 12909906388 ZIP SHA256 `39ab4c5bbb7d33d791ce1d6f66adbf924a6f724b9dd3717de4b87134e1c00b6e`, matching GitHub artifact digest. All five inner SHA-256 manifest entries, source blobs, exact oracle/runner hashes, and 56/56 original functional records independently verified.

| Source arm | Targets /6 | Controls /8 |
|---|---:|---:|
| 00 baseline | 1 | 8 |
| 10 reference compiler only | 1 | 8 |
| 01 reference runtime only | 1 | 8 |
| 11 both reference files | 6 | 8 |

**Frozen decision: QUALIFIED historical reference-source task**, eighth unique PR in seventh repository, NOT a model repair. Five target cases have nonzero casewise factorial outcome interactions; eight controls have zero interaction.

## Crucial limitation: ABI confounding

Compiler-only failures include `TypeError` from forwarding newly emitted `_loop_vars` and `_block_vars` to the old runtime. Runtime-only lacks compiler-emitted assignment dictionaries and leaves a scoped-loop `UndefinedError`. Hence observed two-file necessity and five outcome interactions **do not certify ABI-independent semantic/dataflow interaction**. Mechanism status remains `UNKNOWN`; no original criterion was retuned.

After original recovery, source inspection showed the compiler emits private loop/block assignment dictionaries while the runtime derives context from them and removes private kwargs before calling user functions. A separately labelled **post-outcome miniature CPython model**, not historical source replay, executed 4,096 seeded context-transfer checks without disagreement. It shows ABI-only stripping prevents keyword errors but does not transfer assigned values. An actual historical compatibility-only ablation is proposed for Run345, not counted here.

Three independent local tests pass; four adversarial evidence mutations detected. Complete local SHA-verified reproducibility archive SHA256 `eb43f0146b9269bad921f67b298c85a394395957037a1eb1691590f328864144`. Auditor and code preserved locally; [original SHA-frozen oracle](run344_jinja_oracle.py.zlib.b64), [runner](run344_historical_runner.py.zlib.b64), [independent auditor](run344_independent_audit.py.zlib.b64) mirrored here.

**No new model inference, no powered IR-vs-Python/AST advantage, no breakthrough.** Eight reference-qualified issues are not eight independent model successes. All 89 boundary issues sealed.
