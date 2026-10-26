# K-SYNTH-1 Run273: urllib3 frozen-authority reference reachability

Date: 2026-10-26 UTC / 2026-10-27 IST. One branch, one draft PR #9, all 89 boundary issues sealed.

## Scientific result

On independently qualified REAL urllib3 PR5071 (base `f4e4bc31f40f8c94c6a1f1685df28f97ff48c305`, reference `f5cf122346141b187cca0db6e6445297d336b610`), the UNCHANGED Run271 blind baseline-derived candidate generator yielded 192 AST nodes, 96 per production file. Post-freeze reference-privileged analysis identified three nonoverlapping source-derived If candidates for manager port-zero, proxy port-zero and URL-netloc port-zero handling. Replacing those three conditions reconstructed both upstream reference production files byte-exactly. This proves gold expressibility under frozen edit authority, not model repair.

Frozen facts SHA256: `669e1a217298b61cf5ffd6612fe05e899192554f4b4d259dcf8ef39f684bce52`. Candidate IDs: manager `c1d6ef8be275ba8d7d6de762`, proxy `cca3735bb8d068c19ce1b59a`, URL `37c416d5f2a8c0c774eec80d`.

## Independently executed functional ablation

GitHub Actions run [40379403952](https://github.com/sushxnthd/lattice/actions/runs/40379403952) SUCCESS. Artifact ID `12678926150`, original ZIP SHA256 `69856210c6b0da6f30301d759cc4ef282c472512f626d9748aa27ff6504ff21e`. Independently verified all 11 artifact-manifest entries, source hashes, original frozen requests and reversible facts. All 8 combinations of the three source corrections were tested with a six-check trusted pinned-source oracle. All **48/48** outcomes matched expected manager/proxy/URL behavior and nonregressions. This is a finer-grained source ablation, NOT a third independent real issue.

Independent local replay of all four true AST-node vs authorized Python byte-span Run271 conditions, using unchanged v4 atomic compiler and exact frozen urllib3 facts, showed 4/4 byte-exact gold positive controls and **0 discordances across 576 matched mutations / 2,304 strict compiler executions** (384 cases accepted, 192 rejected). All 192 AST candidate IDs mapped to distinct byte spans. These are compiler/interface controls, not model outcomes.

Initial workflow [40379340781](https://github.com/sushxnthd/lattice/actions/runs/40379340781) failed before jobs because embedded Python source was not YAML-indented; fixed in commit `813f46963eb172c13cfb4236e617dca1e996c570`. Failure preserved.

## Limits

Run271 blind Qwen Actions [40357685395](https://github.com/sushxnthd/lattice/actions/runs/40357685395) still IN_PROGRESS at eight requests; no raw completions, tokens or functional model outcomes recovered. Two independent qualified tasks total. Graph JSON and Python literal share identical facts; no intrinsic semantic-IR superiority or statistical significance is identified. Complete historical GitHub mirroring remains incomplete. Full SHA-verified local Run273 archive SHA256 `bb2841907b9044700d41e04588a3d717155253a785addd6f6e75f22277bb6f32` (13 manifest entries), available as local conversation artifact.
