# K-SYNTH-1 Run231 — Independent audit of completed Run230 Qwen inference

**Source:** [Run230 completed cloud experiment](https://github.com/sushxnthd/lattice/actions/runs/40132162305), artifact `12576070605` (digest `sha256:0a141d00fb3aafd1cc4039bdcb4638bd2e9185cf7d732c95bad48f412b445197`). Two actual Qwen2.5-Coder-7B-Instruct Q4_K_M completions were recovered and independently scored under the *unchanged prospectively frozen* five-field action grammar, common compiler and Run227 16-case necessary-condition evaluator. The model SHA-256, request and response hashes, prompt hashes, seed `1560714227`, temperature 0 and token counts all verified.

| Frozen outcome | Semantic-IR JSON | Annotated Python |
| --- | ---: | ---: |
| Prompt tokens | 1,018 | 964 |
| Completion tokens | 741 | 478 |
| Schema-valid actions | 2/2 | 2/2 |
| Common compiler acceptance | **Yes** | **Yes** |
| BatchStudy behavioral cases | **0/12** | **0/12** |
| Simulation behavioral cases | **4/4** | **4/4** |
| Total necessary conditions | **4/16** | **4/16** |
| Complete functional repair | **No** | **No** |

The independently calibrated corrected positive control passes **16/16**. All **nine new audit tests** and **22 inherited protocol tests** passed locally. The complete independent audit, raw model records, per-case evaluator traces, original downloaded artifact, and SHA-256 manifest are preserved in the Run231 local reproducibility archive.

## Shared falsifying mechanism

Both completions copied Simulation's `if self._solution is None:` guard into `BatchStudy.create_gif`. However, BatchStudy tracks solved state through its `sims` collection, including each simulation's `solution` field. The new BatchStudy guard raises `AttributeError` for every tested state, even when the object is fully solved. Both arms correctly handle the four Simulation conditions. This is a **cross-class state-proxy transfer**, not an action-schema or compiler failure.

The five-field reformulation eliminated Run228's common six-field inversion, allowing both outputs to compile, but it did **not** yield functional correctness. Run230 changed prompt wording and schema together, so the difference from Run228 cannot be assigned causally to either component.

## Scientific decision

**Representation superiority remains unproven.** This is only **one** two-file issue with zero discordant paired successes. No meaningful population effect estimate, equivalence claim, or full upstream integration result follows. The reduced method-only snapshot omits relevant class lifecycle context.

Stop cosmetic reformulations on this issue. Shift the research thesis toward trusted semantic edit authority, immutable epoch/root histories and transactional compilation. Any efficiency claim must use a prospectively frozen diverse multi-repository cohort with relevant class context, independently calibrated functional oracles, matched Python and AST-action baselines, cluster-aware power, and a reserved unseen-boundary prediction. Preserve all 89 reserved boundary issues. The adequately powered comparison remains outstanding.

The frozen primary endpoint and earlier model results have not been reclassified. No new inference was run in Run231.