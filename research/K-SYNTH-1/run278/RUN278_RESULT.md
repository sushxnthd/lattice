# K-SYNTH-1 Run278 | Third independently qualified real two-production-file repair

**2026-10-26 UTC / 2026-10-27 IST.** Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9. All 89 reserved boundary issues SEALED.

## Prospectively frozen scientific qualification

[Werkzeug PR3136](https://github.com/pallets/werkzeug/pull/3136) was merged 2026-03-24. Exact direct-parent base `b913d68db5898c8f3def3c09a653aaf95abe38e5`, direct-child reference `23142a3cb5d1b5ba8e9914980934477e0abdc30e`. Production components `src/werkzeug/routing/matcher.py` and `src/werkzeug/routing/rules.py`. Frozen before source ablations: four public-API target checks, six nonregression controls, four source configurations and joint component-necessity criterion.

Original successful [Actions 40423005451](https://github.com/sushxnthd/lattice/actions/runs/40423005451), artifact 12698880923, original ZIP SHA256 `cf421939e7d689a334f1deccbd9dd9ebecd2822c043f19cb287d941d507e5123`. All five original artifact manifest hashes independently verified. Separate read-only auditor confirmed all 40 public-API outcomes and exact source configuration hashes.

| Source configuration | Targets | Controls | Total |
|---|---:|---:|---:|
| Baseline | 0/4 | 6/6 | 6/10 |
| Matcher only | 1/4 | 6/6 | 7/10 |
| Rules only | 2/4 | 6/6 | 8/10 |
| Full reference | 4/4 | 6/6 | 10/10 |

The frozen T3 joint long-slash repair passes **only** with both production components. Finite 2x2 correctness interaction: `10-7-8+6=+1`, all from targets; controls remain 6/6 in every variant. This establishes source-component necessity for these tests, **not impossibility of alternative one-file repairs**.

## Post-qualification, pre-execution frozen mechanism holdout

Committed `holdout_prediction.json` **before** executing six new seven-slash-length cases on four configurations. Corrected [Actions 40423352600](https://github.com/sushxnthd/lattice/actions/runs/40423352600), artifact 12698936318, ZIP SHA256 `7c25f4721dd70cfa9c1b2424b5b89d271fecf9ac483c228b565a44f1312821f3`. All five manifest entries independently verified; all **24/24 frozen binary predictions correct**; identical source hashes to original qualification. This is within-issue mechanism prediction, **not unseen-issue generalization**.

## New soundness-scoped semantic result

Implemented `slash_quantifier_ir.py` and `test_slash_quantifier_ir.py`. For maximal slash run length `k`, literal `re.sub('/{2,}?','/',s)` produces `ceil(k/2)` slashes, while literal `re.sub('/{2,}','/',s)` produces one slash for `k>=1`. Proof: non-greedy global matches consume disjoint pairs, greedy consumes the maximal run. Other characters remain unchanged. This is exact only for these two literal patterns, literal slash replacement, exact Python strings and zero flags. Dynamic bindings/patterns are explicitly `UNKNOWN`. 1024 deterministic random-string trials per pattern, exhaustive slash lengths 0..512, 14/14 local tests passed across audits, freeze and semantic tests. **Not a general sound Python dataflow IR**.

## Preserved infrastructure failures

Original [40422855823](https://github.com/sushxnthd/lattice/actions/runs/40422855823), ZIP SHA256 `01917d3c336511ce27cbe470f67383dbc8a01018310f88556091b83f848b62ad`, produced 40 path-related `HARNESS_EXIT:2` outcomes; scientifically censored, not repair failures. Transport retries 40422958233 and 40422988084 failed byte-SHA assertions. The final transport-only correction, runner SHA256 `a074e85a9e9be7544db62aa1120d468b37326ee716c3a762453aa1fdf3089c40`, preserved the original frozen cases. First holdout [40423264293](https://github.com/sushxnthd/lattice/actions/runs/40423264293) failed result serialization because a variable was shadowed; no outcomes counted. Two-site transport-only fix runner SHA256 `5d26ec150a6166121c8db7315f676c65cfa7721311a391b8f03630d87bfc2780` preserved frozen holdout predictions and cases.

## Status and limits

Independently qualified real issues: **3** (Flask PR6096, urllib3 PR5071, Werkzeug PR3136). Werkzeug PR2860 and PR2535 remain excluded. Same-ecosystem clustering and topic-aware case design are limitations. No new coding-model inference, accepted model patches, isolated model-patch functional oracle, powered McNemar result, semantic-IR-vs-Python superiority, or breakthrough. Full historical GitHub ZIP mirroring remains incomplete; complete SHA256-verified Run278 archive is preserved locally. One branch, one draft PR, all 89 boundary issues sealed.
