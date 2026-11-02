# K-SYNTH-1 Run441 — urllib3 2.7.0 cross-version functional repair

Date: 2026-11-02 UTC. Canonical branch research/exp003-context-order; one draft PR #9; all 89 reserved boundary issues sealed.

## Frozen design and provenance

A known-issue cross-version transfer test of the urllib3 PR5071 port-zero mechanism against the locally installed, SHA-pinned urllib3 2.7.0 source. This is NOT a new independent issue qualification, blind localization, new model inference, or evidence that PR5071 was included in a release.

Before local variant execution, froze 180 public API observations (3 hosts × 2 schemes × 6 port values × 5 endpoint conditions), including 150 nonzero/absent-port controls. Frozen protocol SHA256 ca9a35eb4290d9831fc41c772a0a01908326e65ff13fe4161345072dde014ee2; frozen case-set SHA256 f1cd630961affc530a2ae4b1927c585606db4cec92da07907ec3904c410e8bd7.

Original production source SHA256:
- poolmanager.py: 734ae1d2b7140b5b79b431ae51e188800ce512b6ac3cec16c0b881ebb957f293
- util/url.py: 59187e4cc617a2c9a0a7c9bc953e07e6ca681f0e7252395c3027d4e77024a00b
- connectionpool.py: b0616775d5d8c25c7b282e0908fd602af74d18b34af984c22437460021a3dd8f

## Actual production public-API results

| Variant | Correct / 180 | Port-zero failures | Nonzero/absent-port regressions |
| --- | ---: | ---: | ---: |
| Base | 162 | 18 | 0 |
| poolmanager.py only | 174 | 6 | 0 |
| util/url.py only | 168 | 12 | 0 |
| connectionpool.py only | 162 | 18 | 0 |
| poolmanager.py + util/url.py | 180 | 0 | 0 |
| Full three-file guard repair | 180 | 0 | 0 |

All six variants were executed in separate isolated CPython processes with networking forbidden. The independent auditor replayed all 1,080 API observations, matched every raw receipt, and independently reconstructed every changed source byte from SHA-locked AST spans. Total 2,160 executed public API calls; 11/11 regression/adversarial tests passed. Clean ZIP extraction replay passed.

## Mechanism and limitations

Truthiness tests conflate absent None and explicit integer port 0. Bounded exact-int/None repairs replace the relevant tests with identity comparisons and preserve all source bytes outside authorized spans. The connectionpool.py edits were unnecessary for these frozen endpoints; this does not establish global redundancy. The observed 180 cases are deterministic checks, not independent statistical repair tasks.

No model-generated code was run. No coding-model completion or powered semantic-IR superiority evidence was produced. The qualified independent real multi-source repair count remains TWO (Flask PR6096, urllib3 PR5071).

## Evidence

Minimal SHA-locked production witness: research/K-SYNTH-1/run441/run441_minimal_witness.py. Complete offline archive (source and license, frozen protocol/cases, lossless editor, raw traces, independent evaluator, tests and manifest) is retained as lattice_run441_urllib3_2_7_0_cross_version_repair.zip, SHA256 9d0f6cb1d2da7038cad306bc013dd3a7281e0008cdad33a0b055408642960f85. Complete ZIP is locally preserved; byte-identical GitHub mirroring of the entire archive is pending.

Next: genuine paired strong open-coding-model inference on the two qualified historical repairs, with identical facts and authority, actual raw completions, model SHA, isolated oracle and independent audit; new prospectively qualified independent public-repo repairs.
