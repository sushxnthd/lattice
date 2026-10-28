# K-SYNTH-1 Run304 prospective experiment freeze

Committed before any trusted CPython functional execution. This is a **bounded lexical-provenance precision experiment**, not the sixth independent repository qualification or a representation-superiority study. Run303's original model scores remain immutable.

- Frozen generator: `run304_experiment.py`, SHA-256 `7fe65688feeeccdf496cb36c98d789a5eb97d72f66afaeb0065f59853d3e57ef`.
- Frozen correction: `run304_shadowing_transfer.py`, SHA-256 `974d6e01a175c1959fc2dd5b01daace7e1d27253d377b365fc919dd4ab2a96f9`.
- Frozen source manifest: canonical JSON SHA-256 `923fa8cd7f204378dd22f7a21fa8f53cfb3cac492452c490f2fc277f7807a375`; 24 hardcoded templates, 64 correlated seed variants each, 1,536 executions. Full source manifest is retained locally.
- Original Run293 analyzer SHA-256 `ca7ce7fb9d54cc5bdadbbba4ae824488191164fd61f4ade9ae85ac2c8e309b6f`; original Run301 corrected decorator analyzer SHA-256 `69b5e57b7c0c676f4387ef976d48914b56270167a9dd989d2bbf1b6baf5a0ba0`.
- Hypothesis: an undecorated Python `def len` or `def sum` creates a fresh function object, **not** the existing builtin. The inherited Run301 transfer mistakenly labels its call `MAY_TARGET`. Correct transfer assigns `NON_TARGET`; decorated functions remain `UNKNOWN`.
- Frozen expectations: shadowed definitions 512/512 old MAY_TARGET, new NOT_KNOWN_TARGET, runtime builtin calls 0; direct builtins 256/256 MAY_TARGET in both and one builtin call; `from builtins import ...` aliases 256/256 MAY_TARGET and one builtin call; decorated function rebinding 256/256 UNKNOWN_DYNAMIC and one builtin call; unrelated local controls 256/256 NOT_KNOWN_TARGET and zero builtin calls.
- Trusted CPython source is generated **only from hardcoded templates**, never from a model. Record raw profiler identities, source hashes, static classifications, failures, and exact result values. Any mismatch is a frozen failure; do not retune after seeing outcomes.
- The 1,536 executions are correlated variants of 24 templates, not independent repairs or powered statistical evidence. Scope: trusted module-level no-unmodeled-mutation, builtin len/sum identity, not general Python soundness.
- Continue the primary prospectively frozen multi-repository paired model program; no sixth qualification or IR advantage may be claimed from this experiment. One K-SYNTH-1 kernel, canonical branch, one open/draft/unmerged PR #9, all 89 reserved boundary issues sealed.
