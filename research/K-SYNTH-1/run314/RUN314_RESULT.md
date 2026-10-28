# K-SYNTH-1 Run314: byte-safe common compiler and true Python AST-action parity

Date: 2026-10-28 UTC. Canonical `sushxnthd/lattice`; branch `research/exp003-context-order`; one open/draft/unmerged PR #9; all 89 reserved issues sealed.

## Prospective provenance
Frozen protocol commit: `666d7de38a9fb94abb452669048521686798fd07` **before** primary execution. Frozen 1,024-case JSONL SHA-256 `5bd87106b6ab13326767018d65264c9738d7bde2b2c09baa4beee485cfc3b09d`. Frozen executable SHA-256 `76303ad14489e035d95a1714469e7ba333efd6d5b8f06f3ecdcf4646333ec839`. CPython 3.13.5.

## Result
Python AST column offsets are UTF-8 byte offsets, not Unicode character indices. A naive character-index source splice failed **768/1,024** exact-edit controls in six of eight correlated templates. The SHA-preconditioned byte-safe atomic compiler produced **1,024/1,024** byte-identical results from (A) typed IR and (B) an actual parsed Python `ast.Constant(value=...)` constructor action, without `eval` or execution of model code. All 1,024 AST functional checks passed.

An independently implemented read-only auditor reconstructed all edits from UTF-8 source bytes, verified the frozen input/output hashes, and executed all 1,024 **trusted generated** functions under restricted builtins, with **zero discrepancies**. Postfreeze exploratory negative controls rejected 10/10 unauthorized AST actions and 3/3 stale source/node preconditions.

## Limits
Eight synthetic templates x 128 correlated variants, **not** 1,024 independent real repairs. This is a bounded compiler-contract result, not semantic-IR superiority. No new model inference, no newly qualified real repair, no powered claim or breakthrough. The IR action here replaces a uniquely identified integer constant; it is not a production semantic/dataflow editor. Six previously qualified historical repairs remain six. Failed historical qualifications remain failed. All 89 reserved issues remain sealed.

Full 12-payload SHA-verified archive retained locally with generator, original raw traces, independent auditor, negative controls and manifest. Archive SHA-256: `861ec3d2b69d4efdeba9e9a3765a8fc898c68ddcb0dfceda66147a94303b6987`. Large historical GitHub ZIP mirroring remains incomplete.

## Next
Implement a multi-file atomic transaction with rollback, independently validated compiler and information-equivalent real AST-action/semantic IR frontends, then run actual paired capable-model inference on independently qualified public-repository repairs without reference-derived localization. Preserve raw prompts, model SHA, seeds, tokens, completions, compiler/oracle traces and negative outcomes.

Bounded source-compiler prototype committed as `research/K-SYNTH-1/run314/atomic_compiler_prototype.py` (local SHA-256 `4c278e0f8f109a3c6bd883626df26239b4ee23674cb516ab08771048a832aedf`), smoke-tested on UTF-8/CRLF and malformed-action rejection. The original frozen experiment runner and all raw records remain in the local ZIP; the prototype is a separately extracted implementation, not a retroactive modification to the frozen runner.
