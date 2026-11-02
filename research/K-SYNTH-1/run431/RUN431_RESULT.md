# K-SYNTH-1 Run431 — original historical HTTPX replay independently audited

**Decision: NOT QUALIFIED.** The original Run430 historical HTTPX #1833 workflow [41393308474](https://github.com/sushxnthd/lattice/actions/runs/41393308474) completed successfully. Its original artifact 13117874956 was recovered; ZIP SHA-256 `29fc7159730814d2ff06f6038ea2076d9ee66c6a75ab0ed51a3fa76e2e833da3` matches the GitHub artifact digest. All 14 original embedded payload hashes, original raw stdout/JSONL equivalence, 32 genuine historical functional observations and import-failure receipts passed an independent read-only audit. GitHub commit metadata independently confirms merge `57daabf673705954afa94686c0002801c93d31f3` and first parent `7c53d99da8351eea5ff71e1fa829e1d2e9727c0d`.

| Variant | Frozen targets | Frozen controls | Interpretation |
|---|---:|---:|---|
| Base | 0/2 | 6/6 | Negative baseline |
| Full reference | 2/2 | 6/6 | Passes finite oracle |
| One-file query stripping | 2/2 | **5/6** | Fails fragment-only query-preservation control |
| Parser-only reference | 0/2 | 6/6 | No target repair |
| URL-only reference | N/A | N/A | Import fails: missing `httpx._urlparse` |

**New finite-oracle result:** The four importable variants form three observational equivalence classes on the eight frozen cases: `{base, parser-only}`, `{one-file}`, `{full reference}`. Exhaustive subset enumeration proves exactly two minimum two-case distinguishing witnesses: indices `(0,6)` and `(1,6)`. A positive malformed-query target and the fragment-only query-preservation control are both needed. This is a finite result, not a universal semantic equivalence theorem or a proof of intrinsic multi-file necessity.

**New post-reference mechanism test:** 512 real HTTPX 0.28.1 public-API URL joins, checked against `urllib.parse.urljoin`, plus a query-prestripping surrogate: 256/256 fragment-only queries preserved by HTTPX and stdlib, 0/256 preserved by the surrogate; 128 path-change and 128 query-replace controls agree in both arms. An independent stdlib-only auditor recomputed 1,024 expected/surrogate joins with zero disagreements. Twelve adversarial/regression tests passed. The surrogate is not historical source-level qualification.

**Status:** Only two independently qualified real multi-source repairs (Flask PR6096 and urllib3 PR5071). No new coding-model completions, powered IR superiority or breakthrough. The 89 reserved boundary issues remain sealed. PR #9 remains draft and unmerged. Run428 historical workflow failure and incomplete historical ZIP mirroring remain open.

The complete local reproducibility ZIP includes original cloud artifact, raw traces, independent auditors, tests, full report and SHA-256 manifest.

### Run428 historical retry completed and independently audited

The corrected [Run428 historical workflow 41400313503](https://github.com/sushxnthd/lattice/actions/runs/41400313503) **completed SUCCESS** across all three pinned historical refs. Original artifacts 13120783856 (issue base), 13120873542 (PR parent), and 13120459977 (PR reference) were downloaded. All three original ZIP SHA-256 hashes matched GitHub's published digests; internal JSON receipt SHA-256 checks passed. Independent replay recomputed **42/42** original frozen case predicates. Issue base: **2/6 targets, 8/8 controls**; PR parent: **2/6, 8/8**; PR reference: **6/6, 8/8**. The missing generated `urllib3._version` was supplied by a recorded, import-only in-memory metadata shim for two refs; upstream source bytes and the frozen oracle were not modified. **14/14** local tests passed.

This is **not a third qualified multi-source repair**: urllib3 PR #4952 changes only one production Python file, and the server-only path oracle retains the previously identified raw-wire normalization ambiguity. The failed original workflow and corrected retry remain distinct immutable evidence.
