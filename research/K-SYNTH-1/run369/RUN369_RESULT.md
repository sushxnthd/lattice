# K-SYNTH-1 Run369 — bounded cross-module MAY graph, independently replayed

**2026-10-30 UTC.** Canonical sushxnthd/lattice, branch research/exp003-context-order, sole OPEN/DRAFT/UNMERGED PR #9. All 89 reserved issues SEALED.

## Scientific question

Can a soundness-scoped two-module semantic/dataflow MAY graph provide a defensible noninterference certificate without pretending to handle dynamic Python? Implemented a bounded pure Boolean fragment, explicit NO_DEPENDENCE / MAY_DEPEND / UNKNOWN, shared stale-preimage-checking atomic AST edit compiler, and two source-complete information-equivalent views (semantic graph versus ordinary Python/AST action).

## Actual results

| Experiment | Programs | CPython output evaluations | NO | MAY | UNKNOWN | False-negative NO |
|---|---:|---:|---:|---:|---:|---:|
| 4,096 seeded two-file AND-to-OR edit pairs | 4,096 | 32,768 | 3,506 | 590 | 0 | 0 |
| All 16 Boolean producer truth tables, fresh consumers | 512 | 34,816 | 416 | 96 | 0 | 0 |
| Six dynamic counterexamples and one masked-call false positive | 7 | 56 | 0 | 1 | 6 | N/A |
| **Total** | **4,615** | **67,640** | | | | **0 observed** |

Every original source, seed, exact Boolean output vector, status, and source SHA-256 was preserved. An independently implemented AST-call-graph and CPython execution auditor replayed **all 67,640 outputs** and found zero disagreements. **14/14 local tests passed**, including deliberately tampered outcome and classification evidence rejected by the auditor. The portable certificate agreed with the full checker on 4,103 source cases. Both presentation views used identical complete source facts and edit authority; all **4,096 common compiler transactions** yielded identical edited Python bytes.

The theorem is proved by induction on the accepted pure acyclic call DAG. A masked call is a genuine MAY false positive. Six dynamic cases return UNKNOWN despite observable output changes. The certificate is **not** a general Python analysis.

## Reproducibility

The complete 13-entry locally SHA-256-verified ZIP contains full runner, exhaustive truth-table evaluator, independent auditor, 14 tests, 4,615 original consumer sources, raw functional outcomes, theorem, protocol and manifests.

Archive SHA-256: `a880ff3aa190243b35f1fd453ec421b48fcb4829d911e7327c6379f5108b8c6f`.

This is a **synthetic soundness diagnostic**, not a real-repository qualification or model result. Nine unique historical reference-qualified PRs across seven repositories remain unchanged. No new model inference, powered IR advantage or breakthrough is claimed.

## Next

Recruit a genuinely reference-blind real multi-production-source issue; prospectively freeze target, heldout and controls before seeing the patch; execute exact historical factorial source variants in isolated oracles. Run a token-controlled capable-model semantic-IR versus ordinary Python/AST-action comparison with identical source/task facts, edit authority, compiler and evaluator. See PROTOCOL_RUN370.md. No sealed issue mutation.
