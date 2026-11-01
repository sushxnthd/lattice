# K-SYNTH-1 Run414: exact historical four-arm real TLS component-necessity diagnostic

Date: 2026-11-01 UTC. Canonical `sushxnthd/lattice`, branch `research/exp003-context-order`, sole PR #9. All 89 reserved issues sealed. **No new model inference.**

## Original historical artifact recovered and transport failure

Recovered [original Run411 Actions 41298036956](https://github.com/sushxnthd/lattice/actions/runs/41298036956), artifact `13080355960`, ZIP SHA-256 `48a973c69e9d1e9e27fce0e9e2283baee8c2b36342f102b2d246791ffa152ca1`. The job was marked success even though all four oracle subprocesses exited 1 with `ModuleNotFoundError: urllib3._version`: historical git archives omit the generated module and the workflow had ignored subprocess exit codes. **Those are transport failures, not repair outcomes.**

Restored the same generated-version import shim to all four arms without changing either historical production file or the frozen mock oracle, and enforced successful subprocess exit/JSON. [Restored Actions 41311026343](https://github.com/sushxnthd/lattice/actions/runs/41311026343), artifact `13085322562`, ZIP SHA-256 `57c3af4c99af68a261d6c0bbb9567375e2e2289a922601f6d9f0b2f7117b0048`, succeeded. Exact first-parent base `e6cc4bf15798176c22bfcec7e4854cc42b6e25e2`, merge `07408cec79d1856d81bb42c74a904a24fdb9e465`.

The unchanged eight-case mock SSL-policy oracle: base **5/8**, connection-only **8/8**, poolmanager-only **5/8**, full **8/8**. All 16 corresponding raw row pairs (base versus poolmanager-only; connection-only versus full) were exactly equal.

## New actual HTTPS proxy experiments at exact historical source

Ran actual isolated localhost TLS handshakes through a forwarding HTTPS proxy with generated certificates, independent trust/hostname interventions and target-only identity/credential interventions. [Original real-TLS Actions 41311201155](https://github.com/sushxnthd/lattice/actions/runs/41311201155), artifact `13085084123`, ZIP SHA-256 `eaae8cda70c6f813ca5a6a5b2107474a2ed6d09426afe1cd333414582da2e5bf`. [Expanded real-TLS and fallback Actions 41311273641](https://github.com/sushxnthd/lattice/actions/runs/41311273641), artifact `13084534772`, ZIP SHA-256 `20a8aa8c6a80c77d43c8aeae4306183d240ec4017b55dd93f2ccf8442450e2f8`.

| Exact historical arm | Forwarding + identity /19 | Explicit/fallback SSL contexts /16 | Total /35 |
|---|---:|---:|---:|
| Base | 11 | 13 | **24** |
| `connection.py` only | 19 | 16 | **35** |
| `poolmanager.py` only | 11 | 11 | **22** |
| Full two-file reference | 19 | 16 | **35** |

Across the **140 actual localhost TLS trials in the expanded artifact**, connection-only and full reference have zero acceptance disagreements in 35 matched cases. Poolmanager-only causes two additional fallback false rejections relative to base (cases 6 and 7). The exact 2x2 correctness interaction is **+2**, entirely from fallback; the marginal contribution of poolmanager conditional on the connection fix is zero on this finite grid. No unsafe false acceptances observed in these cases.

An independent read-only auditor performed **499 checks** with zero disagreements, including all payload SHA-256 digests, exact historical source hashes, source-arm topology, pinned commits, case facts, real proxy HTTP observations, scores and failure consistency. **19 regression/adversarial tests passed**, including forged source SHA, corrupted manifest, forged scores and the original import-transport failure. Complete raw artifacts and local audit code are in the SHA-verified Run414 reproducibility archive.

## Strict scope and decision

The historical two-file diff is **not evidence of two-file behavioral necessity**. On these 35 post-reference real TLS conditions, the exact historical `connection.py` edit alone is sufficient, while `poolmanager.py` has no additional benefit. This **does not prove global redundancy**: untested public behavior could require both files. The diagnostic is post-reference, not prospectively source-distinct heldout evidence, and cannot redefine the Run410 frozen qualification gate. **urllib3 issue #3472 / PR #5093 remains NOT QUALIFIED.** Qualified real repairs remain Flask PR6096 and urllib3 PR5071 only.

No new capable-model inference, powered semantic-IR superiority, or breakthrough. Next priority is a fresh issue-first real two-source repair with prospectively frozen source-distinct public/heldout/nonregression and an equal-information functional semantic-IR versus Python/AST-action model comparison. All 89 reserved boundary issues remain sealed.
