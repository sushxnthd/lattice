# Run274: Prospective third independent real two-production-file qualification

Date: 2026-10-26 UTC / 2026-10-27 IST. K-SYNTH-1; branch `research/exp003-context-order`; one draft PR #9.

Independently discovered merged [Werkzeug PR2860](https://github.com/pallets/werkzeug/pull/2860) fixing repeated-slash redirects (issue #2834). Pinned base `f516c4005c7c4510b61ae07969450771b929809d` and direct-child reference `e075bba892f6f1bf72eef2de945286df974afb88`; the patch modifies TWO production files `src/werkzeug/routing/map.py` and `src/werkzeug/routing/matcher.py`, plus tests and changelog.

BEFORE any source ablation, froze seven independent public-API checks and four expected source-component variants: base, map-only, matcher-only, full. Two checks target Map-level dynamic merge_slashes forwarding, one targets rule-level merge_slashes=False, four are nonregressions. Executable SHA-pinned harness SHA256 `9a6976dd3c912ce8e7ef3669b95c6e5b35f4549d5f29493ad910f04ca2757592` records exact source hashes, all 28 functional outcomes, stderr, environment and artifact manifest. Six local freeze/integrity tests PASS; actual upstream ablation outcomes NOT YET recovered.

Mirrored compressed executable harness commit `a809aac8242e1b3263e160bde2774d02e0ba5025`, frozen specification commit `d9955f7284c6d308c3991bf49d381e09d95956ff`, workflow commit `e5cbe763b64c81da4e8c5d443d2c339b21e5e67c`. [Qualification workflow 40385611001](https://github.com/sushxnthd/lattice/actions/runs/40385611001) QUEUED at last check. This is a prospective THIRD CANDIDATE, **not yet qualified**. Even success would establish two necessary REFERENCE-PATCH components under frozen tests, not exclude alternate single-file solutions.

[Run271 blind Qwen workflow 40357685395](https://github.com/sushxnthd/lattice/actions/runs/40357685395) remains IN_PROGRESS at eight frozen requests; no raw outputs/tokens/model patches recovered. Do not score pending as failed.

Only TWO independently qualified real tasks currently: Flask PR6096 and urllib3 PR5071. No powered model result or intrinsic semantic IR superiority. No model-generated source executed on host. Full SHA-verified local Run274 ZIP and prior Run273 archive preserved. Historical GitHub mirroring incomplete. All 89 reserved boundary issues SEALED.

## Original artifact recovered: predeclared construct fails

Workflow [40385611001](https://github.com/sushxnthd/lattice/actions/runs/40385611001) COMPLETED FAILURE **at scientific qualification**, not infrastructure. Original artifact ID 12680576224, ZIP SHA256 `38e26c80d66dca4a469f85a194274b804b1a83307c08c75aa051d84fc526caee` matches GitHub digest. Both manifest entries and all four exact source-SHA pairs independently verified. All four oracle processes returned 0. **27/28 frozen checks matched**; baseline, map-only and matcher-only were 7/7 each. Full reference was 6/7: the prospectively frozen `toggle_on` case expected REDIRECT but observed NOT_FOUND. The map-only reference component DOES redirect, so the full two-component reference is non-monotonic under this stronger post-construction mutation test.

Mechanistic source inspection: `Rule.bind` snapshots `map.merge_slashes` into a default Rule; the new Map property setter updates only `_matcher.merge_slashes`, while the reference matcher rejects merged redirects if `rv[0].merge_slashes is False`. A Map initialized false and later set true can therefore have matcher flag true but rule flag false. **This is a bounded dynamic-configuration counterexample**, not proof that post-binding mutation is a supported upstream API or that the PR fails its own intended tests. Do not retrofit frozen expectations. **Werkzeug PR2860 is NOT promoted to third independently qualified issue** under this protocol. Cohort remains TWO.

Read-only local `audit_run274_original.py` verified the original raw artifact and precisely one discordance. Full SHA-verified local archive contains original cloud ZIP, audit, mechanism analysis, frozen tests, code and prior Run273 archive. Blind Qwen Actions 40357685395 still in progress; no raw completions recovered. No model superiority, statistical significance or breakthrough. 89 boundary issues sealed.
