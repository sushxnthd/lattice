# K-SYNTH-1 Run201: independent replay and anchored-address counterfactual (2026-10-23)

The completed [Run200 cloud experiment](https://github.com/sushxnthd/lattice/actions/runs/39979993291) produced six Qwen2.5-Coder-7B-Instruct Q4_K_M completions: two passing elementary positive controls and four real-issue responses across two repositories. Independent replay of raw requests, response JSON, source SHA-256s, AST outlines, seeds, usage and the unchanged common compiler yields **0/4 accepted real-issue patches**. No SWE-bench functional resolution was evaluated.

| Issue | AST-first original | Python-first original | AST-first post-hoc anchored | Python-first post-hoc anchored |
| --- | --- | --- | --- | --- |
| getmoto__moto-7211 | truncated JSON at 1024 tokens | stale range | unrecoverable | syntax-accepted |
| scrapy__scrapy-6469 | stale range | stale range | syntax-accepted | syntax-accepted |

The **3/4 post-hoc compiler-acceptance rate** is not preregistered, not a functional success rate, and not evidence of IR superiority. It comes from locating a unique exact `old_text` interval in a file whose SHA-256 matches the model's claim. The original line-addressed scorer is preserved unchanged. The shared opt-in `anchored_compiler.py` adapter enforces unique nonempty anchors, edit authority, CAS, nonoverlap and syntax; nine local adversarial tests passed, plus one independent replay test in the downloadable evidence bundle.

**Unambiguous-anchor lemma:** For a fixed snapshot, if a nonempty line-aligned exact preimage has one occurrence, its edit location is unique, independent of line arithmetic. This does not establish behavioral correctness, authentication, or protected-output preservation.

**Important design correction:** Run200 presented identical Python source and AST facts in different order and used the same patch JSON action grammar in both arms. It therefore compared AST-first vs source-first presentation, **not semantic-IR versus ordinary-Python editing languages**. No representation-science claim can be made from it.

The local reproducibility archive contains the verbatim original GitHub artifact (ID 12513929042), independent six-response replay, exact hashes, token counts, errors, tests, and a prospectively frozen eight-repository discovery-only feasibility batch. The 89-issue boundary set remains untouched. No additional capable-model inference occurred in Run201. Next: a genuine semantic action interface and matched Python baseline, plus independent functional evaluation. Do not pool the two original issues with a prospective anchored experiment.
