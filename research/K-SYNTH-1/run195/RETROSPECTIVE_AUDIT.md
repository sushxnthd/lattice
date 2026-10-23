# Run195 retrospective mechanism audit of Run194 outputs

**Status:** post-hoc descriptive audit, NOT a preregistered success criterion or a new model run. Input: all 516 raw Qwen2.5-Coder-7B-Instruct responses from Run193/194 (8 GitHub Actions artifacts, workflow run 39923385972).

We removed the exact outer Markdown JSON fence, read the existing `gate` string when present, discarded every other model-produced field, and rescored that one expression with the original `FramedProgram` verifier and independent CPython lowering. This is a permissive diagnostic that violates the original strict output contract; **it is not a replacement primary score**.

| Diagnostic | IR | Python SSA |
|---|---:|---:|
| Responses | 258 | 258 |
| String-valued gate candidate recovered | 236 | 110 |
| Candidate syntactically valid Python | 236 | 88 |
| Gate candidate explicitly references current `gate` | 214 | 87 |
| Literal `gate` identity candidate | 111 | 19 |
| Gate-only semantic successes | **0** | **0** |
| Cycle failures after gate-only normalization | 214 | 87 |
| Wrong-goal failures | 22 | 1 |
| Invalid Python syntax | 0 | 22 |
| Missing gate candidate | 22 | 148 |

**Interpretation:** Output-envelope mismatch is only one failure. Even after generous post-hoc normalization, no model completion repairs the policy. Many candidates attempt a self-reference to the root being replaced, which the existing compiler correctly rejects as a cycle; the frozen benchmark's historical-reference defect makes that particularly important. Neither representation is demonstrated superior, and the difference in candidate recoverability reflects prompt/interface confounds. The original four-family task clustering prevents population-level inference.

The separately preregistered Run195 constrained-JSON pilot is designed to isolate format validity; it must not be pooled with these retrospective counts. Complete local audit script, per-response classifications and raw model responses are preserved in the Run195 archive; original raw outputs remain attached to the Run193 GitHub workflow run.
