# K-SYNTH-1 Run338: Rich #3180 prospective qualification FAILED

2026-10-29 UTC. Canonical `sushxnthd/lattice`, `research/exp003-context-order`, draft PR #9. All 89 reserved boundary issues SEALED.

## Original prospectively frozen experiment

Candidate [Textualize/rich PR #3180](https://github.com/Textualize/rich/pull/3180), issue #3176. Protocol frozen in Run337 at commit `5768baf35c3999847c2a7878547374a6a16a4d88`. Executable oracle finalized **before reference patch inspection** at `02e22c699b16b68200d7f5a7dd56bc50e55a5bc6`. Base `e76f3c3ea78481342e21a7b3328075462ab69c2b`, head `05c5dfc8fcbb1c967490540cc080c3d534a91a12`. Baseline Git blobs `rich/_wrap.py` `c45f193f74ad7385c84f3b935663198415cfaa4b`, `rich/cells.py` `9354f9e3140999702ec8c140636c511d71c340b2`.

Original [GitHub Actions run 40848215638](https://github.com/sushxnthd/lattice/actions/runs/40848215638) COMPLETED SUCCESS; artifact `12885179492`, ZIP SHA256 `65fc6369073d5e07d12b785d70d2e484c8e87d2af3a57b06dc172a341da3e452`; raw JSON SHA256 `1cfbead213d8a1ead63ae9ff261daef8d2d5ba22cac913fe47fdd80415ac41fd`.

| Arm | Targets / 11 | Controls / 9 | TypeErrors |
|---|---:|---:|---:|
| base wrap + base cells | 4 | 8 | 0 |
| ref wrap + base cells | 0 | 8 | 11 |
| base wrap + ref cells | 0 | 8 | 11 |
| ref wrap + ref cells | 11 | 8 | 0 |

**NOT QUALIFIED.** The complete reference fixes 11/11 targets but violates the frozen nonregression control `hello world` at width 5. Direct `divide_line` yields `['hello ', 'world']`, with cell widths `[6,5]`. The oracle likely overconstrains trailing whitespace relative to higher-level Console rendering, but cannot be changed retrospectively. This does not show the original Rich patch is incorrect.

The single-component variants produce `TypeError` on the 11 target cases because the `chop_cells` caller/callee keyword changes from `max_size` to `width`. These are **ABI incompatibilities**, not independently observed functional regressions. [Executable keyword-ABI counterexample](keyword_abi_counterexample.py) proves that a keyword rename can create apparent 2x2 joint necessity even when the semantic fix is confined to one callee.

## Independent replay and adversarial tests

A separate read-only auditor checked **80/80 original records**: case identity, cuts, segment reconstruction, Unicode display widths, SHA256, source identities, classifications and frozen decision; **zero discrepancies**. Six adversarial mutations with recomputed SHA256 were detected: falsified full control, changed cut, changed cell width, wrong source blob, false promotion and duplicate case. Full local reproducibility archive has 11 SHA-verified payloads and a manifest, ZIP SHA256 `4cffe293ccaf0c166cab330d062108de611201c16f8f21055ff2d096bca3f1de`. Original cloud artifact preserved within it.

Scope: direct historical `rich._wrap.divide_line` public function, not full Console integration. No new model inference or powered IR advantage. **Three** independent historical production repairs remain qualified: Flask #6096, urllib3 #5071, HTTPX #1183. All 89 reserved issues remain sealed.

## Run339

Pre-register a new independent repository and an end-to-end public API oracle, with an ABI-compatibility negative control to distinguish interface co-change from semantic necessity. Do not retune or promote Rich #3180. Continue the information-matched semantic IR versus Python/AST model study, independent evaluation and artifact mirroring on the same branch and draft PR.
