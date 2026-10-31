# K-SYNTH-1 Run385: complete finite counterfactual ANF certificate

Date: 2026-10-31 UTC. Branch: research/exp003-context-order. PR #9 remains open/draft/unmerged. All 89 reserved issues SEALED.

## Finding

Run384's 4x4 input-indexed influence matrix is not a complete semantic description. Two admitted programs can have identical influence support but different truth tables and pairwise interactions. Run385 implements a four-row, 16-coefficient algebraic normal form (ANF) certificate, complete for the finite producer-intervention semantics. Unsupported/nonterminating programs return UNKNOWN.

The original frozen Run374 (1,100 programs) and Run384 (768 programs) corpora were reused unchanged, with source SHA-256 checks. Across 1,868 programs, 1,307 were admitted total and 561 returned UNKNOWN. An independent auditor recompiled and re-executed all admitted synthetic sources in fresh CPython, using an AST-whitelisted grammar, removed imports and empty builtins. All 83,648 observations, 20,912 support entries, and 31,368 pairwise interaction entries agreed, with zero mismatches. The auditor reconstructed ANF using a separate exhaustive proper-subset recurrence rather than the implementation's fast Moebius transform.

There were 41 distinct support patterns; 26 patterns contained multiple ANF behaviors, representing 100 distinct ANF certificates within colliding buckets. 68 admitted programs exhibited pairwise interaction (115 positive pairwise entries), but no frozen program had an ANF monomial of degree three or four.

Five separately labeled adversarial cases underwent 320 additional fresh CPython observations. Guarded AND and XOR have identical 4x4 influence matrices but different ANF and second-order interactions. Constructed examples demonstrate degree-three and degree-four interaction. Eight tests passed, including exhaustive ANF roundtrips for all 65,536 Boolean functions of four variables and 4,000 seeded derivative checks.

## Scope

This is a complete finite-domain Boolean semantic certificate, NOT a general Python dataflow engine. The production-repair cohort remains ten historically qualified PRs. Run380's real Qwen comparison remains IR 2/2 and Python/AST 2/2 on the same issue with identical completions. No new coding-model inference, powered superiority evidence, or breakthrough.

Issue-only pre-reference triage inspected HTTPX #1833/#318, AnyIO #1081 and Requests #1189; none was promoted to qualified repair. Next priority: genuinely unseen coupled multi-source bug with prospective oracle and matched model evaluation.

The full SHA-verified executable evidence archive, including the 1,868 program records and raw independent audit, is preserved locally. Historical GitHub ZIP mirroring remains incomplete. All 89 reserved issues untouched.
