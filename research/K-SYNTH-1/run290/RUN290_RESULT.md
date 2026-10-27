# K-SYNTH-1 Run290: annotation-time provenance and frozen functional validation

2026-10-27 IST. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one open/draft/unmerged PR #9. All 89 reserved boundary issues SEALED.

## Pre-execution commitment and actual functional observations

The frozen JSON was SHA-256 `ccfe66f7d7096eeda297a8a08ad3aec6da9033dcebd32e63b9fd7d45e275d6e6`, committed in `research/K-SYNTH-1/run290/RUN290_FROZEN_COMMITMENT.md` at Git commit `02d14bbbfac09d305deef364dc03ec54a8d72a11` **before executing** the separate trusted CPython oracle. Six distinct hand-authored Python 3.13 mechanisms, each with 256 seeded integer-value variations (1,536 runs, **not 1,536 independent semantic tasks**). All 1,536 frozen predictions matched real CPython executions, zero censored. Raw outcomes SHA-256 `4d2248fcdb92f6b46ffa5f5c4afc73a0600291864d1470684066d27f57a9c945`. A separate read-only auditor recomputed every expected value/event from the frozen record rather than trusting oracle `match` flags: 1,536/1,536, zero discrepancies.

The six temporal mechanisms are: (1) eager function annotation evaluated at definition-time, (2) `from __future__ import annotations` postpones evaluation into a string, (3) `type A = ...` lazily resolves the then-current binding on first `__value__` access and caches it, (4) generic type-parameter bound lazily resolves the then-current binding on first `__bound__` access and caches it, (5) type alias forced before rebind caches the old value, (6) generic bound forced before rebind caches the old value. No model-generated source was executed. The oracle only compiled trusted hard-coded templates and integer literals.

## New source-only analysis limitation and repair

Run289 lexical scanner did not visit function annotations or type-parameter bounds. Its `TypeAlias` generic traversal labelled a lazy alias call as module-level, losing evaluation-time provenance. A 1,536-case read-only source audit of the original scanner found **1,024 omitted target calls** and **512 calls without a temporal phase tag** (six templates, not 1,536 independent bugs). New `run290_annotation_guard.py` tags eager, postponed, lazy alias, lazy generic bound, and ordinary body contexts without executing source; runtime object identity, mutation stability, and unconditional soundness remain `UNKNOWN`. The semantic-IR and ordinary Python/AST-action views carry **identical canonical facts** in all 1,536 parity checks. This establishes coverage and fact parity, **not a model advantage**. New tests: 8/8. Run289 regression tests: 9/9. Total 17/17 passing after correcting a local missing import during test setup.

## GitHub CI failure recovered

Original Run289 Actions `40486504311` completed **FAILURE**. The exact exception was `KeyError: 'len'` because the compact witness chose `outer.get_children()[0]`, which is the lambda symtable, not nested `f`. The original failure remains preserved. The corrected witness selects the child named `f`, asserts unique match, and passed all four trusted fixtures locally. Fix commit `0897afc3bd2dedca07c4c97c4edf4ad0945e6c2c`. New GitHub CI workflow `lattice-run290-temporal.yml` committed to execute the corrected witness and the Run290 minimal counterexample on Python 3.13; cloud outcome was **not independently recovered at report time**.

## Claim boundary and priorities

Four independently qualified real multi-production-source issues remain: Flask PR6096, urllib3 PR5071, Werkzeug PR3136, HTTPcore PR1000. This is **not** a fifth issue or a general theorem. No new coding-model completion, no model-generated repair, no powered paired IR-versus-Python result, and no breakthrough. The original Run283 failed holdout remains a failure. Historical GitHub ZIP mirroring is still incomplete. All 89 reserved boundary issues untouched.

**Run291:** first obtain genuine paired capable open-coding-model repairs with frozen equal facts, source, edit authority, compiler and isolated oracle, then qualify more independent multi-file production PRs. Annotation provenance is a guardrail, not the primary endpoint. Preserve SHA artifacts, raw completions, token counts, precompletion failures and clustered uncertainty; never execute untrusted model code on host.
