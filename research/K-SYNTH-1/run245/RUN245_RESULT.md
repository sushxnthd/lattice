# Lattice Run245 — compact typed-graph referential-integrity failure

Date: 2026-10-25. Kernel K-SYNTH-1. Branch `research/exp003-context-order`. Draft PR #9. **No new model inference or representation-superiority claim.**

## Independently reproduced negative result

The Run244 compact graph assigns structural-node IDs by DFS preorder but copies call and binding references from `ast.walk`'s BFS enumeration of the *full* AST. These are different ID namespaces. Run244's round-trip and information-parity checks could not detect the issue because both renderings exposed the same malformed facts.

Independent frozen-source audit (Run237 12-repository cohort plus Run242 CrossGL; 269 parseable Python targets, 26 non-Python exclusions):

| Check | Result |
|---|---:|
| Syntactic call candidates | 1,053 |
| References to intended compact Call node | **3** |
| Out-of-range call references | **912** |
| In-range references to non-Call nodes | **66** |
| In-range references to the wrong Call | **72** |
| Targets with invalid call references | **181/269** |
| Binding records | 1,284 |
| Out-of-range binding references | **683** |
| Targets with dangling binding references | **204/269** |

Thus **1,050/1,053 (99.72%) call references were invalid**. This falsifies the referential integrity of Run244's compact typed graph, not its source round-trip or serialization-size results. Any dependency-localization claim based on v1 must be withdrawn.

## Correction and independent validation

Created a compact v2 encoder locally with call references assigned during structural traversal, separate contiguous `binding_id` namespaces, explicit `owner_node` and `definition_node`, strict parent and call-type validation, exact UTF-8 source recovery, and full re-derivation checks.

All **269/269** parseable frozen targets passed source recovery, matched IR/Python fact exposure, and reference checks; all **1,053 calls** and **1,284 bindings** had valid namespace-aware references. **22/22 local tests passed** (12 existing, 10 new). V2 IR costs **708,067 bytes** versus **623,908 bytes** for v1 (+13.49%); v2 Python+same facts costs **673,224 bytes**. These are bytes, not model tokens.

Frozen source SHA-256:
- Run237: `76c0e84f052f9dc87d9d8147e3fd2916539c36939dbc899adc0011c003dfc748`
- Run242: `83f82851d62fd2a147fa274f338e569ce01684e10d28a5f5edf989327ef383ab`

**Reproducibility status:** The full 1.23 MB archive with executable v2 implementation, independent auditor, regression tests, 269-target JSON traces, and original frozen ZIPs is preserved in the run's local artifacts. This GitHub report does **not** imply that the full code/archive has been mirrored to GitHub; that persistence remains outstanding.

## Next decisive experiment

Qualify at least two additional independent real multi-file issues with pinned commits, original-failing/reference-passing functional oracles, and per-file reversion controls. Then run an adequately powered, cluster-aware capable-model comparison between corrected v2 and genuine ordinary Python, with identical information, authority, compiler, verifier, seeds and budgets. Measure tokens with the pinned model tokenizer. The previous 306 independent-pair estimate is a hypothetical lower bound; with five tasks per repository and assumed ICC 0.10, an illustrative design effect of 1.4 raises this to about 429 total pairs (not an exact clustered power calculation). Preserve the 89 untouched boundary issues.

**Scientific status:** typed syntactic graph, not sound call resolution; no model inference this run; no IR win; Lattice unfinished. Do not pause the hourly research automation if GitHub persistence or CI is blocked.
