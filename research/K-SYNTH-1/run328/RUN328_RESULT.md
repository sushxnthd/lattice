# K-SYNTH-1 Run328: third independent historical production issue qualifies

Date: 2026-10-29 UTC. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, one open/draft/unmerged PR #9. All 89 reserved boundary issues sealed.

## Prospective order and independent repository

Different public repository `encode/httpx`, pre-fix issue [#1146](https://github.com/encode/httpx/issues/1146) dated 2020-08-07, merged [PR #1183](https://github.com/encode/httpx/pull/1183). Exact pinned baseline `891d865044d27c229278f0fa20d84ba4007cb289`, historical reference merge `a226c60861f651b9874e31e66b3bb7f0db46c96d`. The candidate was locked in Run327 before reference diff inspection. This run read only the original issue, PR metadata, and baseline source to author the nine-case oracle; **no reference source or diff was read before freezing**. The original oracle was committed `4d5f3d4fe5b9d4a533288d10a3dd5f6d18f977eb`, and the exact qualification gate was committed `09808f2897cf0bd6a3cfb9a09423bc00d7618339` before any outcome. Runner commit `3dee70615c01baa4b3db270ca724f6d03bf41b52`; workflow commit `e7c397b518ba17a857a32d1c9848a59ef6953c05`.

## Original cloud result

[Original GitHub Actions run 40794660996](https://github.com/sushxnthd/lattice/actions/runs/40794660996) completed successfully at approximately 00:32 UTC. Original artifact ID `12863302060`, ZIP SHA256 `b98a032547ded33da80fbaa096cddfed8cacbcbd11a35cdc2040520324d11b45`. All nine outer evidence entries and all five inner SHA manifest entries verified. The exact frozen oracle SHA256 was `51cefba11ede1692bf543500f410fcf3406f95705f6b5876af886893574394f7`.

The four arms use source bits `_api.py`, `_client.py` (0=baseline, 1=reference), with exact source Git blob verification. All four separate Python 3.8 subprocesses completed and returned nine raw functional case records each. No model code or external network was executed.

| Source bits | Target correct /3 | Controls correct /6 | Joint correct /9 |
|---|---:|---:|---:|
| `00` baseline | 0 | 6 | 6 |
| `10` reference `_api.py` only | 1 | 6 | 7 |
| `01` reference `_client.py` only | 2 | 6 | 8 |
| `11` full historical reference | 3 | 6 | 9 |

**Prospective qualification: PASS.** Baseline fails all three default HEAD redirect targets while preserving all six controls; full reference repairs all three while preserving all six; removing either production component loses joint target-plus-control correctness. The heldout two-hop HEAD redirect passes only when the client component is present. This is the **third independently qualified historical issue from a third repository**, following Flask PR6096 and urllib3 PR5071. It is not three model-generated successful repairs.

## Independent read-only evidence audit

A separately implemented auditor imports neither the production source nor the runner. It verifies exact baseline/reference identities, original oracle SHA, four source-blob pairs, SHA manifests, nine unique frozen case IDs per arm, recorded stdout JSON identity, individual pass flags, 36 functional records, and the original qualification decision. Output: `QUALIFIED`, 36 records, five inner payloads verified, zero discrepancies. The nine outer artifact hashes also passed `sha256sum -c`. The original installed distribution list includes `httpcore==0.10.2`, `rfc3986==1.5.0`, `chardet==3.0.4`, and `idna==2.10`.

## Strict limitations

The trusted evaluator intercepts `_send_single_request` with a deterministic in-memory fake transport, while exercising actual historical public entrypoints, redirect processing, and response history. It does not exercise real sockets, HTTP/2, TLS, network timeouts, or the entire upstream suite. The three targets and six controls are correlated within a single issue. The auditor independently checks original records rather than re-running the reference in an entirely separate infrastructure. Historical dependencies were resolved by `pip install -e .` and captured after installation; individual wheel SHA hashes were not prospectively pinned. Qualification supports the frozen nine-case criterion only, not general program correctness.

**No new model inference, no evidence of semantic/dataflow IR superiority, no powered result, no breakthrough.** Do not count these nine cases as nine independent tasks. Continue recruiting truly independent repositories and executing the prospective information-equivalent IR-versus-Python/AST paired model comparison. PR #9 stays draft/unmerged; all 89 reserved issues remain sealed. Historical artifact mirroring remains incomplete.
