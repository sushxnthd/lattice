# K-SYNTH-1 Run387: prospectively qualified Rich cross-file repair and annotation counterexample

**New independently qualified historical bug:** [Rich #3176](https://github.com/Textualize/rich/issues/3176), [PR #3180](https://github.com/Textualize/rich/pull/3180). Frozen issue-derived black-box oracle committed **before inspecting reference diff**, commit `c598d9a9`, oracle SHA256 `c2b12bf0dfeb75f97f1cd113c739d11cdd7559c46d3bab7b60aea78dc4308072`. Pinned base `e76f3c3ea78481342e21a7b3328075462ab69c2b`, reference `05c5dfc8fcbb1c967490540cc080c3d534a91a12`.

| Variant | Public targets | Heldout targets | Controls | Original process |
|---|---:|---:|---:|---|
| Baseline | 1/4 | 3/4 | 8/8 | success |
| Reference `_wrap.py` only | not observed | not observed | not observed | TypeError unexpected `width` |
| Reference `cells.py` only | not observed | not observed | not observed | TypeError unexpected `max_size` |
| Both production sources | **4/4** | **4/4** | **8/8** | success |

Both source components are necessary for the prospectively frozen **joint target-plus-control** oracle. This qualifies a genuine historical two-source repair, not a blinded model experiment. The mechanism is exact direct-call API coupling: `divide_line` and `chop_cells` must change keyword names together. A separate binding-only AST certificate reports **compatible/incompatible/incompatible/compatible** across the four SHA-pinned source combinations. It is conditional on import completion, direct binding, no rebinding, and fixed argument shapes, not a general semantic proof.

The **post-freeze**, separately labeled casewise diagnostic records 64 outcomes: baseline 12/16, A 2/16, B 2/16, full 16/16. Per-case 2x2 correctness interaction is 0 in 2 cases, +1 in 4 and +2 in 10. Do not substitute these into the original oracle, whose A/B processes aborted on the first case.

Original failed infrastructure attempt [41192183856](https://github.com/sushxnthd/lattice/actions/runs/41192183856) was preserved. Corrected original experiment [41192239326](https://github.com/sushxnthd/lattice/actions/runs/41192239326), original source/contract [41192328244](https://github.com/sushxnthd/lattice/actions/runs/41192328244), final diagnostic [41192395371](https://github.com/sushxnthd/lattice/actions/runs/41192395371). Final artifact ID `13039416240`, original ZIP SHA256 `8bab8077bbed0e86769365e8d72054c883352a99dd238c9e3d6a1c7c2730fdf0`. Independent auditor verified **33 internal SHA entries**, four pinned source SHA256s and four original GitHub blob SHAs.

**Separate soundness correction:** Run386's effect certificate incorrectly admitted parameter annotations, although CPython may evaluate them at function definition time. Constructed executable `NameError` and event-emission counterexamples; hardened analyzer returns explicit `UNKNOWN`. 1,024 deterministic annotated cases rejected; all 256 prior unannotated certificates retained exactly, covering 16,384 finite observations. See local full evidence archive and the committed executable `run387_definition_time_guard.py`.

Full SHA-verified local reproducibility ZIP: `lattice_run387_prospective_rich_crossfile_repair_and_soundness_falsification.zip`, SHA256 `3bda5a5451f2a3d9f13b5b6b5260d6b9c5fb86ac744070ad75d8e4f2bcc8edd9`, 23 payloads; clean extraction, independent audit, 1,024-case fuzz and 7/7 contract tests PASS. Full ZIP mirroring to GitHub remains incomplete.

**No model inference, powered IR superiority, general Python soundness or breakthrough claimed.** One K-SYNTH-1 kernel, one canonical branch, sole draft PR #9. All 89 reserved issues sealed.
