# K-SYNTH-1 Run259 — source-exact Qwen launch and open-world import counterexample

Date 2026-10-26. Persistent branch `research/exp003-context-order`; draft PR #9; 89 boundary issues sealed.

## Actual capable-model status

The two **prospectively frozen** Run258 Flask PR6096 requests are now persisted byte-for-byte at `run258_frozen_requests.zlib.b64` (commit `e08705d`). The new cloud workflow `.github/workflows/lattice-k-synth-1-run259-source-exact.yml` (commit `bfd1ae8`) launched as [Actions run 40255809444](https://github.com/sushxnthd/lattice/actions/runs/40255809444). GitHub independently confirmed all source restoration, pinned upstream controls, frozen-request SHA checks, and isolated Docker evaluator setup succeeded; model engine build was **in progress** at the last inspection. **No Run259 raw model completion, tokenizer usage, compiler outcome or functional repair is claimed yet.**

Frozen JSON request SHA256 `cc2e2795196d37c76543a8a49e262356f4f75d01bddcc46dd7ae1bb6c223ebfc`, prompt `ee93022a116b3c72cb81202cd5cd38080ffeab9aa45bed98ce67beb672a7d40d`, 3954 bytes. Python-comment request SHA256 `1e70ebc612224afaa09d7218c9ef3917b6ff7d7553130a888666782802bd330c`, prompt `ac923f307bb5d96376c8b1ca9a38796d03050d0d29d9d70b6d4398ee461443af`, 3967 bytes. Pinned Qwen2.5-Coder-7B-Instruct Q4_K_M SHA256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, seed 258001, temperature 0, max 2048. Same source/facts/edit authority/compiler/oracles, different **fact encoding only**, not genuine IR-vs-Python. Same Flask issue as prior run; do not double-count as independent sample.

## Constructive scientific counterexample

A source-verified import edge is **not a guaranteed runtime class binding** under open-world Python semantics. Two identical pinned Python source files, with `App.create` executing `from .client import Client`, produce different instantiated classes if the runtime environment replaces `sys.modules['package.client']` with a module exposing another `Client`. A deterministic 64-case executable witness changed runtime class identity **64/64 times without changing source bytes**. Therefore pinned source alone cannot uniquely determine the runtime binding in unrestricted Python. This does not rule out conservative static analysis or closed-world assumptions.

The bounded AST verifier records source hashes, relative import, target ClassDef uniqueness, local alias, and explicit dynamic unknowns. It rejects ambiguous, missing, star-import, and renamed targets. On the exact pinned Flask source, `Flask.test_client` has a syntactic import candidate to `FlaskClient` with local alias `cls`, **not guaranteed runtime invocation**. Eleven new tests passed; combined Run258/259 regression suite **21/21**. Source is mirrored compressed at `run259_import_provenance.py.zlib.b64` (decompressed SHA256 `e47e6d70d34230a5389ee02d3a78916a7208da838c17e4c254f5970f961c04b9`).

## Independent task screening and limitations

Werkzeug PR3238's two production edits were screened with an executable abstraction of the patch logic: original 500, matcher-only 500, converter-only 404, both 404 on over-limit integer routing. Thus the second file is not independently required for the targeted 404-vs-500 behavior. **Reject as a two-source benchmark** pending full pinned-upstream confirmation. Werkzeug PR3308 remains unqualified.

No new independently qualified real two-source issue, powered model comparison, general sound Python semantic IR, mechanism ablation, or unseen prediction was achieved. Full tests, traces, exact source snapshots, frozen requests and SHA-256 manifest are preserved locally; retry full mirroring without blocking scientific work.

Next: independently retrieve Run259 model artifact, audit strict compiler and all functional oracles; qualify new real two-source issues with source ablations; build information-equivalent semantic-IR/ordinary-Python study and independently validate open-world boundaries.
