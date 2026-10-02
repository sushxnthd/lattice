# Scope-preserving compiler validation

Registered separately from the frozen model-generation experiment, before reading
its outputs. This is a deterministic compiler validation, not an AI benchmark.

Compile replacements against immutable, versioned rule nodes. The caller supplies
the allowed output set. Protected output roots keep their old node identity; the
reachable closure of that node remains immutable. Authorized output roots bind
to new versions of authorized dependencies and prior versions of protected ones.

**Frame proposition:** for any supported input valuation and protected output,
the compiled replacement returns the same value as the prior program. Its root
and every reachable node are unchanged, and evaluation is a pure function of the
same inputs and that immutable subgraph. This is a structural argument, not a
machine-checked proof in a theorem prover.

Test 100 seeded trajectories, 20 replacements each, five output nodes and six
Boolean inputs. Evaluate every input and protected output for every edit. Check
the interpreter against native Python emitted by the compiler. Store every
replacement and the first observed ordinary-graph regression witness.

The ordinary live-name rule graph is an ablation without frame compilation. It
receives the same edits but has different accumulated state after past regressions;
its rate is therefore a stress-test result, not a controlled AI accuracy effect.
A conventional Python library invocation of the framed compiler is an equivalence
control; it must have exactly the same results. Intent correctness is not measured.

This property is restricted to pure Boolean outputs: shared mutable objects,
external effects, timing, and arbitrary application code are outside the model.
Graph size may grow across edits as protected outputs capture old versions. The
lowerer emits only versions reachable from current roots.
