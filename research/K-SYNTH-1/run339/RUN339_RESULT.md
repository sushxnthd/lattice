# K-SYNTH-1 Run339: real Rich ABI-factorized necessity falsification

2026-10-29 UTC. **Post-outcome mechanistic experiment only** on previously FAILED Rich PR #3180. Do not promote Rich to qualified. All 89 reserved boundary issues SEALED.

Replayed all **80/80** original Run338 frozen arm/case records (20 cases × four source combinations), matching exact cuts, widths, exceptions and outcomes. The historical baseline files' Git blob SHAs were checked. The reference `divide_line` and `chop_cells` function bodies were transcribed from the public historical source. Local `wcwidth` table used in place of historical Unicode table, with 80/80 original parity required. Independently audited 80/80 new ABI-bridge records, 6/6 adversarial corruptions detected, 512/512 seeded adapter equivalences, and explicit nonzero-position rejection.

| Source combination | Original repair targets /11 | ABI-only bridge targets /11 | Bridge controls /9 |
|---|---:|---:|---:|
| base wrap + base cells | 4 | 4 | 8 |
| base wrap + ref cells | 0 (11 TypeErrors) | **11** | 8 |
| ref wrap + base cells | 0 (11 TypeErrors) | 4 | 8 |
| ref wrap + ref cells | 11 | 11 | 8 |

The bridge only translates `max_size` ↔ `width`, requiring `position=0`; it never alters callee return values or semantic algorithms. On the frozen 11 targets, reference `cells.py` alone repairs every target once the ABI mismatch is removed. Reference `_wrap.py` contributes **zero** additional target passes on these cases. This is a finite, real-production counterexample to interpreting naive source-swap necessity as semantic necessity.

Naive 2x2 target-count interaction: `11 - 0 - 0 + 4 = +15`. ABI-factored interaction: `11 - 4 - 11 + 4 = 0`. The entire apparent interaction disappears under compatibility-only bridging. The unchanged `hello world`, width-5 control still fails in all four arms (8/9 controls), so Rich remains **NOT QUALIFIED**.

**Limits:** post-outcome analysis; manually transcribed reference functions, not independently exact reference Git blobs; parity verified only on the 20 original cases; no installed Console integration; no new coding-model inference, no powered semantic-IR advantage.

**Prospective next candidate:** [HTTPcore PR #882](https://github.com/encode/httpcore/pull/882), [issue #872](https://github.com/encode/httpcore/issues/872). Frozen public-API protocol [PROTOCOL_RUN340.md](PROTOCOL_RUN340.md), committed **before reference patch inspection** at `84b77aba6974119955a898fdef3bcbe94eddbfb9`. Qualification PENDING. Exact pinned historical source SHAs, four CONNECT/Upgrade targets, six controls, four sync/async source arms and ABI negative control are in protocol.

Qualified repositories remain **Flask, urllib3, HTTPX (three)**. [Draft PR #9](https://github.com/sushxnthd/lattice/pull/9) must stay open/unmerged. All 89 reserved issues sealed. No superiority or breakthrough claim.

Local full SHA-verified evidence archive includes original raw Run338 records, baseline sources, functional runner, independent auditor, 160 original/bridged traces, 512 property checks, six adversarial tests, protocol and full report.

## Run340 implementation status at end of Run339

The frozen ten-case sync/async public-API oracle and independently implemented qualification auditor were committed at `764a3554c6f7b672074f7ec613c2e5e5bc7eee45` and `46636496e55bdea1c0445cd9b27ab3489793a02d`. A push-triggered historical four-arm GitHub Actions workflow was committed at `06bd9a582bd312c45a58182e3997277144e58710` ([workflow](https://github.com/sushxnthd/lattice/actions/workflows/lattice-k-synth-1-run340-httpcore.yml)). The local scaffold using **installed HTTPcore 1.0.9**, not the pinned historical source, passed **10/10** cases. This is a harness smoke test only, not historical qualification. The historical GitHub Actions run ID/results have **not** been recovered or independently verified. Do not count this as a fourth qualified repository.
