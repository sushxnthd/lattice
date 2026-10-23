# K-SYNTH-1 Run197: independent replay of Run196

Date: 2026-10-23. **Retrospective diagnostic, not a representation-superiority claim.**

Four Qwen2.5-Coder-7B-Instruct CPU shards completed. All 32 repeated positive-control completions passed. The 64 main completions were all schema-valid.

| Frozen primary result (16 tasks per cell) | Compact | Expanded |
| --- | ---: | ---: |
| Semantic IR | **2/16** | **0/16** |
| Python SSA | **3/16** | **1/16** |

The paired exact McNemar p-value is 1.0 in both variants. This does not establish equivalence.

An independently written restricted-AST Boolean interpreter audited all four original GitHub Actions ZIPs, matching their SHA-256 digests and the prospectively frozen prompt-manifest SHA-256 `66cfba6c50c40590b459dba34a1adcb029bca65e9132e5d607e547b002eb45ba`. It verified 64 raw requests, completions, token counts, seeds, model IDs, prompt hashes and verifier traces. The semantic-IR and Python SSA views agreed on **1,024 input assignments**. Independent output scoring generated **4,096 exhaustive input-level traces**. Six adversarial tests passed.

## New measurement-validity counterexample

The task contract asks for a *Python Boolean expression*, but the shared production compiler only accepts `and`, `or`, and `not`. Eight model outputs (four per Python variant) used valid Boolean XOR `old_gate ^ old_bridge` for the XOR task family and were rejected as `BinOp`. Two more Python-expanded outputs used valid conditional syntax `old_gate if a else old_bridge` and were rejected as `IfExp`.

**Strictly post-hoc sensitivity analysis:** A separate safe Boolean interpreter admitting only XOR and conditional expressions scored the same immutable model outputs as follows:

| Post-hoc widened Python Boolean syntax | Compact | Expanded |
| --- | ---: | ---: |
| Semantic IR | **2/16** | **0/16** |
| Python SSA | **7/16** | **7/16** |

These are **not** preregistered scores. Nominal task-level exact paired p-values (0.0625 compact, 0.015625 expanded) are inappropriate as generalization evidence: there are only four repeated instruction families. The four-family exact sign test is **p=0.5** in each counterfactual variant. The experiment also uses synthetic module labels, not real repository files.

**Decision:** Do not claim IR advantage. Pivot the core thesis toward immutable epoch/root identities, trusted edit authority, and protected-output guarantees. Widen the compiler's safe Boolean grammar **symmetrically for both interfaces** in a new experiment, without changing the original frozen results. The next confirmatory study must use independently sampled real multi-file repairs, an ordinary-Python and AST-action baseline, cluster-aware power, independent scoring, and a preregistered unseen-boundary prediction.

The full local reproducibility archive includes all four original ZIPs, an independent AST evaluator (no project compiler or `eval` on untrusted code), six tests, 64 per-completion records, 4,096 oracle traces, and SHA-256 manifest.

Original raw inference: https://github.com/sushxnthd/lattice/actions/runs/39946522022

**No new capable-model inference occurred in Run197.** No world-class completion or breakthrough is claimed.
