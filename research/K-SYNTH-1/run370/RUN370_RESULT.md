# K-SYNTH-1 Run370 — reference-blind freeze, ownership counterexamples

**2026-10-30 UTC.** Canonical `sushxnthd/lattice`, one K-SYNTH-1 kernel, branch `research/exp003-context-order`, sole PR #9. All 89 reserved boundary issues remain SEALED.

## Prospective provenance
Selected [encode/httpcore issue #550](https://github.com/encode/httpcore/issues/550) from its pre-fix report, with `httpcore` 0.14.7 source, **before viewing any reference PR**. [The immutable prospective freeze](PROSPECTIVE_FREEZE.md) was committed as `0933976ba3e1443f29176122a453f15b1ca5d464` (Git blob `a48357763948261bbd39fc420c7e1db5cbe70bf8`). It declares six targets, eight controls, and exact-base, all-four-arm, importability, independent-audit and joint-necessity rules. Never revise it after outcome.

Mirrored three original pre-fix source files byte-identically, confirmed by matching Git blobs: sync pool `32bc77895191c35e0f155c913462395f1b2067d6`, async pool `ae3854b1815540625c1dffa1b8503fd9b9f07f44`, synchronization `e7cb1d60c1a6043555e2a9b4f0a2d85089255c7a`.

## Substantive experiment
An executable finite-state model with two requests, one connection and explicit ownership exhaustively explores three timeout cleanup rules:

| Rule | States | Transitions | Orphan-capacity witness | Shared-close witness |
|---|---:|---:|---|---|
| Dequeue only | 42 | 70 | Four steps | None |
| Unconditionally close | 46 | 74 | None | Six steps |
| Close only if unowned | 42 | 72 | None | None |

The third rule is safe **only within this bounded abstraction**. A separately implemented graph interpreter independently checked all counts and witness transitions. The [minimal executable counterexample](run370_minimal_bounded_witness.py) is SHA-identical to the tested local code.

A source-equivalent, scheduler-controlled CPython excerpt replay found 1,024/1,024 sync preassigned-event zero-timeout controls succeed; a timeout decision followed by assignment before cleanup leaves an orphan; 128/128 modern AnyIO zero-timeout waits on already-set events timed out; the excerpt's async dequeue-only cleanup retained an unavailable connection. These are real excerpt executions, **not historical full-tree runs**. The synchronous race requires the timeout decision **before** assignment; a preassigned sync event cannot time out under the tested zero-timeout control.

## Strictly post-reference finding
Only after the freeze, a search located [merged HTTPcore PR #688](https://github.com/encode/httpcore/pull/688), commit `c353ce297502b4c87dab0a59e0d3d2be261574d7`, modifying both production pool files with `if self.connection is None` before waiting. Its historical base is later than the frozen 0.14.7 source, so **it cannot qualify this frozen task**. In a separately labeled post-reference excerpt ablation, the guard fixed the preassigned async zero-timeout symptom (128/128), but the sync timeout-decision → assignment → dequeue race still produced an orphan. This is a bounded insufficiency witness for the guard as a general cleanup proof, not a full-tree regression claim.

Independent audit: three graph modes, three fresh functional replays, 14/14 local tests including tampered evidence rejection. Full raw traces, source-excerpt code, independent verifier, theorem, protocol and SHA manifest are preserved in the Run370 local reproducibility archive.

## Verdict
**INCONCLUSIVE / BASE_MISMATCH.** No new qualified historical repair, no full-tree 2×2 oracle, no new coding-model inference, no powered IR advantage, no breakthrough. Cohort remains **nine unique qualified PRs across seven repositories**. All 89 reserved issues untouched. Next: new exact-base, genuinely independent repair and fair real-model paired trial with actual model/tokenizer SHA and raw completions. Never treat abstract/source-excerpt evidence as historical model performance.
