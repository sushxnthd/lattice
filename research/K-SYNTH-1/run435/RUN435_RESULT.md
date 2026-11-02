# K-SYNTH-1 Run435 — PEP 669 monitoring is invisible to sys.gettrace

## Decision
Executed a new bounded CPython 3.13.5 counterexample and a trusted restricted-fragment isolated-worker positive control. A `sys.monitoring` LINE callback mutates a live frame's exact-integer `x` via `frame.f_locals` while both `sys.gettrace()` and `sys.getprofile()` are None. Therefore those two checks alone cannot verify the closed-world precondition of Run432's assignment-commutation theorem. Run434's existing `environment_verified=false` receipt remains correct.

## Exact witness
Original: `a=x+3; b=x*5; return a-b`. Swapped: `b=x*5; a=x+3; return a-b`. With `x=7`, both closed-world returns are -25. A PEP 669 callback changes x to 99 immediately before the second assignment: original returns -485, swapped returns 67. No sys.settrace/sys.setprofile callback is installed.

For the general family `a=x+c; b=k*x; return a-b`, a mutation x→x' after the first assignment yields original `x+c-k*x'` and swapped `x'+c-k*x`. Their difference is `(k+1)(x-x')`, nonzero when k≥2 and x≠x'.

## Executed evidence
- 128 deterministic trusted constructed programs; 128/128 paired semantic-IR and ordinary AST compiler output digests agree.
- 128/128 closed-world return pairs equal; 128/128 PEP 669-mutated return pairs differ and match the algebraic prediction, with sys.gettrace() still None.
- 128/128 isolated `python -I -S` child pairs agree; children report no active monitoring events, no trace/profile callbacks, and isolated/no-site flags, while a PEP 669 LINE observer was active in the parent during child creation (at least one parent callback in each case).
- An independent auditor using a DIFFERENT PEP 669 tool ID replayed 128 pairs (256 extra CPython executions) and verified 1,664 predicates without disagreement.
- 1,024 CPython function executions across the main and independent experiment; 12/12 regression and adversarial tests passed.
- First attempt timed out in a child after seven records; the incomplete file was discarded and a full 128-case run succeeded with a longer timeout. The scientific protocol was unchanged.

## Scope
This is a conditional observational-contract finding, not evidence of semantic-IR repair superiority. `python -I -S` is not a general security sandbox; only trusted constructed fixtures were executed. No untrusted model-generated patch ran on the host. The two independently qualified real multi-source repairs remain Flask PR6096 and urllib3 PR5071. No new model completions or powered superiority evidence. All 89 reserved boundary issues sealed. Historical ZIP mirroring incomplete.

Local SHA-verified reproducibility archive: `lattice_run435_pep669_monitoring_scope_and_isolation.zip`; SHA256 `5eae55dbb3fa585076977d282bcb216d5d5f2ff14977aa5822bdc4fa39312f1e`; 16 verified payloads / 17 ZIP entries. Original source, raw JSONL, independent auditor, isolated worker, tests, and stdout are in the archive.
