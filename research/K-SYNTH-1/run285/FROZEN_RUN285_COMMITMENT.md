# Run285 prospective multi-idle holdout commitment (2026-10-27 IST)

This commitment precedes any Run285 upstream functional-oracle execution. **No real HTTPcore outcomes have been observed.**

- Frozen complete local JSON SHA-256: `811e33423dc734ab5d0fbe72de4e9c5277b68bed86315b9e7373c01b157be571`.
- Pinned base: `5974b03c7df89d3ee4e23779900d5349d550753c`.
- Pinned source-identical direct-child reference: `10a658221deb38a4c5b16db55ab554b0bf731707`.
- Sync source SHA base/ref: `6be4fc2d3b14c5ceebd16c356ad7c7483a163e34347c0f1497b4b7f85d0c8fbd` / `c9f87e893f679d23053ba00ee971904780c0348f2aa96987a3ff56a14f40279d`.
- Async source SHA base/ref: `0ce210dacd9909ff6a7f0c61ccca6b4cf2ea08bf0ec465e2285eaa447c6f5726` / `42a35957e780753c59d05058209dcd0a2e0d50c25afca0939c42768ca243eb5c`.
- Frozen generated network-disabled public API oracle SHA-256: `b81b7c1b469f42a3d2d38b7f2f472ab3095178043eab1b5fd34efb52a99bbcc0`.
- Case triples (initial idle m, keepalive k, new active q): (2,2,1), (2,2,2), (2,2,3), (2,3,2), (2,3,3), (3,3,1), (3,3,2), (3,3,3), (3,3,4), (3,4,2), (3,4,3), (3,4,4), (4,5,2), (4,5,3), (4,5,4). Each tested sync and async (30 cases) across baseline, sync-only, async-only and full reference (120 predictions).
- Each case expects `before=m`. For reference-corrected mode expect `during=m`. For original mode expect `during=min(m,max(0,k-q+1))`. All four arms use the same pinned public API mock backend and isolated network-disabled oracle.
- Missing cases, import errors, timeouts and malformed observations are **CENSORED**, never scored as functional repair failures.
- This is a within-issue holdout, **not** a fifth independent issue. Run283 failed 8/32; Run284 passed 72/72; preserve both unchanged.
- Original local executable bundle, raw abstract traces and SHA manifests are retained in Run285 local reproducibility archive. This GitHub commitment is a summary, not a replacement for the exact frozen JSON bytes.
- All 89 reserved boundary issues SEALED. ONE K-SYNTH-1 kernel, ONE OPEN/DRAFT/UNMERGED PR #9.
