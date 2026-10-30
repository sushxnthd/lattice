# K-SYNTH-1 Run362b: independently verified NEW AnyIO PR #595 does NOT qualify

**Date:** 2026-10-30 UTC. **Outcome:** NOT_QUALIFIED under the original prospective freeze. **No retroactive retuning.**

## Original failure and source-transport replay

The ORIGINAL Run362 workflow [41035497706](https://github.com/sushxnthd/lattice/actions/runs/41035497706) failed before any historical oracle because the deleted PR head tree could not be checked out (`fatal: unable to read tree (3f2f1f2f2c8b3b84c133e257af80b4ac4bb18466)`). It is preserved as a SOURCE_TRANSPORT_FAILURE, not counted as a repair/model failure. Independent GitHub reads established that the reachable merge commit `6b0a1f351c50119f807ba874e01bb0cf488ecac6` contains the two exact pinned PR-head Git blobs, so the separately named [Run362b replay](https://github.com/sushxnthd/lattice/actions/runs/41035860378) changed only source transport, not the frozen scientific contract.

The replay completed SUCCESS. Artifact ID `12967123800`, original ZIP SHA-256 `411d14d6a1092355736830cf4d8c948d4861e68d816e27c9edd655e0ba663f32`, matching GitHub's reported artifact digest. The independent read-only gate verified **9/9 original SHA256 manifest entries**, four historical source Git blobs, all **48** original functional outcomes, 12 exact case IDs in each variant, Python 3.11.9 and historical `/src/anyio` import paths. Its own 13/13 adversarial local tests pass. Original ZIP is included unmodified in the local archive.

## Prospectively frozen 2x2 outcome

| Source configuration | Six targets passed | Six controls passed |
|---|---:|---:|
| Historical baseline | 4 | 6 |
| Asyncio backend only | 6 | 6 |
| Memory stream only | 1 | 6 |
| Both production files | 6 | 6 |

The backend-only change **already passes all 12 frozen cases**, so the original requirement that both components be necessary is not met. The memory-only change additionally loses three previously passing memory-race cases. The three memory cases have casewise factorial correctness interaction +1; the other nine cases have interaction zero. These finite outcomes are not independent samples and do not establish a general theorem about AnyIO.

**Verdict: NOT_QUALIFIED.** Do not add AnyIO #595 to the qualified cohort. The cohort remains **8 unique PRs across 7 repositories**. Do not post-hoc change target cases or pass criteria to promote this candidate. The observed pattern is consistent with a backend cancellation-delivery fix plus a memory-side cleanup that depends on it, but it does not identify a unique causal mechanism or prove the memory change is globally redundant.

## Separate mechanism-identifiability result

The executable `run362_mechanism_nonidentifiability.py` uses the original independently audited Run361 Jinja casewise matrix. Two structural models agree on all 48 observed 2x2 outcomes but differ under seven explicitly hypothetical ABI-shim interventions. This is a constructive counterexample to inferring shim effects or unique mechanism from source-factorial data alone. It is NOT a real Jinja shim experiment.

No new model inference, token-controlled IR-vs-Python comparison, powered advantage or breakthrough occurred. All 89 reserved boundary issues remain sealed; one draft/unmerged PR #9 is maintained.
