# K-SYNTH-1 Run212 — independent Run210 model audit and semantic-rename counterexamples

Date: 2026-10-24. Branch: `research/exp003-context-order`. Draft PR #9.

## Recovered actual capable-model results

Both jobs of [Run210](https://github.com/sushxnthd/lattice/actions/runs/40051627638) finished and published artifacts 12544752630 and 12545931336. Model: Qwen2.5-Coder-7B-Instruct Q4_K_M, GGUF SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`. Audited all 12 request/response/verifier triples for prompt hashes, seeds, token counts, completion reasons, and recorded verdicts.

Six of six positive controls passed. On the two real-repository issues (six completions), compiler acceptance was semantic-node-IR **1/2**, Python-short-ID **1/2**, Python-text **0/2**. IR and Python-short-ID tied on both issues (one both accepted, one both rejected). **Zero functional issue resolutions were evaluated.** The two accepted Zulip edits touched different files and neither has an independent functional pass. The Ragna metadata-filter issue failed in all three arms. The operational IR and short-ID representations still share the same target IDs and differ primarily in wording. No representation advantage can be inferred.

The Zulip requirement includes fallback to old presence constants on older servers; the IR accepted edit merely reads optional initial-data fields with `.get(...)`, without implementing that fallback in the edit. The accepted short-ID edit changes theme configuration, apparently unrelated to the presence issue. These are inspection warnings, not a substitute for independent functional evaluation.

## Decisive Run211 counterexamples

The previous semantic rename kernel accepted all four of these behavior-changing edits:

1. Python `match x: case old: return old`: pattern capture binds `old` without `ast.Name(Store)`; rename changes `probe(11)` from integer 11 to a function object.
2. `import builtins as b; b.getattr(target, "o" + "ld")()`: rename changes a successful call returning 7 into `AttributeError`.
3. `import target as t; alias = t; alias.old()`: module alias escapes the direct AST attribute pattern, so the old kernel leaves the call stale and causes `AttributeError` after renaming.\n4. `old.__name__`: rename changes the observed string `old` to `new`.

These falsify any general behavior-preservation claim for the original prototype. The accompanying `semantic_refactor.patch` now rejects these and related pattern-capture/reflection/alias-escape cases. **This is not a proof of soundness** for arbitrary Python or dynamic external callers. The complete before/after execution witnesses, compiler traces, original/patched source and model archives are preserved in the local Run212 reproducibility ZIP.

Validation: **29 tests passed** (20 prior tests + 9 new regressions). GitHub branch contains the patch and tests; apply the patch to the Run211 source archive.

## Power and next experiment

The earlier 468 discovery-pair estimate was a simulation under optimistic assumptions. A conservative normal-approximation paired design calculation at alpha 0.05, power 80%, 30% discordance, 65% IR wins among discordant pairs, ICC 0.5 and mean 391/157 tasks per repository gives approximately **289 independent or 504 cluster-adjusted discovery pairs**. The frozen discovery cohort has 391. This is a planning sensitivity, not an effect estimate. The 89 held-out boundary issues remain sealed.

Next decisive gate: compare a genuinely distinct semantic edit action against ordinary Python edits and an equally compact Python short-ID baseline with identical task facts, edit authority, compiler, verifier and model, followed by independent functional evaluation. Keep one K-SYNTH-1 kernel and one draft PR. GitHub/CI interruptions must not pause scientific work.

## Limitations

No new capable-model completions were generated in Run212; its model evidence is an independent audit of completed Run210 inference. Original workflow artifacts lack full base repositories, so raw/record/verifier consistency was checked but full compiler re-execution and functional issue tests were not possible in this run. The semantic editor remains a prototype.
