# Run790 — paired wheel-attestation falsification (2026-11-21 UTC)

Research branch: research/exp003-context-order; PR #9 remains the sole intended draft PR. No kernel or boundary-issue changes.

## Executed local evidence

Implemented a fail-closed four-artifact paired-build comparator, with 11/11 Python unittest cases passing in 0.018 s. Inputs: two distinct JSON attestations and two distinct wheel paths. Checks: source SHA-256, command, environment SHA-256, distinct declared build/builder IDs, filenames, actual wheel digests, byte identity. Controls: changed bytes with recalculated digest; forged digest; same build ID; same builder ID; source/environment/command mismatch; path alias; malformed digest; filename mismatch. All rejected or returned UNKNOWN as designed. The passing control returns MATCH_UNAPPROVED, explicitly NOT independently verified or release-approved.

## Counterexample and scope

**Counterexample:** An adversarial producer can copy one wheel to two paths, invent distinct build_id/builder_id values, and produce internally consistent JSON attestations. All local checks pass, although no second build occurred. Thus even matching source/environment assertions and wheel bytes do NOT prove independent builds or release approval. External authenticated CI job identity and source provenance are required. This is a release-integrity negative result, not evidence of semantic-IR superiority.

The full executable comparator, 11 tests, raw output, and SHA-256 manifest are preserved in the Run790 local reproducibility archive. The GitHub connector cannot access container-local files, so only this factual report is mirrored in this commit; do not treat the local code as durably mirrored.

## Outstanding gates

No actual pair of independent pinned-source wheel builds was performed. No public release tag was created. The real-repair qualification count remains 2. Next: obtain authenticated separate CI build records, independently compare real wheel bytes, then run approved single-artifact Python 3.11–3.13 installation.