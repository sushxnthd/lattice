# K-SYNTH-1 Run448 — observed cross-file calls do not certify joint repair necessity

Date: 2026-11-03 IST. **Exploratory post-outcome mechanism audit**, using the already frozen Run442 urllib3 2.7.0 cases. Not a new independent repair qualification or model result.

Recovered SHA-locked original urllib3 2.7.0 source and the 396 frozen public-API cases from Run442. Reconstructed all eight combinations of three AST-verified production-file edits: P = `poolmanager.py`, U = `util/url.py`, C = `connectionpool.py`. Isolated CPython public-API calls with network disabled and recorded bounded `sys.setprofile` projected stack ancestry for the three files.

- **3,168 genuine API executions**, **61,200 target-file call events**, 24 target function nodes, 34 projected edge types, 6 cross-file projected edge types.
- Cross-file projected calls occurred in **2,880/3,168** variant-case executions. **3,168/3,168 functional outcomes** exactly matched the unmodified original Run442 raw oracle receipts.
- Baseline **372/396** correct, 24 failures. **18/24 failures** executed projected cross-file calls.
- P alone repaired 12 pool/proxy failures, U alone repaired 6 URL-netloc failures, C alone repaired 6 same-host failures. The full PUC repair passed **396/396**.
- Every one of the 396 cases was affected by **at most one** file edit in all four settings of the other components. **Zero context-sensitive component effects** and **zero cases with multiple causal edit components**.
- In six actual same-host failures, `connectionpool.py:is_same_host` called `util/url.py:parse_url`; editing U did not change the failure, while editing C fixed it. In six pool-manager failures, execution visited all three files, yet only P fixed the result.
- **19/19 regression and adversarial tests passed**, and an additional independent three-process witness reproduced BASE=True, U-only=True, C-only=False for `is_same_host('http://example.com:0/')` against expected False.

**Scientific interpretation:** `OBSERVED_CALL` is not `MUST_EDIT_TOGETHER`. The soundness-scoped IR must distinguish observed stack ancestry, bounded MAY-reachability, verified finite counterfactual effects, and UNKNOWN outside the tested domain. A dynamic call is not proof of repair necessity; a zero finite interaction is not universal semantic independence.

Full 84-entry local reproducibility archive, 83 SHA-verified payloads, clean-extraction auditor/tests/staging replay passed. ZIP SHA-256: `fad9405965318a0d230b81fe1812fc0283a8a2932f5e7561ab89709f0285daf3`. Complete raw traces and original production source are in the local archive; GitHub full-archive mirroring remains incomplete.

**Unchanged primary gate:** two independently qualified real multi-production-source repairs (Flask PR6096, urllib3 PR5071); no new model inference, powered McNemar evidence, IR superiority or breakthrough. All 89 reserved issues sealed. Single OPEN/DRAFT/UNMERGED PR #9 on the same branch. Run449 prioritizes genuine functional matched open-model inference and new independently qualified PR-parent tasks.

## Executable finite-effect IR

Added `run448_effect_ir.py`: 396 provenance-checked finite certificates, 1,044 observed projected cross-file call-edge occurrences, 24 nonzero single-component edit effects. The validator rejects forged `MUST_EDIT_TOGETHER`, erased UNKNOWN scope and altered effect receipts. This is a bounded observed-input IR, not sound whole-program Python analysis. Local 19/19 tests passed. The final SHA-verified local archive is `fad9405965318a0d230b81fe1812fc0283a8a2932f5e7561ab89709f0285daf3`.
