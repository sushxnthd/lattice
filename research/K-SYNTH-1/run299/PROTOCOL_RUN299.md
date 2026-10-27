# K-SYNTH-1 Run299 prospective freeze (2026-10-27 UTC)

Research question: can the SHA-pinned free Qwen2.5-Coder-7B Q4_K_M produce genuine completed paired h11 repairs under a source-only bounded prompt, after the original Run298's 900-second CPU timeouts occurred before completion?

This is a **new reformulation**, not a rescue or relabeling of the original Run298 outcome. The original Run298 arm failures remain precompletion TIMEOUT, never model abstentions or repair failures.

- Task: historical h11 issue, baseline commit `522b00470b5776dda2dc7e98ff778eb1e418e6ad`, preselected after seeing the upstream PR. One real task, not blind task discovery.
- Input source: Run298 canonical facts from historical baseline only; no reference checkout or patch in source selection.
- Source-only selection: whole top-level Python functions/classes and methods, fixed issue-token lexical scoring, deterministic four-file character budgets. Both arms contain the exact same selected source text and original full-file SHA hashes.
- Edit authority: same original four modules, exact unique source-span preimages, shared Run295 v2 compiler and isolated Run297 5-target/5-control oracle.
- Model: Qwen2.5-Coder-7B-Instruct Q4_K_M SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; seed 299001, temperature 0, max output 768 tokens, 900s per arm.
- Original Run298 had 14,731 and 16,224 input tokens and timed out after 900s each without producing completions. Preserve those exact failures.
- Frozen compact source SHA256: `2c0b38d27897567ee920120216188de9bf3ecebbd8049d2e8c5c8d4438ced797`.
- Compact context SHA256: `1a68ad280455912ee21703543d2282a36fc81a976b36c6215349b6ec6e656c59`.
- Frozen request SHA256: IR `66fe3c17da322cbf7c6e817999cf3d409dd7c03e498ad088d0d2053a7cdfb7f3`; Python/AST `89d2dd72941f8ba98f04366f92c60b92d0ef6788ada1bab8930929e570376843`.
- Selected exact source characters: 15,895 from 4 historical files across 12 non-overlapping windows. Prompt lengths: IR 17,103 characters, Python/AST 17,179 characters.
- Prospective result: raw completion and inference metadata; exact compiler acceptance and full 10-case isolated oracle; no repair success inferred from compile alone.
- Predeclared failure: prompt overflow, model timeout, invalid output, compiler rejection, or oracle failure are reported separately. Zero valid completions means no model performance comparison.
- Explicit limits: representation is a *presentation-only* contrast using shared JSON edit grammar, not proof of a sound semantic-IR editing language. One task is underpowered. No claim of IR superiority or breakthrough.
- Never touch 89 sealed boundary issues. Use only `research/exp003-context-order` and existing draft PR #9.

This freeze is recorded **before** any Run299 model inference or reference-patch coverage audit. Any subsequent localization coverage measurement is postfreeze descriptive and cannot modify these source windows.
