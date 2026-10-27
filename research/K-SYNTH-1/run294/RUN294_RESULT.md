# K-SYNTH-1 Run294: Frozen shared edit compiler and information-equivalent control

## Prospective chronology and original artifacts

- Before any Run294 execution, committed `RUN294_PROSPECTIVE_FREEZE.json` to the canonical branch at GitHub commit `28d4907b5d8e7041805e64868fc53065dfa2195d`, Git blob `697c5050d49c2fd39ae312133dc95de714727ccae`, SHA-256 `c2419743aae0f35c4952487c3020640bb0218c3f1a38b705bcdb8d65172d7e2f`.
- The freeze pins compiler SHA-256 `8801e6da5c9bf37c353d8378bb334b0aeb53e104239d71bdd53a60bf7df50df3`, 24 adversarial scenarios, expected accept/reject codes, both representations, random seed 294001 and 1,024 valid paired trials. The compiler source committed to GitHub at `b1805819ac2d5339e7bb299868d5225df9f7e0b6` has independently matched Git blob `6cc795c59be03d39ae312133dc95de714727ccae`.
- Executed the **original frozen compiler**, without postfreeze changes. All **48/48** scenario/representation outcomes matched the frozen predictions, including cross-file success, stale-file rejection, span mismatch, overlapping edits, path traversal, symlinks, malformed JSON, invalid syntax, split UTF-8, and ambiguous insertions. All 48 input snapshots were unchanged.
- The **1,024/1,024** seeded valid paired edit transactions normalized to identical canonical SHA-256 and produced identical staged file SHA-256 in both representations. These are correlated synthetic transactions, **not** 1,024 independent repairs or model completions.
- A separately implemented read-only auditor, importing neither the compiler nor the experiment runner, checked the complete 48-row adversarial and 1,024-row parity traces, with zero discrepancies.

## Compiler contract

Both `SEMANTIC_IR` and `PYTHON_AST_ACTIONS` are strictly parsed into the same canonical sequence of SHA-pinned UTF-8 Python byte-span replacements. All edits are validated before a complete isolated candidate snapshot is exposed. The input repository is never edited. Unsupported operations are rejected; runtime binding remains `UNKNOWN`. No candidate Python code is executed by the compiler. The compiler checks AST syntax only, not functional correctness or safety.

**Deterministic parity proposition.** For fixed immutable input snapshot S, equal canonical transactions T and deterministic compiler C, both representations yield the same staged file bytes, rejection code or canonical transaction hash, provided the same bounded filesystem and execution assumptions hold. Proof: the representation-specific parser produces T in both cases; all subsequent validation and byte replacements are functions only of (S,T). The 1,024 paired checks are a finite implementation test of this proposition, not a proof of model-level performance.

**Critical limitation:** This run establishes shared **edit-action** parity, not genuine soundness-scoped semantic/dataflow IR superiority. A future model comparison must add independently verified semantic facts, keep task facts/source/edit authority identical, and run a genuinely capable open model on qualified real issues. The source snapshot is assumed not to undergo concurrent hostile mutation. The returned stage is a validated complete snapshot, not a crash-atomic multi-file commit or a sandbox for executing untrusted model code.

## Research status

Four independently qualified real multi-production-source issues remain: Flask PR6096, urllib3 PR5071, Werkzeug PR3136, HTTPcore PR1000. No fifth qualified issue, no new model inference, no model-generated repair, no adequately powered IR-versus-Python evidence, and no breakthrough. The 89 reserved boundary issues remain SEALED. Historical GitHub ZIP mirroring remains incomplete. PR #9 must remain open, draft and unmerged on `research/exp003-context-order`.

Next: use this exact shared compiler/verifier in a blinded paired capable-model pilot on the four real qualified issues, then independently qualify new multi-production-source issues with prospective target-plus-control necessity. Preserve raw prompts, checkpoint SHA, seeds, completions, failures, and isolated oracle traces; no untrusted model code on host.
