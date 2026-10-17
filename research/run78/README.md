# Run 78: independent oracle CI gate

Date: 2026-10-17. Branch: build/run78-oracle-production-gate-20261017.

SCIENCE: The active question is whether semantic IR improves coding-model repair versus Python with the same compiler, verifier, scope, information, and token budget. Primary metric: paired hidden-test recovery at fixed cost. Alternative: gains come from verifier feedback or prompt differences. Falsification: no gain on unseen paired tasks. Publication requires replicated effect, uncertainty and prior-art audit. Product relevance requires fewer repairs with no protected-output regressions. Retire the kernel after three uninformative tests. No model experiment was run.

SYSTEM: Five independent oracle tests previously excluded from default collection now execute against the production framed compiler. Commit d2195c9. Actions 39037092808: 55 tests passed, compared with 50 previously. Claim limited to test collection and production execution.

BLOCKER: source-bound provenance implementation could not be committed. It remains a local prototype. Next: freeze and run the paired capable-model repair experiment. No user spend or laptop use.
