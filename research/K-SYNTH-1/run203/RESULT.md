# K-SYNTH-1 Run203 — power correction and matched-address ablation

Status (2026-10-23): **outcome-blind analysis executed; no new capable-model inference.** Source code, independent checks, original requests and detailed reproducibility records are preserved in the local Run203 archive.

## Corrected primary-study power

The frozen SWE-rebench V2 sample contains 480 multi-file issues from 196 repositories, but 89 issues/39 repositories are reserved as an unseen boundary set. The valid primary discovery sample is **391 issues from 157 independent repositories**.

Under the previously declared Run199 assumptions (30% discordance; repository direction ICC 0.5; two-sided cluster-level t test, alpha 0.05), 20,000 simulations yield:

| Scope | Issues | Repositories | Power at 65% conditional IR wins | Power at 60% |
| --- | ---: | ---: | ---: | ---: |
| Discovery primary | 391 | 157 | **73.365%** (MC SE 0.313 percentage points) | 39.770% |
| Boundary holdout | 89 | 39 | 22.715% | 12.825% |
| Entire frozen set (not a valid primary set) | 480 | 196 | 81.520% | 47.445% |

**Correction:** The previously reported ~81% power was for all 480 issues, including the unseen boundary set. It must not be used to characterize the discovery-only primary analysis. A bootstrap cluster-size planning grid first crossed 80% near **187 discovery repositories / 468 discovery issues** under the same hypothetical large effect, approximately 30 additional independent repositories and 77 additional discovery issues. This is a planning sensitivity, not a guarantee or an authorization to inspect held-out tasks.

## Mechanism: address length is not semantic expressivity

Recovered 6 real model-visible Python files from 2 previously exposed Run200 issues, verifying original request/source hashes. Run202's bounded target universe contained 38 unique AST targets. Structural target IDs required fewer JSON-serialized characters than exact Python-text anchors in **38/38** cases; median savings **48.5 characters** (range 1 to 3,942).

In an explicitly hypothetical independent per-character corruption channel with p=0.001, mean exact-copy probability was 0.96849 for structural IDs versus 0.78734 for text anchors. **These are mathematical channel probabilities, not observed coding-model outcomes.**

A decisive control is ordinary Python with the **same short IDs**. It has identical address length and normalized compiler authority as the structural-ID arm, and exactly the same channel probability under the length-only model. Thus a structural-ID advantage over long Python anchors alone would not establish semantic-IR superiority.

**Bounded equivalence:** For an immutable snapshot and a finite authorized target set, when both the target-ID and exact-text maps are injective and normalize to the same compiler edit, the interfaces are bijective over authorized targets and have equal expressivity. Any performance difference must arise from generation, localization or transmission, not from additional edits being permitted.

## Next decisive step

Launch the already frozen Run202 2x2 open-coding-model pilot after positive controls. Then prospectively freeze the matched three-arm mechanism test: structural ID, Python exact-text anchor, and Python short ID, with identical task information, compiler, edit authority, verifier and repair budget. Keep the 89 boundary issues sealed. Obtain functional issue-resolution evaluation before claiming a useful semantic-editing advantage.

Local checks: **18 passed**. No new model outputs or real-issue resolution measurements in Run203. Research kernel K-SYNTH-1 and the existing draft PR remain unchanged.