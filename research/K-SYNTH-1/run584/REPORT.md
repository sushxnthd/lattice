# Run584: mean-zero does not validate cluster sign-flip

Exact enumeration, not observed model repairs. Independent repository effects X are +9 with probability 0.1 and -1 with probability 0.9. E[X]=0, but the sign distribution is asymmetric. Two-sided exhaustive sign-flip inference implicitly needs sign symmetry/exchangeability, not merely independent clusters or zero mean.

| repositories | exact false-positive probability at nominal 0.05 |
|---:|---:|
| 6 | 0.531442 |
| 8 | 0.43049062 |
| 10 | 0.3488253427 |
| 12 | 0.282970768303 |

The 6-repository all-negative outcome occurs with probability 0.9^6=0.531441, yet has sign-flip p=1/32. This is a counterexample to using sign-flip as a generic mean-zero test. It does not invalidate sign-flip under stronger sharp-null or symmetry assumptions. Prospective Lattice analysis must specify its estimand and null, preregister independent-cluster robust inference with enough repositories, and test sensitivity to skewed repository effects. No new real repair or model outcome. All 89 reserved issues remain sealed.

Local SHA-verified archive: lattice_run584.zip SHA256 5654dbe2be7d0d52b4cd949fa1c25d4d41f410677cbab0edd5d8bcaac1a07dac. Contains executed experiment.py, raw.json, report, SHA256.json. GitHub raw/code mirroring outstanding.