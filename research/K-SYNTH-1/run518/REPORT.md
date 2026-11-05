# Run518 — prospectively frozen two-source qualification gate

Date: 2026-11-05 UTC. Branch: research/exp003-context-order. PR #9 only. All 89 reserved issues sealed.

## New artifact
`run518_gate.py` is a stdlib-only executable qualification gate. It requires pinned 40-character base/reference SHAs, two distinct production paths, disjoint target/control sets, an oracle identifier and precommitted holdout digest. Its canonical JSON SHA-256 freezes the task specification. A 2x2 arm matrix is checked for completeness and boolean outcomes.

## Mechanism and falsification
Full reference must repair every frozen target and preserve every frozen control; base must fail targets and preserve controls. Both component removals must each fail at least one **target**, not merely regress a control. The latter is intentionally stronger than generic target-plus-control component necessity, and avoids mistaking the PR2535 control-only interaction for target-level joint necessity. This strict criterion is a chosen screening rule, not a mathematical requirement for all genuine multi-file repairs: it can reject valid fixes with a control-only component.

Four directed self-test assertions are included: accepted synthetic joint-target fixture, rejected control-only confound, rejected post-freeze spec mutation, rejected incomplete arm matrix. **Execution not verified in this run** because the local Python/container runtime returned infrastructure errors. No synthetic outputs are represented as observed measurements.

## Limitations
The gate cannot prove an oracle independent, verify GitHub source identities, execute isolated environments, establish production code soundness or guarantee pre-outcome registration from a file alone. A future real candidate needs external time-stamped freeze, SHA-verified source snapshots, independently executed oracle traces, adversarial review and raw artifact mirroring. Historical failed candidates must not be retroactively promoted. No new task qualified, no coding-model inference, no IR-vs-Python result.

## Next
Run the self-test on a trusted executor, obtain raw stdout and SHA manifest; then freeze and independently qualify a new real multi-source PR before running a blinded paired pilot.