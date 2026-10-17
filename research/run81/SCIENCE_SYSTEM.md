# Run81 — representation identifiability and execution blocker (2026-10-17)

## One active kernel (continuation of Run79; no holdout accessed)
- **Question:** Does explicit semantic representation improve capable-model repair beyond Python with identical verifier/compiler and identical semantic facts?
- **Best-known baseline:** Run79 Python dictionary-of-expressions edits through `FramedProgram.edit`, independent three-way oracle and exhaustive target truth tables. Run80's 384 matched candidate expressions compile to identical framed programs and lowerings. CI passes, but no Run79 7B inference has executed.
- **Intervention:** Run79 model emits `read = a or b`; Python control emits `{'read': a or b}`. Both parsers return the same `dict[str,str]` and use the same compiler.
- **Matched control:** Identical facts, token gate <=5%, tasks, model/seed/turns, compiler, verifier and feedback.
- **Scalar primary metric:** paired difference in independent correctness by two model calls, including invalid outputs as failures.
- **Strongest alternative:** format-following and tokenization, not semantic representation, because both patches normalize to the same internal dictionary.
- **Decisive falsification:** if any advantage disappears when cross-format outputs are canonicalized and rescored, there is no semantic-repair evidence; an intrinsically stronger IR intervention must be separately preregistered.
- **Publishable threshold:** prospectively frozen realistic multi-file tasks, independent evaluator, matched controls and tokens, capable-model replication, uncertainty, adversarial ablations and unseen predictions.
- **Product threshold:** >=10% fewer median repair calls or >=10 percentage-point recovery gain without more forbidden-state regressions on real repository edits.
- **Kill condition:** three substantive capable-model comparisons with no surviving effect/boundary; do not count CI or blocked infrastructure as science.
- **Backups:** verifier-only effect; provenance-bound semantic diff (both inactive).

## SCIENCE ledger
Run80 established a strict **identifiability limitation**: for matched edit expressions, the alleged IR and Python arm feed the exact same patch to the exact same compiler, yielding identical semantics. Thus a future Run79 arm difference can at most establish an interface/prompt-format effect unless a stronger semantic representation intervention is introduced. Run80 has 384 exact matched cases, and one explicit format-rejection contrast. No capable-model result, no holdout inference, no representation breakthrough.

## SYSTEM ledger
Run78 brought independent oracle tests into default CI (55 tests). Run79's evaluator is committed but the paired 7B runner is not activated. A format-independent diagnostic is designed to split interface compliance from semantic correctness, but the connector rejected the code write in this run.

## Execution and blockers
- Research branch: `research/run81-paired-repair-inference-20261017`, created from Run80.
- Latest inspected Actions: Run80 CI 39044903716 succeeded; no Run79 or Run81 model inference run.
- Attempted new isolated workflow `.github/workflows/run81-paired-repair.yml`: **blocked by GitHub connector safety checks**, not a failed scientific hypothesis.
- Attempted diagnostic implementation `research/run81/format_control.py`: **blocked by GitHub connector safety checks**.
- The prior workflow source is preserved in the conversation attachment `lattice_run79_paired_repair.yml`. It requires branch trigger adaptation before use.
- Model planned: Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M, seed 271828, temperature 0, two turns, 256 max tokens, pinned llama.cpp. **No inference or raw transcripts in this run**.
- Frozen Run79 tasks and model protocol were not modified. No cost or user laptop usage.

## Smallest supported claim
The current Run79 intervention is an **output-notation comparison**, not a distinct semantic-IR compiler representation. Model inference remains blocked by workflow-write safety checks. The next highest-information discriminator is to execute the frozen paired pilot and separately rescore cross-format semantic content, then either reformulate the IR intervention or pivot toward the independently useful semantic compiler/editor.
