# K-SYNTH-1 Run211 — semantic refactor kernel and representation-equivalence limit

Date: 2026-10-24. Persistent branch `research/exp003-context-order`; draft PR #9.

## Executed

Implemented a conservative, closed-world, multi-file Python symbol-renaming kernel using AST bindings and a common transactional text compiler. It handles direct imports, aliased imports, module-attribute references, recursive references, UTF-8 byte offsets, authorization and source hashes. It fails closed on partial snapshots, dynamic reflection, star/relative/nested imports, shadowing, new-name collisions and ambiguous text anchors.

Local validation: **20 unit/integration tests passed**, including before/after execution across four Python modules. A seeded 600-case compiler differential study accepted 300 admissible cases and rejected 300 intentionally unsafe cases. These are compiler tests, not capable-model experiments or real issue resolutions. Exact source, tests, per-case traces, hashes and the full report are preserved in the Run211 local reproducibility archive.

## Information-equivalence proposition (not novel)

Let X be the complete task state, A(X) the identical action set, and L(X,a) the identical loss. If renderers r1 and r2 are deterministic mutually invertible on the support of X, any unrestricted decision rule d1(r1(X)) can be implemented as d2(y)=d1(r1(r2^{-1}(y))). Consequently the optimal expected risk is identical. This is a deterministic special case of statistical experiment equivalence; see Blackwell (1953), *Equivalent Comparisons of Experiments*, DOI 10.1214/aoms/1177729032.

**Consequence:** With information and edit authority matched, any Lattice gain must arise from bounded model computation, search locality, token constraints or verifier interaction, not additional information. Static cross-file renaming is prior art (e.g. LibCST ScopeProvider/QualifiedNameProvider), not a breakthrough by itself.

## Boundary and experiment status

Naive renaming breaks Python reflection: `globals()['foo']` can fail after `foo` is renamed. This kernel rejects several dynamic cases but is not a complete Python resolver or production editor. The Run210 Qwen2.5-Coder-7B Q4_K_M workflow run 40051627638 had both jobs executing inference at inspection; run 40051685116 was queued. No Run210 raw model outputs were available, and no model advantage is claimed.

The previous conditional repository-clustered power simulation estimated about 468 discovery pairs across 187 repositories for 80% power under a large-effect assumption, versus 391 available discovery issues. The 89 boundary issues remain held out. Recalculate power from real functional discordance.

## Next decisive gate

Independently recover Run210 outputs. Integrate a genuinely distinct semantic edit action into the same backend and evaluate it against ordinary Python text and matched Python short-ID baselines with equal information, authority, prompts except representation, model configuration and functional issue verifier. Measure uncertainty and test a frozen mechanism ablation. Keep K-SYNTH-1, one research branch and draft PR #9.