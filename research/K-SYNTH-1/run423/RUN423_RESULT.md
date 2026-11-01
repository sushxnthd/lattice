# K-SYNTH-1 Run423: production repair replay and isolation failure

**Verdict:** Five of five real production conditional edit sites from urllib3 PR5071 were expressible in the Run422 typed MAY-dataflow action encoding and ordinary AST actions through the same Run419 compiler. Seven nonempty source variants compiled byte-identically in both arms. This was a **post-reference** study on the complete locally installed urllib3 2.7.0 package, **not** the exact historical PR-base tree and not a new qualified repair or coding-model inference.

## Executed evidence

- 8 factorial source variants over three production files; 50 no-network urllib3 API observations per variant = **400 primary functional observations**.
- The full historical edit changes 10/50 observations relative to the installed base, preserving 40/40 controls.
- Component agreement with the full edit on the ten changed observations: base 0; url only 2; poolmanager only 6; poolmanager+url 8; connectionpool only 2; connectionpool+url 4; connectionpool+poolmanager 8; full 10. All arms preserved 40/40 controls.
- An independent exact-preimage byte-replacement auditor rebuilt all eight variants without the typed/AST compiler and independently executed **400 further CPython API observations plus 44 source/anchor checks**, 444 checks, zero disagreements.
- 12 adversarial and regression tests passed.
- **Important contamination counterexample:** In this runtime, Python startup hooks preload `urllib3` into `sys.modules`. A naive `sys.path.insert(0, isolated_dir)` still imported the unmodified installed library, falsely reporting zero behavior differences. Corrected subprocesses evict all cached urllib3 modules, assert the isolated import path, and remove stale pycache. The naive zero-difference result is invalid.

## Historical source audit

The actual PR was https://github.com/urllib3/urllib3/pull/5071. Independently read the complete upstream production files at merge commit `f5cf122346141b187cca0db6e6445297d336b610^` and confirmed each of the five original preimage anchors occurs exactly once. Historical blob SHA-1: connectionpool `7e6f54c82e3b8d4b5bfee7b48c8717fa2b650f1f`, poolmanager `b7248d210dc8adea1b48dccab2c08860ad543328`, util/url `6d0c66a30f5abea74db7bf0cd99da1c62b23a10d`. These historical hashes differ from the executed installed-source hashes. Historical Flask PR6096 anchors were likewise inspected, but its full compiler replay was not executed.

## Interpretation

This is evidence of production editor **expressibility and parity**, not semantic-IR superiority, sound noninterference, prospective repair qualification, or powered model performance. The two independently qualified real multi-production-source tasks remain Flask PR6096 and urllib3 PR5071. No new coding-model completions were obtained. The 89 reserved boundary issues remain sealed. The SHA-verified local reproducibility archive includes the complete installed source package, license, scripts, raw traces, independent auditor and tests; historical GitHub ZIP mirroring remains incomplete.

Next: exact historical-base replay, new prospectively frozen two-source repairs, functional matched open-model inference, and independently isolated oracles.