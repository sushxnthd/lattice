# K-SYNTH-1 Run406: structural heldout audit and frozen oracle CLI correction

Date: 2026-11-01 IST. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole draft PR #9; 89 boundary issues remain SEALED.

## Original workflow failure and repair

The Run405 prospective pytest #14997 oracle requires `--output <directory>`, but the Run405 GitHub workflow called it with the positional argument `evidence`. Reexecuting this **exact original invocation** produces argparse exit code **2** before any test runs. This is an infrastructure failure, not a repair failure.

Corrected only the workflow invocation, not the frozen oracle or eligibility criteria. Correction commit: `a6a4c8e9430fb58f12886693c65a62944dedb328`. Frozen oracle SHA-256: `5bbb1ec4b94f18e00f22ac9c4ae5f532cca45d6fc8d62b991b210cb9815c16b9`.

The GitHub connector's commit-run lookup returned no PR-triggered runs for the original or corrected commits, but that lookup excludes push-triggered runs. Therefore the exact pinned pytest 9.0.3 and 9.1.1 outcomes are **not independently verified**.

## New methodological finding and actual execution

Read-only AST inspection of the original Run405 `CASES` proves that all six public/heldout target argument sequences belong to **one abstract structural class**: `PACKAGE → TOP → PACKAGE`. The heldout arguments are disjoint but do not test a different abstract interleaving mechanism. This does not establish full semantic equivalence or statistical dependence. The control cases span four abstract classes.

Executed **48 actual isolated CPython/pytest 9.0.2 processes**, consisting of the 12 frozen cases across identity, alpha-renamed package/fixture symbols, changed fixture values, and combined transformations. **48/48 passed**, with no metamorphic status disagreements. Raw commands, stdout, stderr, return codes, durations, source hashes, and transformation labels were preserved locally. An independent verifier performed **422 checks**, including four separate functional reexecutions, with **zero disagreements**. **15/15** regression/adversarial unit tests passed.

These postfreeze diagnostic transformations **do not** change the original prospective eligibility, are not new qualified repairs, and do not establish the 9.1.1 regression. The installed 9.0.2 is not the pinned 9.0.3 negative control.

## Decision and reproducibility

pytest #14997 remains **NOT QUALIFIED**, pending original pinned cloud outcomes, full-reference and joint target-plus-control two-production-source necessity. Do not retune. Historical qualified independent multi-source tasks remain **two** (Flask PR6096 and urllib3 PR5071). No new model inference, powered semantic-IR superiority or breakthrough.

Full 15-payload SHA-verified local archive: `lattice_run406_structural_holdout_and_frozen_cli_repair.zip`; ZIP SHA-256 `8bd6e59a184a2634e9dadd4b78c3036a9fad25ec47e2e7a5b8eaaa6122712682`. Includes full executable metamorphic generator, independent verifier, 48 raw subprocess traces, tests, original oracle copy, failure log, manifest and report. Complete historical GitHub artifact mirroring remains incomplete.
