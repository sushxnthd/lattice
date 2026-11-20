# Research Activity

Updated: 2026-11-20 UTC

- Active research branch: `research/exp003-context-order`
- Draft PR: #9 (last confirmed OPEN/DRAFT/UNMERGED on 2026-11-20).
- Latest durable research commit: `b801c2f2e0fd3635103dd0fa4b58ed31cc338b1a`.
- Evidence: Run763 found a reproducible packaging-integrity counterexample. The Run762 static wheel auditor accepted a ZIP-CRC-valid wheel with altered compiler.py despite mismatched wheel RECORD hash and size. A conservative RECORD-aware prototype accepted the clean wheel and refused the tampered wheel. Report persisted on research branch; full archive not mirrored.
- Local archive SHA-256: `e77286349f848ee5c2ea1ce89f1ce2b0eb2789a6918e5cdbbc480e04f8d0ac9f`.
- Limits: No production repair qualification or model inference; independently qualified real repairs remain TWO. No semantic-IR superiority claim. All 89 reserved boundary issues remain sealed. Experimental verifier is not validated for release.
- Experimental code/results remain on research branch. Ledger is an activity checkpoint, not validation or release approval.
