# Run 17: Versioned semantic edit protocol (local validation)

Status: locally validated compatibility prototype; NOT integrated into canonical CI. No coding-model inference, user spend, or laptop compute.

The experimental protocol composes the existing bounded Boolean Program and FramedProgram compiler into a source-bound, machine-readable edit interface. A trusted authority binds a baseline SHA-256 digest and authorized output names. An untrusted edit can be expressed as a Lattice assignment or a Python expression dictionary. Both representations use the identical frame compiler and Python lowering.

The new sequential API serializes immutable rule versions and their captured dependencies. Every subsequent edit requires a fresh trusted digest. Protected outputs retain prior versions until explicitly authorized for rebinding. Deterministic rejection covers unauthorized targets, stale preimages, malformed version histories, unsupported expressions, and duplicate JSON keys. A reachable-context projection omits discarded versions from agent-visible context.

Local combined compatibility validation: 82 tests passed (75 previous compatibility tests plus 7 new tests, including paired-evaluator fixtures). The new protocol tests include 200 deterministic edit variants, eight Boolean valuations per variant, and a three-stage mixed Python/Lattice edit trajectory. The compatibility copies of the canonical compiler were reconstructed locally; these results are not canonical CI validation. GitHub rejected the attempted code write to branch build/semantic-state-compiler-v1-20261012.

Scientific boundary: the Python and Lattice patch interfaces generate identical code for equivalent edits. This is an engineering integration, NOT evidence of representation-specific superiority. No fresh four-arm model benchmark has run. Existing frozen negative Qwen results remain preserved.

Prospective evaluation: freeze independent realistic repository tasks, hidden tests, prompts, models, seeds, token budgets, and thresholds; compare ordinary Python, Python+identical compiler, Lattice+identical compiler, and simpler executable controls. Report task-level perfect-repository outcomes with Wilson intervals and paired exact sign tests, with clustering by repository where necessary.

Next blocker: canonical integration of code and tests, then prospectively frozen evaluation using capable zero-cost coding models. Preserve all frozen evidence and opened holdouts.
