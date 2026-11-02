# K-SYNTH-1 Run432 — conditional pure-int assignment commutation

## New theorem (soundness scoped)
For adjacent straight-line assignments `a=eA`, `b=eB`, if `a != b`, `a` is absent from the free names of `eB`, and `b` is absent from the free names of `eA`, swapping the assignments preserves the final local store and returned value, **provided** all inputs are exact built-in Python `int`, all expressions consist solely of integer literals, local names, unary +/-, and binary +/-/*, all reads are bound, and both executions terminate normally without resource exhaustion. No calls, attributes, subscripts, global effects, annotations, decorators, exceptions, control flow or arbitrary objects are admitted.

**Proof:** Both RHS expressions are pure and evaluate identically under either order, because neither reads the other target. Assigning those values to two distinct local names commutes. The return reads the same final store. This is a theorem about a restricted fragment, not arbitrary Python semantics.

## New executed results
- 512 deterministic constructed programs; 2,295 eligible adjacent swap positions; 512/512 paired IR and ordinary AST action transactions matched through the same validator/compiler and edit authority.
- 8,192 real CPython before/after comparisons, zero disagreements.
- An independent AST auditor executed 16,384 further CPython calls and checked 12,288 predicates, zero disagreements.
- Four functional counterexamples demonstrate the necessity of RAW, WAR, WAW guards and the exact-int precondition. A custom `__add__` object changes the side-effect trace from `[1,2]` to `[2,1]` after swapping otherwise lexically independent assignments.
- 14/14 regression/adversarial tests passed. Seed 432101. Raw JSONL SHA-256 `9629b4a1b408c797c1ebf46dad56f2e7a71f775ab7e75e043a02b86a37a76887`.
- Local clean-extraction ZIP SHA-256 `062e2d066d2b013eb94cd34e7deb9b139b2d8898697e83f0dd66caa0d1c07cd6`; 14 internal SHA-verified payloads.

## Qualification decision
**No new real repair qualified.** The two existing historical qualified tasks remain Flask PR6096 and urllib3 PR5071. No coding-model completions or powered IR superiority evidence. The typed MAY-graph remains descriptive and explicitly UNKNOWN outside this new tiny pure-int certificate. All 89 reserved boundary issues remain sealed. Historical failed candidates remain failed; raw GitHub artifact mirroring remains incomplete.

## Next
Run433: prospectively freeze a fresh independently specified multi-source public-repo repair, independently validate both target and nonregression behavior, and execute matched functional open-model inference with exact model/prompt SHA and raw traces. No untrusted generated code on host.
