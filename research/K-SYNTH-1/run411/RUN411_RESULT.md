# K-SYNTH-1 Run411: one-file sufficiency diagnostic for urllib3 #3472

Date: 2026-11-01. Sole kernel K-SYNTH-1; branch `research/exp003-context-order`; PR #9 remains draft. All 89 reserved issues sealed.

## Executed finding

[Issue #3472](https://github.com/urllib3/urllib3/issues/3472) was closed as fixed by [merged PR #5093](https://github.com/urllib3/urllib3/pull/5093), which modifies two production files (`src/urllib3/connection.py`, `src/urllib3/poolmanager.py`), tests and changelog. **Two changed files do not establish two-file behavioral necessity.**

An exploratory local ablation copied actual installed `urllib3==2.7.0` to isolated source roots and changed exactly one production statement in `HTTPSConnection._connect_tls_proxy`, choosing the explicit proxy context's `verify_mode` rather than the destination connection's `cert_reqs`. `poolmanager.py` and all other Python source files were byte-identical.

The trusted oracle executed real urllib3 TLS-policy code with socket I/O mocked: **baseline 5/8, one-file fix 8/8**. Baseline failed three cross-policy cases (verified proxy/unverified destination with and without hostname checking; unverified proxy/verified destination). Both no-explicit-proxy-context controls passed in both arms. Independent read-only SHA/source-scope audit: **122 checks, zero disagreements**, including two fresh isolated subprocess replays. **11/11** tests passed.

Installed `connection.py` SHA256 `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`; one-file variant `dbdc023bd113b1df25abe4165af0d821beca43dedcdc86f7a8c79107c06b87cc`; unchanged `poolmanager.py` `734ae1d2b7140b5b79b431ae51e188800ce512b6ac3cec16c0b881ebb957f293`. Local 13-entry SHA-verified reproducibility archive SHA256 `d19ad8bfccbbcae5e96aed0b15e2e138c2e860265adc8f81797229860236f339`.

## Limitations and strict gate

This is **not** a pinned historical PR #5093 base/reference ablation. The eight cases were designed after reference inspection, use mocked transport rather than real HTTPS CONNECT, and do not prove the historical `poolmanager.py` change unnecessary for forwarding, fallback, identity, or other controls. The result only refutes *universal* two-file necessity for this bounded oracle.

**urllib3 #3472 remains NOT QUALIFIED**: no prospective source-distinct heldout set, pinned four-arm reference comparison, or genuine joint target-plus-control component necessity. Original Run410 freeze unchanged; no retrospective promotion.

Historical qualified real multi-source count remains **two** (Flask PR6096 and urllib3 PR5071). No new model inference, powered semantic-IR advantage or breakthrough. Next: exact PR #5093 first-parent/full-reference four-arm experiment with real loopback HTTPS proxy and distinct CAs, and new independent issue-first qualification. Preserve all 89 sealed cases.