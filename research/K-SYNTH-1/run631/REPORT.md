# Run631 — Aggregate necessity does not imply per-target interaction

Exact exhaustive enumeration of 4,096 Boolean assignments for four repair variants (base, A-only, B-only, full), each with two target tests and one control. Requiring baseline control pass, both single variants control pass, baseline fail at least one target, both single variants fail at least one target, and full pass all yields **27** assignments. **12/27** have no individual target requiring both components.

Concrete counterexample: base=(0,0,1), A=(0,1,1), B=(1,0,1), full=(1,1,1), coordinates (target1,target2,control). Both components are necessary to repair the *task set*, but neither target exhibits within-target interaction. Distinguish **task-set necessity** from **within-target interaction**; the former is scientifically valid but does not imply the latter.

Exact enumeration via itertools.product((0,1),repeat=12). This is a finite structural result, not empirical prevalence. No real production oracle or model inference; qualified count stays two; 89 sealed issues untouched. Local ZIP SHA256 524c3ab8524e13026ef83fb9cdf3668ca6a00baf7afe4f074c149a5d0a42c919.