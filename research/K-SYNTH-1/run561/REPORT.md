# Run561 — exact cluster-aware inference counterexample

Synthetic constructed dataset, **not** real coding-model evidence. Eight repositories each contribute ten perfectly correlated discordant issues. Seven repositories favor IR, one favors Python. Issue-level exact two-sided McNemar: **3.161290522649495e-12** (70 IR-only, 10 Python-only). Exact two-sided repository sign-flip randomization across all 256 assignments: **0.0703125** (not below 0.05). A seemingly decisive issue-level result is not significant when the independent randomization units are repositories.

This is an **inference design counterexample**, not evidence for IR. Cluster sign-flip inference assumes exchangeability/sign symmetry of repository-level treatment differences under the null; it is not universally exact for arbitrary observational paired data. Freeze cluster handling before model evaluation. No real task qualification or model inference this run. Two previously qualified real repairs remain; 89 reserved issues sealed. PR #9 remains draft and unmerged.

Files: experiment.py (executable), results.json (raw output). The local archive may have a source formatting variant but produces identical values.
