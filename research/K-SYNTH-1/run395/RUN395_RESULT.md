# K-SYNTH-1 Run395: fail-closed behavioral-necessity gate

Date: 2026-10-31 UTC / 2026-11-01 IST. All 89 reserved boundary issues remain sealed. No model inference, powered advantage or new real production repair is claimed.

## Original Run394 replay
The original Run394 archive (SHA-256 c0920b6acc9a29209841c05d276f7edc3667a1dfb9792ae700c610ec65346c84) was read without changing its frozen scores. The original corrected Actions ZIP SHA-256 8ff633a4f8ef03f6e6162015a4e064392aa478953ed0676d2720fe28c906c16e and separately labeled post-hoc shim ZIP SHA-256 436e282727dd21e89c59c3e6eb3d31947deba1d6565b872f68bfa8545bb0347f were independently manifest-verified.

The new gate returns REJECT because frozen nonregression controls C5_parametrized and C6_private_nonautouse already fail at baseline. The fixtures.py-only import failure is an ABORT, not a behavioral test failure. The separate post-hoc import shim still passes 12/12. Run394 remains a literal original-checklist pass but is NOT promoted to the primary semantic-coupling cohort.

## New CPython experiment
A fixed trusted generator created 192 seeded two-module synthetic scenarios, 64 each of (1) genuine two-module behavioral contribution, (2) mechanical import dependency, and (3) behavioral effect outside the frozen finite oracle. Six source combinations per scenario yielded 1,152 fresh CPython -I -S subprocesses and 5,760 frozen-case statuses. Raw source text, SHA-256 hashes, outputs, import failures and classifications were preserved. An independent auditor, importing neither the generator nor gate, completed 13,760 checks with zero discrepancies. Fourteen adversarial/regression tests passed, including a mutated raw-output rejection.

Gate decisions: 64/64 behavioral scenarios ELIGIBLE_BOUNDED; 64/64 mechanical-import scenarios REJECT; 64/64 out-of-domain scenarios REJECT. In the last group, a predeclared x=99 probe reveals an actual effect absent from frozen x={1,2,3}. This demonstrates the gate's honest observational scope, not universal semantic equivalence.

## Gate and limits
Frozen case IDs must be disjoint; baseline controls must all pass; at least one baseline target must fail; full reference must pass every frozen case; and both documented neutral-shim ablations must execute, preserve controls and each fail a target. Missing or unverified shim evidence returns UNKNOWN, not a fabricated success. Shim neutrality itself requires external scoped validation and cannot be established by a boolean declaration.

This is a qualification-methodology result using synthetic programs, NOT new real-repository paired-model evidence. Full executable scripts, original artifacts and raw traces are in the SHA-verified local Run395 reproducibility archive. Next: unseen issue-first real multi-source qualification, then genuinely matched semantic/dataflow IR versus Python/AST functional model evaluation.