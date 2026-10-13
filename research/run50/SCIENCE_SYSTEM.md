# Run 50 — matched-information verifier control (post-freeze development)

## SCIENCE ledger: one active kernel

| Field | Definition |
|---|---|
| Question | Does explicit semantic IR reduce capable-model repair complexity beyond identical Python facts and verifier/compiler? |
| Best baseline | Python structured edit with the identical semantic frame/compiler (B). Archived 7B pilot on a separate task had zero successes. |
| Intervention | Lattice semantic IR (C) instead of ordinary Python specification (B), preserving semantic facts and frame. |
| Matched-information control | B versus C for representation. For **verifier-only** effect, newly specified A* and B receive byte-identical B Python prompts, but A* has no frame/feedback and B has frame/feedback. |
| Scalar success | Paired fully feature-correct, independently oracle-correct, authorized hidden-test recovery at fixed repair iterations and token budget; record calls, regressions, forbidden states, churn. |
| Alternative explanation | Verifier effect, extra information, prompt/token length, model failure, task difficulty, or evaluation defects. |
| Decisive falsification | No repeatable C-over-B improvement on solvable unseen tasks with independently checked semantics. |
| Publishable threshold | Pre-registered multi-repository tasks, independent evaluator, same compiler, simpler state-machine control, capable models, matched budgets, uncertainty, adversarial ablations, unseen prediction and clean replication. |
| System threshold | Reduced authorized repair cost or regressions without reduced feature completion. |
| Kill condition | Three substantive solvable capable-model comparisons without effect or explanatory boundary; retain compiler/editor, drop language superiority thesis. |

## Exact development-only control counterexample

Run44 frozen ordinary-Python A prompt omits the five explicit semantic fields **authority, protected, states, capabilities, dependency** that B/C/D receive. On itsdangerous, frozen A is 3,964 bytes and B is 4,395; on ticketflow, A is 2,721 and B is 3,093. Thus the original A-vs-B comparison is **not an information-matched verifier-only experiment**, independently of the Run49 A-arm frame leakage.

Run50 defines A* to use **the exact frozen B prompt bytes** with the verifier disabled. B uses the same prompt with the verifier enabled. For a fixed candidate, this isolates verifier acceptance; causal effects on *repair behavior* require a prospective multi-turn experiment with identical starting prompts and different verifier feedback. Original frozen A/B/C/D prompts and tasks are preserved, not silently rewritten.

B/C/D contain the same five semantic facts (including all protected-list members despite different JSON/Python list serialization). Byte lengths B/C differ: 4,395/4,549 and 3,093/3,268, respectively; representation claims still require token accounting and robust controls. The current audit checks literal inclusion, **not full semantic equivalence**.

**Evidence:** `research/run50/evidence/control_audit.json` records frozen prompt SHA-256 and lengths. Local audit used the unmodified Run44 protocol from the Run49 complete archive. Five focused tests passed. No model inference; no representation advantage established; no publication claim.

## SYSTEM ledger

Added a deterministic control-parity audit and exact prompt-sharing helper for an A* vs B verifier experiment. This prevents falsely attributing extra semantic information to verification. Next system milestone is executing a capable-model multi-turn, matched-information experiment with strict Docker scoring and raw transcript attestation, not adding DSL syntax.

## Controlled serendipity

Cheap prompt-asymmetry probe identified a distinct confound. It strengthens the same active kernel; no wildcard replacement.

## Limits and provenance

Post-freeze development evidence only. Frozen Run44 tasks are opened; no independent holdout or capable-model success. The source archive is `lattice_run49_complete_20261013.zip`; no original Run44 hashes or results were altered. CI must not be interpreted as validating unavailable Run44 fixtures. Negative results are retained. No force-push or merge.
