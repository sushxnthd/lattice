# Run375: target-scoped totality and noninterference

Assume the admitted pure two-module Boolean grammar. Producer defines a total Boolean function with no calls. Consumer imports it through a statically resolved alias and defines functions with two Boolean parameters and one return expression using Boolean literals, parameters, not/and/or, conditional expressions and statically resolved calls. No mutation, dynamic lookup, defaults, annotations, decorators, generic type parameters or other statements are admitted. Function definitions are side-effect-free.

**Target totality theorem:** If the consumer call graph induced by functions reachable from `target` is acyclic, then `target(x,y)` terminates with a Boolean result for every Boolean input pair. Proof: topologically order the target-reachable functions. The producer is total; every reachable consumer function applies total Boolean operations to Boolean inputs and calls only already-total functions. Unreachable recursive helpers are defined but never invoked, and have no definition-time effects in this grammar.

**Target noninterference theorem:** If no static path exists from `target` to the producer, replacing the producer by any other admitted pure total Boolean implementation cannot change `target` on Boolean inputs. Proof: topological induction over the target-reachable consumer subgraph. Its expressions never invoke the producer. MAY_DEPEND is only a conservative possibility, not proof of a behavioral effect.

**Boundary examples:** An unreachable `f(x,y) -> f(x,y)` does not invalidate a target returning `x`. A reachable `p(x,y) or target(x,y)` may diverge when the producer is False, so it remains UNKNOWN. A 1,000-unary-not AST exceeds the conservative parser-depth bound and returns UNKNOWN. Generic function type parameters are outside the admitted grammar.

The theorem does not cover arbitrary Python, dynamic dispatch, import-time side effects, concurrency, exceptions, resource exhaustion or coding-model representation superiority. The finite experiment covers 1,100 synthetic programs and 70,400 fresh CPython observations; it does not establish model performance.
