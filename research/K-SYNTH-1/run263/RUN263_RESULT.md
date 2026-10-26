# K-SYNTH-1 Run263 result (2026-10-26)

**Scope:** one research kernel, branch `research/exp003-context-order`, draft PR #9, 89 boundary issues sealed. No new model inference or independently qualified issue.

## Independent upstream qualification audit

- Corrected checkout workflow [40271613254](https://github.com/sushxnthd/lattice/actions/runs/40271613254) ran six frozen urllib3 PR5071 ablations and printed `QUALIFIES False`, but wrote `qualification.json` inside a temporary worktree that was deleted before artifact upload.
- Diagnostic workflow [40274147736](https://github.com/sushxnthd/lattice/actions/runs/40274147736) failed before qualification because its overlay text did not match. This failure is preserved.
- Diagnostic workflow [40274278040](https://github.com/sushxnthd/lattice/actions/runs/40274278040) ran all six pinned variants and uploaded artifact 12629662134, ZIP SHA256 `bc90b672a04fd10c2f8a79d926c5a962b31d04d8565cd918db8fe6d44202ea70`. Independently audited the full artifact: **all six variants failed before functional checks** with `ModuleNotFoundError: No module named 'urllib3._version'`. Its `qualification.json` matches the artifact's SHA manifest; `console.txt` does not because `tee` appended after the manifest was generated. **Candidate remains UNQUALIFIED.**
- Submitted strictly environmental, identical-in-all-arms generated-version shim `__version__ = '0+source-checkout'` without changing the three production targets or any frozen endpoint. Runner SHA256 `601b4fedc0aed933fb91d05c86c1149dde890fefaf70253344497f75a95e5756`; workflow commit `0e80559af0ad1d00bcdf0869c57c69ecff1adfb1`, [run 40274404783](https://github.com/sushxnthd/lattice/actions/runs/40274404783) queued at last inspection. No outcome claimed.

## New executable construct-validity counterexample

Run261 editor v2 used `ast.parse` as its final Python validity check. **Parsing does not imply compilability.** Seven executable witnesses (module-level `return`, `break`, `continue`, `nonlocal`, `yield`, `await`, and duplicate parameters) passed `ast.parse` and the v2 editor but failed CPython `compile(..., 'exec')`.

Built editor v3, SHA256 `987785d5ffcbb2386a4af9bb71aa808db10140124b24ad84a6d8f62ad6a126bb`, replacing only the final check with non-executing `compile(..., 'exec', dont_inherit=True)`; all original SHA-pinned byte-span, Unicode-boundary, authority and atomicity checks remain. Restore using `research/K-SYNTH-1/run263/RESTORE_COMPILABLE_EDITOR.py`. CPython 3.13.5 local results: **40/40** tests pass; 7/7 explicit witnesses rejected by v3; **512/512** seeded invalid compile-time mutants accepted by v2 and rejected by v3. Repeated the 512-mutant paired AST-anchor/Python byte-span parity experiment with v3: **145 accepted, 367 rejected, zero arm disagreements**. Five real Flask reference edits reconstruct both files exactly. These are compiler tests, **not model outcomes or semantic-IR superiority**.

## Next

Audit the environmental-shim run, qualify independent genuine two-source public-repo repairs, implement bounded verified semantic/dataflow IR versus information-equivalent ordinary Python using the same v3 compiler and isolated oracle, then run prospective capable-model inference. Preserve all failures, exact prompts, raw outputs, token counts, uncertainty and SHA manifests. No significance or breakthrough claim without powered independent evidence. Full local Run263 archive includes complete auditor, seven witnesses, 512-case raw stress traces, code and upstream artifact.
