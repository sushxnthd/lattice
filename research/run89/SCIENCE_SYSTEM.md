# Run89 — source-bound oracle integration attempt and experimental identification

Date: 2026-10-18. Branch: `research/run89-structural-view-control-20261018`.

## Active kernel (one only)
- **Question:** Does a structural versioned semantic IR reduce capable coding-model repair complexity beyond Python given the identical compiler, verifier, semantic facts and edit authority?
- **Best-known baseline:** Python dictionary patches through `FramedProgram.edit`, Run62 three-way oracle, Run82 format-neutral diagnostic. Run79 six-task Boolean pilot is not a structural intervention and has no inference results.
- **Intervention:** Explicit versioned dependency graph and captured references as the primary editing view, with the same Python patch output grammar in both arms.
- **Matched-information control:** Lowered Python view, plus exactly the same canonical frame context, task, allowed scope, feedback, model, seed, budget and compiler. Token parity must be verified using the *model tokenizer* before inference. No model-specific syntax acceptance.
- **Primary scalar:** Paired difference in independently correct task recovery by at most two calls; incomplete/invalid outputs are failures. Secondary: calls, regression count, protected-output violations, semantic churn and total tokens.
- **Strongest alternative:** Different salience/length of redundant views rather than an intrinsic semantic representation effect; task triviality and feedback dominate.
- **Decisive falsification:** Effect disappears after equalized syntax/information/budget, or fails to replicate on prospectively frozen multi-file repairs and a second capable model.
- **Publishable threshold:** Primary prior art, frozen realistic tasks, Python + same-compiler and executable-state-machine controls, independent oracle, at least two capable models, uncertainty, adversarial ablations, unseen prediction and clean reproduction.
- **Product threshold:** >=10% lower median repair calls or >=10 percentage-point recovery improvement on real repository tasks with no increased forbidden-state violations.
- **Kill condition:** Three substantive solvable capable-model comparisons without surviving effect/boundary. Workflow/write failures do not count.
- **Backups (inactive):** verifier-only effect; provenance-bound semantic diff.

## SCIENCE ledger
- No capable-model inference this run. Run79 remains a notation-only pilot, not a test of structural semantic IR.
- Existing exact paired-power audit: six development tasks cannot establish a 10-point effect with credible power.
- A graph/versus-lowered-Python *view* contrast, even if successful, establishes a view/salience effect; a structural-edit intervention and unseen-repo replication are necessary for a representation claim.
- The production compiler and independent evaluator remain available; no holdouts accessed.

## SYSTEM ledger
- Attempted to integrate a source-bound provenance auditor in `src/lattice/provenance_audit.py`, reconstructing canonical versioned transitions independently and hashing the **full prior graph** with patch and authority.
- GitHub rejected the code-file write with: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.`
- This is a write-path/infrastructure blocker, **not** a failed scientific hypothesis. The branch was created successfully. Existing CI and Run84 branch were inspected; latest visible CI run on Run84 was successful.
- Prior local prototype is in the Run83 evidence package; no production integration claimed.

## Highest-information next action
Run a capable-model paired development pilot with a single Python output grammar and two semantically equivalent views, retaining raw prompts, tokens and model responses. A workflow write is currently blocked; preserve this as a blocker. If unavailable, implement/test an exact source-bound counterexample and preserve the smallest negative claim. Do not repeat cosmetic syntax comparisons.

## Evidence status
- Model identifier planned: Qwen2.5-Coder-7B-Instruct-GGUF Q4_K_M, seed 271828, temperature 0, llama.cpp commit 8bb3cf0d216a5ae48360179f2931daf284be4d01; **not invoked**.
- Raw model transcripts: none.
- Frozen holdouts: untouched.
- Source code write: rejected; no CI assertion for proposed source-bound module.
- Smallest claim: the full-prior provenance commitment is a proposed product hardening step; no new efficacy evidence.
