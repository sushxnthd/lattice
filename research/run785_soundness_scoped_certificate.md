# Run785: narrow expression dependency certificate

Local executable reproducibility archive: Run785 (12/12 deterministic tests; SHA256 archive 57112f15225e98b6f9fea85e825334b67d137f801af52d5f8cb0dfa414d35de0).

A checker certifies only exact scalar literals and a single allowed variable reference, returning UNKNOWN for operators, calls, attributes, comprehensions, comparisons and other constructs. Counterexamples: Python `x and False` may invoke user-defined `x.__bool__`; `x+1` may invoke `x.__add__`. Therefore AST syntactic dependence does not certify purity or semantic necessity.

Restricted theorem: an allowed direct variable lookup yields the same object reference in environments agreeing on that binding, assuming ordinary name lookup and no concurrent environment mutation; exact scalar literals are environment-independent. This is not general semantic/dataflow IR soundness or repair superiority. No model inference or independent real task qualification attempted. Local executable archive not yet mirrored to GitHub.
