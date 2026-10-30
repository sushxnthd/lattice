# K-SYNTH-1 Run356 — independent original Qwen audit and reference expressibility

Date: 2026-10-30 UTC. Branch: `research/exp003-context-order`. One K-SYNTH-1 kernel; PR #9 remains draft; all 89 reserved issues sealed.

## Original Run355 experiment recovered, not rescored

[GitHub Actions run 40991223306](https://github.com/sushxnthd/lattice/actions/runs/40991223306) completed successfully. Original artifact 12950476688 ZIP SHA-256: `06202b2053c84702f805b4e2dd76626f2e979871091d100f94d6c8d4b35187cc`. Independent verification: **27/27** original manifest entries, both frozen source Git blobs, both prompt hashes, fact hash and pinned model SHA.

| Frozen metric | Semantic IR | Python/AST |
|---|---:|---:|
| Actual prompt tokens | 7,301 | 7,848 |
| Completion tokens | 148 | 189 |
| Proposed edits | 2 | 2 |
| Exact old preimage occurrences (sync/async) | 0/0 | 0/0 |
| Compiler accepted | No | No |
| Candidate functional oracle completed | No | No |

Both outputs used nonexistent single-line read-call preimages; the original historical source splits the call across multiple lines. The original compiler's `PREIMAGE_NOT_UNIQUE` label conflates absent and ambiguous substrings; **all four were absent**, independently verified against the original Git-blob-pinned source. The IR output additionally suggested a zero-byte read, while Python/AST suggested modifying trailing data at the wrong location. These are post-outcome diagnostics, not alternative success scores.

The original isolated baseline oracle recorded **6/10** passing cases. Neither candidate reached its functional oracle. The 547-token prompt-length imbalance remains. This run establishes two genuine model completions and two compiler-stage failures, **not functional equivalence, semantic superiority, or successful repair**.

## Reference expressibility, after the freeze

Using [merged HTTPcore PR #882](https://github.com/encode/httpcore/pull/882) strictly as a post-outcome positive control, a new atomic line-addressed compiler reproduced both exact reference source Git blobs:
- Sync `a74ff8e8092f94ccc8dc6b72d1dd8cb6fb49b31c`
- Async `0493a923dc19a1a740a3c1a6f8fb3fbfb429d6f5`

There were **9 line hunks per file, 18 accepted line-addressed edits**. The new grammar uses `{path,start_line,end_line,new}`, full baseline Git-blob pins, authorized paths, bounds, overlap/no-op checks, atomic staging, and AST parse without executing untrusted code.

An independent dynamic-programming calculation over contiguous line-aligned LCS-hunk groupings found that the *old* maximum-three-exact-preimage-actions-per-file grammar needs **15,287 old/new source characters before JSON overhead** to express the reference (7,512 sync + 7,775 async). The new line-action JSON requires **4,909 characters total** and exactly reproduces the reference blobs. This is not a global character-level lower bound and **not an actual Qwen token count**. The original 2,300 completion-token cap may have been restrictive, but token infeasibility is not established.

## Verification and next experiment

**26/26** local tests passed. **1,024** seeded compiler transactions: 256 valid accepted, 768 adversarial rejected, zero independent reconstruction mismatches, zero input mutations. Raw original model outputs, functional baseline traces, source pins, independent auditor, reference action list, DP cost analysis, and test/stress traces are retained in the local SHA-verified Run356 archive.

No new model inference or production repair occurred in Run356. The historical reference-qualified cohort remains eight PRs across seven repositories; failed Werkzeug PR2535 remains unqualified. No powered IR advantage or breakthrough is claimed.

Next: freeze a **new** matched-token paired Qwen study on Jinja #1242 and HTTPcore #882 using the *same new compiler and isolated oracle* for both arms, with no reference-derived localization; prospectively qualify new independent two-source PRs. Preserve PR #9 open/draft/unmerged and all 89 boundary issues sealed.
