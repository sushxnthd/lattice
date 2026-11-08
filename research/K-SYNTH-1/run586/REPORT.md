# Run586: AST call-edge phase counterexamples

Eight deterministic Python AST fixtures executed locally. Four contained UNKNOWN call sites. The simple AST walker misattributes definition-time default-argument calls to function invocation and traverses nested lambda bodies without phase separation. Direct syntactic call edges are only DIRECT_MAY, never guaranteed runtime execution. Alias, getattr and dynamic globals require UNKNOWN. The local reproducibility ZIP SHA-256 is 95d43208da071d6ce4edb40220c7d437721e678114381f883ea66e0227ed639d.

This is a synthetic bounded counterexample, not a qualified real repair, production IR, or model comparison. Qualified real tasks: two. Reserved 89 boundary issues remain sealed. Next: phase-aware analysis and prospective real task qualification.
