# K-SYNTH-1 Run266 — deferred-call provenance counterexample

Date: 2026-10-26. Existing branch and draft PR #9; 89 boundary issues sealed.

## Constructive falsification
Run265's bounded MAY provenance graph incorrectly analyzes calls nested inside a lambda at *creation time*, although a lambda body runs later. Executable CPython counterexample:

```python
def f():
    target = lambda: 1
    thunk = lambda: target()
    target = lambda: 2
    return thunk()
```

Actual result: `2`. The Run265 call record for `target()` contains only the line-2 lambda, omitting the executed line-4 lambda and `UNKNOWN`. Thus even this restricted MAY analysis is unsound on this example.

## Corrective implementation and evidence
Local `bounded_provenance_ir_v2.py` marks calls nested under `Lambda`, `GeneratorExp`, `ListComp`, `SetComp`, or `DictComp` as `evaluation_phase=deferred_or_nested_unknown` and includes `UNKNOWN` in the may-origin set. Direct-call precision is retained. This is conservative, not a sound general-Python analysis.

Seed 2662026, 256 deterministic executable closure-rebinding programs: old analyzer misses actual callee in **256/256**, v2 covers actual callee via UNKNOWN in **256/256**. These are adversarial witnesses, NOT independent real-repository samples or statistical evidence. **67/67 local tests passed** on CPython 3.13.5.

Pinned Flask PR6096: 179 call sites and 3 source-verified import candidates in both versions. Two calls newly labeled deferred/nested; all 179 already had UNKNOWN in the old graph, so no real-task precision improvement. Old graph SHA256 `b51913f505276f7a32c0a2600159ddda49ce1f13d46cf584d62856ddaae4dc11`; new graph SHA256 `48018d1b5181caa33f8509508fec46d78d817299053e3b2884fbc51f6ffe68d9`. New source SHA256 `38f60d2f17d14300d307b061988ae6a9600b45851149399df0144b8c06c02eda`.

## Scientific status
Two independent qualified real two-production-file reference-patch tasks remain Flask PR6096 and urllib3 PR5071. Run265 frozen Flask requests remain unchanged. **No new model inference, urllib3 prompt freeze, or model-patch functional oracle evaluation occurred.** No representation advantage, statistical significance, or breakthrough is claimed.

Full 77-entry SHA256-verified local evidence archive: `/mnt/data/lattice_run266/lattice_run266_deferred_provenance_counterexample.zip`; archive SHA256 `8e65f1a06cfbccbdcad74dab0e471aabb4a3a2f2a251eb09f49c49b7072cdd36`. Includes code, exact prior frozen prompts, 256 raw witness traces, 67-test run, pinned Flask snapshots and provenance deltas. Full source and frozen requests are not yet mirrored to GitHub; retry persistence.

Next: mirror full executable sources, freeze urllib3 paired requests, launch pinned Qwen7B on both qualified issues, and expand independent issue qualification.