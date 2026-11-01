# K-SYNTH-1 Run407 prospective reference-ablation gate, pytest #14997

Frozen 2026-11-01 IST BEFORE inspecting the fixing PR, changed files, reference patch or reference behavior. The original Run405 public/heldout/control oracle is immutable.

## Original recovered evidence

- Issue: https://github.com/pytest-dev/pytest/issues/14997
- Pinned control `a7d58d7a21b78581e636bbbdea13c66ad1657c1e`, regression `cf470ec0bf7eb89cd97dd56df4859eae5db46447`.
- Original GitHub run: https://github.com/sushxnthd/lattice/actions/runs/41274411758
- Control artifact 13071331496 SHA256 8476adf7ac95eb32c4d92be3e4269093945761cb4f851bdeef84d1f3cc63a15e.
- Regression artifact 13070971375 SHA256 89bbb9ecf1269044cc5ee78b27bf6ec2c384cd49bbc73374bbb12a250e971633.
- Actual original GitHub oracle SHA256: 9af9417ad6b082968557bf43820dcf20c6fcb8ee9354334e90909590b933135d.
- Independent frozen outcomes: control 3/3 public, 3/3 heldout, 6/6 controls pass; regression 0/3 public, 0/3 heldout, 6/6 controls pass. Each failed target shows two passes plus one fixture-not-found error. All six targets share one abstract interleaving pattern; not six independent repair tasks.

## Frozen qualification algorithm

1. Identify historical fixing PR and exact reference commit from the issue's documented resolution. Record exact parent and source lineage. If not compatible with pinned baseline, mark INCOMPARABLE; no unverified transplant.
2. Pin exact reference, parent, Python/dependency environment and production source hashes. Independently execute all twelve unchanged original cases on baseline and reference in isolated worktrees. Full reference must pass all six targets and six controls.
3. Enumerate all production .py files actually modified by fixing PR, excluding tests, docs, examples, generated code and metadata. Require at least two modified production files; do not add unchanged files post hoc.
4. For EACH changed production file, perform leave-one-file-out ablation: restore that file's baseline bytes while retaining other reference production files. Every ablation must be importable without compensating edits and lose at least one target-plus-control outcome compared with full reference. Import/signature/harness failures alone do NOT prove behavioral necessity. Any proposed compatibility shim must be independently shown neutral on both endpoints before use.
5. At least two distinct production files must have genuine behavioral necessity on the joint target-plus-control oracle. If single-file reference, no necessity, or neutrality cannot be proven: NOT QUALIFIED. Never change thresholds after outcomes.
6. Preserve all source hashes, commands, stdout/stderr, exit codes, reference/ablation failures and independent evaluator traces. This is task eligibility, not model success or semantic-IR superiority.

## Run406 transport correction

The actual GitHub frozen oracle takes its output directory as `sys.argv[1]`, NOT an `--output` option. Run406's workflow change to `--output evidence` writes to a directory literally named `--output` and omits `evidence/` from the uploaded artifact despite green jobs. Preserve those failure artifacts; restore the original positional invocation separately. Never alter the frozen oracle.

Single K-SYNTH-1 kernel; canonical sushxnthd/lattice branch research/exp003-context-order; sole open/draft/unmerged PR #9; all 89 boundary issues SEALED. Until full ablation, qualified independent real multi-source repair count remains TWO.
