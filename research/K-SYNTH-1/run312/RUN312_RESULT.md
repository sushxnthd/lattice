# K-SYNTH-1 Run312 result — sixth historical real repair qualified

Date 2026-10-28 UTC. One K-SYNTH-1 kernel. Canonical branch `research/exp003-context-order`, PR #9 open/draft/unmerged, all 89 reserved boundary issues sealed.

## Original h11 PR #115 prospective public qualification

Pinned upstream base `522b00470b5776dda2dc7e98ff778eb1e418e6ad` and reference PR head `a1197d68630bc37a941b516c7cc74833460fc97c`; changed production files `h11/_receivebuffer.py`, `h11/_connection.py`, `h11/_readers.py`. Frozen protocol commit `338aca5cb91a0747a5b61a73c25fb9c80e09eb08` precedes oracle execution. CPython 3.9.25 in disposable GitHub Actions. Original attempt [40663248246](https://github.com/sushxnthd/lattice/actions/runs/40663248246) failed before scientific execution because fork head was not fetched; corrected [40663342378](https://github.com/sushxnthd/lattice/actions/runs/40663342378) succeeded without changing criteria.

| Arm | Targets /6 | Controls /6 |
|---|---:|---:|
| BASE | 0 | 6 |
| BUFFER+CONNECTION | 6 | 4 |
| READERS | 0 | 4 |
| FULL | 6 | 6 |

Original artifact ID `12804318765`, ZIP SHA256 `cd6b78d59128c656162427d1a9bc2090077e7ebfa19f991ba6b3115cd9cd1128`. Independent read-only replay verified 10 manifest entries, all 48 original event traces, source SHA relationships and zero functional-label discrepancies. Public-only gate passed; full qualification required a separate heldout.

## Prospectively frozen independent heldout

Supplemental protocol committed `038c05a440455dcf92e0fc6af9a1642e51cb331b` **before** heldout execution. Seed 312115; 32 LF/mixed targets, 32 CRLF/chunked controls with randomized fragmentation, exact response status/body/header/EOM oracle. Seven historical-source arms, 448 functional event traces. Original isolated [Run312B cloud run](https://github.com/sushxnthd/lattice/actions/runs/40663627762) succeeded. Independent auditor verified all 16 manifest entries, all 448 event traces, all source SHA constraints, zero outcome discrepancies.

| Arm | Targets /32 | Controls /32 |
|---|---:|---:|
| BASE | 0 | 32 |
| BUFFER only | 0 | 0 |
| CONNECTION only | 0 | 32 |
| READERS only | 0 | 24 |
| BUFFER+CONNECTION | 32 | 24 |
| BUFFER+READERS | 0 | 0 |
| FULL | 32 | 32 |

Original heldout artifact ID `12805146193`, ZIP SHA256 `c64f41b0bad8a2dca8cf670c58209c1e73ad2b58855fff7d3a9847f8e31eaeaf`. Both frozen gates PASS. Three changed production files are necessary for the joint target/control contract: receivebuffer enables LF/mixed headers, readers restores chunked controls, connection removes obsolete `compress()` use. **Sixth independently qualified historical multi-production-file repair.** This is *not* a model-generated repair or proof of semantic-IR superiority. The 64 heldout cases are correlated within one repository, not independent issues.

## Run312 secondary synthetic estimand counterexample

Prospective design protocol commit `de86f3cc415af90539896992f74b94c84586b9ba`. With 100 small repos (2 issues each, p=.8 IR win conditional on discordance), 100 large repos (20 issues each, p=.4), and discordance q=.3, the theoretical repository-weighted paired effect is **+.0600**, but the issue-weighted effect is **-.0381818**. In 10,000 frozen simulations, 9,986 studies showed opposite signs; 8,859 issue-weighted tests rejected negatively and 8,461 repository-weighted tests rejected positively (cluster-aware t tests). Independent audit rederived 2,000,000 repository scores and every decision with zero discrepancies. Raw gzip SHA256 `bedc668c51f4e24187e0d037cc8d58d431213beaa656aa5fe6b39c9f016cd87c`. Synthetic design result, not model performance.

## Decision

Six qualified historical repairs, but **no new capable-model inference, powered IR-vs-Python comparison, mechanism attribution or breakthrough**. Primary future estimand should be issue-weighted paired repair effect with repository-cluster-aware inference; report repository-weighted effect separately. Continue frozen, reference-localization-blind real paired coding-model experiments. Local full 14-payload SHA archive: `lattice_run312_h11_qualified_and_estimand_counterexample.zip` SHA256 `477c932fde534277dda236543dbd5e9628ce5b5337056c6ca9086743316d05e3`; full historical GitHub ZIP mirroring remains incomplete.
