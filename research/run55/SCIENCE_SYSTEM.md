# Run 55 — independent frame-oracle discriminator

## SCIENCE
Active question: Does semantic IR reduce repair complexity beyond ordinary Python using identical verifier/compiler? Status UNTESTED on capable-model, information-matched, multi-turn repository repair. Earlier six-domain structured-topology control was positive (neutral 60/72 versus prose 19/72 on untouched holdout), but all six holdout programs were imperfect and it does not isolate IR over Python plus the same compiler.

### Common-mode evaluator risk
The bounded lowering audit compares emitted Python with `after.run`, which uses the production frame interpreter. This independently interprets the emitted Python AST, but it is **not** independent of the framed-program semantics. If frame evaluation and lowering share a version-binding mistake, both can agree and report no mismatch. Protected-output checks likewise compare production `before.run` with `after.run`.

Hypothesis: an independent interpreter of the immutable versioned rule graph can reveal common-mode frame/lowering errors that the existing audit misses.

Mechanistic prediction: fault injection that changes both the production interpreter and lowering in the same way should evade the current audit but be detected by an independent bound-graph oracle.

Observed: static source audit confirms shared production frame semantics in the current lowering check; no runtime fault-injection result yet. This is a CAPABILITY-BUILDING discriminator, not a representation gain.

Alternative: the finite Boolean interpreter and lowering are already correct; independent evaluation adds defense in depth rather than changing measured outcomes.

Uncertainty: no independent bound-graph oracle executed yet. Cheapest discriminator: implement AST-only bound-rule evaluation without calling `FramedProgram.run` or `semantic_edits.evaluate`, and mutate the production interpreter/lowering consistently in a test fixture.

## SYSTEM
Needed: a shared verifier usable by **both** ordinary Python and semantic-IR experiment arms. The current exact finite-domain frame/lowering audit provides useful baseline machinery but is not a complete independent oracle of intended behavior. Keep authority and target intent outside model-generated output.

## Decision
No breakthrough or IR-specific causal effect established. Do not count CI success as model-repair evidence. Preserve frozen tasks and artifacts; never reuse an opened holdout as fresh.
