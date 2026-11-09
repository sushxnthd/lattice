# Run598: AST call-site inventory versus actual execution

Executed 20 Python snippets in separate isolated `python -I -c` processes. Raw local archive contains each source, AST call sites, stdout, stderr, exit code and interpreter version. All 20 exited successfully. Total syntactic Call nodes: 27; total stdout events: 11 (not a one-to-one mapping).

This bounded semantic counterexample suite shows syntactic Call presence does not establish execution at module evaluation time. Deferred function/lambda/generator bodies, short-circuit expressions, unreachable branches and postponed annotations differ from eager default arguments, decorators, class bodies and eager annotations. A soundness-scoped IR needs phase distinctions and UNKNOWN for dynamic cases.

Local reproducibility ZIP SHA256: 078c0e5f14b3bc33647535c7134e7a165e01d62c49ad256219edf87f7dbecb64. This is NOT a production repair or model superiority result. Only two real repairs remain qualified; 89 sealed issues untouched.
