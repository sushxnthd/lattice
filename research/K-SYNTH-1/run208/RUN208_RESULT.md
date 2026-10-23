# K-SYNTH-1 Run208 — model-output transport correction

**Date:** 2026-10-24. **Research branch:** `research/exp003-context-order`. **Status:** Run208 cloud pilot launched by workflow commit; model outcomes pending.

## Independent Run207 artifact audit

Downloaded and independently inspected both completed Run207 inference artifacts (GitHub Actions run 40035581215). Both jobs stopped at the all-arms positive-control gate; **no real-repository inference was attempted**.

| Arm | Job 0 | Job 1 |
| --- | --- | --- |
| semantic_node_ir | correct replacement | correct replacement |
| python_short_id | correct replacement | correct replacement |
| python_text | rejected | rejected |

The exact-text Python arm emitted **16 duplicate file-deletion actions** rather than the requested one-function replacement in each job. The other arms emitted one correct replacement. Run207 used a constrained JSON Schema `oneOf` over replace/create/delete action variants. A decoding/transport confound is evident, but its causal origin is **not established**. Both Run207 jobs used the same control seed and prompt, so these are repeated executions, not independent statistical samples. Treating this as an IR advantage would be invalid.

## Prospective protocol amendment

Run208 replaces the arm-specific `oneOf` grammar with **one identical flat seven-string-field action grammar for all three arms**. The unused fields must be empty strings; the common normalization layer rejects nonempty unused fields and cross-arm address contamination. Replace, create and delete remain supported; repository-wide edit authority, model ID and checksum, issue data, shared retrieval and compiler/verifier are unchanged. The control seeds now differ by matrix task index.

**Patch:** `research/K-SYNTH-1/run208/run208_runner_patch.gz.b64` applies to the SHA-matched Run207 source bundle. **Workflow:** `.github/workflows/lattice-k-synth-1-run208-flat-schema-pilot.yml`. Run208 is a new feasibility experiment, not a post-hoc alteration of Run207 observations. Both prospectively selected real issues remain discovery-only; the 89 boundary issues are still sealed.

## Executed independent local validation

29 unit tests passed; 2,000 synthetic cases yielded 6,000 matched compiler executions plus 2,000 non-Python transactions, with zero disagreements against the direct-replacement oracle. Independently checked all six raw Run207 control responses, model IDs, seeds, prompt hashes, token usage and verifier records. Synthetic compiler parity is **not** model evidence.

## Statistical and scientific limitations

The previous 391-discovery-issue/157-repository cohort has approximately 73.4% modeled cluster-adjusted power for the specified large effect; earlier sensitivity estimated ~468 issues/187 repositories for ~80%. These are conditional planning simulations, not observed results. Recompute for the functional outcome after obtaining a viable positive-control pass rate. A two-issue AST-changing compiler pilot cannot demonstrate issue resolution, a complete semantic-IR advantage or a representation-science breakthrough. The next decisive gates remain independent pinned functional evaluation, adequately powered matched Python baseline including short-ID control, mechanism ablation, adversarial tasks and unseen-boundary prediction.

All original model artifacts and the complete amended code/test suite are preserved in the Run208 local reproducibility archive.
