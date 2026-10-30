# Run373 corrected bounded totality and noninterference theorem

**Original counterexample.** `def x(x,y): return False; def target(x,y): return x(x,y)` was admitted by Run369 as NO_DEPENDENCE, but Python resolves the called `x` to the Boolean parameter, not the global function, and raises TypeError on every admitted input. The old admitted language was not total. This does not itself show a missed Boolean-output dependency.

**Repaired grammar.** Retain Run369's two-module pure Boolean expression grammar, immutable producer aliases, direct-call resolution and acyclic graph restrictions, and additionally reject any direct `ast.Call` with callee name `x` or `y`. All accepted functions have formal Boolean parameters named x/y. Calls to other names must resolve to declared consumer functions or the imported producer.

**Totality lemma.** Producer Boolean expressions are total. In topological order over the finite acyclic consumer graph, every direct call resolves to an already total pure function (or the producer), and the remaining expression constructs are Boolean operations and conditionals on total Boolean expressions. Thus every accepted consumer function is total on Boolean inputs.

**Noninterference.** If the conservative graph has no path from target to the producer, replacing the producer's admissible pure Boolean body cannot change target on Boolean inputs. Induct on the reachable graph: leaves have no producer call and unchanged expressions; nonleaves call only invariant descendants.

**Scope.** This is not a theorem for arbitrary Python, dynamic calls, mutable globals, import hooks, non-Boolean arguments, or untrusted generated code. UNKNOWN is not a safety guarantee; MAY_DEPEND does not imply an actual causal effect. An unused module-level function named x is allowed; a syntactic call to x is conservatively UNKNOWN even if unreachable.
