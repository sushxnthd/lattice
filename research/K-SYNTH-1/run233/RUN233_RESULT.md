# Run233 — Actual lifecycle-context model outputs and guard-mechanism witness

**Status:** executed; exploratory; no representation-superiority claim. Original paired Qwen2.5-Coder-7B-Instruct Q4_K_M inference: [Run232](https://github.com/sushxnthd/lattice/actions/runs/40139137530), completed 2026-10-24 UTC. Artifact ID 12577239550. Frozen model SHA-256: `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`; seed 1560714227; temperature 0.

## Unmodified primary endpoint

Independent replay verified the exact prompt and response hashes, model hash, schema hash, source-fact equivalence, and shared compiler. Both genuine completions compiled, but neither passed all 16 preregistered necessary-condition behavioral probes.

| Arm | Prompt tokens | Completion tokens | BatchStudy | Simulation | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Semantic-IR JSON | 1,300 | 745 | 0/12 | 4/4 | **4/16** |
| Annotated Python | 1,246 | 479 | 6/12 | 4/4 | **10/16** |

Historical Run230, independently replayed against the same 16-case evaluator, scored 4/16 for each arm. The frozen Run232 prediction that lifecycle context might improve at least one arm was met for Python, but **neither arm achieved functional success**. This historical comparison was not randomized. Sixteen probes on one issue are correlated, not sixteen independent samples; no population inference is justified.

## Diagnosed mechanism

Both completions guard `Simulation` using `self._solution is None`. The IR output copies this invalid attribute into `BatchStudy`, causing AttributeError in all 12 BatchStudy states. The Python output uses `self.sims == []`, which rejects an initialized empty list but misses absent, single-unsolved, and partially solved states.

A **post-hoc, oracle-informed intervention**, replacing only the first BatchStudy guard predicate in each output with `not hasattr(self, "sims") or not self.sims or any(getattr(sim, "solution", None) is None for sim in self.sims)`, passed 16/16 for both outputs under the same compiler and frozen evaluator. The remaining generated method bytes are unchanged. This is a local sufficiency witness, **not** a model completion, prospective mechanism ablation, or full upstream PyBaMM integration test.

Eight independent regression tests passed locally. Original responses, compiler traces, per-case failures, guard-intervention traces, provenance, SHA-256 manifest, and reproducibility code are preserved in `lattice_run233_lifecycle_guard_mechanism.zip` (local archive).

## Decision

Do not redesign syntax cosmetically. Advance to prospective, multi-repository experiments with class-lifecycle state invariants, shared verifier-repair loops, information-matched Python/semantic-IR conditions, independent adversarial evaluators, and cluster-aware sample-size planning. Run226's simulation shows 688 issues may provide only ~65–73% power under assumed clustering, while 1,024 issues may provide ~81–87%; these are planning assumptions, not observed effects.

**Limitations:** one two-file issue, reduced method snapshots, one 7B model, necessary-condition evaluator only, no full upstream resolution, no prospective ablation, no held-out boundary test, no adequately powered comparison. The 89 reserved boundary issues remain untouched. Research branch `research/exp003-context-order`; draft PR #9 remains open.
