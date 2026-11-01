# K-SYNTH-1 Run410 — valid weak-null cluster e-process; issue-first urllib3 diagnostic

Date: 2026-11-01 IST. Branch `research/exp003-context-order`, sole OPEN/DRAFT/UNMERGED PR #9; all 89 reserved boundary issues SEALED.

## Mathematical result
For prospectively sampled independent repositories, let X_r be the mean paired repair-success difference in [-1,1]. Under the **conditional weak null** E[X_r | past] <= 0, each product W_t(lambda)=prod(1+lambda X_r) for lambda in [0,1] is a nonnegative supermartingale. A fixed equal mixture over lambda={.025,.05,.1,.2,.4,.8} is also an e-process. Ville's inequality gives P(sup_t E_t>=20)<=.05, even with optional stopping. This is not valid for arbitrary hand-picked repositories, cross-repo dependence, or outcome-selective missingness; it targets the mean repository effect, not the mean issue effect.

Exact enumeration of the Run392/400 asymmetric zero-mean counterexample (+1 with probability 1/6, -1/5 with probability 5/6, n=20) gives a rejection probability of **0.0001050193565**, below 5%. This remains conservative.

## Genuine raw simulation, seed 410
10,500 simulated independent-repository trials, eight issues per repo, discordance .30, within-repo sign ICC .30, all raw cluster vectors archived. Independent auditor reconstructed 2,287,584 checks with **zero disagreements**. Counts below are e-process anytime crossings / 1,500 trials; the one-sided terminal Hoeffding bound rejected 0/1,500 in every scenario.

| Repos | Issues | P(IR win | discordance) | E-process crossings |
|---:|---:|---:|---:|
| 60 | 480 | .50 (null) | 0 |
| 60 | 480 | .65 | 298 |
| 135 | 1080 | .50 (null) | 2 |
| 135 | 1080 | .60 | 681 |
| 300 | 2400 | .50 (null) | 7 |
| 300 | 2400 | .60 | 1412 |
| 500 | 4000 | .60 | 1493 |

The moderate-effect simulation has 45.4% power at 135 independent repositories and 94.13% at 300; these are **synthetic** model-specific estimates, not coding-model evidence. The 300-repository setting needs 2,400 issues, above the initial 400–800 issue target.

## New real-library issue-first candidate
Prospectively froze [urllib3 #3472](https://github.com/urllib3/urllib3/issues/3472), reported with historical source commit cc42860721836febf3fb6ebb485ed27d7f80122d. A trusted bounded internal TLS-policy probe on locally installed urllib3 2.7.0 executed seven cases: four targets reproduced `ValueError: Cannot set verify_mode to CERT_NONE when check_hostname is enabled`; two controls passed; one control failed because the **fake transport lacked close()**, a harness defect. The target variants share a mechanism. This is NOT a full loopback public-API test and is **NOT QUALIFIED**. No reference repair or two-production-file ablation was verified; original gate unchanged.

## Status and evidence
Full local Run410 archive contains complete simulation code, all 10,500 raw cluster vectors, exact rational enumeration, independent auditor, seven unit tests (7/7 pass), issue-first freeze, seven probe traces, SHA-256 manifest, and clean-extraction replay. ZIP SHA-256: `6964b1a42892b7dd01af44ad638b0cdedb9809e7b99dcee53808109bfd718e30`. No new coding-model inference. Exactly TWO historical qualified real multi-production-source tasks. No semantic-IR superiority or breakthrough claimed.

Next: genuine two-file independent production repairs, full isolated loopback proxy oracle for #3472, matched strong open-model IR versus Python/AST repair experiments, and repository-level inference with an explicit sampling mechanism.
