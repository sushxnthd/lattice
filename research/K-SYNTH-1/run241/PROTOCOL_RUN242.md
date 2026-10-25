# Prospective Run242 protocol — design freeze (no inference yet)

Date: 2026-10-25. Run240/Run241 are discovery data; their outputs cannot count as a prospective experiment.

**Question:** Does removing model responsibility for copying hashes and paths reduce malformed edits, and is any residual effect attributable to source presentation rather than edit authority or compiler differences?

**Paired arms:** Semantic-IR source view versus ordinary-Python source view with identical source bytes, immutable facts, editable selectors, read-only context, open coding model, seed policy, inference budget, JSON schema `{selector, content}`, trusted compiler and independent issue-specific functional evaluator. The compiler derives path and file hash from the frozen snapshot. Gold patches are excluded from model prompts.

**Separate ordinary-Python baseline:** Permit the model to return actual Python replacement source, not the same JSON action language; normalize it through a deterministic adapter to the same trusted transactional compiler. Report this baseline separately, with full prompt-token differences and unchanged edit authority.

**Primary endpoint:** Complete functional repair: all independent issue-specific checks pass, declarations/decorators preserved, transaction valid and Git patch applies. **Secondary:** Schema acceptance, unauthorized-selector rate, declaration deletion, invalid intermediate states, semantic churn, token counts, repair loops and runtime. An unqualified task must be rejected *before* inference; post-hoc fixes never count as model successes.

**Prediction P1 (already observed, not held out):** Trusted metadata derivation alone cannot repair either Run240 completion; both erase a target method at action 0.

**Prediction P2 (prospective, by construction):** Stale-hash errors must be zero with the trusted metadata-free action schema. Authority and declaration failures remain observable. No advance claim of improved functional accuracy.

**Power:** Exact two-sided paired McNemar alpha .05; 30% discordance assumed. For conditional IR wins among discordant pairs of .65, 306 independent pairs reach ~80% power (258 give ~72%). At .60, ~681 independent pairs are needed, before repository clustering. Re-estimate design effect from independent repository groups, without inspecting held-out boundary outcomes.

**Boundary:** Keep 89 reserved issues sealed until mechanism and unseen-condition prediction are frozen. If Python matches or beats IR in two carefully controlled reformulations, pivot toward trusted semantic transactions and publish a rigorous negative result rather than cosmetic syntax revisions.
