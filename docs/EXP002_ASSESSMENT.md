# Lattice: executable edits and the current evidence

Date: 2 October 2026. Status: a functioning bounded compiler with validated scope
preservation; no demonstrated general language or scientific breakthrough.

## What changed

The original preflight checked proposed metadata. The new prototype executes
actual Boolean permission policies, applies edits, checks every supported input,
returns concrete counterexamples, and lowers the policy to conventional Python.

The independent contract oracle is evaluator-authored and cannot be edited by the
model. This separates specification correctness from whether generated code obeys
the specification. The system still cannot automatically ratify real user intent.

A separate framed compiler uses immutable, versioned output dependencies. Consider:

```python
read = auth and not blocked
edit = read and owner
ship = edit
```

The request `read = not blocked` ordinarily also expands edit and ship for
unauthenticated owners. A caller-authorized scope of `{read}` instead binds edit
and ship to their previous rule versions. The compiler emits ordinary Python with
distinct version names. It enforces this frame without access to a correct target
answer. To propagate changes, the caller must explicitly authorize the affected
output roots. This is a library capability that Python can use too.

## Compiler evidence

Frozen seeded stress test: 100 trajectories, 20 edits per trajectory, six independent
Boolean inputs, five outputs, one authorized output per edit. Every valuation and
protected output is checked after each edit: 512,000 protected output/input pairs.

| Condition | Edits with protected-output changes | Changed protected output/input pairs |
|---|---:|---:|
| Ordinary live-name rule graph | 867 / 2,000 | 24,131 |
| Versioned frame compiler | 0 / 2,000 | 0 |
| Conventional Python calling the same compiler | 0 / 2,000 | 0 |

Generated native Python matched the framed interpreter on all 128,000 complete
input evaluations. No model inference or target oracle was used in this experiment.
The live and framed trajectories diverge after past regressions, so this is a stress
test of the mechanism, not an estimate of AI accuracy improvement.

For protected outputs, the root and its reachable immutable subgraph are unchanged.
Pure evaluation therefore has the same result for the same input. This structural
argument explains preservation for the supported semantics. It is not a formal
proof checked by a theorem prover. Tests additionally cover malformed state,
unauthorized targets, cycles, dependency traps, name capture in lowering, and
repeated edits. The current local suite passes 27 tests.

Reproduce with `python experiments/exp002/frame_validation.py`. The full list of
edits, witnesses, seed and source hashes is in
`artifacts/exp002/frame_validation.json.gz`. Its readable summary is adjacent.

## Frozen model experiment

Three conditions receive durable requirements, the same ordered natural-language
changes, the same exhaustive checker and one repair opportunity:

1. Complete Python function replacement.
2. Conventional Python dictionary of changed expressions.
3. Lattice named-rule assignments.

The Python-patch condition controls for scoped editing, dependency graphs,
persistence, compilation and verification. The framed compiler above is separate
and was not substituted into the frozen model run. Each call has a 220 generated-
token ceiling; actual tokens are retained. All 64 input valuations are checked.

Eight synthetic trajectories (two development and six hold-out name variants),
three edits each. These are three correlated policy families, not independent
real-world application domains or a long-horizon repository benchmark.

The frozen model commit is
`631bdc4c20a9131f323fc70ff99c7227fadf117c`. Task source SHA256:
`678f1372ec4a728a10137ec1eb66b78aba722851c440c5d7c87909f08628781e`.
[Original workflow](https://github.com/sushxnthd/lattice/actions/runs/37017261765).

### Qwen2.5-Coder 0.5B

| Condition | Hold-out first-attempt checkpoint success | Hold-out success after one repair | All three checkpoints succeed |
|---|---:|---:|---:|
| Complete Python | 0 / 18 | 0 / 18 | 0 / 6 |
| Python expression patch | 0 / 18 | 0 / 18 | 0 / 6 |
| Lattice assignment patch | 0 / 18 | 0 / 18 | 0 / 6 |

Development also had zero successful checkpoints in all arms. The run contains
144 model calls, with every prompt and raw response preserved. Full Python often
echoed the initial function. The Lattice arm frequently copied generic example
names into tasks with different input names; 21 of its 24 first attempts across
both splits were invalid. The shared accuracy floor does not establish an advantage.

### Qwen2.5-Coder 1.5B

| Condition | Hold-out first attempt | After one repair | All three checkpoints |
|---|---:|---:|---:|
| Complete Python | 0 / 18 | 0 / 18 | 0 / 6 |
| Python expression patch | 0 / 18 | 0 / 18 | 0 / 6 |
| Lattice assignment patch | 0 / 18 | 0 / 18 | 0 / 6 |

These are completed artifact values. Full prompts and generations:
artifacts/exp002/Qwen2.5-Coder-1.5B-Instruct.json.gz.
Both model sizes are one model family; no general-language superiority
or external application result is inferred.

## Diagnostic after the negative pilot

Experiment 003 separately freezes a 2x2 prompt diagnostic: edit request before vs
after current source; generic vs task-named syntax example. It uses one first-step
task from each policy family in all three representations, with one model call
per combination. Previously evaluated tasks are reused deliberately for diagnosis.

Its results cannot be presented as untouched hold-out confirmation. A benefit from
prompt placement must not be credited to Lattice semantics. Frozen diagnostic
commit: `c9776b56d75104a170052d3adb6d40278febb7bf`.


### Completed prompt diagnostic

| Prompt variant | Complete Python | Python patch | Lattice patch |
|---|---:|---:|---:|
| original | 0 / 3 | 0 / 3 | 0 / 3 |
| request_last | 0 / 3 | 1 / 3 | 0 / 3 |
| alias_example | 0 / 3 | 1 / 3 | 1 / 3 |
| both | 0 / 3 | 1 / 3 | 0 / 3 |

This diagnostic did not establish a Lattice advantage. Task-named examples
solved one of three tasks for both patch interfaces. These previously evaluated
tasks cannot serve as fresh hold-out confirmation. Full transcripts:
artifacts/exp003/prompt_order.json.gz.
[Diagnostic workflow](https://github.com/sushxnthd/lattice/actions/runs/37018691609).

## Existing negative evidence

The earlier runnable-code gate selected prose on development (13/40 tests) and
obtained 8/40 on hold-out. The alternatives scored 7/40, 6/40 and 0/40 on hold-out.
No condition produced a perfect program. This result is preserved in
`artifacts/prior/codegen_gate_v1.json.gz`, with its original raw generations.
[Original workflow](https://github.com/sushxnthd/lattice/actions/runs/36906853934).

## Prior work and novelty boundary

The broad claim that an LLM-oriented DSL can improve generation is already tested
by [Anka](https://arxiv.org/abs/2512.23214), which studies constrained data pipelines.
[Dafny as a verification-aware intermediate language](https://arxiv.org/abs/2501.06283)
already explores validating generated intermediate code before lowering it.
[Regression verification](https://www.microsoft.com/en-us/research/video/regression-verification-proving-the-equivalence-of-similar-programs/)
and [self-adjusting computation](https://arxiv.org/abs/1106.0478) are established
related areas. [semctx](https://github.com/hoklims/semctx) supplies authored intent,
semantic slices and change-contract checking. These works set comparison targets;
their scope is not assumed identical to this prototype.

Immutable versions and structural frame preservation are not asserted to be new
inventions. A distinct Lattice contribution would require evidence that its edit
semantics improve practical coding outcomes over equally capable conventional
interfaces, with larger models and external task suites. That evidence is absent
from the completed small-model pilot.

## What can be claimed

Lattice has a reproducible bounded mechanism for preserving explicitly protected
Boolean outputs across dependency-changing edits, with conventional Python lowering
and concrete counterexamples from an independent oracle.

What cannot be claimed: general AI coding superiority, a novel universal programming
language, zero regressions in arbitrary apps, automatically correct user intent,
runtime-efficiency improvement, or a field-level scientific breakthrough.

The next decisive test should use compiler-enforced output frames as the intervention,
include a conventional Python interface to exactly that mechanism, and test multi-
step application changes with a capable model. It must establish useful feature
completion as well as protection, rather than obtaining zero regressions by rejecting
all edits. It should be frozen before new hold-out tasks are evaluated.
