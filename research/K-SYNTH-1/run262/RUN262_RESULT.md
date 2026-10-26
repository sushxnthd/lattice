# K-SYNTH-1 Run262 (2026-10-26): real control failure and AST-action parity

## Real urllib3 qualification

Independently inspected GitHub Actions runs 40265337553, 40265376918, 40265427439 and 40265430861. All **FAILED BEFORE any functional ablation**. In the latest run the original runner SHA256 59d598432bb2acc9a5715d869924394e65c0a02a168b70a60c70cae2779fb35a was verified, but the checkout lacked `base/src/urllib3/poolmanager.py`; traceback was `FileNotFoundError`. Latest job 121386688343, artifact 12626605859 (609 bytes), uploaded ZIP digest reported by Actions c1bc9bd97212467ecbf5adfd0a511a790ed079bf93fa315de3fa6938eb905f2e. Exact root cause not established. No qualified new issue and no model inference.

Created checkout-only correction in .github/workflows/lattice-k-synth-1-run262-urllib3.yml. It replaces the partial clone/local re-clones with full clone and detached pinned worktrees, retains all original frozen six ablations, endpoint checks and upstream SHAs, and fail-closes on missing source files. Patched runner expected SHA256 74e46f0c751853e6471255306318fcbc75a942c1b9a4dd432033b229708b39f6. Corrected commit ddb5091d56fa84dbd171ddb7486aa53482ade425, run 40271613254 QUEUED at last observation. Earlier overlay revisions are not science results. Do not count urllib3 until independent oracle audit.

## New scientific/engineering control

Implemented a deterministic AST-anchor editing arm and ordinary Python absolute-byte-span arm with **identical** pinned source, AST/import facts, file authority, SHA-pinned atomic editor and functional oracle contract. Each AST node has a source-hash-bound ID and byte offsets; imports are explicitly syntactic candidates, not runtime guarantees. Both arm-specific plans normalize to the same canonical atomic transaction. This is an **AST anchoring representation contrast, NOT verified semantic/dataflow IR superiority**.

On pinned real Flask PR6096 reference edits, both arms reconstructed two upstream source files **byte-for-byte**, including all five patch transactions. 12/12 unit tests passed. The frozen source index contains 3,469 AST nodes and 70 syntactic ImportFrom records. One of five reference edits requires Module fallback, an explicit representational limitation. In 512 seeded mutant transactions (seed 2622026), both arms agreed on 145 accepted and 367 rejected, zero discordances. These are deterministic compiler parity controls on a previously used issue, NOT independent coding-model repairs or a statistical result.

Compressed source committed at research/K-SYNTH-1/run262/paired_semantic_edit_v0.py.zlib.b64; decompressed SHA256 b6bba0c379ccde4e4f1bddf71bad5eda36639a606b941107ff5af781ab0e107b. Verified base64 length 3072 and FNV32 f32150a9 after upload. Full independent tests, 512 raw outcomes, snapshots, and SHA256 manifest preserved locally in Run262 ZIP SHA256 7dd30226e2f4a1abf4054b73efa554c0055d4cd654740e5f4e17b66406480f01. Retry mirroring full archive.

## Next

Recover corrected urllib3 cloud evidence, reject if frozen controls fail; qualify additional independent multi-production-file public-repo issues. Extend into soundness-scoped cross-file dataflow IR with explicit open-world unknowns and same-information Python baseline. Prospectively freeze and run actual capable-model paired inference with raw completions, tokenizer counts, compiler and isolated oracle traces. Keep branch research/exp003-context-order, draft PR #9, and all 89 sealed issues unchanged. No breakthrough or significance claim.
