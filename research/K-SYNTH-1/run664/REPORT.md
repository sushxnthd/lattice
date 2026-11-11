# Lattice K-SYNTH-1 Run664 — definition-time expressions

Run663's conservative descriptor analyzer still treated method defaults and annotations as inert. Python evaluates these expressions during class creation. In a closed-world two-class witness, a default expression on an unrelated child method executes `setattr(A, 'text', 42)`, replacing the parent `property` with an integer.

Run664 rejects nonempty defaults, parameter/return annotations and type parameters as `UNKNOWN / DEFINITION_TIME_EXPRESSION`. All 16 executable regression/adversarial tests passed. A separately executed fixed synthetic witness confirmed `A().text == B().text == 42`, parent descriptor type `int`, and revised analyzer `UNKNOWN`.

Synthetic static-analysis correction only; no real upstream PR qualification or model comparison. Qualified tasks remain two; all 89 reserved boundary issues sealed. Local archive SHA256 `1122cc3854527d25b42c4a99f32f6811823ef0eb07563e7c226e909ffe7c8110`. Executable/raw GitHub mirroring pending.
