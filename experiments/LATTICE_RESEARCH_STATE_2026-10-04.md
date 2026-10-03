# Lattice Research State

## Active foothold
**State:** ANOMALOUS / candidate foothold  
**Evidence:** prospective Qwen2.5-Coder-1.5B runnable code-generation gate produced 85% hidden-test accuracy for violation-normal versus 55% prose on both development and previously unopened holdout.  
**Residual:** violation-normal used about 228.5 prompt tokens versus about 171 for prose, so semantic organization and representational budget remain confounded. Zero condition produced a perfect program.

## Equal-budget replication
**Class:** DISCRIMINATION  
**Hypothesis:** with model, semantic facts, decoding, and prompt budget controlled, violation-normal organization improves hidden functional-test performance over strong prose on unseen domains.  
**Mechanistic prediction:** violation-normal should retain a positive holdout advantage after token matching; a >=10 percentage-point advantage is the preregistered candidate-effect threshold.  
**First observed result:** PRE-GENERATION CONTROL FAILURE, not a model result. Strong prose tokenized to 211 tokens and violation-normal to 231 on Account, an 8.66% relative gap, exceeding the frozen 5% gate. Execution aborted before model loading/generation, leaving all six new holdout domains unopened.  
**Assumption weakened:** the initial hand-written conditions were not naturally token matched.  
**Competing explanations for the original +30pp:** (A) semantic violation-normal organization; (B) extra prompt budget/redundancy; (C) interaction between explicit negative predicates and this model family; (D) small-domain sampling.  
**Uncertainty:** high; no equal-budget model output exists yet.  
**Cheapest next separator:** use the preregistration-permitted, pre-generation prose-only budget correction already committed as `experiments/run_codegen_equal_budget_v1_matched.py`, verify <=5% on all 12 domains before model loading, then execute exactly once without further wording changes.

## Belief ledger
| Claim | State | Confidence | Evidence / reason |
|---|---|---:|---|
| Surface representation alone helps Qwen-0.5B | FALSIFIED | high | v1/v2 null/floor results and runnable-code gate favored prose |
| Violation-normal can alter Qwen-1.5B runnable-code behavior | KNOWN | high | frozen 85% vs 55% result |
| The 1.5B effect is caused by semantic organization rather than extra budget | UNTESTED | low | equal-budget gate has not executed |
| The effect transfers across model families | UNTESTED | low | no cross-family replication |
| Lattice has a breakthrough-level result | FALSIFIED (current evidence) | high | breakthrough gate not satisfied |
| Token budget is a material confound | KNOWN | high | original prompts differ substantially; first equal-budget attempt failed at 8.66% |

## Failure clustering
Earlier failures share two recurring mechanisms: (1) benchmark floors/degenerate answer priors obscuring representation differences, and (2) representation comparisons changing more than one causal variable at once. The current first-class target is therefore **causal identifiability of representation effects**, not adding more representation variants.

## Hypothesis population
1. **Constraint-normalization mechanism (BELIEVED, low confidence):** explicit violation predicates reduce missed rejection branches.
2. **Redundancy/budget mechanism (BELIEVED, moderate):** more tokens or repeated constraints explain much of the 1.5B gain.
3. **Model-scale interaction (ANOMALOUS):** 0.5B and 1.5B results differ sharply; representation utility may emerge only above a capability threshold.
4. **Negative-space salience (UNTESTED):** enumerating forbidden cases, rather than a language/IR property, drives the effect.
5. **Task-topology interaction (UNTESTED):** gains may be restricted to rule systems dominated by invalid-state/permission branches.
6. **Active semantics (UNTESTED):** executable invariants/state machines may outperform passive text only when multi-edit state retention matters.

## Experiment ranking
1. **DISCRIMINATION:** matched-budget frozen replication — highest uncertainty reduction per cost.
2. **SURPRISE:** if replication runs, inspect per-test error categories for rejection-vs-update asymmetry; no fresh holdout reuse.
3. **DISCRIMINATION:** fresh cross-family replication only if matched-budget effect survives.
4. **EXPLOITATION:** fresh multi-edit repository evolution only after causal control survives.
5. **WILDCARD (~10-15% cheap budget):** exploratory dev-only sweep across context length × invalid-branch density to test for a scale/topology transition; never use sealed holdouts.

## Claim boundary
The strongest defensible statement remains: a prospectively selected violation-normal representation produced a large candidate effect on one small Qwen2.5-Coder-1.5B runnable-code benchmark and transferred to its fresh domains, but causal attribution to semantic representation is unresolved because prompt budget was unequal.
