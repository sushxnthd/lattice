# Run542: environment closure contract

Executed three actual Python subprocesses with identical Python entrypoint and interpreter, varying LC_ALL (unset, C.UTF-8, C). All three returned exit code 0; captured stdout respectively `UNSET\nUTF-8`, `C.UTF-8\nUTF-8`, and `C\nutf-8`. Thus an unchanged entrypoint and imported-file hashes do not fix observable behavior without environment closure. This is a synthetic bounded counterexample, not proof of isolation or oracle correctness.

Local SHA-verified archive: run542.zip SHA256 `88bb6e1b7a005ce8515268cd14d2779fd963ce029d705f4d2732204135a6ca6c`; source SHA256 `69bbe7c716c90573bca8cf49e95db26844e88a4f16e09287328dc008a7c476bd`; raw JSON SHA256 `2b4fa30bf94a1293558de6171aadbae188bb35fe7fa2c2bc987acc705eecdc7f`. Source/raw GitHub mirroring pending.

No new real repair, no model inference, no IR superiority. Two independently qualified repairs remain; all 89 reserved issues sealed. Next priority is prospectively frozen real multi-source qualification and paired model evaluation.
