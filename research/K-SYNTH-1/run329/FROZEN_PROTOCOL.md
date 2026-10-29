# K-SYNTH-1 Run329 prospective signature-default compiler experiment

Frozen 2026-10-29 UTC before primary execution. This is a **compiler/representation feasibility study**, not a paired model-success study or a new independent repair. Canonical sushxnthd/lattice branch research/exp003-context-order; PR #9 stays OPEN/DRAFT/UNMERGED; 89 reserved issues remain SEALED.

## Source-derived problem
The already qualified HTTPX PR #1183 historical reference changes the default `allow_redirects` argument from `False` to `True` in three functions across two production files (`httpx/_api.py::head`, `httpx/_client.py::Client.head`, `httpx/_client.py::AsyncClient.head`). The Run324 `If/IfExp.test`-only compiler cannot express such a change. This expressibility limitation is **postqualification analysis**, never a new issue qualification.

## Frozen experiment
Implement a shared, SHA-preconditioned, atomic, byte-preserving Python AST-action editor for default arguments in module/class sync/async functions. An ordinary Python/AST-action arm and any future semantic/dataflow-IR arm MUST compile through this identical trusted editor and receive identical source facts, function authority, and output schema. It must reject unknown scopes, missing/ambiguous defaults, stale hashes, duplicate targets, malformed expressions, non-expression syntax, unauthorized files, and lexical AST boundary escape. It must not execute untrusted model code.

Seed 3292026, 256 independent-seed **correlated synthetic** two-file fixtures, each with three `allow_redirects` defaults and 3 explicit-value controls. Expected accepted edits: 256/256 complete 3-function transactions, byte-identical source except the three literal default spans, and exact intended whole-module AST congruence. Independent read-only auditor must check all 256 results and replay 256*3 default-call functional cases plus 256*3 explicit-false control cases in a restricted trusted subprocess. Separately, 128 adversarial malformed/stale/unauthorized transaction attempts must be rejected with unchanged source snapshots. Primary frozen outcome is the complete counts, including failures, not a claim of semantic-IR superiority. The independent auditor must not import the compiler.

No reference-derived localization is permitted in future **model prompts**; using the historical reference to establish editor expressibility here is explicitly allowed and is NOT model inference. Real HTTPX oracle remains frozen. If any original protocol or test failure occurs, preserve it and label later corrections postfreeze.

## Next decisive gate
Execute genuine positive-control-gated paired Qwen2.5-Coder-7B model inference on independently qualified Flask, urllib3 and HTTPX, with pre-fix issue text, verified information-equivalent source/semantic facts, full raw responses, exact model SHA/seed/token budgets, shared atomic compiler and isolated oracle. Three issues are feasibility only; no powered superiority claim.
