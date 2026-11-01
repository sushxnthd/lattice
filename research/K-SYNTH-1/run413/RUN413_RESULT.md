# K-SYNTH-1 Run413: real CONNECT verification and target-identity falsification

Date: 2026-11-01 UTC. ONE K-SYNTH-1 kernel. All 89 reserved boundary issues sealed.

## Executed offline experiments

Built an actual loopback HTTPS CONNECT proxy and separate HTTPS origin with independently generated certificates. The proxy terminates its own TLS handshake, reads a real CONNECT request and tunnels encrypted records to an independent target TLS handshake and HTTP GET. A 16-case factorial varies proxy verification, target verification, proxy CA trust and target CA trust. Expected acceptance: `(not proxy_verify or proxy_trust) and (not target_verify or target_trust)`.

| Installed urllib3 2.7.0 source arm | Correct/16 | False accept | False reject |
|---|---:|---:|---:|
| Unmodified | 12 | 0 | 4 |
| Run411 one-line connection.py edit | 16 | 0 | 0 |
| Run412 exploratory three-line connection.py edit | 16 | 0 | 0 |

Thus Run411's one-line edit genuinely repairs the bounded CONNECT path, despite Run412 proving it fails forwarding. The baseline has two wrong-proxy-policy trust rejections and two verify_mode/check_hostname ValueErrors.

Independently ran four real TLS HTTPS-forwarding proxy cases per arm with trusted proxy certificate: control, wrong *target* assert_hostname, wrong *target* assert_fingerprint and missing *target* client cert. These target-only settings should not change proxy TLS acceptance.

| Arm | Correct/4 | Failed target-only interventions |
|---|---:|---|
| Baseline | 2 | fingerprint, missing client cert |
| One-line edit | 2 | fingerprint, missing client cert |
| Three-line edit | **1** | hostname, fingerprint, missing client cert |

**Counterexample:** The previous Run412 16/16 three-line forwarding fix fails 3/4 target-identity cases. The new tests falsify its general sufficiency; these are post-reference exploratory interventions, not unseen heldout evidence. This confirms that trust, identity and client credentials require distinct oracle coverage.

## Verification

60 original real localhost TLS attempts plus 12 independent identity replays = **72** actual connection attempts. Independent read-only auditor passed **525 assertions** over source SHA, 36 Python files per arm, complete 16-case factorial, CONNECT and origin HTTP traces, identity outcomes and aggregate counts. **8/8 adversarial tests** passed; identity replay matched **84 stable observations**. All non-connection.py source files, including poolmanager.py, were byte-identical.

connection.py SHA-256: baseline `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`; one-line `dbdc023bd113b1df25abe4165af0d821beca43dedcdc86f7a8c79107c06b87cc`; three-line `7cc77c57dd62b148578ebf1510e582f70d8d1826aa6a8137e9721669428418ea`. Shared poolmanager.py `734ae1d2b7140b5b79b431ae51e188800ce512b6ac3cec16c0b881ebb957f293`.

Local clean-extraction reproducibility ZIP: `lattice_run413_real_connect_and_identity_falsification.zip`, SHA-256 `cf15cc5627f2ee8ab436b5c58cb407f24558f9852396be432abf9ff099c1e121`, 138 independently SHA-verified payloads. Full ZIP mirroring to GitHub is not yet complete.

## Nonclaims

urllib3 issue #3472 / PR #5093 remains **NOT QUALIFIED**: the original historical first-parent/reference four-arm cloud artifact was not recovered, no exact historical component necessity was established and no prospective source-distinct heldout was run. The inspected historical workflow uses a mocked policy oracle, not this real TLS transport. Qualified multi-production-source tasks remain **two** (Flask PR6096 and urllib3 PR5071). No new coding-model inference, powered IR advantage or breakthrough.

Next: recover exact historical artifacts and execute frozen full CONNECT/forwarding/identity/fallback four-arm oracle; independently qualify additional production repairs; run matched functional IR/Python coding-model inference. Never touch the 89 sealed issues.
