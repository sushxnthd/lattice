# K-SYNTH-1 Run343 — seven-task cohort reconciliation and new Click negative

**2026-10-29 UTC.** Canonical branch `research/exp003-context-order`, sole OPEN/DRAFT/UNMERGED PR #9; 89 reserved boundary issues SEALED.

## Historical cohort correction

Re-fetched the immutable GitHub qualification reports and their Git blob SHAs. Deduplicate by **(repo, PR)**, not by automation run or oracle. The historical reference-source-qualified cohort is **SEVEN unique PRs in SIX repositories**:

| Original run | PR | Evidence |
|---|---|---|
| 256 | [Flask #6096](https://github.com/pallets/flask/pull/6096) | [report](../run256/RUN256_RESULT.md) |
| 264 | [urllib3 #5071](https://github.com/urllib3/urllib3/pull/5071) | [report](../run264/RUN264_RESULT.md) |
| 278 | [Werkzeug #3136](https://github.com/pallets/werkzeug/pull/3136) | [report](../run278/RUN278_RESULT.md) |
| 283 | [HTTPcore #1000](https://github.com/encode/httpcore/pull/1000) | [report](../run283/RUN283_RESULT.md) |
| 297 | [h11 #115](https://github.com/python-hyper/h11/pull/115) | [report](../run297/RUN297_RESULT.md) |
| 328 | [HTTPX #1183](https://github.com/encode/httpx/pull/1183) | [report](../run328/RUN328_RESULT.md) |
| 340 | [HTTPcore #882](https://github.com/encode/httpcore/pull/882) | [report](../run340/RUN340_RESULT.md) |

The previous Run328 “third” and Run340 “fourth” labels inadvertently omitted earlier Run278/283/297 qualifications. Run342 h11 #115 is a failed *holdout of an already counted PR*, not a new task. This correction does not promote excluded PRs or equate source qualification with model-generated repair. Five of six two-component factorials have aggregate target interaction zero; Werkzeug #3136 has +1. The seventh is a three-file leave-one-out. Mechanism certification remains UNKNOWN.

## Prospectively frozen new Click PR1604 experiment

Frozen before inspecting reference patch or running the historical oracle: [PROSPECTIVE_FREEZE.md](PROSPECTIVE_FREEZE.md), commit `8b5192d3ae0693f5191bcac4052480aa1dad8349`. Frozen oracle SHA256 `903b306fca3f2fb03eb8277cc6d34631dd1edde032aa665f5b013c9045bdf397`, protocol SHA256 `b90f142e29a68e20a4c03d1a142074016d08849c708a6d37641cb8cef4d1bc5a`. Source base `6271cee2e8b2cf9a392377271bc9ed8345ce77c8`, head `3d3ea9c64420fd8978a41ce8b4db3ac2d245849c`; GitHub comparison confirmed head is one commit ahead, zero behind.

[Original Actions 40891441900](https://github.com/sushxnthd/lattice/actions/runs/40891441900) **SUCCESS**, original artifact 12903609831, ZIP SHA256 `142ca704753eaf1db29840ed41351ee2bfb7c72219822f36ee2df6591399203f` (matches GitHub digest). Five frozen source arms, 14 cases each:

| Arm | Targets /6 | Controls /8 |
|---|---:|---:|
| base | 1 | 8 |
| core-only | 3 | 8 |
| parser-only | 4 | **6** |
| full reference | 6 | **6** |
| identity ABI negative | 1 | 8 |

**Original prospective qualification FAILED**. Full reference violates frozen CLI controls C01 (variadic CLI arguments disappear without envvar value) and C08 (envvar overrides explicit CLI arguments). No retuning, no promotion. Independent read-only audit verified 6/6 original artifact manifest entries and **70/70 original functional classifications**; all 14 casewise 2×2 interactions are zero. 15 local tests PASS, including 24/24 adversarial evidence mutations.

Only **after** outcome recovery, inspected PR patch: `Argument.process` sets `value = None` when `nargs == -1 and obj.envvar is not None`, testing declaration rather than actual envvar presence. This provides a bounded source-level explanation for the two observed regressions; it is not a claim about current Click or all runtime contexts.

Exact SHA-frozen [compressed oracle](run343_click_oracle.py.zlib.b64), [isolated runner](run343_historical_runner.py.zlib.b64) and [workflow](../../../.github/workflows/lattice-k-synth-1-run343-click.yml) are mirrored. Complete local reproducibility ZIP includes raw cloud artifact, all code, tests, full report and provenance ledger. Historical seven-task cloud ZIP reauditing is still incomplete.

**No new qualified task, no new coding-model inference, no powered IR advantage or breakthrough.** Next: new independent repository candidate and matched model feasibility on the corrected seven-issue historical cohort.
