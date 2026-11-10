# Run624: AST union-leaf equivalence does not imply runtime equivalence

Run623 established that the two Werkzeug PR #3335 annotation expressions have equal unordered AST union leaves. That fact is structural, not a general semantic equivalence theorem.

A synthetic Python experiment uses a metaclass overloading `|` and compares `A | (B | C)` with `A | B | C`. Both return A, but the first logs B|C then A|B; the second logs A|B then A|C. Thus grouping and evaluation order are observably different even when unordered leaves match.

This is a **counterexample to a general inference**, not evidence that Werkzeug's actual annotation reordering changes behavior. The real PR remains NOT_QUALIFIED; there are still only two independently qualified real repair tasks. No coding-model inference or IR advantage claim. All 89 reserved issues remain sealed.

Reproduction: see local Run624 SHA-verified ZIP; GitHub executable mirroring pending.