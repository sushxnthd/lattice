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

## Oracle infrastructure failure and recovery
The original workflow failed before oracle execution with `fatal: invalid reference: 8b6b36f57e139755356074908abbcb0b07732d6d`: the reference commit had not been fetched into the baseline checkout. The nine-case oracle is therefore **not qualified by Run324**. Prospectively committed independent recovery workflow `.github/workflows/lattice-k-synth-1-run325-oracle.yml` at `a143ee42a1b44dda98fe6b2d125f5cdfaae85da5`; it fetches both pinned upstream commits, SHA-checks original production files and runs the unchanged oracle inside networkless isolated containers. **Outcome pending independent artifact recovery.**

## Claim boundary
This is a genuine **negative feasibility result for two original completed model transactions**, not evidence of semantic-IR inferiority/superiority. One real issue, post-repair PR-description wording, unequal prompt lengths, noisy candidate localization, limited action grammar and unqualified original oracle preclude causal or powered claims. Six historical independently qualified repairs remain six. No new qualified issue, no breakthrough. Full historical GitHub artifact mirroring remains incomplete.

Local SHA-verified Run325 reproducibility archive: `lattice_run325_original_real_model_negative_and_oracle_recovery.zip`, SHA-256 `92cbde07e545b935f38572ca8d842bd106e621ded978cb8af2f5a4c4216451db`. Contains original cloud ZIP, independent auditor, raw forensic results, lexical filter, independent jq checks and next protocol.
