# Run253: real-upstream pilot queued; iterable-once CFG counterexample

Date: 2026-10-25 UTC. Persistent research branch: `research/exp003-context-order`. Draft PR #9 remains open.

## Executable public-repository pilot

Committed the SHA-pinned `run253_real_paired.py.zlib.b64` (decompressed SHA-256 `1eff65e6c064b85bdae025798a50a1973681f97684b1d3993a4d4a42571cb396`) and GitHub Actions workflow `lattice-k-synth-1-run253-real-paired.yml`. Triggered [Actions run 40226877874](https://github.com/sushxnthd/lattice/actions/runs/40226877874), **still queued at last inspection**. No genuine model completions or upstream qualification outcomes have yet been observed. Do not report functional repair success.

Two prospectively pinned REAL public-repository issues will be checked with executable baseline-negative/reference-positive public and withheld tests before inference:

- `python-humanize/humanize` PR #206: pre-fix `922c5479ac42850e699b47e9e7de5f44a2a6e3bb`, reference `56b4fa812b0961cddc528764b5e2508cfe68e6f1`. Large integer filesize rollover.
- `pypa/packaging` PR #1411: pre-fix `d17cfaf0b77a5690f03087359e7c8d665a3c728d`, reference `959bb79c06cb883bf1ecd1ddc94a079294907e0f`. Dependency-group sibling error aggregation.

Each task has three real source files in context, but **only one editable production file**. These are multi-file-context pilot tasks, NOT a genuine multi-source-edit benchmark. The paired JSON-fact and Python-comment-fact views preserve the same sources and facts and share a strict native patch compiler, edit allowlist, pinned Qwen2.5-Coder-7B-Instruct model, and network-isolated independent functional evaluator. This tests fact ENCODING, not complete semantic-IR superiority or a fact-absent Python baseline.

## Independent science

Found an executable Run252 CFG-v2 overapproximation: a Python `for` iterable expression was incorrectly re-read on each iteration. The runtime witness `for x in (trace.append(x) or (x,x+1))` appends `[0]` exactly once. CFG-v2 assigned two candidate definitions to that iterator-expression read. New CFG-v3 separates `for_iter` (once) from `for_next` (repeated), recovering the single candidate while retaining loop-carried ambiguity in the body. This was spurious ambiguity, **not** a false-unique unsoundness proof.

CFG-v3 passed 5 new and 10 inherited regression tests. It processed all 269 previously frozen dedented real Python snippets, including 193 functions, with 1,605 control-flow edges, 1,835 use records, 812 unique labels and 577 explicit unknowns; zero construction failures. This does not establish general Python semantic soundness. CFG-v3 is locally preserved and will not retroactively alter the queued v2-pinned pilot.

Strict patch-compiler regression tests: 10/10 passed. Full local evidence archive: `lattice_run253_real_upstream_launch_and_iter_once_science.zip`, SHA-256 `661369d8ee49def838b7dba7a3330ed8a56d4aff9af37ec99a94beb9876eeeed`, 57 verified manifest entries. Full CFG-v3 source, independent witness, original frozen audit inputs and archive are preserved locally; complete mirroring remains outstanding.

## Run254 next priority

Recover actual cloud qualification and model traces when Actions runs; otherwise record queueing and continue science without pausing. Qualify truly multi-source-edit real issues across independent repositories. Freeze ordinary-Python information-equivalent baseline, mechanism ablations and unseen boundary prediction. Prior exact paired-power planning: 306 independent pairs for optimistic 80% power, 681 for smaller effects; clustering can increase requirements. The 89 sealed boundary issues remain untouched. Lattice is unfinished and no representation advantage is claimed.
