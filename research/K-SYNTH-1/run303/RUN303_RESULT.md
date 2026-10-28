# K-SYNTH-1 Run303: independently audited isolated model-candidate regression

## Immutable original inference
Run301 original Qwen2.5-Coder-7B results remain **IR INVALID_JSON/truncated (no oracle)** and **Python/AST accepted one edit but 0/5 LF targets, 5/5 CRLF controls**. The original Run301 artifact 12777745815 ZIP SHA-256 `d8feadc2c2328f76c1aaf4548871b490d2ded4abd3817d1848fe7345726a672a` was rechecked against all **84/84** original SHA-manifest entries. No retroactive rescore.

## Original and corrected cloud attempts
- Original [Actions 40599715219](https://github.com/sushxnthd/lattice/actions/runs/40599715219), artifact 12777653080, ZIP SHA-256 `121ef6693d189d66fbc5ba996beec66dd97d568a185f6eb889cd40830d1e0fe6`: **FAILED before candidate execution** because workflow referenced `candidate/_readers.py` rather than `candidate/h11/_readers.py`. Failure log and original artifact retained; 1/1 manifest entry verified.
- Corrected [Actions 40599735911](https://github.com/sushxnthd/lattice/actions/runs/40599735911), artifact 12777713006, ZIP SHA-256 `8b987a111822b9774bec9b191924d1c44d4b1971239480ff95fd7293ea90e7d8`: **SUCCESS**. All 4/4 original manifest entries verified. Pinned staged model reader SHA-256 `f1cec1f102fecd29a459a077b294ae5ace2f998200e42a78926051e20f38232e`, original artifact SHA, imported `/candidate/h11/__init__.py`. Model-generated code ran **only in no-network read-only unprivileged Docker on GitHub Actions**, never on the host.

## Independent trusted baseline
A separate read-only auditor reconstructed historical upstream h11 from the original Run301 stage, replacing its model-generated `_readers.py` with the SHA-pinned **trusted original** `05c760d59ecfb456d30075c053e2a65559d7c3260f7902339949f98dd6f18777`. Only this trusted baseline was executed locally. The auditor compared the corrected cloud candidate's 18 full-message functional traces against 18 trusted baseline traces across six request families and three correlated fragmentations (whole, split, bytewise).

| Input family | Trusted original | Original model candidate |
|---|---:|---:|
| Valid CRLF | 3/3 | 3/3 |
| LF-only | 0/3 | 0/3 |
| **Embedded bare LF in CRLF-framed request line** | **0/3** | **3/3** |
| Extra CR in request line | 0/3 | 0/3 |
| Bare LF in header | 0/3 | 0/3 |
| Valid CRLF with extra header | 3/3 | 3/3 |

**3/18 differential traces, all in the predeclared embedded-bare-LF family.** This is a **verified bounded parser-acceptance regression**: the model candidate accepts a malformed full HTTP request rejected by the trusted original. The intended LF-only repair remains unsolved. The three differences are correlated fragmentations of one family, not independent issues.

**Mechanism:** upstream receive buffering requires CRLF framing, so changing only the downstream request reader cannot repair LF-only input. A CRLF-framed request with a bare LF before its line separator does reach the reader, and stripping that LF relaxes validation. This is **not a claim of exploitability or a security vulnerability**, and it does not establish that semantic IR would have prevented the mistake: the IR model arm produced no valid patch.

## Preservation and limitations
Local Run303 archive: `lattice_run303_original_candidate_isolated_regression_audit.zip`, SHA-256 `a1905e656f60c5cf577671e59ef31176fbe2c8f7ea495e68170ac848e9a5bc66`; eight SHA-256-verified evidence payloads plus manifest, including original Run301 and both original Run302 cloud ZIPs, independent audit script and trusted functional traces. Historical GitHub ZIP mirroring remains incomplete.

**Research status:** five qualified independent real multi-production-source repairs; no sixth, no powered IR advantage, no breakthrough. All 89 reserved boundary issues SEALED. One K-SYNTH-1 kernel, branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9.

Next: prospectively freeze and qualify a sixth independent real repair with joint target+control necessity, then run a valid paired strong-model pilot with genuine semantic/dataflow IR versus information-equivalent ordinary Python/AST actions and a shared compiler/isolated oracle.