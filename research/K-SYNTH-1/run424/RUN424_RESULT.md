# K-SYNTH-1 Run424: frozen oracle misclassifies two repaired false positives

**Status: executed locally on installed urllib3 2.7.0, not yet verified on exact historical PR-base. No new coding-model inference, qualification, or IR superiority.**

The fixed 8-arm factorial port-zero repair study ran 70 no-network public API observations per arm, 560 total. The original frozen oracle comprised 10 explicit port-zero positive targets and 60 controls. Its full three-file reference arm passed **10/10 positives but only 58/60 controls**. The frozen nonregression gate therefore **FAILED**; do not change its original scoring after seeing outcomes.

| Changed production files: connectionpool / poolmanager / util/url | Positives /10 | Original controls /60 |
|---|---:|---:|
| 000 | 2 | 60 |
| 001 | 4 | 60 |
| 010 | 8 | 60 |
| 011 | **10** | **60** |
| 100 | 2 | 58 |
| 101 | 4 | 58 |
| 110 | 8 | 58 |
| 111 | **10** | **58** |

**Construct-validity counterexample:** the two nominal controls were samehost_http_80 and samehost_https_443. A pool at the default port must not treat a URL explicitly specifying :0 as the same host/port. Without the connectionpool fix, both return the incorrect True; the full repair correctly returns False. The poolmanager+util/url arm passes all ten frozen positive targets while missing both necessary negative checks. Therefore target-only success does not establish joint component necessity. Calling the two changed cases additional targets is **post-outcome explanatory analysis**, not a retroactive change to the frozen oracle.

An independently written evaluator reconstructed all eight variants, replayed **560** isolated CPython observations, and checked **24** source hashes: **584 checks, zero disagreements**. All **12/12** regression tests passed. A generated _version.py import transport shim was independently tested on the installed package: its absence causes import failure; restoring it yielded **560/560** identical API observations. No untrusted model code was executed.

The complete local SHA-verified archive includes raw outputs, both evaluators, the executable minimal witness, source and license, tests, manifest, and next protocol.

**Exact historical follow-up:** committed [Run424 cloud source replay](https://github.com/sushxnthd/lattice/blob/research/exp003-context-order/research/K-SYNTH-1/run424/run424_cloud_exact.py) and [workflow](https://github.com/sushxnthd/lattice/blob/research/exp003-context-order/.github/workflows/lattice-k-synth-1-run424-exact.yml). The workflow pins upstream merge commit f5cf122346141b187cca0db6e6445297d336b610, fetches its first parent, verifies the three original production Git blob SHAs, checks the full reference production files byte-for-byte, and records all 8 x 70 isolated outcomes. Its cloud outcome and artifact **remain unverified**; do not call this an exact historical replay yet.

The two previously independently qualified real multi-production-source tasks remain the only qualified tasks. The 89 reserved boundary issues remain sealed. Sole draft PR #9 stays unmerged; no breakthrough claim. Historical GitHub raw-artifact mirroring remains incomplete.
