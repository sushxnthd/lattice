# Run374: Short-circuit traversal invalidates the claimed totality lemma

## Counterexample

Producer: `def produce(x,y): return False`. Consumer:

```python
from producer import produce as p
def target(x,y):
    return p(x,y) or target(x,y)
```

The Run373 analyzer returns `MAY_DEPEND`, although `target(False,False)` raises `RecursionError`. Its recursive graph visitor used `any(visit(child) for child in sorted(edges[name]))`. Because the producer sentinel sorts before `target`, `any` stops at the first `True` and never visits the self-edge. With a producer returning `True`, the function terminates; the defect is therefore conditional on producer behavior.

A separate program with a recursive but unreachable helper is classified `NO_DEPENDENCE` by Run373. That target may still be total and independent, but the stronger published lemma that *every accepted consumer function is total* is false. These cases must not be counted as valid accepted-grammar examples.

## Corrected totality lemma

Assume the exact Run374 grammar: Boolean arguments and constants, `not`, `and`, `or`, conditional expressions, calls only to declared consumer functions or the imported producer, no dynamic Python features, no parameter-shadowed callable names, and a **globally acyclic** consumer call graph. The producer is total for Boolean arguments. Then all declared consumer functions are total and Boolean-valued on Boolean arguments.

Proof: Acyclicity permits a topological order. Every leaf expression consists only of total Boolean operations on Boolean inputs and the total producer. Inductively, all calls in each next function are to already established total Boolean functions; thus its expression is total and Boolean-valued. Short-circuit evaluation does not introduce new effects or nontermination because all reachable subexpressions are total and pure. Therefore every consumer function is total.

## Corrected noninterference theorem

Under the same scope, if the complete syntactic call graph contains no path from `target` to the producer, replacing the producer with any other admitted total Boolean implementation cannot change `target` on any Boolean input. The proof is topological induction over the reachable consumer subgraph. `MAY_DEPEND` remains a conservative possibility, not a claim of causal effect. `UNKNOWN` has no guarantee.

## Limits

The finite experiment is an exhaustive test of a specified 1,100-program *synthetic grammar*, not a proof of soundness for arbitrary Python, and not evidence that semantic IR improves coding-model repair performance. Runtime exceptions are functional outcomes, not model failures. The Run373 observations remain historically intact; this correction supersedes only its grammar-totality claim.
