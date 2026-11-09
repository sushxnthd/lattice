# Run595 — Exact unequal-cluster counterexample

Prospective mathematical stress test (synthetic, not a coding-model result). Null: independent fair signs at repository level; one repository contributes 100 perfectly correlated issue outcomes and each other repository contributes one. All 2^R sign configurations enumerated; two-sided exact binomial p-values calculated once per issue (invalid independence assumption) and once per repository (valid sign-test assumptions).

| Independent repositories | Issues | Naive issue-level false-positive rate | Repository sign-test rate |
|---:|---:|---:|---:|
|2|101|100%|0%|
|4|103|100%|0%|
|8|107|100%|0.78125%|
|12|111|100%|3.857421875%|

The single large repository controls the issue-level test even when every other repository disagrees. This demonstrates that an issue-level nominal 5% test can reject with probability one under a repository-cluster null. The valid repository sign test assumes independent symmetric nonzero repository effects; it does not establish any IR advantage.

Reproduction: exact rational arithmetic with Python fractions and exhaustive enumeration; source and raw JSON archived locally. No real repairs, model inference, or reserved boundary issue access. Qualified real tasks remain two. Do not change frozen protocol or promote failed Werkzeug cases.
