# Run243 — Independent five-arm audit and parser counterexample

**Date:** 2026-10-25. **Status:** genuine Run242 outputs independently audited; no new model inference. **Original artifact:** GitHub Actions run 40175492288, artifact 12593037101; immutable ZIP SHA-256 `25bda92d766cd8061d14102a228eff0a68669b8501a860c08d2a5e401e2dbf3b`.

All five requests matched prospectively frozen SHA-256 hashes. Independently verified exact prompts, raw response and completion hashes, model identity, seed, token counts, and exact reconstruction of seven immutable source blocks in both source presentations. Pinned model: Qwen2.5-Coder-7B-Instruct Q4_K_M, weights SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; seed 24241.

| Frozen arm | Prompt/completion tokens | Compiler | Functional | Decisive failure |
| --- | ---: | --- | --- | --- |
| IR JSON, trusted metadata | 2615/489 | Rejected | Not run | Read-only selector; declaration renames |
| Python JSON, trusted metadata | 2345/378 | Rejected | Not run | Missing original method declarations |
| IR JSON, copied metadata | 2630/757 | Rejected | Not run | Same read-only selector and declaration renames |
| Python JSON, copied metadata | 2360/284 | Rejected | Not run | Missing original method declaration |
| Native Python source blocks | 2389/390 | Accepted | **3/5** | Both else-if cases fail |

The original source passed 3/5; the independently authored three-file reference passed 5/5. The native arm modified only parser and generator, not lexer, and **did not improve** functional correctness.

## Independent necessary-condition witness

A separate AST-allowlisted token-stream execution of the genuine native Python parser reproduced:
- if-only and plain if/else: pass;
- single else-if with no final else: `Expected ELSE, got EOF`;
- two else-if branches followed by else: `Expected LBRACE, got IF`;
- newline-separated else then if: `Expected ELSE, got EOF`.

This is a narrow independently executable counterexample, **not** a rerun of the full repository oracle. The cloud oracle independently recorded the same chain and multiline failures. The model unconditionally consumes an `ELSE` after parsing a nested if-body, breaking chained or unterminated else-if.

## Construct-validity finding

The so-called semantic-IR view is **JSON wrapping raw Python source strings** with selector, path, name, kind and edit authority. It has no typed AST, dependency graph or operational semantics. This is a source-block presentation comparison, not a defensible test of semantic IR.

Removing metadata-copy responsibility did not eliminate either family’s failures. The first action's selector and replacement content were identical across copied/trusted conditions within each representation family. Copied paths and hashes were correct for all known selectors; metadata-copy error was not the limiting mechanism in this one pilot.

The native Python condition uses unconstrained plaintext output instead of constrained JSON decoding, so its compiler acceptance cannot be attributed causally to Python representation. **No representation advantage is established.** This is one issue and one seed; the five arms are not independent statistical units.

## Reproducibility

Original cloud evidence: https://github.com/sushxnthd/lattice/actions/runs/40175492288

A separately preserved Run243 archive contains the immutable original ZIP, `audit_run242.py` (full provenance/action auditor), `native_witness.py` (independent executable counterexample), `test_run243.py` (13 passing tests), machine-readable results, witness traces, preregistration, and SHA-256 manifest. The complete archive was retained as a conversation artifact, not yet as a GitHub release asset.

## Next scientific decision

**Stop cosmetic single-issue syntax experiments.** Qualify new real multi-file issues from independent repositories using original failures, passing reference repairs, seeded negative controls, and frozen independent functional oracles. Develop a genuinely typed/lossless semantic representation and a Python baseline with **identical semantic facts**. Freeze a common output protocol/compiler and capable-model inference budget. Size the prospective cohort using cluster-aware paired power (the earlier independent-pair assumptions imply ~306 or ~681 pairs depending on effect, before repository clustering). Reserve the 89 boundary issues for an unseen prediction. Pivot toward transactional compiler safety if Python ties or beats IR in two controlled reformulations.

No breakthrough or completed system is claimed.
