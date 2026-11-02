# K-SYNTH-1 Run430 — issue-first dependency closure and URL-oracle screening

**Decision:** Three historical HTTPX issues were frozen *before* consulting fixing PRs or issue comments. No new independently qualified multi-production-source repair. Qualified count stays **two** (Flask PR6096, urllib3 PR5071). No new model inference or IR superiority.

## Freeze
[Original issue-first freeze](RUN430_PROSPECTIVE_FREEZE.md) was committed as \`adbd1c6649b3ffe0704f3d410796f47cfe3fa3fc\` before reference inspection. Primary HTTPX #911, secondary #318 and #1833; unchanged original qualification rules.

## Post-freeze source adjudication
- [HTTPX #911](https://github.com/encode/httpx/issues/911): issue discussion says resolved by **httpcore >=0.8.3** (comment 625077272), not a multi-production-source HTTPX patch. **Reject** as cross-repository dependency-closure confound.
- [HTTPX #318](https://github.com/encode/httpx/issues/318): [PR #321](https://github.com/encode/httpx/pull/321) changes only \`httpx/middleware.py\`. **Reject** as one production Python file.
- [HTTPX #1833](https://github.com/encode/httpx/issues/1833): [PR #2252](https://github.com/encode/httpx/pull/2252) changes \`httpx/_urls.py\` and introduces \`httpx/_urlparse.py\`; merged reference \`57daabf673705954afa94686c0002801c93d31f3\`. **Not qualified**: import-only reference ablations cannot establish irreducible multi-source repair; historical factorial replay still unverified.

A dependency upgrade can change consumer behavior without changing consumer source. Source-level repair attribution therefore requires a pinned transitive dependency closure.

## Genuine executed exploratory production-library observations
- Installed HTTPX 0.28.1 / CPython 3.13.5: 192 constructed URL joins (4 paths x 8 queries x 6 relatives), **192/192** matching \`urllib.parse.urljoin\`; zero exceptions.
- Isolated loopback HTTPX AsyncClient forward proxy: **9 actual HTTP requests** in seven cases, with two target hosts, 302 and followed redirects, and direct non-proxy control. Raw request-line bytes and Host captured alongside public \`response.url\`/history; **31/31** primary predicates passed.
- Independently implemented auditor replayed 192 joins, validated proxy receipts, and made **8 additional raw-socket HTTP requests**; **1,031 predicate checks, zero disagreements**, three corrupt/duplicate receipts rejected.
- **12/12** adversarial/regression unit tests passed.

These are **post-freeze newer-release diagnostics**, not historical repair qualification or model outputs.

## Exact historical replay prepared, not verified
[Runner](run430_historical_httpx.py) and [isolated Actions workflow](../../../.github/workflows/lattice-k-synth-1-run430-historical.yml) committed. The workflow clones upstream, derives the exact first parent of merge \`57daabf...\`, and tests five source variants: base, full reference, one-file query-strip alternative from original issue, reference \`_urls.py\` only and reference \`_urlparse.py\` only. It preserves source SHA-256, import paths, raw cases and stderr/stdout.

**Cloud execution result/artifact not retrieved or verified at this report.** Do not infer success from workflow creation. Future run must retrieve original ZIP and independently audit.

## Boundaries
One K-SYNTH-1 kernel; one research branch \`research/exp003-context-order\`; [PR #9](https://github.com/sushxnthd/lattice/pull/9) open/draft/unmerged; all 89 reserved boundary issues sealed. Original Run428 artifact verification and historical ZIP mirroring remain incomplete. No superiority, statistical significance or breakthrough claim.

Local reproduction and raw receipts are in the separately SHA-256-verified Run430 archive. Next: [Run431 protocol](PROTOCOL_RUN431.md).
