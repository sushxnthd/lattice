# K-SYNTH-1 Run437 — Lossless source transaction and real issue-first screening

## Scientific finding
The previous Run436 two-file compiler used `ast.unparse` to rewrite entire source files. An executed adversarial fixture demonstrates that it silently drops shebangs, copyright/SPDX headers, comments and other source trivia **even for a semantically no-op edit**. This violates byte-level edit authority and provenance preservation, despite semantic and SHA-locked preconditions.

A new bounded UTF-8 AST-byte-span transaction changes only two authorized integer literals, retaining all other source bytes. It uses the same `inspect`, canonicalization, SHA locks, edit authority and output checks for the semantic IR and ordinary AST-action views. It is in-memory atomic only; no filesystem crash guarantee or general Python soundness is claimed.

## Executed local evidence
- 256 seeded trusted two-source fixtures with non-ASCII comments, legal headers, shebangs, trailing comments, negative integers and 128 CRLF cases.
- Original compiler removed legal headers in **256/256**; lossless compiler preserved them in **256/256**.
- **512** lossless compiler transactions (256 IR, 256 AST); **256/256** paired output byte parity; exact no-op preservation.
- **16,384 actual CPython function calls** comparing old and new semantics, zero disagreements.
- Independent auditor: **8,192 additional CPython calls**, **4,608 byte/source/function checks**, zero disagreements.
- **14/14** adversarial and regression tests passed. Raw receipts, full code, tests, SHA-256 manifest and clean-extraction replay are in the local Run437 ZIP.

The conditional byte-preservation theorem follows directly from `output=source[:start]+replacement+source[end:]` with AST byte-offset verification, source-hash locks and postcondition validation. Scope is only the trusted exact-integer affine grammar, not general Python or untrusted model code.

## Real issue-first candidate screening
1. [Flask issue #4037](https://github.com/pallets/flask/issues/4037) was frozen on this branch in commit `e0aea6d` **before** reading the reference. [Merged PR #4036](https://github.com/pallets/flask/pull/4036) changed only one production Python file, `src/flask/blueprints.py`. **REJECTED** under the original >=2-source criterion, without retuning.
2. [Flask issue #4297](https://github.com/pallets/flask/issues/4297) was frozen in commit `495cd71` before reference inspection. [Merged PR #4487](https://github.com/pallets/flask/pull/4487) changed five production files: app, blueprints, helpers, scaffold and typing. The pinned historical source/ablation cloud workflow was committed (`3c8037b`), but **its execution and original artifact remain unverified**. Its runnable oracle was implemented after reference inspection, so any outcome is exploratory and must not be retroactively promoted to strict prospective qualification. Unmerged single-source proposals #4305/#4306 are warnings, not verified successful alternatives.

## Status
Qualified real multi-source repairs remain **two**. No new open-model completions, powered IR superiority evidence or breakthrough. All **89 reserved boundary issues SEALED**. Full historical ZIP mirroring incomplete. One intended open/draft/unmerged PR #9 on `research/exp003-context-order`.

## Reproduce
The complete local Run437 archive includes `run436_dual_view_compiler.py`, `run437_lossless_transaction.py`, experiment, independent auditor, 256 raw fixture receipts, 14 tests, reports and SHA manifest. Run `python run437_experiment.py && python -I -S run437_independent_audit.py && python -m unittest -v test_run437.py`.
