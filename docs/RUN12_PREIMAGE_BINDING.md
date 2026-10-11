# Run 12: paired preimage-binding diagnostic (engineering only)

**Classification:** DISCRIMINATION + CAPABILITY-BUILDING. Local prototype; implementation not integrated.

**Prediction:** A candidate-only source-hash verifier can approve a candidate against a trusted manifest even when the *actual original checkout* has drifted. Independently snapshotting the original and requiring an exact match should reject stale-preimage workflows.

**Result:** 21 local tests passed. A deterministic synthetic differential had four regimes with 300 variants each. In the stale-original regime, the prior candidate-only v3 accepted 300/300 and paired v4 rejected 300/300 with `baseline_mismatch`. Both accepted 300/300 authorized edits and rejected 600/600 protected-candidate changes across the other two regimes.

**Interpretation:** This is a provenance/workflow guard, not semantic program verification or a Lattice-specific advantage. Git `apply --check --index` already checks index/working-tree consistency; broad preimage-binding novelty is not supported (https://git-scm.com/docs/git-apply).

**Limits:** Four synthetic regimes with repeated variants, no model inference, no real-repository validation, no atomic promotion or concurrent-mutation guarantee. Historical Qwen negative results are unchanged.

**Reproduction:** Run-12 source, 21 tests, differential probe, raw JSON, SHA-256 manifest, paper addendum, and draft four-arm evaluation protocol are preserved in a downloadable bundle outside GitHub. Source commit was rejected by safety checks; do not treat this branch as containing the code.

**Next:** Integrate source-bound preflight into an isolated build branch, independently validate against Git-backed repositories, then prospectively freeze capable-model A/B/C/D evaluation with same-compiler and matched-token controls.
