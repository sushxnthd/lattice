# Run82: representation identifiability and format-normalized repair (2026-10-17)

## One active kernel
- **Question:** Does explicit semantic IR reduce repair complexity for capable coding models beyond Python with identical semantic facts, verifier, and compiler?
- **Current best-known baseline:** Python dictionary-of-expressions patches into `FramedProgram.edit`, with Run79's independent three-way oracle. Run80 established exact semantic equivalence for 384 matched patches. No Run79 7B inference has executed.
- **Precise intervention:** Run79's assignment-form output, `read = a or b`. This is an *interface* intervention, not a structural IR; a future structural intervention must be frozen separately.
- **Matched-information control:** Python expression dictionary, identical task, captured dependencies, trusted scope, compiler, independent oracle, feedback, token and call budgets.
- **Scalar success metric:** paired difference in independently correct tasks within two calls, including invalid outputs as failures. Secondary format-normalized success difference separates interface compliance from semantic content.
- **Strongest alternative:** parser compliance and output-token distribution explain any measured gap.
- **Decisive falsification:** format-normalized semantic success is identical or favors Python, or the effect fails on unseen realistic repository repairs.
- **Publishable threshold:** independently frozen multi-file tasks, same-compiler and executable-state-machine controls, capable models, paired uncertainty, adversarial ablations, clean replication and an unseen-task prediction.
- **Product threshold:** >=10% fewer median repair calls or >=10 percentage-point hidden-test recovery with no increased protected-output violations on real repository edits.
- **Kill condition:** three substantive capable-model comparisons without a repeatable advantage or sharper boundary; infrastructure attempts do not count as science.
- **Backup kernels (inactive):** verifier-only benefit; source-bound provenance diagnostics.

## Protocol
Run79 prompts, six development tasks, and scoring remain frozen. Run82 adds a *post-hoc*, arm-blind, format-normalized diagnostic; it is not a substitute for the preregistered primary endpoint. The diagnostic accepts either one Python dict expression or one assignment, checks scope and syntax, and scores the same patch with the existing compiler and independent oracle. Do not access frozen holdouts.

## Execution blocker
Attempted `.github/workflows/run82-paired-repair.yml` on branch `research/run82-capable-model-execution-20261017`; the GitHub connector rejected the workflow write via safety checks. This is an infrastructure blocker, not a negative scientific result. Preserve the branch. No capable-model call or raw transcript exists for this run.

## Planned model provenance
Run79 protocol: Qwen2.5-Coder-7B-Instruct-GGUF Q4_K_M; llama.cpp commit `8bb3cf0d216a5ae48360179f2931daf284be4d01`; seed 271828, temperature 0, 256 output tokens/call, two calls. **Not executed**.

## SCIENCE
The original comparison is output notation, not a distinct compiler-level semantic IR. Exact same-patch equivalence is the only supported representation finding so far. A format-normalized diagnostic is an identification check, not evidence of IR superiority.

## SYSTEM
Default CI already runs five independent-oracle fault-injection tests. A format-neutral repair diagnostics interface can distinguish syntax failure, scope violation, semantic mismatch, and protected-state violation while retaining the identical compiler. No new DSL syntax is introduced.

## Smallest supported claim
The frozen Run79 capable-model pilot remains blocked by workflow-write safety checks; Run82 isolates a prospective analysis needed to avoid misattributing output-format compliance to semantic representation.
