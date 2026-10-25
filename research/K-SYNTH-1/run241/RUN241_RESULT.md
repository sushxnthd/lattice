# Run241 — completed CrossGL capable-model pair and independent trust-boundary audit

The previously launched Run240 experiment completed successfully as a cloud *workflow*, not as a model repair. The original GitHub Actions run is https://github.com/sushxnthd/lattice/actions/runs/40169894610 and its artifact ID is 12590395845. The immutable 17-file artifact contains original requests, raw responses, parsed outputs, verifier records, model hashes and token counts. The independent auditor verified request/response SHA-256, frozen-facts SHA-256, model identity, seed, exact reproduction of both prompts, and information equivalence of the seven displayed source blocks.

| Result | Semantic-IR source view | Ordinary-Python source view |
| --- | ---: | ---: |
| Model | Qwen2.5-Coder-7B-Instruct-GGUF Q4_K_M | Same |
| Seed | 24041 | 24041 |
| Prompt tokens | 2596 | 2324 |
| Completion tokens | 690 | 712 |
| Generated actions | 3 | 3 |
| Metadata-valid actions | 1 | 2 |
| Read-only target attempts | 1 | 1 |
| Editable actions erasing original declarations | 2 | 2 |
| Lexer edits | 0 | 0 |
| Compiler accepted | **No** | **No** |
| Functional oracle executed on model patch | **No** | **No** |

IR's compiler failed on a stale file SHA. Python-view's compiler failed on a read-only selector. Independent AST checks establish that both first actions replace `parse_if_statement` with a differently named `parse_else_if_statement`, and both generator actions replace `generate_if_statement` with a differently named method. Both also attempt to modify the read-only `parse_statement`. Thus neither has a valid transaction even after post-hoc metadata normalization.

**New implementation and counterexample:** A trusted-selector adapter accepts `{selector, content}` and injects path and file hash from immutable source facts. This removes the model's hash-copy burden by construction but rejects both original outputs for method-declaration erasure. This is a deterministic post-hoc diagnostic, not prospective inference or a functional win. Seventeen local tests passed, including independent integrity checks, tamper detection, exact request regeneration, authority enforcement and declaration-preservation tests. Full code, original cloud outputs, traces, tests and SHA-256 manifest are preserved in the Run241 local reproducibility archive.

**Interpretation:** The pair is a concordant failure, with zero discordant outcomes. No representation effect is estimable. Furthermore the so-called ordinary-Python arm shows Python source but still emits the same JSON action grammar as IR. This is a source-presentation comparison, **not** a true ordinary-Python editing baseline. The prompt lengths also differ by 272 tokens.

**Power remains a constraint:** Under hypothetical 30% discordance and 65% IR wins among discordant pairs, exact two-sided McNemar testing gives ~72.3% power for 258 independent pairs and ~80% for 306; a 60% conditional win rate requires ~681 independent pairs, before clustering adjustments. These are assumptions, not observed effects.

**Next:** Freeze metadata-free action schemas, a genuinely ordinary-Python editing baseline, identical trusted compiler and independent functional oracles across multiple qualified repositories. The 89 reserved boundary issues remain untouched. No representation breakthrough is claimed.
