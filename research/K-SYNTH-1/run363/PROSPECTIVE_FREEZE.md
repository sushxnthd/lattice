# K-SYNTH-1 Run363 prospective freeze: Flask PR #5928

Frozen 2026-10-30 UTC before historical functional outcomes. Source: https://github.com/pallets/flask/pull/5928 (merged 2026-02-20). Public issue description: teardown callbacks must all run despite errors, and errors should be collected across request and application teardown and signals.

Baseline commit: `7b0088693ece1bd3a9238a6fdf56ed8df7a4d43b`
PR head commit: `fbb6f0bc4c60a0bada0e03c3480d0ccf30a3c1df`
Transport-only merge commit: `c34d6e81fd8e405e6d4178bf24b364918811ef17`

| Production file | Base Git blob | PR head Git blob |
|---|---|---|
| src/flask/app.py | 9a6fdd40d2edb1b7575bed5c68655706e18c4d35 | 652b9bbf719b626c6b66cb545b27264a46453fc9 |
| src/flask/ctx.py | 8876efd04f0552fb5db315701abfcbcedcfeb447 | dbd62e7505382954cd61a59bff317ca3d27d6f1a |
| src/flask/helpers.py | 3b65664afe9510c40b63f8f05e0adb9c6a3addd8 | 8befe719695e12bd6374605c9a90e88f36e5c494 |

Scientific contract: CPython 3.11, isolated runner, all eight source combinations of the three files, exactly six repair targets and six controls from `run363_flask_oracle.py`. Each case must run in a fresh process. Preserve raw callback events, error-type multiset, stdout/stderr, source blobs, environment, failures. Independently recompute outcomes; no reference diff or changed-line information enters model prompts.

Targets T01-T06: one and two failing request teardown callbacks; one and two failing app-context teardown callbacks; callback failure plus request/app teardown signal. Controls C01-C06: clean LIFO teardown, exception forwarding, nested contexts, empty request.

Qualification is prospective: baseline fails >=1 target and preserves >=5/6 controls; full reference passes all 12; no singleton-file change passes all 12; at least one strictly positive casewise target interaction in a two-file factorial square conditional on the third file. Missing observations or source mismatch mean INCONCLUSIVE, not model failure. Do not revise criteria post-outcome. A qualified result still requires deduplication against the existing eight-PR ledger, and is not evidence of semantic IR superiority.

All 89 reserved boundary issues remain sealed. Preserve only PR #9, open/draft/unmerged, on research/exp003-context-order.