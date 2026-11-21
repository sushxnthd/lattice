# Research Activity

Updated: 2026-11-21 UTC

- Active research branch: `research/exp003-context-order`
- Draft PR: #9 (verified OPEN/DRAFT/UNMERGED on 2026-11-21).
- Latest durable research commit: `9dc1cef802998a21009cf28379de0a29581fc634`.
- Evidence: Run787 committed a bounded ZIP/RECORD wheel-integrity checker. Seven local Python 3.13 adversarial tests passed; a newly rehashed tampered wheel with stale RECORD is refused. Source SHA verified in local archive.
- Local archive SHA-256: `7b2915739bdaf7114525227150d26fc49f69c84057a9f5782d549fdc73abd846`.
- Limits: checker not integrated into release CI; no authenticated external approval, public alpha tag, new qualified production repair, or model inference. Qualified real repairs remain TWO; semantic-IR superiority unestablished. All 89 reserved boundary issues remain sealed.
- Experimental code/results remain on research branch. Ledger is an activity checkpoint, not release approval.

## Prior checkpoint (2026-11-20 UTC)

# Research Activity

Updated: 2026-11-20 UTC

- Active research branch: `research/exp003-context-order`
- Draft PR: #9 (last confirmed OPEN/DRAFT/UNMERGED on 2026-11-20).
- Latest durable research commit: `b801c2f2e0fd3635103dd0fa4b58ed31cc338b1a`.
- Evidence: Run763 found a reproducible packaging-integrity counterexample. The Run762 static wheel auditor accepted a ZIP-CRC-valid wheel with altered compiler.py despite mismatched wheel RECORD hash and size. A conservative RECORD-aware prototype accepted the clean wheel and refused the tampered wheel. Report persisted on research branch; full archive not mirrored.
- Local archive SHA-256: `e77286349f848ee5c2ea1ce89f1ce2b0eb2789a6918e5cdbbc480e04f8d0ac9f`.
- Limits: No production repair qualification or model inference; independently qualified real repairs remain TWO. No semantic-IR superiority claim. All 89 reserved boundary issues remain sealed. Experimental verifier is not validated for release.
- Experimental code/results remain on research branch. Ledger is an activity checkpoint, not validation or release approval.
