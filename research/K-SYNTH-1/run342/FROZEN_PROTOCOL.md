# K-SYNTH-1 Run342: prospective h11 #115 qualification protocol

Frozen 2026-10-29 UTC **before reference source/diff inspection or historical oracle execution**. Canonical sushxnthd/lattice, branch `research/exp003-context-order`, sole open/draft/unmerged PR #9; all 89 reserved issues SEALED.

## Independent production candidate and provenance

- Repository: `python-hyper/h11`, historical PR [#115](https://github.com/python-hyper/h11/pull/115), addressing LF-only response headers from nonconforming HTTP/1.1 servers (independent issue [#7](https://github.com/python-hyper/h11/issues/7), related HTTPX [#1378](https://github.com/encode/httpx/issues/1378)).
- Exact base `522b00470b5776dda2dc7e98ff778eb1e418e6ad`, independently verified as parent of PR's first commit `fda65a25b30f087b39fd56832fb658284547b12d`.
- Exact reference head `a1197d68630bc37a941b516c7cc74833460fc97c`. These are fixed, NOT floating branch tips.
- Two factorial components across three production files: A=`h11/_receivebuffer.py`; B=`h11/_readers.py` plus `h11/_connection.py`. Tests, docs, metadata excluded from components.
- Original pre-fix source inspected for `ReceiveBuffer.maybe_extract_lines` and `ChunkedReader`, but reference patch/source **not inspected before this freeze**. Base blob SHA: `h11/_receivebuffer.py` `c56749a3a80733d89b6279dc4af7de94cdbea24d`, `h11/_readers.py` `cc86bffb5b36fb019a0bcb53e34d3e439f13f932`, `h11/_connection.py` `410c4e91a04587d4c7254cc5d439b36ce37393f8`.

## Frozen independent public-API oracle

Use `h11.Connection(h11.CLIENT)`, send a GET request and EndOfMessage, feed raw response chunks, normalize `Response(status, headers)`, `Data(bytes)`, `EndOfMessage`, `NEED_DATA` and `RemoteProtocolError`. Compare exact event sequences and payload bytes. No reference-derived expectations.

**Targets (4):** T1 LF-only Content-Length 5 with X-Test and body `hello`; T2 LF-only 204 empty response; T3 LF-only response headers with Transfer-Encoding chunked and standard CRLF chunk frames; T4 LF-only Content-Length response split immediately before the blank-line LF, expecting NEED_DATA before complete response.

**Controls (6):** C1 conventional CRLF Content-Length; C2 CRLF 204; C3 CRLF chunked; C4 CRLF incremental split; C5 invalid status `HTTP/1.1 abc OK\r\n\r\n` must raise RemoteProtocolError; C6 invalid header `BadHeader` must raise RemoteProtocolError. Exact frozen byte strings and event sequences live in `run342_h11_oracle.py`. The separately recorded installed h11 0.16.0 scaffold passed 4/4 targets and 6/6 controls, **not** historical evidence and **not** a qualification result.

## Prospective inclusion/qualification rule

Run **isolated** historical source configurations `base_base`, `ref_A`, `ref_B`, `ref_ref`; no network, no model-generated code. Require: baseline 6/6 controls and at most 2/4 targets; full reference 4/4 targets and 6/6 controls; both single-component arms 6/6 controls and fewer than 4/4 targets; for each component there exists a target repaired by full and failed when that component is omitted. Require additionally either (i) each single-component arm improves at least one target over baseline or (ii) a target has strict synergy pattern (0,0,0,1). **Do not change criteria after outcomes.** If failure, preserve as NOT QUALIFIED.

**ABI negative control:** compare callable signatures, AST call arities and import/call dependencies between all four arms. If a single-component arm's failure is explainable by incompatible callable interfaces, mark `ABI_CONFOUNDED`, and do NOT promote without a separately preregistered, semantics-preserving ABI adapter. No post-outcome adapter is permitted to rescue qualification. Record per-case 2x2 outcome interaction and UNKNOWN for global semantic claims.

## Preoutcome mechanism prediction

Base `ReceiveBuffer.maybe_extract_lines` requires CRLF and `_readers` delegates response parsing to it. Predict T1/T2/T4 are primarily buffer-sensitive; T3 may require buffer plus chunk parser coordination. This is an **unverified** preoutcome prediction; zero casewise interaction, partial arm failures, ABI drift, or failed qualification must be reported unchanged. Neither observed joint necessity nor positive interaction alone proves cross-file semantic mechanism.

## Evidence and model comparison

Preserve exact source SHA, oracle SHA, source-group manifest, every case/arm's normalized events, raw exceptions, stdout/stderr, GitHub Actions IDs and SHA-256 evidence manifest. Independent auditor must replay exact 40 records and detect adversarial mutations. Only **after qualification** consider matched semantic/dataflow IR vs true Python/AST-action model arms with identical task facts, authorized source, edit authority, atomic compiler, isolated oracle, model SHA/seeds/prompts/tokens/raw completions. Do not count deterministic or retrospective repairs as model success. All 89 reserved issues stay sealed.
