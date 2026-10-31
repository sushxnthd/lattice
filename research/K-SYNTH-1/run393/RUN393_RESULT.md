# K-SYNTH-1 Run393: ORIGINAL pinned urllib3 PR5126 socket oracle

Date: 2026-10-31 UTC. Sole kernel K-SYNTH-1; canonical branch `research/exp003-context-order`; sole PR #9 draft/unmerged; 89 sealed issues untouched.

**Original prospective qualification: FAILED. Do not promote, retune, or count as a qualified task.**

Frozen protocol (before reference inspection): [Run392 PR5126 protocol](../run392/PROTOCOL_PR5126_PRE_REFERENCE.md), commit `3b951406391805a2fb8bd95710dc8e0401fe9211`. Exact base `e349d97f2bf234b95d5dd9e689d056a521dfc3b0`; reference `580df2aab0340c2f81cf2770012875e4530a101d`. All source Git blob hashes verified.

| Original case group | Baseline | connectionpool only | poolmanager only | Full reference |
|---|---:|---:|---|---:|
| Public T1-T3 | 0/3 | 0/3 | import failure | 3/3 |
| Heldout H1-H4 | 0/4 | 0/4 | import failure | **3/4** |
| Controls C1-C6 | 6/6 | 6/6 | import failure | 6/6 |
| Total | 6/13 | 6/13 | import failure | **12/13** |

The poolmanager-only source cannot import `_is_same_host` from the unmodified connectionpool module. The full reference passes all cases except the **original H4 exact Host serialization check**. The original H4 wire shows `GET http://google.com:80/second HTTP/1.1`, `Host: google.com`, and preserved Authorization/Cookie, whereas the oracle expected `Host: google.com:80`. These hosts have equivalent default-port HTTP origin semantics. **Post-hoc sensitivity only**: this suggests an underspecified/overstrict oracle, not license to change the original FAIL or qualification outcome.

First cloud attempt [41218649287](https://github.com/sushxnthd/lattice/actions/runs/41218649287), commit `86328fdd`, failed to import checkout because generated `urllib3._version` was absent. Corrected attempt [41218713569](https://github.com/sushxnthd/lattice/actions/runs/41218713569), commit `fd8b4c37`, installed the pinned checkout; source-hash preflight passed in all four jobs. All original artifacts preserved, including the failed attempt. An independent read-only auditor verified eight original ZIP SHA-256 digests, corrected internal manifests, exact source blobs, oracle SHA-256 `036dff47bcbf96484d37bd98c08528b4671cd17d64aa6e7f7442696d5a43824b`, all 39 executed outcomes and original H4 wire. Six adversarial/regression audit tests passed.

The locally SHA-verified 21-payload archive is `lattice_run393_original_pinned_pr5126_oracle_and_h4_failure.zip`, SHA-256 `ee13680f51f1f70753cf3dc89dfdb9ec8f0b16c6a758bf0a740950c84cc7ceb1`. Historical qualified cohort unchanged. No model inference, functional model repair, semantic-IR superiority or breakthrough claim. PR5126 is solution-contaminated for blind model evaluation. Continue recruiting genuinely unseen multi-source tasks with prospectively specified Host-equivalence semantics.
