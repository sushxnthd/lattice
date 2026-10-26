# Run276 prospective qualification: Werkzeug PR2535

This specification and executable harness are frozen **before** source ablation execution. Independent public upstream merged PR: https://github.com/pallets/werkzeug/pull/2535.

- Exact base: `8a782e7a1419d8927350de4d141abdef006635dc`
- Exact direct-child reference: `a80dc5e9398572366061721b8b0cb2307860ce34`
- Production files: `src/werkzeug/routing/matcher.py`, `src/werkzeug/routing/rules.py`.
- Executable harness decompressed SHA256: `ff441b7f7b4d4cdc07f9e1d53d0d7a720b2f3978235eaf94b0a97414a185b4da`
- Canonical `python run276_werkzeug_2535_qualify.py --freeze > RUN276_FROZEN_SPEC.json` output SHA256: `d225b4e0eedd46cbf8f08ebc31666372ec739aff547cd4b79c4a525ff6b60da0`.

Nine public-API checks: three path-converter rules requiring a trailing slash, two valid trailing-slash path-converter matches, a literal leaf match, a literal branch redirect, an unknown path, and a path-converter without a required trailing slash. The first three must return NOT_FOUND on the baseline and REDIRECT to the slash-appended absolute URL on the full reference; the six controls must remain unchanged. Four source configurations: base, matcher.py-only reference, rules.py-only reference, full reference. To qualify, base and full must match all nine frozen outcomes, and each single-file reference ablation must fail at least one target. Exact single-file outcomes are not assumed. All 36 outcomes and source hashes must be retained, including errors.

This establishes necessity of both *reference patch components* under these tests, not impossibility of alternative one-file solutions, model repair, or semantic-IR advantage. If qualification fails, retain the negative result and do not revise frozen expectations. The 89 reserved Lattice boundary issues are not used.
