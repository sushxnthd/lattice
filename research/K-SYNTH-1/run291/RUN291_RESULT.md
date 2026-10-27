# K-SYNTH-1 Run291: annotated-target and temporal MAY-call counterexample

Eight distinct trusted CPython 3.13 templates passed 16 functional checkpoints. A read-only independent AST audit verified 15 syntactic `len`/`sum` call positions and information-equivalent canonical facts in semantic-IR and ordinary Python/AST-action views. Thirteen local tests passed.

**New falsification:** the prior Run290 source-only analyzer omitted 2/15 syntactic call sites: `a[len(xs)]: int = 7` and `a[len(xs)]: int`. Even the value-less annotated subscript evaluates its index on CPython 3.13. The initial Run291 hypothesis that the value-less form did not evaluate `len` failed its first actual CPython assertion; this was retained in the local failure ledger, not retroactively represented as a prospective success. Bytecode shows CALL for both subscript forms but not simple `a: int`.

A new local analyzer separates lambda default creation from invocation, generator outer iterable creation from iteration, decorators from function bodies, and annotated targets. Its records are conservative syntactic MAY facts with runtime identity **UNKNOWN**. They do not establish reachability, binding identity, purity, general Python soundness, or superiority over Python.

The complete SHA-256-verified local archive includes source, tests, raw functional records, independent auditor, bytecode traces, and failure ledger; full GitHub archive mirroring is pending. The exact prior analyzer Git blob is `eb691508ca42937d3b5f2cd6fb5cf58433083e49`.

**Research status:** Four qualified real repair issues, zero new model-generated repairs, zero new independent issues, no powered IR-vs-Python result. All 89 boundary issues SEALED. One K-SYNTH-1 kernel; one draft/unmerged PR #9. Next: genuinely paired strong-model inference on four qualified real tasks and a prospectively qualified fifth issue.
