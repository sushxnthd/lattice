# Run451: independent re-audit and finite-observation non-identifiability

Independently parsed the original Run450 ZIP, checked eight variant tables against all 120 frozen IDs, and verified 960 observations. Six changed IDs: 9,25,41,61,77,93. Zero violations of the observed connectionpool-only finite-effect pattern. No new model inference or new API calls.

**Counterexample theorem:** For any finite observed set S and unseen u outside S, two deterministic effect functions can agree on S and differ at u. Hence zero observed cross-component interactions cannot certify zero unseen interactions without assumptions about function class or sampling. Executable test included in local SHA archive.

For zero events among 120 IID trials, the illustrative one-sided 95% upper bound is 2.466%, but the constructed correlated cases violate IID assumptions, so this is not an applicable generalization bound. Eight variants of one issue are not eight independent benchmark issues.

Local independent audit: 3/3 tests pass. Local archive SHA256 afc238bb6b2a7d07057885c3dec06c6f73f343a69a4cd5a32a78f2dddc617f42. Original Run450 ZIP SHA recorded in archive. No superiority claim; two qualified tasks unchanged; all 89 reserved issues sealed.