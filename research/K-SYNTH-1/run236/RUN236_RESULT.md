# Lattice Run236: nine-repository paired audit and patch-validity counterexample

Date: 2026-10-25. Original frozen experiment: [Run234](https://github.com/sushxnthd/lattice/actions/runs/40148667367). All primary functional outcomes remain **NOT_EVALUATED**. This is an independent secondary audit, not a retrospective change to the frozen endpoint. The 89 reserved boundary issues were not accessed.

## Authentic evidence

Recovered five additional genuine Qwen2.5-Coder-7B-Instruct Q4_K_M artifact pairs (indices 2,5,6,8,9), combined with the four pairs previously audited in Run235 (0,1,3,4). Independently checked all nine SHA-256 manifests, frozen prompts, model IDs, seeds, token usage, source-fact equivalence hashes and original verifier records.

| Measure, nine repositories | Semantic IR | Annotated Python |
| --- | ---: | ---: |
| Actual model completions | 9 | 9 |
| Frozen compiler accepted | 6 | 4 |
| Git patch check passed among accepted | 6 | 3 |
| Accepted edits erasing named declarations | 3 | 3 |
| Truncated/invalid JSON | 0 | 1 |
| Total prompt tokens | 74,275 | 78,151 |
| Total completion tokens | 2,713 | 4,381 |
| Fully verified issue resolutions | none established | none established |

Compiler acceptance was discordant in four pairs (IR-only 3, Python-only 1), exact two-sided McNemar p=0.625. Compiler acceptance is **not** functional success; these nine issues cannot establish representation superiority.

## New executable counterexample

The genuine annotated-Python completion for `oceanparcels__parcels-2091` was marked `accepted=True` even though its recorded `git apply --check` returned **128**, `error: corrupt patch at <stdin>:28`. Its replacement omitted a terminal newline. Run234's `difflib.unified_diff` patch writer failed to encode the missing newline, and `invoke` set `accepted=True` without requiring a successful patch check. This makes one compiler-accepted output unusable as a Git patch. Original records are unchanged. A prospective byte-faithful `git diff --binary` serializer with replay verification was implemented locally.

## Independent necessary conditions

Among ten compiler-accepted completions: six erased their selected function/method declarations (both arms in Benchopt and Bluesky, IR in Amaranth, Python in Midea); the Sphinx IR edit disabled the extension instead of fixing it; the pipx IR edit reproduced the same failing launcher argument (independent Run235 witness); and the Parcels Python edit produced the invalid patch above. Thus **9/10 compiler-accepted completions fail at least one independently checked necessary condition**. Eight more completions were rejected by the frozen compiler. **17/18 are ruled out under available necessary conditions; the remaining Parcels IR edit is unverified, not successful.** This is a bounded finding for the completed tasks, not an estimate of general model reliability.

## Artifacts and next experiment

Local reproducibility package: `run236_audit.py`, `run236_patch_serializer.py`, two test modules, original nine raw artifacts, JSON audit, frozen unseen-boundary preregistration and SHA-256 manifest. **16 local tests passed.** The auditor handles malformed/truncated JSON without crashing and never re-scores frozen outcomes. The patch serializer handles missing newlines, new/deleted files, binary content, and exact-byte replay.

Recover pending Run234 indices 7,10,11; prospectively enforce declaration survival, Git patch replay and executable functional oracles in the next cohort; preserve matched source facts, model, compiler and edit authority between arms. Do not use compiler acceptance as a repair proxy or redesign syntax cosmetically. No representation advantage or world-class completion is claimed.