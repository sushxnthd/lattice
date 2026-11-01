# K-SYNTH-1 Run412: real TLS forwarding falsifies mocked proxy-policy sufficiency

2026-11-01 UTC. Canonical branch `research/exp003-context-order`, sole draft PR #9. All 89 reserved issues sealed.

## Executed result

Run411's one-statement `HTTPSConnection._connect_tls_proxy` patch passed 8/8 mocked TLS-policy cases. Run412 instead used a real loopback TLS server with an ephemeral self-signed localhost certificate, actual SSL handshakes, and `urllib3.ProxyManager(use_forwarding_for_https=True)` against **installed urllib3 2.7.0**. No external hosts were contacted; the proxy returned a fixed HTTP response to an absolute-form HTTPS URL. This tests proxy TLS in HTTPS **forwarding** mode, **not CONNECT or target TLS**.

After an initial 8-case exploratory diagnostic, a separately frozen expansion exercised 2 proxy verification settings x 2 target verification settings x 2 CA trust settings x 2 proxy hostname settings = 16 real TLS cases per arm. The independently specified acceptance contract is `not proxy_verify or (ca_trusted and proxy_host == "localhost")`.

| Arm | Correct/16 | False acceptance | False rejection | Certificate-verified rejections |
|---|---:|---:|---:|---:|
| Byte-identical installed baseline | 8 | 3 | 5 | 3 |
| Run411 `_connect_tls_proxy`-only patch | 8 | 3 | 5 | 3 |
| New exploratory **single-file two-path** `connection.py` patch | 16 | 0 | 0 | 6 |

The original and Run411 patch **accepted an untrusted HTTPS proxy certificate when proxy verification was required but target verification was disabled**, and also accepted a proxy certificate with the wrong hostname in one case. Conversely, they rejected five permitted connections because target TLS policy overrode proxy policy. The one-line patch never executes on the forwarding path, so its earlier 8/8 mocked result was insufficient to establish real transport correctness.

The exploratory patch modifies **three existing lines in `connection.py` only**: one `_connect_tls_proxy` policy argument, plus forwarding `cert_reqs` and `ssl_context` arguments inside `HTTPSConnection.connect`. `poolmanager.py` and every other Python source file are byte-identical across all three arms. This is **bounded one-file sufficiency**, not a historical PR5093 replacement or proof that two files are unnecessary for the full historical contract.

## Exact finite-grid mechanism

Independent exhaustive enumeration establishes the exact 16-point acceptance function `accepted = not target_verify` in both the baseline and Run411 one-line arms. In the exploratory two-path arm, the exact function is `accepted = not proxy_verify or (ca_trusted and proxy_hostname_matches)`. All eight target-verification interventions flip acceptance in the first two arms, and none flip acceptance in the corrected arm. This is an **exact finite-grid counterexample**, not a theorem about every urllib3 execution path. The standalone `run412_boolean_mechanism.py` and raw result are preserved in the local Run412 reproducibility ZIP.

## Verification

48 original real TLS handshakes; 48 additional independently replayed handshakes. Read-only auditor: **449 checks, zero disagreements**; independent replay: **559 stable checks, zero disagreements**; **7/7 adversarial tests** passed, including source tampering, fake certificate rejection, duplicate cases and falsified result fields.

Source SHA-256 `connection.py`: baseline `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`; Run411 one-line `dbdc023bd113b1df25abe4165af0d821beca43dedcdc86f7a8c79107c06b87cc`; exploratory two-path `7cc77c57dd62b148578ebf1510e582f70d8d1826aa6a8137e9721669428418ea`. Common `poolmanager.py` SHA-256 `734ae1d2b7140b5b79b431ae51e188800ce512b6ac3cec16c0b881ebb957f293`.

## Strict interpretation

**urllib3 #3472 / PR #5093 remains NOT QUALIFIED.** No pinned historical-base/reference four-arm oracle, real CONNECT/target TLS, independent heldout programs, or original prospectively frozen joint component necessity was established. The exploratory three-line patch was designed after inspecting failures and cannot be counted as prospective. The 16 cases are not 16 independent repair issues. No model inference or semantic-IR superiority claim. Historical qualified real multi-source repair count remains **two**.

Complete raw evidence, local source copies, code, independent auditor, adversarial tests, replay, SHA manifest and ZIP are preserved in the Run412 local artifact. GitHub historical ZIP mirroring is incomplete. The next decisive test is pinned historical four-arm source ablation with real CONNECT and independent target/proxy CAs, while expanding real issue-first repair qualification.