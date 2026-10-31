# K-SYNTH-1 Run386: effect-sensitive finite certificate and failed production candidate

**Result:** New bounded effect/exception certificate independently reproduced. No new real repair qualification or coding-model inference.

Run385's Boolean return-value ANF cannot certify preservation of effects. Constructed a return-invariant counterexample whose ordered `emit` trace depends on a producer intervention. Extended the finite certificate to a one-hot ANF for each observable ordered trace plus tagged return/ValueError outcome. The construction is injective over the 4 target inputs × 16 producer truth-table interventions, for a strictly whitelisted loop-free Boolean Python grammar. Unsupported Python is `UNKNOWN`.

**Evidence:** 256 deterministic trusted generated programs, 16,384 functional observations. Independent CPython replay: 16,384/16,384 exact matches. Independent one-hot polynomial decoding: 16,384/16,384 correct. 20/20 adversarial tests pass, including exhaustive 65,536 Möbius roundtrips. 132/256 intentionally effect-rich synthetic programs have intervention-dependent traces with invariant terminal outcomes; 64 have exception outcomes. These are not population estimates. Complete raw traces, code, tests and SHA-256 reproducibility archive are preserved locally; full executable GitHub mirroring is still incomplete.

**Production recruitment:** Before inspecting PR #14694's diff, committed the pytest #14683 candidate protocol at `1e527ee3c323db12a9d22577c60b8192aea6e772`. Independent changed-file listing found only one production source, `src/_pytest/fixtures.py`, plus two test files and a changelog. **NOT QUALIFIED** under the predeclared two-production-source criterion. No historical baseline, factorial or model inference was run; no retuning.

**Limits:** The finite effect grammar is not unrestricted Python or a general contextual-equivalence proof. No powered semantic-IR superiority, model repair or production causal-coupling claim. Historical qualified cohort stays at ten; all 89 reserved boundary issues remain sealed.

Full local evidence: `lattice_run386_effect_complete_certificate_and_rejected_candidate.zip`, SHA-256 `630601cd61e1e7d0d8639fed36162825d8cc3c5c7bd1d2a9d09e6a36fd866d48`. Clean-extraction verification passed.

GitHub-mirrored minimal executable: [`run386_minimal_counterexample.py`](run386_minimal_counterexample.py), Git blob `219a0408fe3128d70c166ef4568f6886f6cc2b60`, independently matched to local source. Full analyzer and 16,384 raw observations remain in the SHA-verified local archive.
