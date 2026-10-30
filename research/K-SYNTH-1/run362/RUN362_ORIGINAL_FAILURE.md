# Run362 ORIGINAL workflow failure (preserved, not a model or repair failure)

- Original workflow run: https://github.com/sushxnthd/lattice/actions/runs/41035497706
- Original commit: `49aac7be70d0d9f2852a7cbd249cedc0807bab09`
- Job `qualify` ID `123995195635`, final conclusion `failure`, 2026-10-30 09:45:12 UTC.
- Failure occurred in step 3, **before Docker build, historical oracle or model inference**.
- Exact log excerpt: `fatal: unable to read tree (3f2f1f2f2c8b3b84c133e257af80b4ac4bb18466)`; exit code 128. The PR head Git commit is fetchable by GitHub's contents API but its tree is not available in the default Git clone. No source verification results or functional outcomes were generated. Artifact upload reported no files found.
- Independent GitHub contents reads established that merge commit `6b0a1f351c50119f807ba874e01bb0cf488ecac6` contains the **same exact two pinned source Git blobs** as the PR head: `f8ed75609c0249ddae5273f589e2df6c7194d63f` and `530c60679d98a43e7ae5bdb158473f2b43d0c66e`.
- A separately named Run362b source-transport replay was committed at `6e674bbf62823e4046894af037fd88c8a8b90498` and triggered as https://github.com/sushxnthd/lattice/actions/runs/41035860378. It substitutes only the reachable merge commit for the PR-head checkout; the frozen source Git blob identities, four factorial variants, 12 oracle cases, pass criteria and isolation remain unchanged.
- Classification: **SOURCE_TRANSPORT_FAILURE**, not a failed semantic repair or failed model attempt. Preserve original run, original workflow and logs. Do not count PR #595 as qualified until replay completes and is independently audited.
