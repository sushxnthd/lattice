# Run100: Observable historical contracts, not representation advantage

## Exact result (post-hoc Run99 diagnostic)
Eight frozen historical memo predicates have identical current unversioned source after retargeting. A protected archive output evaluates old_memo(a,b) AND c. If the same compiler allows protected-output queries with c=true, exactly three nonadaptive probes at (a,b)=(0,0),(0,1),(1,0) identify which of the eight histories occurred. Two probes cannot identify eight binary hypotheses. With c restricted false, every protected archive observation is false, so the history is not identifiable from these probes even with unlimited queries. For the full class of 16 Boolean functions of two inputs, four probes are necessary and sufficient.

This does not show an advantage of semantic IR: versioned Python retains the same historical information. It shows that the Run99 static information bound is conditional on withholding protected-output queries.

## SCIENCE ledger
Active question: Does explicit versioned dependency/state graph reduce repair complexity for capable models versus information-equivalent versioned Python, with the same compiler/verifier and patch grammar?
Intervention: graph with captured version edges and commitments.
Strongest control: versioned lowered Python plus identical compiler, oracle query budget, semantic facts and edit authority.
Capable model: not executed. Intended Qwen2.5-Coder-7B-Instruct or stronger free model.
Prospective tasks: not frozen for model inference in this run. Run99 eight synthetic histories are reused only for post-hoc exact analysis.
Primary model endpoint: paired final hidden-test repair success, not measured.
Strongest alternative: the verifier and runtime queries alone resolve the ambiguity, independently of representation.
Decisive falsification: Python same-compiler achieves equal or better repair success on powered realistic tasks, including history-sensitive ones.
Unseen prediction: historical-version representation is most valuable when relevant protected outputs are unobservable under permitted queries; if accessible cheap probes identify history, its incremental benefit should weaken.
Publication threshold: powered prospective realistic tasks, capable models, independent sealed evaluator, mechanism ablation, uncertainty, prior-art audit, unseen boundary, reproduction.
System consequence: a finite-domain observability probe planner can quantify when historical contracts are recoverable from executable outputs; preserve immutable versions when they are not.

## SYSTEM ledger
A representation-neutral finite Boolean probe planner was locally implemented and tested (7 tests passed), with full raw 24-call witness transcripts. The planner takes permitted query positions and finite protected-output signatures and returns an exact minimum distinguishing set or an unidentifiable-history error. This is not a general-purpose Python equivalence verifier.

## Limitations and provenance
No model inference; no personal spend; no laptop use; no real multi-file benchmark. Exact exhaustive result only for the frozen eight-history class and finite Boolean hypothesis space. Tests ran against the Run99 packaged reconstructed compiler subset, not verified on repository CI. The implementation, tests and raw results were preserved in the Run100 local archive. GitHub's safety checks rejected the source-code write on this branch. No force push or merge.

Smallest supported claim: Three permitted protected-output probes identify all eight Run99 histories; zero-information restricted probes cannot. Representation-specific performance remains untested.
