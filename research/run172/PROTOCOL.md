# Run172 — K-SYNTH-1: restricted temporal semantic editor

Status: no capable-model inference; no representation advantage established.

## Frozen causal protocol (NOT a frozen task set)
Intervention: versioned dependency/state graph with typed transfer edges and explicit protected commitments.
Python control: ordinary Python source with information-equivalent semantic facts and identical authority.
Both arms: identical patch JSON, compiler, independent verifier, model-output cap, and frozen tasks.
Primary scalar: verified repair success (0/1).
Capable model target: Qwen2.5-Coder-7B-Instruct Q4_K_M or stronger open coding model, pinned checkpoint and deterministic decoding.
Real multi-file tasks: **not yet assembled or frozen**. Do not use generated variants as independent real tasks.

Exact paired McNemar planning assumptions: P(IR only)=0.14, P(Python only)=0.06; net effect=0.08; two-sided alpha=0.05; target power=0.80; minimum n=258 independent pairs (computed with unconditional power over discordant counts). Prior n=215 used different assumptions.

Alternative explanation: source ordering / graph navigation rather than semantic structure.
Falsification: equal or better matched Python performance, or disappearance under fact-preserving graph ablation.
Mechanism: dependency search entropy, invalid intermediate states, semantic churn, edit authority localization, verifier loops.
Unseen prediction: advantage strengthens with cross-file state coupling and edit radius, vanishes on single-root depth-one pure repairs.
Publication threshold: n>=258 independent realistic tasks, capable model, independent evaluator, mechanism ablation, prospective holdout prediction, prior-art audit, uncertainty, adversarial counterexamples, clean reproduction.
System consequence: adopt semantic graph view only if causal benefit survives; otherwise retain semantic compiler/editor with Python-first interface.

## Executed system work
Implemented exact protected-trace preservation for restricted deterministic finite-state machines by product-graph BFS, with shortest distinguishing trace. This is a classical finite-state theorem, not a field breakthrough. It cannot verify unrestricted Python. Seven new tests passed; 29 targeted regression tests passed in total. Full legacy suite incomplete due to CPython subprocess timeout (not counted as pass).

GitHub Models is unavailable: GitHub officially retired it on July 30, 2026. Source: https://github.blog/changelog/2026-07-30-github-models-is-now-retired/
SWE-bench Pro V2 (2026-09-22) has 237 Python tasks, so it alone cannot supply 258 independent qualifying multi-file tasks.

No raw model transcripts, model token counts or paired results exist; no inference was executed.
