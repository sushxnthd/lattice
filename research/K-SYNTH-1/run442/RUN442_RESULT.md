# K-SYNTH-1 Run442: real urllib3 port-zero counterexample and complete factorial

Date: 2026-11-02 UTC. Kernel K-SYNTH-1. Canonical branch `research/exp003-context-order`; one draft unmerged PR #9; all 89 reserved boundary issues SEALED.

## Prospectively frozen adversarial prediction

Run441's urllib3 2.7.0 oracle did not cross pool-port and URL-port values. From the original `HTTPConnectionPool.is_same_host` guard `if self.port and not port:`, Run442 predicted that a pool using its default port (80 HTTP or 443 HTTPS) would **incorrectly accept URL port 0 as the same host**. The independent contract treats explicit integer 0 as distinct from the omitted default. The 216-case cross-product (3 hosts × 2 schemes × 6 pool ports × 6 URL ports) was frozen before Run442 source-variant execution; 6 target cases and 210 controls. Frozen SHA-256: `297c998e36204325d56dee8562d3af28b7d1a5df8fc47263ee7be0b2b20784e5`.

## Executed real public-API outcomes

Eight SHA-locked source-component variants were run on the **180 previously frozen Run441 API cases plus the 216 new cross-product cases**. Components: P = `poolmanager.py` (2 guards), U = `util/url.py` (1 guard), C = `connectionpool.py` (2 guards). The original source was archived from locally installed urllib3 2.7.0 with license; edits were confined to AST-verified guard byte spans.

| Components | Correct / 396 | Incorrect |
|---|---:|---:|
| BASE | 372 | 24 |
| P | 384 | 12 |
| U | 378 | 18 |
| C | 378 | 18 |
| PU | 390 | 6 |
| PC | 390 | 6 |
| UC | 384 | 12 |
| PUC | **396** | **0** |

All six newly predicted cross-product targets failed on the baseline and on every variant without C, and passed in every variant with C. All 210 new controls passed in all eight variants. The two-file PU repair that had passed Run441's original 180 cases **fails six new cases**. The minimal executable witness returns `True` incorrectly on the baseline for `HTTPConnectionPool('example.com',80).is_same_host('http://example.com:0/')`, and `False` after the C repair; HTTPS 443 behaves analogously.

The finite factorial decomposes exactly as `errors(S) = 24 - 12*[P in S] - 6*[U in S] - 6*[C in S]`. All pairwise and three-way interactions in correct-case count are **zero**. This is multi-source **coverage necessity** among eight reference-component variants, **not evidence of cross-file causal interaction**. It does not prove that every possible correct repair requires three files.

Independent `python -S -I -B` subprocess replay executed 3,168 further calls, agreeing with all 3,168 original public API calls (6,336 total); 6,360 audit predicates and 14 adversarial/regression tests passed. The local 99-entry archive has 98 SHA-256-verified payloads, raw traces, independent replay, original licensed source, editor, tests and clean-extraction replay. ZIP SHA-256 `c4a0294771281a943b902f1f37edc759e3e47605272b02b33f0875a73074ede3`.

## Scientific interpretation

Run441's frozen 180-case result was valid but incomplete. Run442 adds a real, previously untested port-zero false-positive. It also demonstrates a benchmark construct-validity risk: requiring multiple production-file edits to cover independent endpoints is not the same as requiring cross-file dataflow reasoning. Future qualification should label joint target/control coverage and causal interaction separately; use `UNKNOWN` when interaction is not established.

This is a known-issue, post-Run441 adversarial extension of urllib3 PR5071, **not a new independently qualified issue**, blind localization, model inference, general soundness proof or IR superiority result. Qualified real independent tasks remain **two**; no new coding-model completions or powered evidence. Full local code and raw evidence are preserved in the SHA-verified archive. Next: functional paired open-model inference on Flask PR6096 and urllib3 PR5071, then new independent issue qualification.
