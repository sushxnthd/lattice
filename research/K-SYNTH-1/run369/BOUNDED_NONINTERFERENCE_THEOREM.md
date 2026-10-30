# K-SYNTH-1 Run369: bounded cross-module noninterference theorem

## Accepted language

There are two Python modules. The producer defines exactly one pure total Boolean function `produce(x,y)` as a single return expression built from Boolean constants, Boolean inputs, `not`, `and`, `or`, and conditional expressions. It has no import-time side effects. The consumer imports only the producer function, optionally binds module-level immutable aliases, and defines pure two-argument Boolean functions with one return expression using the same grammar and direct calls. The graph reachable from `target` is acyclic. No reflection, mutation, decorators, default captures, global reassignment, dynamic imports, arbitrary attribute access, or external calls. The authorized edit replaces only the producer return expression without changing signatures or imports.

## Theorem

Let G include every syntactic direct call in each consumer return expression, including both branches of conditionals and short-circuit Boolean expressions. Resolve imported aliases to the producer node. If there is no path from target to the producer, then for every Boolean input pair and every admissible producer-body replacement, target returns the same value before and after the replacement.

**Proof.** On the finite acyclic call graph reachable from target, a leaf consumer function with no producer call evaluates only unchanged inputs and unchanged pure operations, hence is invariant. By induction, each non-leaf function with no producer path calls only invariant functions and has an unchanged return expression, hence is invariant. Target is invariant. Including calls in branches not executed may create false positives, but cannot omit an executed direct call in this grammar. QED.

## Explicit limitations

- MAY_DEPEND does not prove a real effect. `return False and p(x,y)` is a witnessed false positive.
- UNKNOWN is not a safety guarantee. Reflection, dynamic lookup, default captures, star imports, and conditional aliases are outside scope and have executable changed-output counterexamples.
- The theorem does not apply to arbitrary Python, repository repairs, import hooks, monkeypatching, mutable state or module side effects.
- The graph is derived from full source, which the ordinary Python/AST-action baseline also receives. This is not evidence of model representation superiority or general abstract-interpretation novelty.
- Atomic stale-preimage checking is separate from repository-level functional correctness.
