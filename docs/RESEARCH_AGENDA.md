# Research agenda

## Thesis

Current coding agents may be constrained by the software representation they use. Lattice asks what representation an AI would ideally want in order to understand, create, modify, verify, debug, and optimize applications reliably.

The research target is not merely shorter syntax. It is a persistent semantic representation that can retain information ordinary source trees often lose or scatter.

## Evidence-driven bottleneck map

| Bottleneck observed in current coding agents | Candidate Lattice primitive | Mechanism to test | Primary evaluation |
|---|---|---|---|
| Structural erosion and verbosity across repeated edits | explicit component/dependency structure; semantic locality | discourage local patches that accumulate complexity | long-horizon checkpoint success, structural erosion, duplication |
| Specification loss over long sessions | persistent goals, commitments, preserved constraints | keep requirements outside transient conversation context | held-out requirement fidelity after iterative changes |
| Architectural rationale disappears | first-class decisions + rationale + rejected alternatives | prevent agents from locally rewriting intentional architecture | architecture-preservation tests and change-scope metrics |
| Security bugs and broken authorization | permissions, trust boundaries, executable invariants | make unsafe states difficult or invalid to express | held-out security tests, invariant violations |
| Visible-test gaming / reward hacking | semantic contracts + hidden property tests | separate intended behavior from particular test examples | visible-vs-held-out test gap |
| Context-window and repo-navigation waste | semantic dependency neighborhoods | retrieve only the relevant product/state/data subgraph | context tokens, file reads/searches, task success |
| Generic AI-looking UI | explicit visual hierarchy, composition, design constraints, anti-patterns | preserve design intent rather than deriving it from CSS each turn | blind visual ratings, layout consistency, design-drift metrics |
| Broken responsive behavior | responsive invariants and preserved hierarchy | encode what may change and what must survive across breakpoints | viewport test suite |
| State and interaction inconsistencies | explicit state machines / transitions | make legal states and transitions canonical | model-based interaction tests |
| Fixing one bug creates another | dependency/invariant graph + bounded change scopes | constrain blast radius and verify dependent properties | regression rate, changed-surface size |
| Poor edge-case/error handling | explicit failure modes and effect contracts | require exceptional behavior to be represented, not implied | adversarial/negative tests |
| Duplicate/dead code | semantic entities and generated lowering | centralize concepts above implementation level | duplication/dead-code metrics |
| Runtime inefficiency | optimization intent + semantic equivalence constraints | allow compiler/agent to choose better equivalent implementation | latency, memory, bundle size, requests/data movement |
| Fragile config/deployment | environment/resource declarations | promote implicit deployment assumptions into the program model | reproducible clean deploy/build tests |
| Non-experts cannot understand generated systems | inspectable semantic graph | expose product behavior rather than generated framework internals | comprehension/debug tasks |
| Unsafe agent side effects | capabilities/effects for filesystem, network, destructive actions | enforce explicit authority boundaries | side-effect containment tests |

This table is provisional. Every row must earn its place through literature, benchmark, or practitioner evidence and can be removed if unsupported.

## Initial external evidence

### Long-horizon degradation

SlopCodeBench reports that iterative coding-agent trajectories become more verbose and structurally eroded over time, and that prompt-level quality guidance can improve initial quality without stopping degradation.

Reference: https://arxiv.org/abs/2603.24755

### Specification faithfulness

SLUMP reports specification faithfulness loss when requirements emerge over long coding sessions. Its ProjectGuard external project-state layer recovered a large fraction of the measured gap in one evaluated setup, making persistent state/specification tracking a particularly important comparison baseline for Lattice.

Reference: https://arxiv.org/abs/2603.17104

### Security

SUSVIBES evaluates real-world feature tasks with known vulnerable implementations and reports a large gap between functional correctness and security for coding-agent solutions.

Reference: https://proceedings.mlr.press/v306/zhao26ax.html

### Reward/test hacking

SpecBench reports that frontier coding agents can saturate visible validation while failing held-out composed behavior, with the gap increasing with task length.

Reference: https://arxiv.org/abs/2605.21384

### Long-horizon engineering capability

SWE-EVO reports a substantial gap between single-issue benchmarks and multi-step software evolution, motivating evaluation across sequences of changes rather than one-shot generation.

Reference: https://arxiv.org/abs/2512.18470

### Visual/layout generation

Design2Code finds that multimodal models particularly lag on recalling visual elements and generating correct layout structure in screenshot-to-code tasks.

Reference: https://aclanthology.org/2025.naacl-long.199/

## Core experimental design

Compare at minimum:

```text
A. intent → same model → conventional code

B. intent → same model → ordinary persistent specification/planning layer → conventional code

C. intent → same model → Lattice → conventional code
```

The ordinary persistent-specification baseline is essential. If B matches C, the evidence supports better project-state tooling rather than a new programming representation.

Use identical or explicitly normalized model budgets and freeze task sequences before final evaluation.

## Measurement families

### Authoring efficiency
- context tokens
- file reads/search operations
- model/tool calls
- repair iterations
- wall-clock latency where available
- code churn
- semantic blast radius

### Reliability
- functional correctness
- held-out requirement fidelity
- regressions
- security/invariant violations
- visible-vs-held-out test gap
- state-machine correctness
- architecture preservation

### Representation quality
- semantic locality
- traceability from requirement to implementation
- persistence of rationale
- inspectability
- portability across lowering targets

### Visual quality
- hierarchy preservation
- responsive consistency
- layout failures
- blind preference/distinctiveness evaluation
- design drift after repeated edits

### Runtime efficiency
- latency
- memory
- bundle/artifact size
- network/API calls
- data movement
- build/compile overhead

## First falsification targets

1. **Planning confound:** does Lattice help only because it forces the model to plan more?
2. **Memory confound:** is a simple durable spec/state file enough?
3. **Verification confound:** do gains come only from deterministic checks?
4. **Token confound:** does Lattice merely spend more tokens?
5. **Model-specificity:** does the effect survive across more than one model family?
6. **Task specificity:** does it help only on frontends or also on backend/state/security tasks?

## Breakthrough standard

A result is not breakthrough-grade because a Lattice-generated app looks better. A serious claim requires frozen tasks, strong baselines, held-out evaluation, equal-budget controls, ablations, reproducibility, explicit limitations, and evidence identifying which mechanism causes the improvement.
