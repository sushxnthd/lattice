# Run649 — fail-closed cross-arm provenance and transcript audit

Executed an independent local two-commit Git fixture. The verifier validates exact frozen base/head, oracle SHA-256, all four arm names, every arm's two production source blobs against git show and expected base/head assignment, process status, stderr, and typed four-key JSON observations.

Results: 1 valid synthetic transcript returned STRUCTURALLY_VERIFIED_NOT_QUALIFIED; 43 adversarial mutations rejected UNKNOWN, including source-hash tampering, revision substitution, missing observations, invalid JSON, stderr and frozen identity corruption.

This is synthetic contract evidence only. No upstream production execution, model inference, new repair qualification, or semantic-IR superiority claim. The validator does not establish isolation or semantic correctness. All 89 reserved issues sealed.

Local SHA-verified ZIP: lattice_run649.zip, SHA256 a019a07fce49103ae67599d352f2fcf378da3a51c3bddd2a5b91440651a8265d. Executable and raw outputs still require GitHub mirroring.

Next: run actual pinned upstream oracle in isolated CI and independently adjudicate target-plus-control outcomes.