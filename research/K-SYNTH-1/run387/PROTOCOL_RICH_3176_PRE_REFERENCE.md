# Run387: prospective Rich #3176 qualification protocol (pre-reference)

Historical bug: [Rich #3176](https://github.com/Textualize/rich/issues/3176), repaired by [PR #3180](https://github.com/Textualize/rich/pull/3180). Only issue text, PR description, changed *filenames* and PR refs were inspected before freezing this oracle. The code patch was NOT read.

Pinned historical PR base `e76f3c3ea78481342e21a7b3328075462ab69c2b`, reference head `05c5dfc8fcbb1c967490540cc080c3d534a91a12`. Production files `rich/_wrap.py` (A), `rich/cells.py` (B). No reference test file is an oracle input.

Run exact four source variants: baseline, A-only, B-only, full reference. For each: execute `run387_rich_oracle.py` in a clean isolated environment with the historical package installed from pinned base. Overlay exactly the named production source file(s) from pinned reference head, not a cherry-pick of the PR. Test the 4 issue-derived public targets, 4 independently written heldout CJK targets, 8 controls. Every test requires exact concatenated text preservation and no line exceeding its configured cell width. The oracle is independent of reference internals and does not import its tests. Capture stdout JSON, stderr, return code, pinned Git refs, source hashes, environment, and SHA-256 of oracle.

Predeclared qualification: baseline fails at least one public target, full reference passes ALL 16 cases, each single-source ablation fails at least one of the 16, and both production sources are modified by the reference. Separately classify `TRUE_CASEWISE_INTERACTION` iff any individual case has a nonzero 2x2 correctness interaction; otherwise label `JOINT_SUITE_NECESSITY_ONLY` if both files necessary for full-suite success. This latter class is NOT proof of semantic coupling and must not be promoted to a causally coupled primary task. If full reference fails the frozen oracle, reject, do not retune. If the issue is exposed in the model prompt, classify as localization-weak. The historical issue has a known fix, so a model experiment is not investigator-blind.

Frozen oracle SHA256: `c2b12bf0dfeb75f97f1cd113c739d11cdd7559c46d3bab7b60aea78dc4308072`.
Frozen protocol SHA256 (local): `e31685774fc07b2018ac355160f612a06fe6a898724c777698e38efee9df07dd`.

No model inference, superiority, or powered claims follow from qualification alone. All 89 reserved issues remain sealed.
