# Run648: executable counterexample to Run641 transcript readiness

Run641 marks an arm EXECUTED when its subprocess exits zero, even when stdout is not valid JSON. A two-commit synthetic Git repository with the same two source-file paths ran the original Run641 runner with an injected `print('NOT_JSON')` oracle. All four arms exited zero and were marked EXECUTED, with overall qualification REQUIRES_FROZEN_ORACLE_ADJUDICATION. This is a missing structural validation gate, not evidence of a qualified repair.

Independent strict validator: raw transcript UNKNOWN:NON_JSON; valid synthetic fixture STRUCTURALLY_VALID_NOT_QUALIFIED; 20/20 adversarial missing-observation and stderr mutations rejected. Original Run641 runner SHA256 fc333688fa4336ed07091917d089b6780f182faea32950fe4c87c953b490a2c4. Local reproducibility ZIP SHA256 5b1e3995e6504d5222139dd6bb2d47ce1773fdf015537197537cbd262be79bc1. Executable and raw artifact mirroring still pending.

This experiment does not execute Werkzeug, establish source provenance, or qualify a production repair. Two independent real tasks remain qualified; no model comparison; 89 reserved boundary issues untouched.
