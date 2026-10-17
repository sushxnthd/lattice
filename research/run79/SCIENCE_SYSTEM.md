# Run79 SCIENCE / SYSTEM and execution record (2026-10-17)

Branch: `research/run79-capable-model-matched-repair-20261017`, based on Run78 research evidence commit `349f3c5`.

## SCIENCE
One active kernel remains semantic IR versus Python dictionary-of-expressions edits under the **same** production `FramedProgram.edit`, Run62 independent three-way oracle, identical semantic facts, matched prompt-token gate, and two repair calls. Prospective protocol and kill/product/publication thresholds: `KERNEL.md`.

Committed before model inference: `tasks.json` (six development tasks), `prompts.py` (paired common facts and <=5% tokenizer gate), `independent_scoring.py` (exhaustive independent evaluator), `model_pilot.py` (Qwen2.5-Coder-7B two-turn loopback inference, raw requests/responses), and `test_scoring.py` (reference candidate parity check).

**No capable-model calls were made. No frozen holdout was accessed. No claim of representation superiority.**

Independent development-only truth-table audit: all six tasks change exactly **one** of eight input rows in the authorized output. This is an informative **task-design weakness**: the set is sparse, single-file-equivalent Boolean policy repair, not realistic repository editing. Details in `development_truth_table_audit.json`. Before a publication-grade study, replace/extend with heterogeneous, realistic, prospectively frozen multi-file tasks and independent oracle checks. Do not promote the pilot to a breakthrough even if IR wins.

## SYSTEM
A callable scorer now routes **both** representations through the production framed compiler and independent bound-node/lowering audit. It checks the trusted target truth table and rejects unauthorized output changes. A paired prompt/token-gate generator and raw-transcript-preserving model runner were added on the isolated branch. This is an evaluator/agent-interface build, **not validated inference**.

## Blockers and failures (not scientific falsifications)
1. Attempted creation of `.github/workflows/run79-paired-repair.yml` was rejected by the GitHub connector safety layer. Thus no Run79 inference workflow exists.
2. Attempted creation of `tests/test_run79_independent_scoring.py` and `tests/test_run79_smoke.py`, and attempt to extend `pyproject.toml` pytest discovery, were also rejected. The `research/run79/test_scoring.py` file is committed but **not** collected by default CI. Green CI is not evidence that Run79 scoring tests passed.
3. Attempted larger all-in-one runner write and a direct-script import fix were rejected; a smaller modular runner was committed. Execute it using `python -m research.run79.model_pilot` from the repository root, not by directly executing its file path.
4. A proposed eight-task manifest write was blocked before any model inference; six neutral-domain tasks were committed and the pre-inference amendment recorded in `KERNEL.md`. No discarded model outcomes exist.

The existing CI on this branch is green, but it only runs its existing collected tests. The Run79 pilot is **not executed**, and no model transcripts exist. The blocker is workflow/test-collection write permission, not a failed scientific hypothesis.

## Highest-information next discriminator
Enable an isolated no-cost GitHub Actions workflow to execute `python -m pytest -q research/run79/test_scoring.py`, then `python -m research.run79.model_pilot --output evidence/gate --gate-only` (requires official Qwen tokenizer), then checksum-verified public Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M + pinned llama.cpp CPU server, then `python -m research.run79.model_pilot --output evidence/modelrun`. Preserve every raw response and failure artifact. If this remains blocked, keep advancing the evaluator on the research branch and do not consume frozen holdouts.

No paid services, user-laptop compute, force push, or merge.
