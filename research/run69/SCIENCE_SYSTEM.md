# Lattice Run 69 — provenance digest binding counterexample (2026-10-17)

## SCIENCE ledger
Status: **KNOWN negative boundary for traceability**, **UNTESTED** for model-repair representation effect. This is a capability-building/adversarial anomaly probe, not a representation-science experiment. No frozen holdout was opened. No model generation or model transcript exists.

**Active kernel**: Does an explicit semantic IR reduce semantic repair complexity for capable coding models relative to ordinary Python with the identical verifier/compiler and matched information?
- Best-known baseline: Python dictionary patch + the same deterministic framed compiler and independent Boolean oracle.
- Intervention: model edits expressed as semantic IR, parsed to the same canonical rule replacement mapping.
- Matched control: ordinary Python dictionary edits with identical trusted prior, task information, compiler, verifier, decoding, model, and token-budget reporting.
- Scalar primary metric: hidden-test recovery per repair attempt, prospectively averaged over paired tasks; secondary regressions, forbidden states, churn, calls, tokens.
- Strongest alternative: verifier-only benefit or prompt length/format bias rather than semantic representation.
- Falsification: no reproducible paired improvement over Python + identical compiler; or equivalent canonical proposals.
- Publishable threshold (prospective proposal, not preregistration): >=10 pp improvement in held-out perfect-repository recovery across >=30 paired tasks with confidence interval excluding zero and clean independent replication.
- System relevance: >=20% fewer repair attempts at matched correctness without increased forbidden-state violations on real multi-file edits.
- Kill/reformulate after three substantive capable-model discriminators without an effect/boundary; do not kill the system.

**No model evidence from this run.** Prior run66 equivalence probe found 80 equivalent patch maps and 160 truth-table comparisons with zero mismatches; this does not establish coding-model advantage.

## SYSTEM ledger — concrete new adversarial counterexample
Source under examination: Run66 local prototype `src/lattice/provenance_audit.py` (NOT committed to production; production branch reference `cfa8bb7dc5b57deeaa6ee0a4ac8ef400086903fb`).

Hypothesis: `trusted_contract_sha256` identifies the trusted prior state + patch + scope.

Observed falsification: two different trusted prior frames, with `read = a` versus `read = not a`, have identical root indices and identical patch `edit = read` and authority `{edit}`. Both canonical edits are accepted and both return exactly the same contract digest:
`6dad21549803cc8f5eea123a0f0057b6b4ea67818aaec53c406c3c8ec32372cd`.
This is NOT a SHA-256 collision: the hashed preimage omitted the prior frame's inputs/nodes/sources. It is a provenance traceability/identity weakness, not a bypass of `audit_transition` acceptance.

Fix tested locally: hash a canonical serialization of prior inputs, every node source and binding, prior roots/sources, patch, and authority. Fixed digests:
- Prior `read=a`: `c1464f3c027b817483d8a4ff60034e241fddd57c0cbf0880a27690e5b4e697cd`
- Prior `read=not a`: `cebfc2d192b0d3b092a53a3132e6cc031e284916f61687171615a3165820a401`
Both valid edits still accepted. Existing 7 local stand-in tests pass after the fix (`7 passed in 0.03s`). Production integration and CI are **not** verified.

## Blocker, attempts, and next discriminating action
- Created isolated branch `build/run69-source-bound-provenance-20261017` at `cfa8bb7dc5b57deeaa6ee0a4ac8ef400086903fb`.
- Attempt to create `src/lattice/provenance_audit.py` through GitHub connector was rejected by the write safety layer. Preserve the rejection as an infrastructure blocker, not a scientific failure. No attempt to bypass policy.
- Local reproducible files: `provenance_digest_collision_probe.py`, `provenance_digest_fixed_probe.py`, `digest_counterexample.json`, `digest_fixed.json`, and fixed local `src/lattice/provenance_audit.py`.
- Cheapest next discriminator: production-integrate the independent oracle/provenance checks if code-write becomes available; then prospectively freeze realistic paired Python-vs-IR repair tasks and use a capable no-cost coding model. Do not treat CI success as representation evidence.
- Smallest claim: the original local prototype's contract digest does not bind the prior frame; a corrected digest does on this adversarial pair. This is a system provenance improvement only.
