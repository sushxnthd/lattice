# K-SYNTH-1 Run325: genuine paired-model negative feasibility and independent artifact audit

Date 2026-10-28 UTC / 2026-10-29 IST. One K-SYNTH-1 kernel; canonical branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9, all 89 reserved issues sealed.

## Original cloud artifact, no posthoc replacement
Original GitHub Actions run [40761695337](https://github.com/sushxnthd/lattice/actions/runs/40761695337) completed at job level, but its compile and oracle steps were configured continue-on-error. Original artifact ID **12848123696**, ZIP SHA-256 **44d70baa072432a15747a03e9aa8bf8bb68d830b8e28145181d71ca31f2c8a68**. Independently verified all **17/17** SHA-256 manifest entries, frozen requests and prompt hashes. Original raw IR response SHA-256 `2eeafaa084109416ff7f3efa52d01e928b26996ceaaf4fff9000f5d49827efe4`; original Python AST response SHA-256 `7e2ec27ee11d55fcf29fe0bbf6ecf796febd4801ab94cc9fb16e7823ea43eefa`.

Two **genuine Qwen2.5-Coder-7B Q4_K_M completions** finished with `finish_reason=stop`: IR 2551 prompt + 377 completion tokens; Python AST 2785 prompt + 441 completion tokens. These are not precompletion failures or abstentions. Preflight token counts were 2522 versus 2756, so prompt length is a confound.

## Strict primary result
Both original responses emitted malformed JSON at the same `port == """` expression. The frozen compiler rejected IR at JSON offset **803** and Python AST at offset **990**. Independent `jq` parsing also rejected both. **Accepted model transactions: IR 0/1; Python AST 0/1.** No model patch was staged and no functional model success is claimed.

Read-only post-outcome forensics recovered 12 IR and 14 Python AST complete JSON action objects preceding the error. An explicitly **counterfactual, non-accepted** escaping diagnostic could parse 15 IR and 17 Python AST actions. Both contained an unknown candidate ID `C63feb4ad28b` (correct frozen ID `Ca63feb4ad28b`); Python AST also violated the 15-edit limit. Of the correctly identified actions, IR changed one unrelated response-condition test to `not SSLTransport`; Python AST changed none. **Never treat these diagnostics as model repairs.**

## Real-source localization defect
The frozen discoverer used `'port' in expr`. Among the 17 actual urllib3 source candidates, **6** were substring-only false positives under an AST identifier-segment criterion (e.g. `supports_http2`, `supports_chunked_reads`, `SSLTransport`). An independent read-only lexical filter retained 11 and rejected 6; 14 adversarial lexical controls passed. This is posthoc **lexical** precision, not semantic/dataflow soundness, and does not change the original prompts.

## Independent isolated oracle recovery, preserving all failures
The original Run324 oracle step failed before Docker execution because reference commit `8b6b36f57e139755356074908abbcb0b07732d6d` was not fetched. This failure is preserved. First recovery [Actions 40770900170](https://github.com/sushxnthd/lattice/actions/runs/40770900170) fetched exact pinned commits and SHA-checked four production files but failed importing missing generated `urllib3._version`; original failed ZIP SHA256 `2a2d0e117a4c730772802d405fd588cdafeb61ce9c9c438e43f88fc5e09b29b5`. Second recovery [Actions 40771424828](https://github.com/sushxnthd/lattice/actions/runs/40771424828) preserved a generated-version bootstrap quoting SyntaxError; original failed ZIP SHA256 `ac306080fc04c30c768a28a0e71de3ff6095c56dbbbcdefd64b66bdb8cdca92f`.

Separately frozen third recovery [Actions 40771462288](https://github.com/sushxnthd/lattice/actions/runs/40771462288) **SUCCESS**. Original artifact ID `12852142958`, ZIP SHA256 `7441799556fda4fd2af1f1622ec021427fecdb4305bc62ee141bcbab6c7c20ec`. All **8/8** manifest entries and **18** frozen functional row outcomes were independently verified with zero discrepancies. Identical generated-version shims (SHA256 `2f9efacd8fb2d8218fb4cfecb699da08d6c455c77c73f974d470090dc2a4b5b2`) were used in separate copies of the pinned base/reference, without changing original source. Both ran in isolated networkless read-only capability-dropped containers.

**Original nine-case oracle now independently qualified in a separate postfreeze experiment:** pinned baseline **1/3 targets, 6/6 controls**; pinned reference **3/3 targets, 6/6 controls**. This does **not** turn either original malformed model completion into a repair, nor make Run324's failed oracle step retroactively successful.

## Claim boundary
This is a genuine **negative feasibility result for two original completed model transactions**, not evidence of semantic-IR inferiority/superiority. One real issue, post-repair PR-description wording, unequal prompt lengths, noisy candidate localization, limited action grammar and unqualified original oracle preclude causal or powered claims. Only two independently qualified real production tasks are established by the original frozen qualification record (Flask PR6096 and urllib3 PR5071); historical repair variants are not additional independent tasks. No new qualified issue, no breakthrough. Full historical GitHub artifact mirroring remains incomplete.

Local SHA-verified Run325 reproducibility archive: `lattice_run325_original_real_model_negative_and_oracle_recovery.zip`, SHA-256 `a65494dadf73344f50f291a17b1dc641612ec11832e5cfcce8ebf94e34658d32`. Contains original cloud ZIP, all three preserved oracle-recovery artifacts (two failures and one success), independent auditors, raw forensic results, lexical filter, jq checks and next protocol.
