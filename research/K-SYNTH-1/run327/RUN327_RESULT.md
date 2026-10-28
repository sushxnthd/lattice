# K-SYNTH-1 Run327: frozen urllib3 PR2482 qualification fails

Date: 2026-10-28 UTC / 2026-10-29 IST. One K-SYNTH-1 kernel, canonical branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9; all 89 reserved issues SEALED.

## Prospective protocol and execution

The nine-case public `HTTPSConnectionPool.urlopen()` fault-injection oracle and strict 2^3 three-production-source necessity gate were committed **before outcomes**: frozen protocol `fabd480914f9a05cb77a02ee0f027799c7106211`, oracle `561f6f54260c8ac8c89c5d09e1b2ad668326ce1e`. Merged upstream `urllib3/urllib3#2482`, baseline `1c6405832e5348c740bc3b67b8b171b5da100a26`, reference `111e609250bc7bf67b080b124298e0cf59efef9d`. The test author had inspected the PR diff before freezing: **source-informed, not blinded**.

Original Actions [40788528345](https://github.com/sushxnthd/lattice/actions/runs/40788528345) stopped after the 001 arm because the runner retained shell `-e`. The original 12-payload SHA-verified failure artifact is preserved. Workflow-only correction `17d42bcc334173667c2fed2663a1592184d9e133` disabled early exit, without changing oracle or gate. Corrected Actions [40788587985](https://github.com/sushxnthd/lattice/actions/runs/40788587985) completed and uploaded 24 SHA-verified evidence payloads.

## Exact 2x2x2 results

Bits correspond to `connection.py`, `connectionpool.py`, `exceptions.py`. All 24 source-component Git blob selections match pinned SHA values.

| Bits | Execution | Targets /3 | Controls /6 |
|---|---|---:|---:|
| 000 | completed | 0 | 6 |
| 001 | ImportError: missing HTTPSProxyError | n/a | n/a |
| 010 | ImportError: missing _wrap_proxy_error | n/a | n/a |
| 011 | ImportError: missing HTTPSProxyError | n/a | n/a |
| 100 | ImportError: missing _should_wrap_https_proxy_error | n/a | n/a |
| 101 | ImportError: missing _should_wrap_https_proxy_error | n/a | n/a |
| 110 | completed | **3** | **6** |
| 111 | completed | **3** | **6** |

The original gate required baseline <=1/3 targets and >=5/6 controls, full reference 3/3 targets and 6/6 controls, **and** a loss of joint target-plus-control correctness after *each* reference component is removed. It **FAILED**: `110` matches all nine `111` functional classifications without the reference exceptions.py change. Five import failures are classified as unimportable, **not** assigned zero functional correctness. Do not retune or promote this candidate.

This is a narrow negative result: exception-class deletion is unnecessary for the **frozen nine-case fault-injection oracle**, not proof that it is unnecessary for the full upstream behavior. The candidate also shares a repository with the already qualified urllib3 PR5071.

## Independent audit and limitations

An independent read-only auditor, importing no tested urllib3 code, verified ZIP CRC, all 12+24 SHA256 payloads, pinned commits, 24 source blob choices, eight exit statuses, 27 executed functional cases, five import-error stderr records and the unchanged qualification gate; **zero discrepancies**. Original ZIP SHA256 `894863f0cc09c2bb66f580753a9271ea33903116f150b4998c51acd46c4a2597`; corrected ZIP SHA256 `eb1ed8fb3ba92496561c0348ddbde5002a86428e0f9b8d4fa52e1c0ca7f4f466`. The canonical oracle and protocol are committed under this run directory; original artifacts are downloadable from the linked Actions runs.

Two independently qualified historical production **issues** remain Flask PR6096 and urllib3 PR5071. No new model inference, powered semantic-IR superiority or breakthrough. Next: evaluator-blind different-repository repair recruitment, pre-fix issue text, and real paired capable-model inference with information-equivalent Python/AST-action baseline. Preserve all failures. All 89 boundary issues sealed.
