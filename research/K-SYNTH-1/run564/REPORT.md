# Run564: short-circuit assignment counterexample

Executed eight CPython cases for `and`/`or` with boolean left operands and assignment-expression right operands. Four cases assign `x`, four do not. A syntactic scan that marks a name definitely assigned upon encountering `NamedExpr` is therefore unsound even in this small fragment. The bounded analyzer returns DEFINITE only when right-hand evaluation is forced, NOT_ASSIGNED when it is skipped, and UNKNOWN for an unknown left operand. Two additional unknown-left cases correctly refuse certification.

Scope: synthetic Python execution and bounded AST analysis; not a real multi-source repair, production model comparison, or proof of full Python soundness. The 89 reserved tasks remain sealed; only two independently qualified real tasks are known. No superiority claim.
