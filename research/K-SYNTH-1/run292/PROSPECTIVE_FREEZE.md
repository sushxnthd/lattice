# K-SYNTH-1 Run292 prospective alias-flow protocol (frozen before execution)

Question: Does Run291's direct-name-only temporal MAY-call inventory miss calls made through ordinary Python aliases? Test a soundness-scoped, path-joined alias candidate graph without asserting runtime builtin identity.

Frozen distinct cases and expected target candidate sets at the designated call site:
1. direct len(xs) => {len}; 2. f=len; f(xs) => {len}; 3. f=len; g=f; g(xs) => {len}; 4. f=len if flag else sum; f(xs) => {len,sum}; 5. f=len; if flag: f=sum; f(xs) => {len,sum}; 6. f=len; if flag: f=lambda x: 0; f(xs) => {len}; 7. import builtins as b; f=b.len; f(xs) => {len} with runtime binding UNKNOWN; 8. from builtins import sum as f; f(xs) => {sum} with runtime binding UNKNOWN; 9. f=len; (f,g)=(sum,len); g(xs) => {len}; 10. f=len; def g(): return f(xs); f=sum; g() => UNKNOWN_DEFERRED; 11. f=getattr(b,'len'); f(xs) => UNKNOWN_DYNAMIC; 12. exec('f=len'); f(xs) => UNKNOWN_DYNAMIC.

All known candidate sets are conditional on single-threaded trusted fixture execution, ordinary Python name assignment, no monkeypatch between alias capture and invocation, and no hidden mutation in branch predicates. The UNKNOWN cases are mandatory abstentions. Each fixture will be evaluated on both branch outcomes where applicable and multiple deterministic values, with independent CPython functional observations and a read-only audit. A nonzero miss or wrong predicted set remains in the failure ledger; never retune this freeze. Distinct cases are 12, not the number of seeded value variations.

Only four independent real repository repair issues remain qualified; this is a diagnostic, not a model-inference superiority trial. No changes to the 89 SEALED issues or PR state. Preserve original raw evidence and SHA-256 manifest.
