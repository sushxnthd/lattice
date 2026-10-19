# Run124 — Active reachable semantic slice theorem

**Status:** Exact bounded semantic-representation result, not a capable-model advantage. K-SYNTH-1 is the sole active representation-science kernel.

## Statement

For a valid immutable `FramedProgram` S, let R(S) be the historical-binding closure of current output roots. Define C(S) to discard nodes outside R(S), renumber remaining nodes in ascending original-index order, and update binding/root indices. Keep inputs and current source expressions unchanged.

Under the current `FramedProgram.edit` grammar (patches name current output roots, not raw historical node IDs), for every trusted authority set and sequence of valid edits:

1. `run(S,x) == run(C(S),x)` for every Boolean input assignment x.
2. `edit(S,p,A)` is admitted iff `edit(C(S),p,A)` is admitted.
3. All subsequent admitted name-scoped edits preserve observational equivalence; compacted successor graphs are isomorphic under canonical renaming.

**Proof sketch.** Evaluation follows only nodes reachable from roots. Edit admission depends on current source-name dependencies, root names, and trusted authority, not unreachable historical node IDs. A new edit captures protected roots and creates new authorized versions. The reachability renaming maps each binding to its corresponding root, and the new nodes are correspondingly isomorphic after compaction. Induction over the edit sequence proves future equivalence.

**Boundary:** This theorem fails for a future API allowing direct raw historical-ID patches unless stable external IDs are preserved. Audit history must remain separately archived. Naively keeping only current roots is unsound: with `permit=a`, `audit=permit and b`, an authorized `permit=not a` edit must preserve the old permit node captured by protected audit.

## Exact finite-state model check

Independent deterministic mirror of current edit rules: seed 12420; 300 sequences × 40 attempted edits; 9,610 admitted, 2,390 rejected; all 12,000 admission decisions matched; 76,880 Boolean input assignments compared after admitted edits; zero output disagreements. Peak raw DAG 52 nodes; peak active DAG 12 nodes. A 40-step trace ended with 47 raw nodes, 3 reachable nodes. This checks a bounded model; integration tests against the actual repository compiler remain pending.

## Direct representation consequence

Keep a full append-only archival graph for provenance but expose only the active reachable semantic slice to the coding model. The indexed-Python arm must receive the identical slice and commitments, with the same authority and patch grammar. The repository's `FramedProgram.context()` currently exposes all historical nodes, whereas `lower_python()` drops unreachable ones. Comparing these directly would introduce a history-dependent information/token-budget confound, not a clean structural representation intervention.

## Research status

No capable-model inference; no representation-specific effect; no breakthrough. The 161-task powered capable-model experiment remains outstanding. Preserve this correction without treating additional evaluator or CI work as research progress.
