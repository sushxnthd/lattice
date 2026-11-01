# K-SYNTH-1 Run409: original pinned pytest evidence and heldout-source duplication

2026-11-01. Canonical branch `research/exp003-context-order`, sole draft PR #9. All 89 reserved boundary issues sealed.

## ORIGINAL Run408 frozen pytest #14992 artifacts

Recovered the original completed [Actions run 41285985063](https://github.com/sushxnthd/lattice/actions/runs/41285985063), artifacts `13074967792` and `13074868016`. The original ZIP SHA-256 values are respectively `b36bd8c58bf7a31ed77b6d190403116a13f84d234b02b1d67b9caf01c20b79ad` and `43d1cf6df8638915580ad8585663ddf3a7421ad98f32ea46536bc8989c770282`. The frozen oracle SHA-256 is `56ea237e58484cdb0e066acc02c0cb1982d657d91cc9df956f9300e17e2bd366`.

An independent read-only auditor reconstructed all 12 test-source pairs per version, verified original source hashes, raw subprocess exits, failure witnesses, pinned source checkout SHA, installed package version, archive and internal hashes: **231 checks, zero disagreements**. Exact pytest 9.0.3 (commit `a7d58d7a21b78581e636bbbdea13c66ad1657c1e`) passed 3/3 public targets, 3/3 heldout targets and 6/6 controls. Exact pytest 9.1.1 (commit `cf470ec0bf7eb89cd97dd56df4859eae5db46447`) passed 0/3, 0/3 and 6/6 respectively. These are 24 original isolated subprocesses.

**New construct-validity failure:** the six alleged public/heldout target cases have only **two distinct byte-identical source pairs**, with **100% public-to-heldout overlap**. There are **zero unseen heldout target programs**, and just four unique source pairs across all twelve cases. These repeated runs are not independent issues or heldout generalization evidence. A naive all-wins sign test on six pseudo-replicates would give p=0.03125, versus p=0.5 for two unique source pairs; neither constitutes a valid independent-repository test.

The frozen summary's hard-coded `NOT_QUALIFIED_REFERENCE_AND_REGRESSION_NOT_RUN` label remains stale even inside the completed regression artifact; the raw records, not this label, establish the reproduced outcome. Six adversarial audit tests passed.

## API scope and actual fixing-reference gate

[Issue #14992](https://github.com/pytest-dev/pytest/issues/14992) was closed as **invalid** by its author after the maintainer explained that mutating `metafunc.fixturenames` is private, undocumented behavior. The attempted [fix PR #14993](https://github.com/pytest-dev/pytest/pull/14993) was closed **unmerged**, changing only **one production Python file** (`src/_pytest/fixtures.py`) plus tests/changelog. The original frozen requirement of a genuine fixing reference and two behaviorally necessary production sources is not satisfied: **NOT QUALIFIED**. No retuning.

Executed a separately labeled **post-outcome** private-hook scope diagnostic in [Actions run 41290284343](https://github.com/sushxnthd/lattice/actions/runs/41290284343): without the hook, both pinned versions produce `precondition, subject_deps, subject, guard`; with the hook, 9.0.3 produces `guard, precondition, subject_deps, subject` and 9.1.1 produces `precondition, subject_deps, guard, subject`. Four original cloud subprocesses passed their exact expectations; independent audit **44 checks, zero disagreements**. The two programs are not semantics-equivalent; the result localizes the observed difference to unsupported private-hook usage, not a public API guarantee.

A second [source-attested cloud run 41290361345](https://github.com/sushxnthd/lattice/actions/runs/41290361345) checked byte-level SHA-256 parity between the pinned Git checkout and installed pytest Python sources: **73/73 files on 9.0.3 and 80/80 on 9.1.1**, zero mismatches. Independent read-only record audit **334 checks, zero disagreements**. Original source-attested ZIP SHA-256 values: `36aeb5e22b81460501bb71279b7c97c5c1d38dc179beb84402980216504be2cc` and `3f3e4d61b3ab39c3ad348a219866a19219669d668940abfa3c5e342864f7e7fd`.

## Scientific status

**Only TWO** historical independently qualified real multi-production-source repairs (Flask PR6096, urllib3 PR5071). No new model inference, no powered semantic-IR superiority, no breakthrough. All 89 reserved issues sealed. The full local Run409 reproducibility archive contains the four original ZIPs, two attested ZIPs, original frozen outcomes, independent auditors, adversarial tests, post-outcome functional traces, report and SHA manifest. Next: genuinely new issue-first two-production-source repair, source-distinct heldout oracle, and matched real-task semantic/dataflow IR versus ordinary Python/AST functional model comparison.
