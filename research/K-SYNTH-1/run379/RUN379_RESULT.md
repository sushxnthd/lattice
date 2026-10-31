# K-SYNTH-1 Run379: prospectively reusable AST-span editor and independent stress audit

Date: 2026-10-31 UTC. One K-SYNTH-1 kernel, same branch and sole draft PR #9. All 89 reserved boundary issues SEALED.

## Non-retroactivity
Run377's original frozen primary results remain **IR 0/1 and Python/AST-action 0/1 valid repairs**; both genuine Qwen completions were rejected by the then-frozen globally unique substring compiler. Run378's retrospective contextual applications passed 12/12 public+heldout checks in both arms, but cannot be promoted to primary successes. Run379 performed **no new model inference**.

## New shared editor
Implemented a transactionally atomic, syntax-scoped AST-statement editor with the same edit authority for both arms. It requires authorized path, exact source SHA-256, class.method, exception-handler type/name, an exact single-line AST statement, and valid replacement. It rejects stale source, unauthorized paths, duplicate paths, ambiguous handler/statement selectors, nonisolated lines and malformed candidate syntax. Candidate Python is parsed and bytecode-compiled, never executed on the host. The selector certifies unique syntactic location only, **not runtime semantic soundness**.

The original HTTPcore baseline files were independently reconstructed from the Run378 post-hoc stage by reversing only the model's proposed change. Their original Git blob SHA-1 values exactly match the Run377 freeze: async `e6c4ef66312d4d6f31fcbfc417905ae329ef5885`; sync `53536d05e8c3d127b466e44dcf20e9f028aadab0`. Pinned upstream base `5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e`.

## Raw stress evidence
A deterministic 2,400-transaction two-file stress study (seed 3792026) accepted **600/600** valid shifted-source transactions, generating 1,200 syntactically valid changed files. It rejected **1,800/1,800** invalid cases: 300 each for duplicate statements, duplicate handlers, stale hashes, incorrect handler bindings, invalid replacement syntax, and duplicate paths. An independent auditor, not importing the editor, reconstructed all **1,200** accepted output hashes and found **zero mismatches**. Eighteen unit/adversarial tests passed, including 1,000 additional seeded cases, nested-handler scoping, rollback, shifted line numbers and an unrelated schema-only positive control.

These are **syntactic compiler tests, not 2,400 coding-model outputs or 1,200 functional repair outcomes**.

## Frozen exploratory paired pilot
Four requests were frozen for Qwen2.5-Coder-7B-Instruct Q4_K_M (model SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`): semantic/control-flow IR vs ordinary Python/AST facts under two prompt-order reformulations A/B, common original source excerpts, same canonical facts, atomic compiler, authorization and 1,500-token output ceiling. Full request/prompt hashes are in the local reproducibility archive. Python/AST presentation is 155 characters longer; exact model-token counts remain unmeasured. The issue is not investigator-blind, because the reference fix was already known; this is exploratory only.

Historical cohort remains 10 qualified PRs. No new model inference, independent issue qualification, powered IR advantage or breakthrough. Next: run SHA-frozen paired inference and independently isolated functional evaluation, then recruit genuinely unseen, cross-file-interacting production issues for a cluster-valid powered study.

Complete local archive: `lattice_run379_prospective_atomic_ast_span_editor_and_independent_audit.zip`, SHA-256 `8e9ff5d86a7796dffc2da8781f20070bfad42ca63594a1a379dd59d85abbc465`, 22 SHA-verified payloads.

## Run380 cloud execution launched

The new four-request Qwen workflow was committed at `6f5b1fb812daedc158cbd75d19bb90fbdcf6f4c1` and automatically launched as [GitHub Actions run 41159715407](https://github.com/sushxnthd/lattice/actions/runs/41159715407). The exact frozen source/prompt hashes and unrelated schema-only positive control passed the original cloud preflight. At last verification, the SHA-pinned model build/download was still in progress. **No new model completions or functional results are claimed yet.** All original failure traces and the historical primary scores remain unchanged.
