# K-SYNTH-1 Run224 — PyBaMM oracle construct-validity falsification (2026-10-24)

**Kernel:** independent functional-evaluator calibration. **No new model inference.** Research branch: `research/exp003-context-order`. Frozen real issue: `pybamm-team__pybamm-3795`, base commit `c3def31a04df163769851733657d9b49b3700bca`.

## New counterexample: the old oracle reverses repair quality

The Run223 witness injected `sims` and `_solution` into *both* classes in *both* solved and unsolved states. At the pinned PyBaMM commit, `BatchStudy.solve()` initializes `self.sims=[]`, while its constructor does not; `BatchStudy` has no `_solution`. `Simulation.__init__` instead initializes `self._solution=None`. The earlier witness also accepted any exception, rather than requiring `ValueError`.

Using the exact original two `create_gif` method bodies extracted from the frozen Run222 prompts, a dependency-isolated CPython calibration compared two prospective patches:

| Two-file guard intervention | Old harness (8 cases) | State-faithful harness (8 cases) |
|---|---:|---:|
| Reference positive: `not hasattr(self, 'sims')` for BatchStudy and `self._solution is None` for Simulation, before plotting | **6/8** | **8/8** |
| Deliberately wrong: `self._solution is None` for both classes | **8/8** | **4/8** |

The old harness ranks the deliberately wrong patch above the reference positive. A smaller independent executable counterexample in `run224_minimal_counterexample.py` reproduces the BatchStudy-specific reversal without third-party dependencies: historical scores **2/4 vs 4/4**, state-faithful scores **4/4 vs 0/4** (reference vs wrong-field).

## Corrected necessary-condition oracle

The corrected evaluator tests solved/unsolved crossed with cached/uncached plot for both classes. Unsolved calls must raise `ValueError` before constructing a plot or writing a GIF. Solved calls must generate exactly one GIF with correct argument forwarding and no redundant plot construction. Eight deliberately defective mutation controls were all rejected (**8/8 mutants killed**); the reference positive passed all eight cases. These are local mutation tests, **not** package-level proof or a statistical sensitivity estimate.

Replaying the **same two** frozen Qwen2.5-Coder-7B Run222 completions (not new independent trials) gave semantic-node JSON **0/8** and annotated Python **4/8** necessary-condition passes. Neither is a verified issue repair; the semantic patch performs plotting before checking, while the Python patch modifies documentation instead of the two Python methods.

## Evidence and limitations

- Pinned upstream source: [BatchStudy](https://github.com/pybamm-team/PyBaMM/blob/c3def31a04df163769851733657d9b49b3700bca/pybamm/batch_study.py) and [Simulation](https://github.com/pybamm-team/PyBaMM/blob/c3def31a04df163769851733657d9b49b3700bca/pybamm/simulation.py).
- Original unmodified model artifact SHA-256: `182b8d97cc43c8a45d7857b13349c9af8df2ee830d4a6f63f469e6a96b0e8531` (from [Run222 workflow](https://github.com/sushxnthd/lattice/actions/runs/40098935864)).
- Full local Run224 reproducibility archive SHA-256: `2d11b32f06b66bb1803e667da4fb157e82f218851b337fba54e14fb2377c23e4`. It includes original raw model artifact, exact prompts, seed/token metadata, complete independent oracle, **13 passing local regression tests**, eight-case traces for each intervention, and a SHA-256 manifest.
- This is an independently constructed **necessary-condition reference**, not the hidden gold patch. Complete PyBaMM issue resolution remains **NOT_EVALUATED**. No adequately powered capable-model comparison, mechanism ablation, or unseen-boundary prediction is claimed.

## Experimental decision

**Require every real-issue evaluator to pass a reference positive and reject adversarial mutants before admitting the issue into a powered paired comparison.** Next capable-model intervention: freeze target-only two-file context for the same issue and run information-equivalent semantic-IR versus ordinary Python with identical edit authority, compiler, verifier, model, seeds, token budget, and the calibrated independent oracle. The ~686-pair planning target remains conditional on assumed effect and clustering parameters.
