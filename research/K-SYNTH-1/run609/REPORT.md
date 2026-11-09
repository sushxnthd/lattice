# Run609: separate target necessity from control-only failure

Executed exhaustive 64 binary ablation outcomes for three frozen target checks and three frozen controls. The full-reference arm is assumed to pass all six checks; these are **synthetic configurations**, not observed production outcomes.

- 56/64 ablations lose at least one target pass, providing target-necessity evidence.
- 7/64 preserve all target passes but lose at least one control pass: joint target-plus-control qualification detects a regression, **not** target repair necessity.
- 1/64 preserves all six passes.
- Therefore the joint gate flags 63/64 but only 56/64 support target necessity. This corrects interpretation, not the gate's use as a quality safeguard.

Executed locally with Python, assertion passed. Reproducer and raw 64-row matrix are in local SHA-verified archive; repository contains equivalent executable below. No real task qualified, no model inference, no superiority claim. Two qualified independent repairs remain. Reserved 89 issues untouched.

Protocol change proposed: record `target_necessity`, `control_regression`, and `joint_quality_gate` as **separate preregistered fields**. Never infer mechanistic target necessity from the joint gate alone.
