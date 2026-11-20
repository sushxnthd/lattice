# Run782: independent GitHub Actions matrix verification (2026-11-20 UTC)

Canonical workflow run: https://github.com/sushxnthd/lattice/actions/runs/44793715007
Research head SHA: `c2b921bb0e55bfc7734dbda9b60dfb6363c1f13e`.

Fetched the GitHub Actions run and all three jobs independently. Overall conclusion **success**. Job 136487685922 (Python 3.11), job 136487686521 (Python 3.12), and job 136487686312 (Python 3.13) each completed successfully. In each job, **Build wheel**, **Fresh isolated install and end-to-end CLI**, and **Unit tests** steps all concluded success (9/9 selected step outcomes). A local deterministic evidence validator accepted the observed 3-job matrix and rejected a deliberately tampered failed-step negative control.

Scope: proves the current branch passed three independent interpreter-specific build/install/CLI/test jobs on GitHub-hosted Ubuntu runners. The workflow **rebuilds a wheel in each job**; it does NOT prove that a single immutable externally approved wheel was shared across jobs. No release tag, publisher-authenticated provenance, or public alpha is established. No new independently qualified production repair or model comparison is claimed.

Local reproducibility bundle SHA-256: `7b6bbc8fcf716e7dc732efe1ef0d54543e604c8f5b6670e8bd4b818693630c01`. Contains `verify_matrix.py`, `observed.json` (compact transcription of independently fetched job/step fields), `result.json`, and `SHA256SUMS`. Full archive remains local unless separately mirrored. Preserve one K-SYNTH-1 kernel, draft PR #9 and 89 sealed issues.
