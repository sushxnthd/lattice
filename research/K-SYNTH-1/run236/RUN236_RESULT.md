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

Local reproducibility package: `run236_audit.py`, `run236_patch_serializer.py`, two test modules, original nine raw artifacts, JSON audit, frozen unseen-boundary preregistration and SHA-256 manifest. **17 local tests passed.** The auditor handles malformed/truncated JSON without crashing and never re-scores frozen outcomes. An independent exact-source Parcels witness reconstructed the baseline with a verified SHA-256, reproduced Git error 128 on the original patch, and verified exact-byte replay of a corrected patch (SHA-256 `d785cdc0ac5ded925a3b0a415156664b996eba0745c22c0f415abf05b33176fd`). The patch serializer handles missing newlines, new/deleted files, binary content, and exact-byte replay.

Recover pending Run234 indices 7,10,11; prospectively enforce declaration survival, Git patch replay and executable functional oracles in the next cohort; preserve matched source facts, model, compiler and edit authority between arms. Do not use compiler acceptance as a repair proxy or redesign syntax cosmetically. No representation advantage or world-class completion is claimed.

## Ten-repository extension and descriptor counterexample

The genuine `cuthbertlab__music21-1775` artifact (index 7) subsequently completed. Both model arms were rejected for invalid Python syntax; their raw completions, prompts, token usage, hashes and verifier traces passed independent artifact verification. The current total is **10 independent repositories / 20 genuine model completions**, with frozen compiler acceptance unchanged at IR 6/10 and Python 4/10. The remaining cloud jobs are indices 10 and 11.

An independent executable witness exposed another distinct safety violation in the only previously unresolved compiler-accepted edit. For `oceanparcels__parcels-2091`, semantic IR removed `@property` from `FieldSet.time_interval` while retaining the method declaration. Reversed the exact genuine Git patch to reconstruct the pinned original source, verified both original and edited SHA-256 hashes, and executed the isolated method with an empty field collection. **Before:** `obj.time_interval is None` and the class descriptor is `property`. **After:** `obj.time_interval` is a callable bound method and the class descriptor is `function`. This is an observable API regression even though declaration preservation and syntax checks pass.

The prospective semantic contract now checks both exact AST scope and decorator/descriptor preservation, unless an explicit decorator change is authorized. This is a necessary safety gate, not a proof of functional correctness. The Run234 frozen compiler and all original scores remain unchanged.

**Updated bounded finding:** All **10/10 compiler-accepted** outputs across the ten completed issues violate at least one independently checked necessary condition (six declaration deletions, one descriptor regression, one disabled extension, one unchanged pipx failing argument, one invalid Git patch). The other 10 outputs were rejected by the frozen compiler. Thus **20/20 observed completions are ruled out under the available necessary conditions**. No fully functional repair was verified. This does not estimate general model performance or prove either representation is better. **24 local tests passed**, including exact original-source reconstruction and independent behavior witnesses. The 89 reserved boundary issues remain untouched.
