# Experiment 002: sequential semantic edits

Frozen before reading model results. This is a falsification experiment, not a
presumption that Lattice beats Python.

## Mechanism and controls

All conditions get the same initial policy, durable requirements, ordered natural
language change requests, exhaustive checker, and one counterexample repair call.
Maximum generated tokens per call: 220. Greedy decoding. Same model per comparison.

1. **Python full:** replace the complete function; assignment/if/return subset.
2. **Python patch:** conventional dictionary containing changed rule expressions.
   Omitted rules persist; the same graph runtime and verifier are used.
3. **Lattice patch:** changed named-rule assignments; omitted rules persist.
   The Python-patch arm controls for edit scope, durable memory, dependency
   propagation, compiler/runtime, and executable checking.

The allowed Boolean expression grammar is identical across arms. No grammar-
constrained decoding is used. Parser failures count as failures. Every raw prompt
and response is retained. No best-of-N extraction or selective task replacement.

## Tasks and evaluation

Eight policy trajectories: two development and six held-out name variants spanning
three semantic families. Three sequential changes each: relaxations, restrictions,
and a dependency trap where broadening read must not broaden edit. These are
correlated synthetic policy tasks, not eight independent real application domains.
Both splits are run under a frozen protocol; no development-driven selection occurs.

All 64 combinations of six independent Boolean inputs and all three output
permissions are checked at every stage. A separately hand-written behavior oracle
is cross-checked against the trusted rule contracts before any model runs. A
rejected edit leaves the program unchanged, but its requirement remains in the
cumulative task: later steps must catch up. No oracle resetting on failure.

Primary endpoint: all three checkpoints succeed within one repair per checkpoint.
Secondary: first-attempt and repaired checkpoint success, model calls, actual input
and output tokens, regressions, parse failures. Wall time is descriptive only;
batched CPU execution is not a fair product-latency measurement.

## Interpretation and boundary

Lattice must beat Python patch to support a syntax/representation effect. Beating
only full-function Python supports scoped editing, which ordinary Python can use.
Exact checking can prevent admitted bounded-policy regressions, but this guarantee
is shared by all arms and is not evidence that Lattice understands user intent.

The trusted target is authored by the evaluator. Translating real user intent into
that target remains unsolved. The language handles only pure finite Boolean rule
graphs. No loops, external state, side effects, database transactions, numerical
algorithms, UI behavior, or unconstrained source code are covered.

Qwen2.5-Coder 0.5B and 1.5B are two sizes of one model family, not independent
model-family replication. Even a positive result requires larger, different-family
models and external long-horizon application tasks before a breakthrough claim.
