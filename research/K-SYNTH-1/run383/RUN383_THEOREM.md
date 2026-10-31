# Run383 bounded exact producer-influence theorem

Let a consumer be admitted by the Run383 AST grammar: a module-level import of a total pure Boolean producer, optional aliases, and single-return pure functions with two Boolean parameters x/y, Boolean constants, and/or/not, conditional expressions and direct calls to declared functions/aliases with x/y arguments. All source, AST-depth, node-count and function-count bounds are checked. The interpreter does not execute the submitted source.

For every producer truth table t in {0,...,15} and input (x,y) in {False,True}^2, define F(t,x,y) as the result of calling target with the imported producer replaced by that truth table. The analyzer follows CPython's short-circuit evaluation order and detects nontermination through repeated active (function,argument-pair) states.

**Theorem (bounded exactness):** If any intervention/input execution does not terminate or the source is inadmissible, the verdict is UNKNOWN. Otherwise, NO_DEPENDENCE holds if F(t,x,y) is constant in t for each input. If not, DEPENDENCE_CERTIFIED is returned with two table indices, one input index and opposite Boolean results.

**Proof sketch:** By structural induction on the admitted AST, the evaluator and CPython agree on terminating expressions, since every intermediate value is Boolean, all call targets are fixed, and evaluation order and short circuit are identical. The finite number of functions and four possible Boolean argument pairs imply any infinite call chain repeats a deterministic active call state. Therefore nontermination is detected exactly within the grammar. Exhaustively checking 16 tables times four inputs decides the counterfactual property; the witness is directly replayable in CPython.

**Limits:** This is not a theorem about unrestricted Python, general dynamic dispatch, side effects, real-world repository repairs, or any LLM performance advantage. UNKNOWN makes no semantic claim outside the admitted total grammar.
