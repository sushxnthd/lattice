# K-SYNTH-1 Run376 — reference-blind HTTPcore #670 qualified

## Prospective chronology
1. Selected [HTTPcore issue #670](https://github.com/encode/httpcore/issues/670) using only issue text and source at issue-linked base commit `5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e`.
2. **Before reading any fixing PR**, committed [PROSPECTIVE_FREEZE.md](PROSPECTIVE_FREEZE.md) at Lattice commit `991c9bcdf6d9ec36b090bf7a22a481788256b88c`. Frozen 2 public targets, 6 controls, 4 heldouts and 6 gates. No retuning.
3. Ran actual pinned historical source in isolated [original Actions run 41146310610](https://github.com/sushxnthd/lattice/actions/runs/41146310610): baseline targets both `ValueError`, 6/6 controls passed. Original artifact ID `13020802040`, ZIP SHA256 `1e25ab26f38a63e5ac73f2cfbde24765c1517b55c2c95942e3d41e7428676fdd`.
4. **After original run**, issue closure identified [reference PR #680](https://github.com/encode/httpcore/pull/680). It changes exactly two production files: `httpcore/_async/connection_pool.py` and `httpcore/_sync/connection_pool.py`. Applying both exact patches to the frozen base reproduced reference head Git blobs `10b7a55a4d0cc89b18247bde06724a561b5f4e7d` (async) and `1a7025e1724d933e1dffc1bcdf28bac5328d5435` (sync).
5. Executed original, async-only, sync-only, full factorial source trees with the **same frozen oracle**, including heldouts, in isolated [Actions run 41146453754](https://github.com/sushxnthd/lattice/actions/runs/41146453754). Artifact ID `13021760768`, ZIP SHA256 `c785739905b89d792f95d1f64d6bad8dabd7ec5812bb141ef3e29e6b029c53eb`.

## Exact functional outcomes

| Arm | Public targets | Public controls | Heldouts | Total |
|---|---:|---:|---:|---:|
| Baseline | 0/2 | 6/6 | 2/4 | **8/12** |
| Async-only reference | 1/2 | 6/6 | 3/4 | **10/12** |
| Sync-only reference | 1/2 | 6/6 | 3/4 | **10/12** |
| Full exact reference | 2/2 | 6/6 | 4/4 | **12/12** |

Independent read-only auditor recomputed all 48 factorial outcomes, exact source Git blobs, per-case raw SHA-256, and all six frozen qualification gates. Six adversarial/integrity tests passed. Both original artifact ZIP hashes were independently verified. Python 3.10.22, original HTTPcore 0.17.0 source, no network I/O, no upstream method monkeypatching. No post-outcome qualification changes.

**Verdict: QUALIFIED** as a prospectively frozen, two-production-source historical reference repair. Historical cohort advances from 9 to **10 unique qualified PRs**. Recompute unique repository count from the canonical cohort manifest before stating a new count.

**Mechanistic limitation:** All 12 casewise factorial interactions are **zero**. The two repairs fix disjoint sync/async behaviors; aggregate all-tests-pass synergy is not semantic coupling. This qualifies a production task but does not demonstrate semantic-IR superiority.

**Model evidence:** No new coding-model inference, no powered paired IR/Python result, no breakthrough. The next run must use reference-blind task facts and actual pinned open-model completions through an information-equivalent semantic-IR vs ordinary Python/AST baseline, same compiler/verifier/oracle, with raw prompts, model SHA, seeds, tokens, failures and functional traces.

**Reproducibility:** Frozen protocol, executable original oracle, factorial runner and two workflows are committed in this run's directory. Full original ZIPs, independent auditor and adversarial tests are preserved in local SHA-verified archive `lattice_run376_original_reference_blind_httpcore_pr680_qualification.zip`, archive SHA256 `2a528f36a614daadd82dee97d88eb22b41d4d1ef1ad675528e9e4083a072f41f` (10 payload hashes verified). Raw ZIP mirroring to GitHub remains incomplete. Sole PR #9 stays open/draft/unmerged on `research/exp003-context-order`; all 89 reserved boundary issues SEALED.
