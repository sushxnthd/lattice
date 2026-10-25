# Run252 — fixed-point CFG counterexample and correction

2026-10-25. No new capable-model inference, no qualified real-world issues, no semantic-IR advantage.

## Falsifying witness
Run251's source-derived semantic-fact encoder marks a read of `x` inside `x=0; for item in xs: observe(x); x=1` as `unique_reaching_definition` from the initial assignment. Real execution with two iterations observes `[0,1]`, so the label is false. Merely reporting `loop_fixed_point_not_computed` does not retract the erroneous positive claim.

## Correction
Implemented a bounded intraprocedural CFG/worklist fixed-point analyzer with explicit branch joins, early returns, loop backedges, zero-iteration paths, break/continue, for-target binding and conservative unknowns. The loop read now has both reaching assignment sites. This is a bounded syntactic/dataflow approximation, **not** a sound general-Python semantic IR.

- 30/30 regression tests passed.
- 269/269 frozen real Python snippets processed; 193 functions, 1,571 CFG edges, 1,835 use records, 804 unique-definition labels and 590 explicit unknown use labels; 25 loop-containing functions. These are isolated dedented snippets, not full repositories.
- 250 deterministic executable generated programs exercised five control-flow patterns. No counterexample to unique reaching-definition was observed among single-return constant-assignment templates. This is not a proof.
- Original v1 false-unique claim and v2 corrected claim independently witnessed.

Local complete 31-entry SHA-256 manifest and archive: `lattice_run252_cfg_fixedpoint_reproducibility.zip`, SHA-256 `d03e1ecc8c0603e68af9f1eab14852df380a0af7dc2ec5a76ed97c0c55fd5cb9`. Complete source and raw evidence are preserved locally; GitHub mirroring of the full capsule remains a separate persistence task.

## Remaining scientific gate
No actual model completions this run. Run251's three multi-file tasks are synthetic; Run237's 11 unique real issues lack executable baseline-negative/reference-positive controls. The adequate paired comparison remains outstanding. Earlier power planning: 306 independent pairs under optimistic assumptions, 681 under smaller effects, with clustering requiring more. The sealed 89 boundary issues were not used.

Next: qualify pinned upstream real multi-file issues with executable before/after and held-out controls, then run Qwen2.5-Coder-7B-Instruct under frozen matched-information semantic/Python conditions and identical compiler/oracle. Do not optimize representation cosmetics.
