# Lattice K-SYNTH-1 Run302: original Qwen audit and parser-frontier counterexample

**Prospectively frozen**: [Run302 protocol](PROTOCOL.md) committed `2aee2823dfefe16de6987a7283aae19e150af9a0`; [512-case fixture SHA freeze](FROZEN_FIXTURES.md) committed `e473d87b4b176bdb89d1d49d7b19ea7577f778eb` before new trusted-source executions.

## ORIGINAL Run301 Qwen2.5-Coder-7B result, immutable

Original [cloud run 40595510454](https://github.com/sushxnthd/lattice/actions/runs/40595510454), artifact ID `12777745815`, original ZIP SHA-256 `d8feadc2c2328f76c1aaf4548871b490d2ded4abd3817d1848fe7345726a672a`. Independent read-only audit verified **84/84** original evidence hashes, exact frozen prompt/request hashes, response-to-completion byte identity, usage, seed `301001`, model SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, compiler decisions, staged file hash and isolated oracle records.

| Original arm | Input/output tokens | Finish | Shared compiler | Frozen isolated oracle |
|---|---:|---|---|---|
| Semantic-IR presentation | 4,222 / 768 | length (truncated) | INVALID_JSON | NO_ORACLE |
| Ordinary Python/AST presentation | 4,246 / 211 | stop | ACCEPTED | **0/5 LF targets, 5/5 CRLF controls** |

The IR response included pseudo-source labels (`LINES 70-81`) instead of exact source and exhausted the token cap; no patch was accepted. The Python/AST response was a genuine one-edit transaction; the exact staged `h11/_readers.py` SHA-256 was independently verified as `f1cec1f102fecd29a459a077b294ae5ace2f998200e42a78926051e20f38232e`. Its accepted patch did **not** solve the issue. No IR-versus-Python success claim follows from this single paired task.

## NEW prospective trusted-source functional experiment

**512/512** frozen predictions matched trusted historical h11, with **0/512** independent replay disagreements. Design: 16 request variants × 8 delimiter families × 4 fragmentations (whole, split, three, bytewise). The 128 valid CRLF-framed traces succeeded; 384 malformed or LF-only traces did not. These are correlated traces, not independent repair issues. Frozen fixture manifest SHA-256: `efca87263ce57d6116599772b9c769df1d11c5a3ede0b02ebaaa956e738b2f1b`.

**Bounded mechanism:** `ReceiveBuffer.maybe_extract_lines()` waits for `\r\n\r\n`, so LF-only messages do not reach the modified request-line reader. However, a malformed CRLF-framed request containing a bare LF immediately before the line's CRLF separator *does* reach that reader with the bare LF still attached. In 64 prospectively frozen variants, the strict request-line regex rejected the line and the diagnostic stripped-LF version matched. Thus the model edit is not universally dead; it is at the wrong upstream boundary for LF-only repair and may loosen acceptance of malformed requests. **This is a source-level counterfactual, not yet a verified full-message acceptance or security exploit.**

## Independent cloud witness and preservation

An isolated, no-network Docker witness for the **original unmodified model-generated candidate** was committed at [lattice-run302-witness.yml](https://github.com/sushxnthd/lattice/blob/research/exp003-context-order/.github/workflows/lattice-run302-witness.yml). Its initial source-path error was corrected, preserving both attempts. [Original attempt](https://github.com/sushxnthd/lattice/actions/runs/40599715219) and [corrected attempt](https://github.com/sushxnthd/lattice/actions/runs/40599735911) were queued at the last check. Do not promote unverified cloud outcomes. No model-generated code was executed on the host.

Complete local reproducibility archive `lattice_run302_original_model_audit_and_delimiter_counterexample.zip` SHA-256 `5cc4cc6189e02e6bfe781578ec23b087abfda5ef66bedc8a5811aa4f2f08ade8`, containing original cloud ZIP, original evidence manifest, trusted source, 512 frozen cases, 512 raw functional traces, 512 independent replays, independent original audit and executable scripts. Historical GitHub archive mirroring remains incomplete.

**Status:** five qualified independent real multi-production-file repairs, no sixth, no powered IR advantage or breakthrough. All 89 reserved boundary issues SEALED. One K-SYNTH-1 kernel, branch `research/exp003-context-order`, one OPEN/DRAFT/UNMERGED PR #9. Failed Werkzeug PR2535 and Click PR2956 remain failed.

**Run303:** Audit both original and corrected isolated witness artifacts, report any malformed-message acceptance narrowly, then prospectively qualify a sixth independently selected multi-production-source repair with joint target/control necessity and run valid paired capable-model inference. Keep all original outcomes immutable.
