# K-SYNTH-1 Run304 independent cloud replication

## Original failed cloud attempt preserved
- Original [workflow run 40614508833](https://github.com/sushxnthd/lattice/actions/runs/40614508833) completed **FAILURE** before functional execution.
- Original artifact 12785025464 ZIP SHA-256 `51c19d70b42e96bfaf675bfbe18e96f4a57930f6a6135679de6923496eca2606`, containing frozen metadata and sources, preserved unchanged.
- Root cause: source-manifest JSON includes `sys.version`, so the local Python 3.13.5 full-manifest hash cannot equal the cloud Python 3.13.x full-manifest hash. This is a replication-contract failure, not a semantic or model failure.

## Corrected cross-environment replication
- Corrected [workflow run 40614571206](https://github.com/sushxnthd/lattice/actions/runs/40614571206) completed **SUCCESS**. The original local result was not rescored.
- Corrected artifact 12784172977 ZIP SHA-256 `ae013b425074ea1ffaef221a1ee20153d632f6fdd84cdc06b6016093317d5390`.
- The correction compares the SHA-256 of the 1,536 ordered `(id, source_sha256)` records, frozen at `a30fb1fac888c840791e76bc4ae57ae1599bc5d317493bc9c600a8a859c0bb10`, rather than environment-dependent `sys.version` metadata. No source, template, expectation, analyzer or oracle logic was changed.
- Independent read-only comparison verified **9/9** cloud manifest hashes: four data entries from the cloud ZIP and five code entries against local SHA-pinned sources. All **1,536/1,536** cloud source records and **1,536/1,536** functional rows matched the local records exactly. Both independent auditors reported **zero discrepancies**, and both identified exactly **512** shadowing-classification corrections.
- Local Python 3.13.5 and cloud Python 3.13.16 have different `sys.version` strings, explaining the different full-manifest roots. The frozen source-only digest and functional results agree.

**Scope:** Two CPython environments, one fixed 24-template suite, 64 correlated seeds per template. This is not a sixth real repair task, model inference, IR superiority or a general Python soundness proof. The failed and corrected workflows are both preserved.

Full local reproducibility archive contains **17 SHA-256-verified payloads**, including both original cloud ZIPs and the independent cross-environment auditor. Final ZIP SHA-256: `6996af8dcb07f6ba189e5758740f7a8cff64e829774ddfbd45f5ddea7172a431`.
