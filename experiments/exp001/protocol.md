# Experiment 001 — executable intent vs passive context

## Question

Does typed, machine-checkable semantic state improve long-horizon coding-agent performance beyond equally informative passive memory and graph context?

## Frozen conditions

All conditions use the same model, starting repository, ordered change requests, visible tests, held-out tests, and approximate token/tool budget.

### A — Direct
Repository plus the current change request.

### B — Passive memory
A plus a complete structured project brief containing durable requirements and prior decisions.

### C — Graph context
B plus explicit architecture, API, and dependency-neighborhood context.

### D — Executable Lattice
C plus typed commitments, legal state transitions, permissions, protected dependencies, and executable invariants. Proposed changes are admitted only after deterministic preflight.

## Primary outcomes

- held-out requirement fidelity after repeated edits
- regression count
- visible-test versus held-out behavior gap
- permission/security violations
- illegal state transitions
- protected-dependency violations
- structural erosion and duplicated logic
- files/repository reads per change
- context/input/output tokens when observable
- repair iterations
- semantic-preflight true-positive and false-positive rejection rates

## Critical ablations

1. remove executable checking while preserving identical semantic content;
2. remove types but preserve content;
3. remove dependency-neighborhood retrieval;
4. remove invariants;
5. replace Lattice with an equally sized Markdown/JSON project brief;
6. equalize planning tokens across conditions.

## Interpretation

- D > C > B > A supports a distinct executable-semantics effect.
- C ~= D > B > A means graph context explains the improvement.
- B ~= C ~= D > A means persistent project state explains the improvement.
- A ~= B ~= C ~= D falsifies this representation hypothesis on the tested tasks.

No post-hoc task changes are permitted after the frozen evaluation begins.
