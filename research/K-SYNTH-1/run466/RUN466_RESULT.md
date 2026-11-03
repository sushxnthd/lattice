# Run466: byte-preserving literal-span verifier

2026-11-03 UTC. This is a bounded structural result, not semantic correctness or IR superiority.

Run465's corrected AST verifier compares AST nodes but does not constrain lexical edits outside the target. In particular, changing a source encoding declaration or a trailing comment while changing the return literal can receive PASS_BOUNDED_AST_TARGET. This is a scope gap: AST structural equality is not byte-preservation.

Run466 introduces a verifier that compares UTF-8 byte prefixes and suffixes around the original and candidate return literal AST spans. Only the literal span may differ. It rejects comment, coding-header, whitespace, and suffix edits, while accepting Unicode literal replacement. The candidate is never executed. Ten deterministic tests passed locally. Exact executable source and raw test output are preserved in local SHA-manifested archive run466.zip. This is a strict *literal-span* guarantee, not a behavioral or side-effect guarantee. No model inference, new qualified repair, or IR comparison was performed. All 89 reserved issues remain sealed.
