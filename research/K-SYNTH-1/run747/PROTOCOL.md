# Run747 protocol

Prospectively fixed seed 747. Generate 256 cases in each of 16 Python source families. Apply only inert module/function docstrings, blank-line variation, and fresh nested identifier suffixes. Parse each source to AST, call the archived alpha compiler's callable_kind on top-level f, compile the same AST with CPython 3.13.5 using dont_inherit=True, extract f's code object without executing the module, and compare Lattice's classification with CPython flags.

Reference mapping:
- CO_ASYNC_GENERATOR -> ASYNC_GENERATOR
- CO_COROUTINE -> COROUTINE
- CO_GENERATOR -> GENERATOR
- otherwise -> FUNCTION

Families:
1. sync plain
2. sync direct yield
3. sync direct yield-from
4. sync nested def yield body
5. sync nested lambda yield body
6. sync nested def default yield
7. sync nested lambda default yield
8. sync nested def decorator yield
9. sync nested def annotation yield
10. sync nested class base yield
11. sync nested class metaclass yield
12. sync nested class method yield body
13. async plain
14. async direct yield
15. async nested def yield body
16. async nested lambda yield body

Fail the run on any mismatch, parse/compile error, missing/duplicate top-level f code object, or unexpected template classification. Candidate source must never be executed.
