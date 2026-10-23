# K-SYNTH-1 Run200 — common multi-file editor and semantic frame counterexample

Date: 2026-10-23. Research branch: `research/exp003-context-order`. Single draft PR #9.

## Executed results (not model inference)

Implemented a common Python multi-file patch compiler, two bijective AST-first/Python-first input views, a gold-blind real-issue pilot runner, and an adversarial test harness. Full source and raw traces are preserved in the local Run200 reproducibility archive.

- 19 local unit tests passed.
- 6,000 deterministic compiler/adversarial records: 1,000 valid repairs accepted; 1,000 unauthorized paths, 1,000 stale file hashes, 1,000 invalid ranges, 1,000 syntax errors, and 1,000 overlapping edits rejected. Five CPython evaluations per valid repair (5,000 checks) produced zero semantic disagreements.
- The compiler enforces trusted file-level authority, exact preimages, per-file version checks, syntax validity, nonoverlapping ranges, and all-or-nothing in-memory compilation. It does **not** provide a crash-atomic filesystem transaction or cross-module semantic noninterference.
- The 480-issue Run199 public manifest SHA-256 was independently checked as `f615b8c5f4f7e4b1996992105515b3e15e9678fb57a3cc0cff5cf1aef64641f2`.
- Two prospectively selected pilot issues (from discovery only): `getmoto__moto-7211`, `scrapy__scrapy-6469`. The selection is deterministic by SHA-256 of `run200-pilot-v1:<instance_id>`, before any real-issue model outcomes. This is a format/compiler pilot, not a confirmatory comparison.

## New scientific counterexample: file immutability does not protect output semantics

Initial modules:

```python
# a.py (authorized)
def f():
    return 0

# b.py (protected)
from a import f
def protected():
    return f()
```

A caller-authorized, compiler-valid replacement of `return 0` with `return 1` changes `b.protected()` from 0 to 1 while `b.py` is byte-for-byte unchanged. Both outputs were executed in separate CPython processes. Therefore a file-level frame theorem does not imply a semantic-output frame theorem in general Python with imports. Any protected-output claim must explicitly constrain dynamic/transitive dependencies or verify observable outputs. This is a counterexample to an overbroad guarantee, not evidence that Lattice IR beats Python.

## Controlled pilot design

Both input views contain identical exact source, SHA-256 hashes, and AST outlines. The AST-first arm places structural facts before Python source; the Python-first arm presents the ordinary Python source first. Both are invertible into the same fact object. They share one compiler, verifier, JSON patch schema, task text, trusted edit authority, model, seed derivation, and decoding settings. Two positive-control completions (one per arm) must both pass before two real issues are attempted.

Pinned intended model: `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M`. Runner retains exact prompts, raw responses, seeds, token usage, verifier traces, and failures. The issue retrieval policy is deterministic and gold-blind (up to three parseable Python files and 8 KB total from the pinned repository commit).

**No Run200 model inference has yet occurred; no real issue was marked solved.** Compiler acceptance is not functional repair success. The 480-issue dataset remains only a preregistered task pool; 480 pairs are approximately 81% powered for a large directional effect under the earlier hypothetical clustered model, not for moderate effects. The next decisive action is cloud model inference, followed by independent sealed functional evaluation and unseen-boundary ablation. Existing restrictions to editable `.py` files and short retrieval contexts may exclude necessary changes; coverage failures must be counted.

Source and evidence archive SHA-256: `0a9b8a13c832cf6778d7932f3f440da5af6fac70cfb8b464acd9ce4ec1889233`. Full source, tests, raw 6,000-record trace, public task manifest, and executed counterexample are retained in the Run200 local reproducibility archive.
