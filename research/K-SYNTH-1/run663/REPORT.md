# Run663: unrelated decorator execution invalidates descriptor binding

Run662's bounded AST analyzer returned RESOLVED for a target `@property` even when a different method in the same class or subclass carried an arbitrary decorator. Python evaluates every method decorator during class creation. Such a decorator may execute arbitrary side effects, so ignoring it violates the analyzer's conservative closed-world contract. The corrected analyzer returns UNKNOWN/UNVERIFIED_DECORATOR for these cases, including inherited-property lookup through a subclass with an unrelated decorator. A clean property inheritance case still resolves. 16 executed unit tests passed.

Local SHA-verified artifact: lattice_run663.zip SHA256 d6c5d446917de681a0494f9f4a1347bd68b6102dc0e3fd6a4b676b9f1f8793d7. Executable and raw outputs not yet mirrored to GitHub.

This is a static soundness correction, not an upstream repair, production oracle, or coding-model comparison. It does not establish IR superiority. All 89 sealed issues are untouched. Upstream candidate qualification and full paired experiment remain outstanding.
