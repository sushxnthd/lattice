# Run457: conservative paired-evidence gate (2026-11-03 UTC)

Implemented a standalone Python 3.11 standard-library paired audit and 11 executable unit tests. Local tests: 11/11 PASS. This is **infrastructure supporting experimental validity**, not new model evidence or an additional qualified repair.

The auditor requires exactly one semantic_ir and one python_ast record per (repository, task), complete SHA-256 provenance fields (source, prompt, model, raw completion, compiler trace, oracle trace), and a functional pass/fail verdict. It excludes incomplete pairs, model/source mismatches, infrastructure failures and unknown outcomes from paired win counts; it retains per-repository discordance for cluster-aware inference. Duplicates, malformed hashes, invalid enums, and schema drift fail closed.

Local SHA-256:
- paired_audit.py: 78a90a626799070a208c29446f8383e34b9952d0846fd7b065d2436a83757626
- test_paired_audit.py: 89f4f4988aebf7151671ecb8a3fca8350c7f78d71713fdb5ab0155158eb189fc
- test_output.txt: 4bf254e14c1b392c33be5b6bed9fc753d1cecef12205e40133c619bcf0e5876a

The local executable archive is retained separately; this report does not assert its GitHub mirroring. **Limitations:** matching source and model hashes alone does not prove equal edit authority, compiler, oracle, decoding parameters or information-equivalent prompts. Those require a separately frozen task-level manifest and executable contract checks before any confirmatory comparison. No model was run. No new qualified task. No significance claim. All 89 reserved boundary issues remain sealed. Keep PR #9 draft and unmerged.

Next: strengthen the manifest to pin oracle/compiler/seed/token budgets and prompt-information parity, then run real paired completions and isolated functional tests. Do not substitute another constructed significance example for primary research.
