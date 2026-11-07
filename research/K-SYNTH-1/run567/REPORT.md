# Run567: exhaustive joint target/control qualification gate

Executed local Python enumeration of all 65,536 Boolean 2x2 component-ablation outcome matrices for two targets and two nonregression controls. A prospectively specified qualification predicate requires: all full-reference outcomes pass; baseline fails at least one target; each component is necessary on at least one target-or-control outcome; and controls remain correct under the full reference.

**Results:** 65,536 matrices enumerated; 2,700 qualified; 5,184 target-only apparent qualifications rejected by the joint gate. All enumerated predicates matched an independent explicit Boolean formula (65,536 assertions). This is a synthetic contract test, not evidence of a new qualified real repair or IR superiority.

Local reproducibility archive: lattice_run567.zip SHA256 3bdcfa99ab060e488152ba5ce82dbe25421d595f311368d9a908a5386d2a7873. Full raw JSON and executed source are in the local archive; not yet mirrored byte-for-byte on GitHub.

Do not retroactively promote Werkzeug PR2535 or alter any sealed 89 issues. Next: prospective real PR qualification and paired model comparison.