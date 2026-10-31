# K-SYNTH-1 Run398 — bounded binding-time IR falsification against CPython

Date: 2026-11-01 IST. This is experiment-authored Python mechanism testing, **not** new qualified public-repository repair, coding-model inference, or IR superiority.

## Design
1024 deterministic two-module Python programs (seed 39820261101) each exercised three call paths: an import-time `from producer import f` snapshot, a live `module.f` dereference, and a definition-time function-default capture. Each runner applied 1–8 seeded assignments; every fourth runner also included an unsupported dynamic effect. Every case executed in a fresh `python -I -S` CPython subprocess. The bounded AST interpreter checked exact producer and consumer bodies and returned `UNKNOWN` on any unsupported effect.

## Original observations
| Metric | Result |
|---|---:|
| Original CPython subprocesses | 1024 |
| Functional call observations | 3072 |
| Bounded MUST predictions | 2304 |
| Bounded MUST mismatches | **0** |
| Explicit UNKNOWN observations | 768 |
| Dynamic/unsupported cases | 256 |
| Fixed-F0 source-name heuristic mismatches | 1166 / 3072 |
| Independent CPython reexecutions | 1024 |
| Independent audit checks | 8192 |
| Audit disagreements | **0** |
| Regression/adversarial tests | **12/12 pass** |

In 768 fully supported cases, import-snapshot versus live-call outputs differed in 385 cases, snapshot versus default in 393, and live versus default in 387. These are synthetic configurations, not independent repairs. The fixed-F0 heuristic is **not** an information-equivalent coding-model baseline.

## Mechanistic counterexample
A callable captured in both an alias and a default argument can have its `__code__` replaced. Both aliases keep exactly the same object identity while output changes from `ORIGINAL:7` to `REPLACEMENT:7`. Thus a sound binding-identity statement cannot be promoted to a MUST_BEHAVIOR statement under mutation. The bounded interpreter rejects such effects with `UNKNOWN`.

## Reproducibility
The local ZIP contains the original 1024 full raw CPython traces, complete AST interpreter, independent state-machine auditor, full CPython replay, 12 tests, counterexample, source hashes, and 14-entry SHA-256 manifest. ZIP SHA-256: `8c37ad05e1aee8acfd2e184a8b5d8cdfac62fa8c8415f84b2a10b00df50aa4c0`. The local archive is in the run history, not mirrored as a GitHub binary.

## Limitations and next priority
No new coding-model completions, independently qualified real repairs, or powered IR superiority result. The exact-source grammar is deliberately narrow; 0 observed mismatches is finite validation, not a general soundness theorem. Resume issue-first prospective real multi-source repair qualification and matched strong-model IR vs Python/AST functional evaluation. All 89 reserved boundary issues untouched.