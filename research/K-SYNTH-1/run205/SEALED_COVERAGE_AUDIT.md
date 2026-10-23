# K-SYNTH-1 Run205: sealed reference-patch coverage audit

Date: 2026-10-24. This is an **independent evaluator-only aggregate** of the frozen SWE-rebench V2 task selection. Gold patches, gold file paths, test IDs, and per-instance eligibility must never enter model prompts or the public research branch.

## Discovery finding

391 issues across 157 repositories were joined to sealed reference-patch changed-file lists:

| Reference patch condition | Issues |
| --- | ---: |
| At most three changed files, all Python | 132 (33.76%) |
| At least one non-Python changed file | 216 (55.24%) |
| All Python but more than three changed files | 43 (11.00%) |

The 132 reference-patch-representable cases span 77 repositories. Repository-resampled 95% percentile interval for the 33.76% proportion (20,000 deterministic replicates): 27.85–39.69%.

**Lemma:** An editor limited to three Python files cannot reproduce a reference patch that modifies a non-Python file or more than three files. The changed-file sets cannot be equal. **This is not an issue-resolution ceiling:** alternate functionally correct fixes may exist using fewer files. Do not select the primary analysis cohort by reference-patch properties.

Under an illustrative unclustered exact McNemar model (30% discordance, 65% IR wins conditional on discordance, two-sided alpha 0.05), 132 pairs have 41.48% power and 391 pairs have 89.17%. These are not the cluster-adjusted primary power estimates (Run203 estimated ~73.4% for the full 391 discovery issues).

## Required prospective correction

1. Retain all 391 discovery issues for intention-to-treat analysis; do not discard issues based on gold metadata.
2. Give **both** semantic-IR and Python conditions identical gold-blind repository-wide search/edit authority, including non-Python files, with identical budget and compiler/verifier.
3. Measure localization failures, unsupported file types, syntax acceptance, and functional resolution separately using a sealed independent evaluator.
4. Include Python with the same short target IDs to rule out copy-length advantage; AST addressing alone is not semantic-IR superiority.
5. Freeze a genuinely powered repository-clustered analysis before observing the main model results.
6. The 89 boundary issues remain unseen with respect to model outcomes. Aggregate boundary changed-file metadata was inspected during this audit, so future predictions about *file-count composition* are not blind; a model-behavior boundary prediction can still be frozen before boundary inference.

## Reproducibility

Public task JSON bytes SHA-256: `f615b8c5f4f7e4b1996992105515b3e15e9678fb57a3cc0cff5cf1aef64641f2`.
Independent local evaluator: deterministic aggregate-only Python, 20,000 repository-bootstrap replicates, exact McNemar calculations; 3 tests passed. Full source, tests, aggregate JSON and hashes preserved in Run205 reproducibility archive; the sealed evaluator is intentionally excluded.

Run204 cloud pilot remained in progress when checked. No new capable-model outcomes or representation superiority are claimed. The experiment's existing branch and draft PR #9 remain in place.
