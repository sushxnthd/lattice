# K-SYNTH-1 Run301 prospective freeze (before CPython execution)

The complete local frozen manifest `RUN301_PROSPECTIVE_FREEZE.json` was generated **without executing templates**. SHA-256: `a646c0e3f681f0d53852ba5851c7602051339fa670a7432edcceeeb54a4440e6`. This hash commits to all 16 exact Python source strings, expected identities, source hashes, and evaluation rule.

**Hypothesis:** Run293 source-only transfer overwrites the binding of a decorated `def g` with `NON_TARGET`, although Python decorators may replace `g` with builtin `len` or `sum`. The original final call to `g` is predicted `NOT_KNOWN_TARGET` for all 12 target templates; a conservative corrected analyzer must classify decorated `g` as `UNKNOWN_DYNAMIC` without claiming builtin identity.

Target templates (12): direct_len, factory_len, stack_len, direct_sum, conditional_len, class_len, lambda_len, alias_len, default_len, holder_len, stack_override_len, direct_sum_alias.

Controls (4): control_undecorated (custom), control_identity (custom), control_none (none), control_lambda (custom).

**Prospective evaluation:** For each source template, 64 trusted CPython executions in a fresh namespace with n=0..63. An independent evaluator records whether `g is builtins.len`, `g is builtins.sum`, or neither, and records call result/exception. Check 1,024 traces, all source SHA hashes, original analyzer classifications, and corrected analyzer classifications. The template family is correlated and is not 1,024 independent repairs.

All 89 reserved boundary issues stay sealed. No model inference or semantic-IR superiority claim is authorized by this experiment. Do not change these criteria after observing results.