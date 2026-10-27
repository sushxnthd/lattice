# K-SYNTH-1 Run286: scoped count IR and Python/AST information control

2026-10-27 IST. One K-SYNTH-1 kernel. All 89 reserved boundary issues SEALED.

## Original Run285 recovery
GitHub Actions [40460886503](https://github.com/sushxnthd/lattice/actions/runs/40460886503), job 122044938234, was still QUEUED on independent connector inspection, with zero artifacts. Therefore **zero original upstream public-API observations** have been recovered from the frozen 4x30 multi-idle experiment. Do not report abstract preflight as an upstream holdout pass. Original Run285 local archive SHA256: `a423e4119b6219d47781627d771eb7a91b0294d076f3867ce4713f963e7ed934`; 21/21 original manifest payloads verified. Frozen spec SHA256: `811e33423dc734ab5d0fbe72de4e9c5277b68bed86315b9e7373c01b157be571`.

## New scientific artifact
Built an independent, gold-blind AST count-family extractor with three kinds: `COUNT_ALL_EVAL_PRED`, `SUM_PRED_VALUES`, `COUNT_TRUE_FILTER`. It renders the same canonical task facts as a semantic IR and an ordinary Python expression/AST view. Both recover the same source facts (iterable, binding, predicate, source span, expression); Python AST text is deterministically derivable from the shared expression. This establishes information-equivalence **only for the bounded extraction subset**, not comparable model performance.

Conditional theorem: for a stable finite iterable of size n, pure exact-Boolean predicate with i true elements and integer threshold k, count-all and true-count guards disagree exactly when `i <= k < n`. Requires explicit trusted attestations for stable finite iteration, pure exact-Boolean predicate, no concurrent mutation, runtime binding and integer threshold. Otherwise return UNKNOWN. Non-Boolean and mutation counterexamples invalidate unconditional claims.

Independent CPython diagnostic: 12,000 deterministic cases, 2,568 predicted/observed guard disagreements, zero mismatches; 9/9 local tests pass. The pinned HTTPcore PR1000 baseline sync/async files were independently inspected through GitHub and contain the expected count-all expression. Local executable fixture is a structurally matching excerpt, **not** a full byte-exact upstream oracle.

No model inference, model patch, powered IR advantage, or breakthrough this run. Qualified cohort remains four distinct real issues (Flask, urllib3, Werkzeug, HTTPcore); Run285 is a holdout on HTTPcore, not a new issue. Historical GitHub artifact mirroring remains incomplete.

## Next
Recover and SHA-audit all 120 original Run285 observations; preserve freeze, censoring and failures. Build identical-facts/authority semantic-IR and ordinary-Python/AST capable-model paired pilot using strict shared atomic compiler and isolated network-disabled oracle. Prospectively qualify unrelated real multi-production-source issues. Keep one open/draft/unmerged PR #9 and all 89 reserved boundary issues SEALED.
