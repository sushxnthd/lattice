# Run557: atomic compiler counterexample

Executed CPython AST parsing and compilation on four exact source variants. Baseline compiled and returned 1; A-only failed IndentationError at line 2; B-only failed IndentationError at line 1; atomic A+B compiled and returned 2. Both assertions passed. Consequently an editor that compiles and rejects each intermediate edit can exclude a valid two-edit transaction; the shared compiler for IR and Python baselines must apply all authorized edits atomically before validation.

This is a synthetic grammar witness, not a real production repair, new model inference, or evidence of semantic-IR superiority. Two qualified real repairs remain; 89 reserved issues remain sealed. Local reproducibility ZIP SHA256 39f0df1401a4fdd916a4f69adb491bbaff1f80f1bd2637dec79e746c3e587a87. Full raw-data mirroring outstanding.
