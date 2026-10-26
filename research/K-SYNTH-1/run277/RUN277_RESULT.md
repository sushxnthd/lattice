# K-SYNTH-1 Run277 — Original qualification failure, source-component interaction and bounded cross-file contract

Date: 2026-10-26 UTC / 2026-10-27 IST. Branch `research/exp003-context-order`, draft PR #9.

## Unchanged original prospective evidence

[Run276 Werkzeug PR2535](https://github.com/sushxnthd/lattice/actions/runs/40407761872) finished with **scientific qualification failure**, not an infrastructure failure. Original artifact 12691554074, SHA-256 `b558cfbc0788c71582ab33ba41f1f349c98fde447d2741db7032d1be1bfa68a1`. Independently verified all three original manifest entries, both identical frozen specifications, 36 raw public-API outcomes and four pairs of source SHA-256 hashes.

The frozen criterion required each one-file reference-source ablation to fail at least one of three target redirects. This is **false**: the rules-only source variant repairs all 3/3 targets but regresses two of six nonregression controls. Do not retroactively change the criterion or promote PR2535 as a third qualified issue.

## Independent, explicitly post-outcome factorial analysis

| Reference-source configuration | Targets correct /3 | Controls correct /6 | Total correct /9 |
|---|---:|---:|---:|
| Baseline | 0 | 6 | 6 |
| Matcher-only | 0 | 3 | 3 |
| Rules-only | 3 | 4 | 7 |
| Full upstream reference | 3 | 6 | 9 |

The rules-only variant redirects a path already ending in `/` to a URL ending in `//`. The matcher-only variant raises `AttributeError: 'RulePart' object has no attribute 'suffixed'` on affected path matches. The complete reference preserves all nine desired outputs.

The finite 2×2 interaction on **binary correctness** is `9 - 3 - 7 + 6 = +5`, entirely from nonregression controls; the target-only interaction is zero. This is a constructive counterexample to identifying target-only component necessity with full repair correctness. It does **not** prove that alternative one-file repairs are impossible. These nine related cases do not support an independent-pair significance test.

## Actual bounded cross-file semantic/dataflow mechanism

Implemented a typed AST contract checker for the exact bounded pattern `State.dynamic: List[Tuple[RulePart, State]]`, `from .rules import RulePart`, loop tuple binding and attribute reads. In pinned upstream source, the new `matcher.py` reads `test_part.suffixed`; the new `rules.py` declares `RulePart.suffixed`. The matcher-only source combination is tagged `UNDECLARED_RUNTIME_UNKNOWN`, not proven absent at runtime. The full reference is `DECLARED`. This agrees with the independent runtime AttributeError without claiming Python-wide soundness. Explicitly unrecognized or rebound variables fail closed to `UNKNOWN`.

Local: 16/16 tests passed, including 256 seeded bounded AST declaration variants. Source analyzer SHA-256 `80b72adfdfd93062dad52c85a9e8ff2db0cba3d1d36cc699e1a5abbf367ca8a4`. [Original cloud contract](https://github.com/sushxnthd/lattice/actions/runs/40413939794) recovered as artifact 12694350910, SHA-256 `95f3778f4b4cd80b7d8ef2ef72c632e153e6a190d294cf68070ce04af4baac39`. Its scientific assertions completed and original source SHAs matched, but the workflow failed in the reporting step due to a JSON field-name mismatch. Corrected workflow launched separately; preserve both failed attempts.

## Status

Qualified cohort remains **two** independent real issues (Flask PR6096, urllib3 PR5071). Werkzeug PR2860 and PR2535 are excluded. No new coding-model inference, model repair, representation advantage, powered significance or breakthrough is claimed. All 89 boundary issues remain sealed; same branch and draft PR #9; complete historical source/ZIP mirroring remains incomplete.

## Final corrected cloud verification

[Run277 corrected cloud experiment](https://github.com/sushxnthd/lattice/actions/runs/40414013511) **COMPLETED SUCCESS**. Original artifact 12695140630 ZIP SHA-256 `39e935deb3e1b7bcb78acc78af078f8c711de336c6c2fa15768c7853f4abf634`, matching GitHub's digest. Both manifest entries independently SHA-256 verified; pinned source SHA-256 hashes match all four original Run276 source variants. Bounded graph reads: baseline only `final/content DECLARED`; matcher-only adds `suffixed UNDECLARED_RUNTIME_UNKNOWN`; rules-only retains baseline read sites; complete reference adds `suffixed DECLARED`. This is source-verified cross-file contract evidence, **not** a soundness proof, model repair, or qualification under the failed original criterion. The prior cloud transport and reporting failures remain preserved.
