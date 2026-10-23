# Lattice K-SYNTH-1: novelty-priority audit, 2026-10-23

This is a targeted priority screen, not a systematic review or a claim that unexamined work does not exist.

## Closest published work: CodeStruct (ACL 2026)

Myeongsoo Kim et al., [CODESTRUCT: Code Agents over Structured Action Spaces](https://aclanthology.org/2026.acl-long.607/), ACL 2026; [released source and results](https://github.com/amazon-science/CodeStruct). CodeStruct exposes `readCode` and `editCode` over named AST entities and compares structured versus text-based editing on SWE-bench Verified and CodeAssistBench. It reports 1.2–5.0 percentage point improvements for most evaluated models, with 12–38% lower token consumption for most. Its released Qwen3-8B SWE-bench Verified result is **negative** (13.2% baseline versus 13.0% structured). **Therefore "structured editing beats text editing" is not a novel Lattice claim and is model-dependent.** Lattice needs a CodeStruct-style structured-AST-action baseline, not just ordinary Python text.

## Other priority and methodology threats

- [Evaluating Symbolic Feedback Granularity for LLM-Based Program Repair](https://conf.researchr.org/details/ase-2026/apr-2026-papers/8/Evaluating-Symbolic-Feedback-Granularity-for-LLM-Based-Program-Repair), APR/ASE 2026: isolates feedback modality, four open-weight code models, 540 tasks; concrete counterexamples outperform raw symbolic traces. Includes token-matched padding and redundant-feedback ablations. Lattice must isolate navigation cues, not assume more graph information is better.
- [Code Reffix](https://aclanthology.org/2026.findings-acl.762/), Findings of ACL 2026: decouples reflection generation from repair generation; a methodological precedent for separately measuring localization, output formatting, and semantic repair.
- [CodeTaste](https://www.sri.inf.ethz.ch/publications/thillen2026codetaste), ICML 2026: real multi-file refactoring tasks with dataflow-sensitive static checks, more adversarial than four Boolean repair families.
- [SWE-bench-Live](https://arxiv.org/abs/2505.23419), 2025: 1,319 repository issues from 93 repositories with reproducible Docker environments; an important task-diversity and contamination-resistance reference.
- [CodeEditorBench](https://codeeditorbench.github.io/): debugging, requirement switching, polishing, and translation, broadening code-edit categories.

## Distinguishable candidate thesis, NOT yet established

Investigate whether **authenticated immutable epoch-to-root bindings, transitive content identities, and protected-output commitments** deliver machine-checkable semantic guarantees under sequential edits, concurrent forks, stale lineage, and history-sensitive references. The target is trace-equivalence and noninterference, not a new syntax or an unqualified AST-editing advantage.

Candidate formal property: For every authorized transaction, protected outputs remain observationally equivalent over all inputs; historical references resolve to the exact epoch/root binding selected at transaction creation; stale conflicting lineage is rejected. Compare against ordinary Python and CodeStruct-style AST actions equipped with the **same** compiler, verifier, and authority controls. Such a property could support a systems soundness result but does not by itself show higher LLM productivity.

## Experimental requirements

1. Add a CodeStruct-style AST-action baseline to real-repository tests.
2. Use pinned source commits, genuine multi-file issues, independent executable tests, and distinct format/syntax/semantic/authority failure categories.
3. Match task facts, patch authority, verifier, output schema, and model budget; include token-matched controls.
4. Preregister an unseen depth/coupling boundary and analyze uncertainty by independent repository/issue cluster.
5. If Python and structured-AST baselines match/beat IR twice under controlled reformulations, pivot to formal soundness or a rigorous negative result.

Expand this screen into a full-text and source-level literature audit before making priority claims.
