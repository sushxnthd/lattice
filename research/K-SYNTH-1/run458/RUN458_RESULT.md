# Run458: fail-closed paired execution receipt audit

2026-11-03 UTC. The previous Run457 receipt audit did not verify shared compiler/oracle/edit authority/decoding contracts. This new executable checks SHA-256 format, duplicate task/arm receipts, pairing, and equality of model, source, task facts, edit authority, compiler, oracle, and decoding hashes. It intentionally does **not** infer information equivalence from hash equality or mark any pair eligible for superiority: semantic information equivalence remains UNKNOWN pending independent content-level verification.

The script includes deterministic self-tests for nominal receipts, unpaired arms, duplicate receipts, oracle mismatch, and malformed hashes. **Execution not independently verified in this run** because local container execution failed (redis ConnectionError). No raw model outputs or qualified repair were produced. Two qualified real tasks remain. The 89 reserved issues are untouched. Do not count this as evidence of IR superiority.

Next: independently verify prompt fact/action equivalence and run actual paired coding-model repairs, then prospectively qualify a third real multi-production-source repair.
