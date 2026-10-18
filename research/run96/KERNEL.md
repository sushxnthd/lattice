# Run96 — Structural view versus Python, same patch grammar (development feasibility)

**Status:** preregistration, no inference and no representation-effect claim. This run supersedes the notation-only Run79 comparison. Do not treat CI, synthetic counterexamples, or provenance as science evidence.

## One active causal kernel
1. **Intervention:** explicit immutable-version graph with node IDs, captured reference edges, protected root commitments and authorized edit scope, rendered as a structural view of a three-module policy fixture.
2. **Strongest control:** ordinary Python source view, with the **same semantic facts** (version, node identity, bound dependencies, protected roots, edit authority), the **same underlying compiler/verifier**, and the **same JSON patch grammar**. Both receive identical request, file boundaries, public diagnostics and token budget.
3. **Capable model:** Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M on free public GitHub-hosted CPU; no API key or user compute. A second model is optional only after first inference succeeds.
4. **Tasks:** freeze an explicit development manifest of multi-module fixtures *before* inference. Synthetic fixtures are not representative independent real-repository tasks. A full 249-independent-task study remains **unexecuted**.
5. **Primary scalar:** paired first-call hidden-target success rate, IR minus Python. Invalid outputs count as failures. Secondary: tokens, parse acceptance, semantic churn, frame violations, tool calls.
6. **Alternative:** graph text is merely easier to read or tokenization/order differs; baseline gets equivalent facts and patch grammar, and a reordered-graph ablation is required before any mechanism claim.
7. **Falsification:** zero or negative paired difference on capable model, or a gain vanishing under equivalent layout/order controls. No syntax pivot.
8. **Unseen prediction (frozen before holdout):** any advantage should increase with depth of protected captured dependencies, and disappear when the edit target has no cross-file dependents. Do not inspect holdout before freezing this prediction.
9. **Publication threshold:** independent evaluator; real held-out repos; predeclared >=80% power for a 10-point paired effect; independent task units; two capable models; uncertainty, mechanism ablation, adversarial controls, clean reproduction and prior-art audit. For hypothetical 20% IR-only / 10% Python-only, exact McNemar requires ~249 independent pairs. This development run cannot satisfy publication threshold.
10. **System consequence:** if the structural view improves semantic repair, expose it in Lattice agent API; if not, prioritize typed edits, versioned capture, sealed validation and semantic diff as a Python-compatible compiler/editor.

## Rules
- Same patch: JSON object mapping authorized root to Boolean expression **string**.
- Never execute model-generated Python; use Lattice's bounded AST parser and FramedProgram compiler.
- Hidden target oracle only runs after all inference calls finish. No hidden witnesses, outcomes or partial results in model context.
- Pair arms per task with identical seed, sampling, model weights and token limits; alternate arm order.
- Freeze manifest hash, exact prompts, model ID/weight checksums and token counts before inference.
- Preserve raw requests, raw responses, compiler traces and failure status in Actions artifacts.
- The first run is an explicitly **underpowered feasibility pilot**, not a scientific or product-scale effect estimate.
- Kill/reformulate after three substantive capable-model runs without a stronger effect or boundary; never disable hourly automation.

## SCIENCE ledger
Run95 finite-state control-read counterexample is not evidence for coding-model representation advantage. Run96 must produce actual paired capable-model responses before adding a representation-performance claim.

## SYSTEM ledger
Existing `FramedProgram` provides immutable bound roots, frame checks and Python lowering; the system test is whether a structural view improves repair beyond ordinary Python with identical compiler access. Any UI/DSL-only changes are out of scope.
