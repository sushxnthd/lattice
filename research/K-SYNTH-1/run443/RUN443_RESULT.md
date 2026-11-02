# Lattice K-SYNTH-1 Run443 — independent original Qwen audit

Source: GitHub Actions [Run442 41492292650](https://github.com/sushxnthd/lattice/actions/runs/41492292650), completed 2026-11-02 17:47:45 UTC; original artifact ID 13165162902, ZIP SHA-256 `a19cec2b78b8f3ffbd13ede3843a653f4f586a2d1c362095f8f6046009b5cb83`. Model Qwen2.5-Coder-7B-Instruct Q4_K_M SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`.

## Independently audited evidence

- All **30/30** original manifest members verified against SHA-256 and byte counts. Six original raw server responses match their six saved completions byte-for-byte, with original receipt SHA and `finish_reason=stop`. These were six genuine model completions.
- Original frozen compiler returned **INVALID_JSON in 6/6**: every completion was surrounded by a Markdown JSON fence despite explicit instructions. **Primary accepted transactions 0/6**. Posthoc removing one exact fence parses 6/6, but this is a **nonprimary diagnostic** and does not change any original score.
- Flask PR6096: both arm completions byte-identical. Positive control: both identical. urllib3 PR5071: arms differ. The six requests have identical task facts, authority, and prompt body after a **descriptive first-line prefix** (six prompt-token difference per pair). **No distinct instantiated IR vs AST-action representation was supplied. This is not a valid IR-vs-AST efficacy comparison.**
- Flask model edit changes `partition(':')` to `rpartition(':')` in two files. Exact built-in Python primitive witness: `example.com` without a port becomes `''`; `[::1]` without a port becomes `'[:'`. On 10 prospectively frozen host cases, original partition passed 6/10 and model rpartition 5/10. This is **not** a complete Flask public-API oracle.
- Both urllib3 completions introduce `elif port == 0` immediately after `if port is not None`. This branch is **unreachable**: its entry requires `port is None`, contradicting `port == 0`. No generated patch was imported or executed on the host.

## Reproducibility

Full original artifact, raw responses, frozen protocol, independent auditor, primitive traces, 12 passing adversarial tests, clean-extraction replay and SHA manifest in [Run443 archive](https://github.com/sushxnthd/lattice/pull/9) (archive also delivered separately in conversation). Archive SHA-256 `b894184ec82268b664731d835b52b8b4a76b7aad8e2e2c02a084c44be305c25c`. Full ZIP mirroring to GitHub is incomplete.

**Status:** two independently qualified real multi-source repairs, unchanged. No powered McNemar evidence, no semantic-IR superiority or breakthrough. All 89 reserved issues remain sealed. Keep ONE K-SYNTH-1, branch `research/exp003-context-order`, ONE OPEN/DRAFT/UNMERGED PR #9.

## Next: Run444

Prospectively instantiate two structurally distinct information-equivalent IR and Python/AST-action representations, with shared atomic compiler and independent oracle, strict prospective format handling and complete raw inference receipts. Continue exact-PR-parent issue-first qualification; never promote previously failed candidates or retroactively score Run442.
