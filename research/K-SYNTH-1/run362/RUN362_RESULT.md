# K-SYNTH-1 Run362: new independent AnyIO PR #595 qualification frozen and launched

Date: 2026-10-30 UTC. Branch `research/exp003-context-order`, sole draft/unmerged PR #9.

## Substantive new task

Selected a **new repository**, `agronholm/anyio`, PR #595 (2023-07-25), distinct from all eight PRs in the verified Run344 cohort ledger. The PR changes two production files with a cancellation/stream-consumption race. Prospectively froze four historical source variants from exact pinned commits and four independently fetched Git blob hashes, six target scenarios and six nonregression controls. Original source verification and functional execution are delegated to an isolated GitHub Actions workflow, which is committed and queued. This is a *candidate* only; the qualified cohort remains eight PRs/seven repositories until original execution and independent audit succeed.

The reference diff was inspected for *qualification design*, not provided to a coding model. No model inference occurred. The frozen 2x2 criterion requires all twelve full-reference outcomes, a failing baseline target with six preserved controls, and distinct partial-component failures. If the reference fails the frozen test, do not modify cases or promote the PR.

## Executable evidence

- Oracle: `run362_anyio_oracle.py`, 12 predeclared asyncio-backend cases, each independently executed with a 3-second deadline.
- Modern AnyIO 4.13.0 / Python 3.13.5 local API **preflight**: 12/12 cases pass. This is NOT historical qualification or evidence about the 2023 source.
- Historical four-variant execution: GitHub Actions workflow `lattice-run362-anyio-qualification.yml`, no-network Docker, read-only source, dropped capabilities, resource limits, Python 3.11.9, pinned idna/sniffio versions.
- Independent auditor: `run362_independent_gate.py` verifies the original SHA manifest, four source Git blob identities, all 48 case outcomes, package import path, Python version, and factorial summary. 13/13 local adversarial tests pass. This tests evidence integrity, not repair correctness.
- Exact source/commit identities, oracle IDs, pass criteria and failure taxonomy are in `PROSPECTIVE_FREEZE.md`.

## GitHub provenance

- Oracle committed `94c53fecc8afa45113305b8c49eb317089cbcf49`, blob `1b27b3855f9e6b1976d9dad068620c8ccfb340cb`.
- Freeze committed `ba5b76fce2878939747c098ef3f737a0d8b0e11d`, blob `5f4a46efbea75f78ec824d6217ba96df4c4271fc`.
- Workflow committed `49aac7be70d0d9f2852a7cbd249cedc0807bab09`, blob `bfa8cbecb09bcc2949cbd4324a874b370827688c`.
- Independent gate committed `ce3885ec3a62993b89fd0c4a80f8587d79e8c43a`, blob `fe29fe09a76643f4b19dce100d40625419b80be4`.
- 13-test suite committed `fa0f151059f7ccbb45668116b999a64e7c452084`, blob `08b6dcadcc7f916c31ac16bec3997f4715e8d53b`.
- Each committed Git blob was independently compared to `git hash-object` of the local file, with exact matches.
- Original workflow run: https://github.com/sushxnthd/lattice/actions/runs/41035497706. Status at last observation: **queued**, no original historical oracle results yet. Subsequent push-triggered runs also queued; do not cherry-pick a favorable run. Audit original run first and preserve all reruns.

## Limitations and next decision

Do not count PR #595 as qualified yet. A modern-version preflight cannot substitute for historical source behavior. The 12 cases are a finite convenience sample, not independent statistical units, and 2x2 necessity does not identify a unique mechanism. A successful factorial qualification is only an eligibility gate for a separately frozen, information-equivalent, token-controlled coding-model experiment. No IR advantage, new model success, statistical significance, or breakthrough is claimed. All 89 reserved boundary issues remain sealed.
