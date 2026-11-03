# K-SYNTH-1 Run449 — unseen real-API factorial transfer

Date: 2026-11-03 UTC. One K-SYNTH-1 kernel; branch `research/exp003-context-order`; PR #9 open/draft/unmerged. All 89 reserved boundary issues sealed.

## Prospective finite-effect prediction
From Run448, only P (`poolmanager.py`) should change pool/proxy outputs, only U (`util/url.py`) netloc outputs, and only C (`connectionpool.py`) same-host outputs, for new frozen cases. This is a *finite outcome* prediction, not a source-level cross-file soundness theorem.

Frozen `FROZEN_UNSEEN_CASES.json` SHA256: `e66a1289fac5d69f8c04a19d9fa81b3309f8f2e943be63b8854f8cd651bc86e9`. The hash and prediction were printed before variant staging/execution. 924 new host/port/API cases, 8 full SHA-pinned urllib3 2.7.0 production-source variants, separate isolated CPython processes, socket networking disabled, no model-generated code executed.

| Public API | Cases | Nonidentical factorial outcomes | Sole observed effect |
|---|---:|---:|---|
| Pool manager | 84 | 12 | P |
| Proxy manager | 84 | 12 | P |
| Netloc | 84 | 12 | U |
| Same-host explicit | 84 | 0 | none |
| Same-host cross | 588 | 0 | none |
| **Total** | **924** | **36** | **no non-owner effects** |

7,392 genuine public-API executions, 11,088 independently audited component-by-context comparisons, zero non-owner effects, zero context-dependent effect indicators. Independent auditor verified 312 staged source-file hashes across eight variants, 924 finite-effect certificates with explicit `UNKNOWN` outside the frozen cohort, and 21/21 tests including three evidence-corruption rejection tests. Clean extraction of the local ZIP independently verified all 382 SHA-manifest payloads and replayed the auditor and 21 tests.

### Exact finite-factorial theorem
For a fixed input x, let F_x:{0,1}^3→Ω be the observed eight-variant outcome function, including exceptions. If for every non-owner component j≠k and all four contexts of the remaining bits, toggling j preserves F_x, then F_x depends only on k on that finite cube. Proof: flip non-owner bits successively to a canonical assignment; every step preserves the outcome. This does not establish general Python soundness, absence of cross-file calls, or mandatory edit dependencies.

**Coverage limitation:** Port choices `None,0,7,81,444,65534,8081` exclude defaults 80/443, so no C effect was activated in the new cohort. This must be tested in a separately frozen follow-up, not retroactively changed. Structured cases are not IID, so no population binomial confidence bound is justified.

**Status:** Still exactly TWO independently qualified historical multi-production-source repairs (Flask PR6096 and urllib3 PR5071). No new model completions, no powered IR-vs-Python superiority evidence, no breakthrough. Full raw traces, 8 staged source trees, original licensed upstream source, independent auditor, 21 tests, manifest and ZIP remain in the SHA-verified local Run449 archive. Historical GitHub ZIP mirroring incomplete.
