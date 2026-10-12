# Lattice Run 29: controlled evaluation preparation

Status: **IN PROGRESS; no new coding-model inference, no fresh frozen holdout results, and no representation-specific advantage established.**

The canonical negative Qwen2.5-Coder results from draft PR #9 remain unchanged. Run 28 local artifacts have not been integrated into this branch or validated by canonical CI.

Primary causal contrast: C (Lattice protocol + verifier) versus B (Python protocol + identical verifier), with matched information and input/output budgets. A is an ordinary Python patch baseline and D is a simpler executable-invariant control. Final holdouts must remain unopened until preregistration, with independent evaluator, pinned model bytes, token usage, exact task commits, and raw transcripts. Engineering verifier improvements must not be mislabeled as Lattice representation gains.

No frozen evidence or existing branches were rewritten.
