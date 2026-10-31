# K-SYNTH-1 Run388: shared atomic function editor + independent binding oracle

Date: 2026-10-31 UTC. One kernel, canonical branch, sole draft PR #9; 89 reserved boundary issues untouched.

## Verified results

- Built a two-file transactional AST-function editor for the historically qualified Rich #3176 repair. Exact authorized paths, source SHA-256, function AST SHA-256, unique top-level function, replacement identity, parse/compile and all-or-nothing output are checked. Generated code is never executed on the host.
- Independently reconstructed two historical reference-function-only syntactic patches and matched both compiler output SHA-256 hashes. This is **post-reference syntax expressibility**, not a model repair or functional success.
- Built a finite Python argument-binding algebra independent of inspect.Signature. Positional-only, positional-or-keyword, keyword-only, defaults, *args, **kwargs, duplicate and missing arguments are covered; dynamic unpacking is UNKNOWN.
- 12,000 deterministic trusted-grammar CPython calls (seed 38820261031, Python 3.13.5): 2,411 compatible, 9,589 incompatible, **zero** disagreements with static decisions. Independent raw-observation replay: 12,000/12,000, zero disagreements.
- Real SHA-pinned Rich source combinations: base COMPATIBLE, wrap-only INCOMPATIBLE, cells-only INCOMPATIBLE, full reference COMPATIBLE. These are **conditional signature-shape** results, not runtime semantic certificates.
- 27/27 local adversarial and regression tests passed. The inherited Run387 23-entry manifest reverified with zero mismatches.

## Bounded counterexample

`def f(x, /, **kwargs): return kwargs; f(1, x=2)` is valid: the keyword x is captured by **kwargs, not bound to positional-only x. A blanket rejection of such keywords is incorrect. By contrast, `f(x=2)` leaves the required positional-only argument unbound.

## Reproducibility

Local SHA-verified archive: `lattice_run388_atomic_function_editor_and_binding_oracle.zip`, SHA-256 `28a907fcf711c823f3994db4b3fb71195641db7657b299a22e973487559445ff`. 23 verified payloads, clean-extraction replay of 27 tests and 12,000 observations passed. Full executable ZIP mirroring to GitHub remains incomplete; local archive is authoritative for executable details.

**No new coding-model inference, isolated generated-patch oracle, independent production issue, powered superiority claim or breakthrough.** The previous Rich frozen outcomes remain unchanged. Next: reference-excluded paired Rich pilot with shared editor and network-disabled oracle; recruit new genuinely unseen cross-file production bugs.