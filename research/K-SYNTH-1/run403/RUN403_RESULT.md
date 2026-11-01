# K-SYNTH-1 Run403 — edit-authority confound and paired-model launch

2026-11-01 IST. **No new qualified real repair or semantic-IR superiority claim.**

## New executable counterexample and correction

Run402's original ordinary Python AST-action compiler accepts edits to *dead assignments*, whereas its semantic IR rejects them because they are not reaching definitions of the terminal return. Thus the arms do **not** have identical edit authority, even though they share the same compiler. This is a pre-inference action-space confound.

A separately implemented ordinary-AST backward-liveness gate restricts AST actions to the same reaching assignments, without calling the semantic locator for its eligibility check. In a synthetic two-file SSA-like domain:

- 512/512 paired authorized edits produced identical source bytes.
- 512/512 original AST dead-definition edits were accepted.
- 512/512 fair AST dead-definition edits were rejected.
- 128 isolated CPython subprocesses produced 2,816 checked function outputs.
- An independent read-only auditor completed 5,120 raw-record checks with zero disagreements.
- 12/12 regression/adversarial tests passed, including clean-extraction replay.

The independent auditor validates the recorded fields and SHA formats, not every reconstructed source edit. The executable tests and CPython oracle supply complementary evidence. The scope is intentionally restricted; dynamic Python requires UNKNOWN.

The complete original local 12-entry archive (11 SHA-256-verified payloads and manifest) has SHA-256 `619a9b57abdca7d51d4ae6d2c903b2c07c39ddd1d5a50050edc073bf8804892e`. It includes original code, tests, raw observations, audit, independent protocol and reproducibility instructions. A small [executable GitHub witness](authority_asymmetry_witness.py) is mirrored; the full ZIP is retained in the run's local artifact, not GitHub.

## Real issue-first screening

[Requests #7456](https://github.com/psf/requests/issues/7456) was frozen before reference inspection at v2.34.0 commit `0b401c76b6e80a4eecf3c690085b2553f6e261ca`, with six exact Git blob SHAs, 3 targets, 4 heldout and 7 controls in [prospective protocol](PROSPECTIVE_REQUESTS_7456.md), commit `52ad09309b8e2e21132c0994a5f65064480f65ca`.

**NOT QUALIFIED (pre-screen):** The issue text itself points to `models.py` as the defect locus. No independent two-production-source behavioral necessity is established. The frozen oracle has not been executed, and no historical reference or source-ablation outcome is claimed. No retuning or promotion.

## Model inference launched, not yet evaluated

A new [pinned Qwen2.5-Coder-7B Q4_K_M workflow](../../../../.github/workflows/k-synth-run403-paired-qwen.yml) was committed at `bbc287d58be3911bd9ff7c15a646f1f84435b328`. It freezes two synthetic tasks and four paired prompts with identical task facts, source, source hashes and edit authority, and distinct semantic-definition versus AST-index action schemas. It records original raw model completions, model SHA, seeds, token usage, parse-only checks, failures and artifact manifests. It does not execute untrusted model code. **No original model artifact has yet been recovered; no model success or failure is claimed.** The parse-only checker is not a production atomic compiler or functional oracle.

## Next

Recover and independently audit original model outputs. Advance real issue-first two-source repair qualification, production-safe atomic compiler, independent isolated functional oracle and adequately powered repository-aware paired inference. All 89 reserved boundary issues remain sealed. [PR #9](https://github.com/sushxnthd/lattice/pull/9) remains open/draft/unmerged.
