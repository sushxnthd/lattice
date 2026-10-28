# K-SYNTH-1 Run310 prospective freeze (before oracle execution)

**Canonical branch:** `research/exp003-context-order`; **one draft PR:** #9. All 89 boundary issues remain sealed.

## Primary bounded question
Does the original Run309 module-binding transfer produce definite-negative false exclusions when a Python 3.13 function annotation executes an `ast.NamedExpr` rebinding `len` to the saved builtin? This is **source-analysis correctness**, not model-repair or representation-superiority evidence.

## Exact frozen inputs
- Manifest file: `RUN310_FROZEN_SOURCES.json`, SHA-256 `6a98891ae449dbe98ed2a048c0d1f8a98b05384159207ba7c905635dc2498726`, 152529 bytes.
- 384 trusted generated source programs, 16 distinct templates × 24 correlated variants.
- Generator SHA-256 `fba68c7ebf6235595289397d45dc646c1d34cb73a5b3fceac92e044ea1129e80`.
- Corrected transfer source SHA-256 `ba7db6d2f0044000fda1a4b7904889f7b6b093ddc80a2aab16420e5b5f9125ba`.
- Original comparator is unmodified `run309_binding_transfer.py` from the Run309 original archive.
- Runtime scope: trusted CPython 3.13 with eager annotations, unmodified builtins, no import hooks, no model-generated code.

## Frozen outcomes and endpoints
- Expected builtin-restoration classes: pos_arg, return, posonly, kwonly, vararg, kwarg, async, fstring, tuple, dict (10 templates).
- Expected nonbuiltin controls: false_if, false_and, lambda_local, nonbuiltin, literal, alias_only (6 templates).
- Primary endpoint: count of definite-negative exclusions when independent CPython execution observes `len is saved_len`, old versus corrected.
- Secondary: number of UNKNOWN classifications on negative controls; source SHA consistency; independent replay discrepancies.
- No post-outcome task exclusions, no retroactive endpoint changes. Any parse/runtime error remains recorded as a failure.
- Each of 384 cases is a correlated variant, **not** an independent repository repair.
- If corrected analyzer still has false negatives, retain them and label the correction failed. Never infer general Python soundness.

## Other Run310 objectives
Independently screen wsproto PR #6 (merge commit `99aeafa3f188d5fb4563d4e9543e8cd8892a793d`, first parent `7314c8428a2d02625828e5a705529b2e2fe1ac21`, second parent `97b9e99d43a727ec6d2d80230a84067965f14f89`) for two-production-file repair qualification, without promoting it unless frozen public/heldout/nonregression and component-necessity oracles all pass. Do not claim new capable-model inference without genuine raw outputs.
