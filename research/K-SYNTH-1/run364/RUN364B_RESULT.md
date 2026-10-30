# K-SYNTH-1 Run364b — original urllib3 factorial + independent ABI-adapter ablation

2026-10-30 UTC. One canonical branch, sole OPEN/DRAFT/UNMERGED PR #9; all 89 reserved issues SEALED.

## Original prospective source experiment

[urllib3 PR #5126](https://github.com/urllib3/urllib3/pull/5126), base e349d97f2bf234b95d5dd9e689d056a521dfc3b0, reference 580df2aab0340c2f81cf2770012875e4530a101d. Frozen public-API loopback HTTP proxy oracle SHA256 **30896d34a903203c27a5da55275d16faaa6eb9f95879f49d3e1b1968152d5ffb**, 7 targets + 6 controls. Original source blobs were SHA-verified before execution.

Preserved first [head-fetch failure 41047243133](https://github.com/sushxnthd/lattice/actions/runs/41047243133) and [packaging failure 41047316919](https://github.com/sushxnthd/lattice/actions/runs/41047316919). The latter original artifact ZIP SHA256 **e10bf0b6f2b21cfb3d1405ef6009b15859a48b93355e5618c0589dd6cfdf7f0f**, inner ZIP SHA256 **748aaf49f7a8ba439f5e0cc2b67245fe79e5f331234b21f9c95e65123b6bdb49**, 12/12 original payload hashes verified. It failed because the generated packaging module _version.py was absent. Restored the identical inert generated version module in every arm, without changing the frozen oracle or two SHA-pinned production files.

[Original historical replay 41047456979](https://github.com/sushxnthd/lattice/actions/runs/41047456979) **SUCCESS**, artifact 12973770012 outer ZIP SHA256 **fca5367a52fbd417af073a6f23bceba9a6751c1d88e28315652742c709faa545**, inner ZIP SHA256 **09a787735ea2689c669002fa002034c8231f74db37203380ccd2b0f7eacb4314**. Independently verified 12/12 inner manifest hashes, all four source blob pairs, frozen oracle and **39 actual functional case outcomes**.

| Original source arm | Targets | Controls | Interpretation |
|---|---:|---:|---|
| Baseline | 2/7 | 6/6 | 13 observed |
| connectionpool.py only | 2/7 | 6/6 | 13 observed |
| poolmanager.py only | N/A | N/A | 13 pre-oracle ImportErrors |
| Both reference files | 7/7 | 6/6 | 13 observed |

The poolmanager-only arm imports _is_same_host, a helper introduced by the reference connectionpool.py. **Original frozen verdict: INCONCLUSIVE**, not qualified, because only 39/52 cases executed. Never code these import failures as functional zeroes or retrospectively change qualification.

## New sharp-bounds counterexample

The casewise 2x2 factorial interaction f11 - f10 - f01 + f00 has exact sharp bounds **[0,1] for each of the 13 cases** because f01 is missing. Treating the ImportErrors as zero would falsely report **13/13 positive interactions, including all six unchanged controls**. The independent executable bounds auditor verified all 12 original manifest payloads and retained missingness explicitly.

## POST-OUTCOME mechanism ablation (not a historical qualification)

A separately labelled 9-line compatibility adapter delegates _is_same_host to the **baseline** HTTPConnectionPool.is_same_host / HTTPSConnectionPool.is_same_host method. Adapter SHA256 **592a3bc138d851f5b8f65548ce949877176fb554372506c3f3da925b2b9bba51**. It does not copy the reference helper.

[Independent isolated ablation 41047685606](https://github.com/sushxnthd/lattice/actions/runs/41047685606) **SUCCESS**, artifact 12972419198 outer ZIP SHA256 **d0782250ecfb8b2d2d35247da39b4c7dc34f7ce55b23a234a317248f930e0d5e**, inner ZIP SHA256 **87974d15989894303880f57da4f7aa5e0db40d2191b786141798739f6885adb1**. Independently verified 5/5 payload hashes, frozen oracle and **13/13 actual functional outcomes**. Reference poolmanager + baseline connectionpool + adapter passes **7/7 targets and 6/6 controls**, matching full reference on this finite oracle.

**Mechanism finding:** observed two-file necessity can be explained by API extraction/import compatibility, not uniquely by a semantic cross-file effect. This is a bounded negative construct-validity result, not general semantic equivalence across all inputs. No new model inference, powered IR advantage or breakthrough. Qualified cohort remains eight PRs across seven repositories.

Complete SHA-verified local archive: lattice_run364b_original_proxy_and_abi_mechanism.zip, 18 payloads, SHA256 **c550fb8364b213c3d06b8768f2b34d89c7c4637bd544d6caa9cef2c3cabae7be**. Continue new independent task recruitment and token-controlled Qwen IR versus ordinary Python/AST-action functional comparison.
