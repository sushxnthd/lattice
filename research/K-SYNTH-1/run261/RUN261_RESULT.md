# K-SYNTH-1 Run261 — Unicode editor counterexample and new upstream qualification

Date: 2026-10-26. Canonical branch research/exp003-context-order; draft PR #9; 89 boundary issues sealed.

## New executable counterexample

Run260's SHA-pinned byte-span editor accepted edits splitting UTF-8 code points. In Python source `value = "é"`, the UTF-8 bytes for é are C3 A9. Replacing only byte C3 with C2 silently yields `value = "©"` (C2 A9), still valid UTF-8 and valid Python. Therefore preimage hashing plus AST parsing does NOT establish character-boundary edit authority. Run261 v2 rejects any byte span whose start or end is not a UTF-8 prefix boundary, adds a 256,000-byte raw transaction cap and a 16-file cap, and handles invalid surrogate-containing JSON/replacements fail-closed. New source SHA256 `9eea3daebc3bc9aa80b09ccce92e21db54481664150054b6a6245e6bf9d0c1b8`.

Validation: 24/24 inherited/reference/new tests passed; 512/512 deterministic invalid-transaction cases rejected; 256 seeded Unicode-span fuzz cases; exact real Flask two-file reference roundtrip still passed. This is a narrow pure-map prototype, NOT production security or semantic correctness.

## New independent REAL upstream bug candidate

[urllib3 PR #5071](https://github.com/urllib3/urllib3/pull/5071) fixes explicit port-zero handling. Pinned first-parent baseline `f4e4bc31f40f8c94c6a1f1685df28f97ff48c305`, reference merge commit `f5cf122346141b187cca0db6e6445297d336b610`. Three production files change: connectionpool.py, poolmanager.py, util/url.py. Prospectively frozen six ablations: baseline, each one-file reference patch, poolmanager+url pair, full reference. Read-only public test checks manager port=0; independent heldout checks URL netloc and proxy port=0; nonregressions cover default ports and host identity. The third source file is NOT presumed necessary for these endpoints.

Committed SHA-pinned qualification runner `research/K-SYNTH-1/run261/qualify_urllib3_5071.py.zlib.b64` (runner SHA256 `59d598432bb2acc9a5715d869924394e65c0a02a168b70a60c70cae2779fb35a`, commit `71256b3f`) and GitHub Actions workflow `.github/workflows/lattice-k-synth-1-run261-urllib3.yml` (commit `c660ef23`). **Cloud qualification result and run ID NOT YET OBSERVED**. Local installed urllib3 2.7.0 failed all three targeted port-zero checks and passed three nonregressions; this is NOT pinned-upstream qualification.

## Scientific status and limitations

No new capable-model inference this run. Previous Flask JSON/comment fact-encoding negative results are unchanged; genuine semantic-IR vs ordinary-Python superiority remains UNTESTED. The new real issue is UNQUALIFIED pending independent cloud evidence. No significance, mechanism claim or breakthrough.

Complete SHA-256-verified local Run261 archive: `/mnt/data/lattice_run261/lattice_run261_unicode_editor_and_urllib3_qualification.zip`, 52 manifest entries, archive SHA256 `ff7f738250d48bccb1415103418ca1384cea6afb932a2d08dcfa5deb90403752`. Full test suite and ZIP remain local; retry GitHub mirroring. Same draft PR, same branch, sealed issues untouched.
