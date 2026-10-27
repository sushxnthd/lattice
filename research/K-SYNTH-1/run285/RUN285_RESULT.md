# K-SYNTH-1 Run285: multi-idle temporal transfer and frozen public-API holdout

Date: 2026-10-27 IST. Canonical branch `research/exp003-context-order`, PR #9 remains draft/unmerged.

## Scientific result

For an explicitly attested finite HTTPcore-like pool with m initially idle distinct-origin connections, 0 <= m <= k keepalive limit, q distinct-origin new active requests, no expiry/reuse/closed connections, no concurrent mutation, unbounded connection capacity, pure exact-Boolean is_idle, stable source/bindings and cleanup-before-create ordering:

- Original length-of-Boolean-comprehension guard retains m idle if q=0; otherwise **min(m,max(0,k-q+1))**.
- Corrected Boolean-sum guard retains **m**.
- The original first loses an idle at q*=k-m+2 when m>0.
- Counterfactual cleanup-after-create moves the threshold to q*=k-m+1.

These are conditional mathematical results, not general Python soundness. The verifier returns UNKNOWN if any required runtime assumption is unverified. Non-Boolean predicates and side effects provide constructive out-of-scope counterexamples.

An independently implemented operational CPython list-mutation interpreter agreed with the closed-form certificate on **42,900 configurations, zero mismatches**, including **2,600 event-order-sensitive parameter settings** and **600 first-loss witnesses**. **12 local tests passed.** The independent operational abstract replay matched **120/120 preregistered abstract expectations**, which is **NOT an HTTPcore public-API functional result**.

The exact frozen real-repository 30-case x 4-source-arm protocol is committed separately as `FROZEN_RUN285_COMMITMENT.md`. The upstream oracle has **not yet executed**. The local SHA-verified archive preserves complete executable runner, frozen JSON, tests, traces, transport and workflow. Full GitHub executable mirroring is still incomplete and must be retried.

Four independent real issues remain qualified: Flask PR6096, urllib3 PR5071, Werkzeug PR3136 and HTTPcore PR1000. No new model-generated repair, powered semantic-IR-versus-Python advantage, or breakthrough is claimed. All 89 reserved boundary issues SEALED.
