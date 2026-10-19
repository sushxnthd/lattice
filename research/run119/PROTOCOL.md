# Run119: exact relational-contract counterexample

K-SYNTH-1 remains the only active representation-science kernel. This run does not test model performance or demonstrate an IR advantage.

## Frozen counterexample

In Run118's bounded `ModuleGraph`, an internal `vault:secret = secret` is imported as `vault` by module `api`. The public `api:release` initially returns `False`, and `api:guard = public` is protected. Trusted edit authority permits changing only `api:release`; historical capture authority is empty. A patch setting `api:release = vault` with capture `{'vault':'current'}` is accepted, and the protected-output frame passes. Nevertheless, the editable low output now reveals the high input.

Exhaustively enumerate all 16 Boolean functions of one high and one low input, encode each as DNF in the same patch grammar, and independently test low-output noninterference using pairs of executions that agree on low input. All 16 preserve protected output `api:guard`; 12 violate noninterference and 4 do not. Both Python lowerings agree with the semantic graph on 128 checks. Three local tests passed. The runnable source, exact results, and test package are preserved in the Run119 artifact, but the Run118 compiler source is not yet integrated into this repository.

## Smallest supported claim

Write authority plus protected-output equality does **not** imply confidentiality for editable outputs. This is an application of established noninterference/hyperproperty theory, **not** a new theorem and **not** evidence that semantic IR beats indexed Python.

## Direct system consequence

Represent trusted high/low labels, current/historical read authority, declassification permissions, and two-execution information-flow commitments in the semantic model. Use the **identical** relational verifier for graph and indexed-Python views. Return `unknown` for unproved arbitrary-Python contracts; do not equate finite testing with proof.

## Sole active breakthrough kernel: K-SYNTH-1

(1) Structural versioned dependency/state graph with immutable semantic commitments. (2) Information-equivalent indexed Python with same facts, compiler, verifier, patch grammar, edit authority and token budget. (3) At least Qwen2.5-Coder-7B-Instruct, pending free hosted compute; second capable model if available. (4) Prospectively frozen independent realistic multi-file tasks; 161 is an optimistic minimum from predeclared exact paired McNemar assumptions, not yet met. (5) Paired first-attempt exact repair success. (6) Layout salience/token budget/weak Python index as strongest alternatives. (7) Falsify if matched Python equals/beats graph at declared precision or mechanism ablation removes gain. (8) Before holdout, predict stronger effect at capture depth >=5 than <=2. (9) Publish only after powered capable-model test, mechanism ablation, prospective boundary, independent oracle, uncertainty, prior-art audit and clean reproduction. (10) Only implement system changes implied by validated causal mechanisms.

## Blockers

The no-cost capable-model run and independently sourced corpus are outstanding. Previous executable-code commits were rejected by repository safety checks; do not bypass. No force-push or merge. No model inference in this run.
