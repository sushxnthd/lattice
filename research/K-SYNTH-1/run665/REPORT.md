# Run665: independent reproduction and narrower eager-expression guard

Independently reproduced the Run663 soundness counterexample: an unrelated method default expression invokes `mutate()` at class creation, replacing a parent `@property` with a string. The prior analyzer reports `RESOLVED/data_descriptor`; executed Python returns `B().text == "replaced"` and `type(A.__dict__["text"]).__name__ == "str"`.

A revised experimental analyzer returns `UNKNOWN/EAGER_DEFAULT_EXPRESSION` for nonliteral defaults and `UNKNOWN/EAGER_ANNOTATION` for method annotations. **19 executable tests passed**, including a literal-default case that remains resolvable. This narrower policy is not yet formally proven sound; Run664's more conservative rejection of all defaults is a defensible alternative.

Local reproducibility archive `lattice_run664.zip` (independent reproduction, packaged before discovering concurrent Run664): SHA-256 `cfdfb7aec6bebe43888ff01af68e4f89df44ed9914d09c88269a8fd1df26c1af`. Contains previous and corrected executable, raw test output, actual Python counterexample, JSON observations and verified manifest.

**No upstream qualification or model inference.** Two independent real tasks qualified, all 89 reserved issues sealed, IR superiority unestablished. Prioritize pinned production oracle, prospective heldout and nonregression tests, and model comparison.