# K-SYNTH-1 Run378: original Qwen outputs recovered, compiler confound isolated, functional post-hoc replay

Date: 2026-10-31 UTC. Canonical repository `sushxnthd/lattice`, sole kernel K-SYNTH-1, branch `research/exp003-context-order`, draft PR #9. All 89 reserved boundary issues remain sealed.

## Original, prospectively frozen Run377 primary result

The original completed GitHub Actions run [41150199531](https://github.com/sushxnthd/lattice/actions/runs/41150199531) succeeded and uploaded artifact 13022519365. Original ZIP SHA-256 `01f2fabd21a71559d48fc04d175166acf3e68bdaeb5ace0cef5e56821a890096`. Independently verified all 37 payloads against the ORIGINAL manifest, the pinned upstream commit `5e06a9bb99a05bfc20f3e0cdb1b969967ae1dc4e`, source blob IDs, model SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, original prompt/request hashes, response bytes, usage, seed `3772026`, temperature zero, and both compiler traces.

Both genuinely completed Qwen2.5-Coder-7B Q4_K_M requests returned **byte-identical** 400-byte fenced JSON, each proposing two guarded removals, one in `httpcore/_async/connection_pool.py` and one in `httpcore/_sync/connection_pool.py`:

```python
if status in self._requests: self._requests.remove(status)
```

IR: 1,227 API-reported prompt tokens, 107 completion tokens; independent tokenizer 1,198 prompt tokens. Python/AST-action: 1,210 API-reported prompt tokens, 107 completion tokens; independent tokenizer 1,181 prompt tokens. Both finished normally with `stop`; neither is a precompletion infrastructure failure. Original outputs were fenced, but the compiler parsed them and rejected each with `preimage_count=2`, not a fence/schema error. In both exact pinned production files the proposed `old` substring occurs twice: in the target exception handler at line 233 and in an already-guarded cleanup at line 280. The original strict compiler requires a globally unique substring. **Original primary scores remain IR 0/1 and Python/AST-action 0/1 valid repairs.** Neither arm reached the original functional oracle. That oracle additionally failed on the baseline due to Git safe.directory ownership; it is not evidence of a functional failure.

## Separately labeled post-hoc contextual rescue

A new independent workflow [41154401443](https://github.com/sushxnthd/lattice/actions/runs/41154401443), committed as `.github/workflows/lattice-run378-replay.yml`, recovered and verified the original evidence and applied a **new, retrospective** source-context selector to the exact unchanged model outputs. This selector identifies the unique `self._requests.remove(status)` statement within an `except BaseException as exc` handler followed by `raise exc`. It is **not** part of the original frozen compiler, and therefore its successful patches cannot be counted as primary model repairs.

The selector found exactly two occurrences per file and exactly one contextual match (line 233). It preserved the model's original replacement text and changed only the selected line in each production file. Both source files were AST-parsed without executing candidate code on the host. Actual execution occurred only in network-disabled, read-only, resource-limited Docker containers. The historical oracle was fixed solely for Git read-only ownership using `GIT_CONFIG_COUNT/KEY_0/VALUE_0` to authorize `/upstream` as a safe directory. Original upstream source hashes were verified. The oracle ran on the original baseline and on both post-hoc candidates.

| Arm | Original strict compiler | Post-hoc public T1,T2,C1-C6 | Post-hoc heldout H1-H4 |
| --- | --- | ---: | ---: |
| Historical baseline | N/A | 6/8 | 2/4 |
| Qwen IR | REJECTED | **8/8** | **4/4** |
| Qwen Python/AST-action | REJECTED | **8/8** | **4/4** |

All 36 actual case evaluations were preserved, with six successful isolated oracle invocations, zero nonzero queue residuals and zero oracle error traces. The baseline reproduced both historical public defects (T1/T2 `ValueError`) and two heldout defects (H1/H2), while both retrospectively patched arms restored the expected cancellation and timeout exceptions and preserved all controls. The two post-hoc candidate production files are byte-identical across arms. The cloud artifact 13023902446 has ZIP SHA-256 `a466995bbcd43921984f91c180a39aedd5ffdd5e5cbc0d82a9834394ecedad44`. An independent local auditor verified its 18 manifest payloads, candidate source hashes and all 36 casewise results. Fourteen adversarial/local audit tests passed (eight original-artifact, six cloud-artifact).

**Finding:** The model generated a functionally successful repair in both representations when an unambiguous retrospective selector was supplied. The frozen compiler's global substring uniqueness requirement prevented either candidate from being applied. This is an editor-interface/construct-validity confound, **not evidence of IR superiority**. The contextual selector was designed after inspecting the output and is therefore diagnostic, not a valid alternative primary score.

## Representation, independence and limitations

The original prompts expose identical baseline source excerpts and AST-derived node facts, but the IR arm explicitly presents WAIT→EXCEPT→REMOVE→RAISE MAY edges while the ordinary Python/AST-action arm renders the node tuples without a separately spelled-out edge. The edges are derivable from the shared source; however, explicitness is a potential representational or token-budget confound. The IR prompt is 17 API-reported tokens longer. Both completions were byte-identical and were obtained sequentially from one model server; the second response reported 166 cached prompt tokens. This single task does not distinguish semantic representation effects, copying from a common prior, or model insensitivity. It was also investigator-informed after the reference repair became known, despite reference-free prompts.

## Next decisive study

Prospectively freeze a shared AST-span/action compiler that can target a unique exception handler and line/span without any post-hoc source localization. Apply **exactly the same** edit authority and atomic verifier to semantic IR and ordinary Python/AST-action presentations. Test an unrelated schema-only positive control in both arms; perform two controlled prompt reformulations and a genuine reference-blind paired pilot on previously unseen independent production issues. Record all raw completions, exact source/model hashes, compiler traces, isolated functional oracles, and per-repository clustering. If Python ties/beats IR twice, pivot to a rigorously characterized negative result rather than claiming superiority.

No powered statistical advantage, new qualified production PR, or breakthrough is claimed. Historical cohort remains 10 qualified PRs; all 89 sealed issues untouched.
