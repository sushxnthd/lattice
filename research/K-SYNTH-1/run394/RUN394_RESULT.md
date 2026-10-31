# Lattice K-SYNTH-1 Run394 — frozen pytest #14004 factorial repair audit

Date: 2026-10-31 UTC. Branch `research/exp003-context-order`; sole draft PR #9. **No new model inference or IR superiority claim.** All 89 reserved boundary issues untouched.

## Original freeze

The issue-first [pytest #14004](https://github.com/pytest-dev/pytest/issues/14004) oracle was prospectively frozen **before inspecting reference patch contents** at commit [`2cb575b0`](https://github.com/sushxnthd/lattice/commit/2cb575b0b57984a66795f55f6fef86f279672d1a). Historical merged [PR #14098](https://github.com/pytest-dev/pytest/pull/14098), base `543b11f2534bb0edc85b86767ed239da9c5bd140`, reference `ad045be6d8bf05a1a0e48da589218d1a5dd5a84d`; compare API verified base as merge base (four commits ahead). Four production Python files changed: `_pytest/deprecated.py`, `_pytest/fixtures.py`, `_pytest/python.py`, `_pytest/unittest.py`. Frozen 12-case oracle SHA256 `de44bc041c9d6c5699e891efa03bac08e1d572a46a9de9888309db958709a6d7`.

The executable oracle was implemented after reference-diff inspection, although its cases follow the frozen prose; auxiliary dependencies were not fully pinned and network isolation was not enforced during pytest. This is **historical exploratory qualification**, not a blinded primary-model observation.

## Exact original failures and corrected experiment

Original [Actions #41226985248](https://github.com/sushxnthd/lattice/actions/runs/41226985248), artifact `13051214315`, original ZIP SHA256 `809d11542895747b3e83a2cc3b1a923632767b5b7403cdabd32a0ccaab62b102`: all 16 configurations failed before pytest collection due to missing `pygments`. Original failures preserved. Corrected [Actions #41227096829](https://github.com/sushxnthd/lattice/actions/runs/41227096829), artifact `13052201359`, original ZIP SHA256 `8ff633a4f8ef03f6e6162015a4e064392aa478953ed0676d2720fe28c906c16e`: same frozen oracle, base/ref and 16 subsets, only dependency fixed.

| Reference source subset | Public /2 | Heldout /4 | Designated controls /6 | Total /12 |
|---|---:|---:|---:|---:|
| Baseline | 0 | 0 | 4 | 4 |
| `deprecated.py` only | 0 | 0 | 4 | 4 |
| `fixtures.py` only | import failure | import failure | import failure | 0 |
| `deprecated.py` + `fixtures.py` | 2 | 4 | 6 | **12** |
| All four files | 2 | 4 | 6 | **12** |

All 16 source subsets were tested (192 case invocations, 468 observed test IDs, 888 fixture events). Independent read-only audit verified 16 matrices, 128 source-origin/hash checks and 468 test-level classifications, zero disagreements; eight local tests passed including an adversarial tampering test. Minimal sufficient reference subset is exactly `deprecated.py` plus `fixtures.py`; `python.py` and `unittest.py` changes were not necessary on this oracle.

## Qualification false positive and posthoc mechanism

The **literal original frozen checklist passes** (baseline target failures, full reference 12/12, four changed production files, two source-reversion necessities). However, `fixtures.py` alone fails import because three deprecation warning constants are absent from baseline `deprecated.py`. This is mechanical import compatibility, not evidence of two independent semantic repairs. Two designated nonregression controls (`C5_parametrized`, `C6_private_nonautouse`) already fail on baseline; their original labels and scores are preserved.

Separate **posthoc, non-rescoring** [Actions #41227295254](https://github.com/sushxnthd/lattice/actions/runs/41227295254), artifact `13052680040`, original ZIP SHA256 `436e282727dd21e89c59c3e6eb3d31947deba1d6565b872f68bfa8545bb0347f`: baseline `deprecated.py` plus only three warning-constant declarations, reference `fixtures.py`, baseline `python.py` and `unittest.py` passed **12/12**. This demonstrates a false positive for behavioral cross-file necessity under the original import-sensitive ablation rule.

**Decision:** Record literal frozen-checklist pass, but **DO NOT PROMOTE** to the primary semantically coupled multi-source repair cohort. This is a methodological negative result, not IR inferiority or superiority.

## Bounded scope counterexample

On normalized relative path tuples without unresolved symlinks or dynamic fixture registration, fixture directory eligibility is component-prefix ancestry, not raw string-prefix matching. Exhaustive 14,400 ordered pairs (1–4 components from `{a,ab,b}`) produced 142 false-positive lexical-prefix scopes. The original bug also exposes empty-baseid fixture leakage. Return `UNKNOWN` outside the bounded scope. This is not a general Python dataflow certificate.

## Next

Run395 prospectively requires **all controls pass on baseline** and behavioral multi-file necessity **after neutral interface shims**. Prioritize unseen issue-first tasks and matched semantic/dataflow IR vs information-equivalent Python/AST, identical compiler/oracle and a strong open coding model. Keep raw model outputs and cluster-aware inference. All original failures and ZIPs are preserved in the locally SHA-verified 19-payload Run394 reproducibility archive.
