# K-SYNTH-1 Run320 prospective freeze (before primary execution)

Date: 2026-10-28 UTC. Canonical sushxnthd/lattice branch research/exp003-context-order; existing open/draft/unmerged PR #9. All 89 reserved boundary issues SEALED.

Exploratory witness (not counted): Run317 replace_stmt accepts a bare @marker replacement, which can decorate the following, otherwise unedited function. Test whether a standalone-statement parser rejects this cross-node binding.

Frozen matrix: 8 families (top_function, top_class, top_async, nested_function, class_method, unicode_prefix, crlf, tab_nested) x 32 variants x 2 operations (replace_stmt, insert_before) = 512 correlated malicious cases; 512 benign complete-statement controls; 128 cross-file malicious-plus-legitimate rollback controls. Payload exactly @marker. The original Run317 compiler is unchanged. New compiler adds standalone single-statement validation for replace_stmt/insert_before.

Success criteria: original accepts all 512 attacks and trusted isolated Python shows touched=True; hardened compiler rejects all 512; 512 benign controls accepted by both with byte-identical output and untouched protected declaration; 128 malicious cross-file transactions reject with input mapping unchanged; independent read-only auditor reconstructs all outputs, checks AST decorator attachment and replays 1,536 isolated evaluations with zero discrepancies. Any failure remains reported without retroactive retuning. Synthetic correlated fixtures only, not independent repository repairs or model inference.

SHA256 pre-execution local source:
run315_multifile_compiler.py 9031621afe53a3d26c961a3a93cbe718730c10f4d327867f014c1ff806f466fe
run317_structural_compiler.py 0d412e45a296e2be56ad9b7a1a3a2c2966e4d064fefa61a0a857c3cf2a9b26c7
run320_hardened_compiler.py a47e77a037ff9e0323305133bb875ee1b023acee64987ba7c4c3d47d0a48b500
run320_experiment.py e065179a87ee9f93e1a137f43724764bb7b9574128ea849659ad251f708ffb4f
run320_independent_audit.py e859735c7a66639fd5ae3011faca9dc4d87193f367ca1fdf74d5e7ab3c5d9e51

This is a bounded transaction-boundary safety test. Do not claim general semantic soundness, real repair qualification, coding-model success or IR superiority.
