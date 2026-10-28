# K-SYNTH-1 Run309: nested assignment-expression false negatives and recovered original cloud evidence

**Original scientific result:** Run308's bounded source-only module-binding analyzer incorrectly excluded a real `builtins.len` call after nested `NamedExpr` rebinding. A prospective 384-case, 16-template trusted CPython 3.13.5 experiment found **192 definite-negative false negatives** in the unmodified original and **zero** after conservative invalidation. The correction returns UNKNOWN in 312/384 cases, including 120 non-builtin/never-executed walrus controls, so it is sounder on this subset but less precise. Independent subprocess replay matched 384/384 functional observations and 384/384 source hashes. No model-generated code was run on the host.

## Prospective freeze

- Protocol committed before oracle execution: `b65c2327803997d629137546dd974010b3897119`.
- Exact source manifest SHA-256 committed before execution: `852a16cafc24ddfece473bae2b3f1bc02144c7d5`.
- Manifest SHA-256 `7e95a86e81fa6039fc116447432eca6575e877fa0ebb7a2bc7237d691518f35b`, 384 cases, 16 correlated templates x24 variants.
- Frozen expected outcome: eight builtin-restoration classes (192 cases), eight negative/control classes (192 cases). All expectations matched observed CPython outcomes.
- This is a committed SHA freeze, **not** a pre-execution GitHub mirror of the full 160 KB manifest; the exact manifest is preserved in the local reproducibility archive.

## Counterexample

```python
from builtins import len as saved_len
len = lambda xs: -777
marker = [len := saved_len]
observed = len([1, 2, 3])  # CPython: 3, genuine builtins.len
```

Run308's `Assign` transfer handled only direct `ast.Call` effects and treated an enclosing list expression as an unknown *value*, without invalidating `len` as a module binding. It therefore returned `NOT_KNOWN_TARGET`, a false negative. Similar failures occur in tuples, dictionaries, f-strings, comprehensions, Boolean expressions and conditional expressions.

The correction walks the RHS for `ast.NamedExpr` targets and conservatively invalidates their bindings. This covers unexecuted branches but sacrifices precision; it is not a full abstract interpretation of Python expression evaluation or closure/comprehension scope.

## Frozen result

| Metric | Run308 original | Run309 corrected |
|---|---:|---:|
| Definite-negative false exclusions of genuine builtin | 192/384 | 0/384 |
| UNKNOWN classifications | 0/384 | 312/384 |
| Non-walrus negative controls retained as definite negative | 72/72 | 72/72 |
| Trusted CPython runtime errors | 0 | 0 |
| Independent replay mismatches | — | 0/384 |

The 384 cases are correlated variants, not 384 independent production repairs. No significance or representation-superiority claim follows.

## Independently recovered ORIGINAL cloud experiments

The two originally queued Run307 Python 3.14 GitHub Actions experiments **completed successfully** and their original ZIPs were downloaded and independently checked:

- Run `40634632773`, CPython 3.14.8, original ZIP SHA-256 `2ef8c68b3309038e4102281bf507ae5c1c12f67ebd6ba10f8e6f0b1227e2c809`.
- Run `40634738705`, CPython 3.14.9, original ZIP SHA-256 `2096d6433a0431e62eefe54aa53fcfde8ee801a0311dcbf9bfdfe4a4293c0c89`.
- Both matched all **256/256** frozen source hashes and original Run307 Python 3.14 predictions, with zero prediction or frozen-expectation mismatches; they agreed with each other on **256/256** observations.
- The original CPython 3.13.5 and 3.14.8 executions differed on **32/256** frozen observations; builtin restoration occurred in 64 vs 48 cases, respectively. This is an empirically verified version-specific effect, not merely symbolic prediction.

The original Run308 cloud reproduction `40636727102` also completed successfully. Its CPython 3.13.16 original artifact ZIP SHA-256 `dbec90aeb1f396d0870dd2ab2da800a92fc68c0786820ff7fa485736e7262083` matched all **384/384** local CPython 3.13.5 functional observations, source hashes, and classifier outcomes. The cloud replicated 128 old false negatives and zero corrected false negatives on the *Run308* fixture set. It is separate from the new Run309 192-failure experiment.

## Limits and research state

The analyzer remains bounded and not Python-wide sound. Comprehension scopes, dynamic descriptors, custom builtins, import hooks, reflection, asynchronous effects and arbitrary third-party code remain unresolved. Run309's repair does not demonstrate that semantic IR helps an LLM repair software. No sixth independently qualified production-repository repair was established, and wsproto PR #6 remains only screened. The prior five-qualified count is retained from the Run308 handoff, not re-audited here. All 89 reserved boundary issues remain sealed. One K-SYNTH-1 kernel, canonical branch `research/exp003-context-order`, one open/draft/unmerged PR #9. Historical GitHub artifact mirroring remains incomplete.

**Next:** Commit a genuinely frozen multi-production-file qualification protocol for a new public repair, run the independent isolated oracle, then conduct capable-model paired inference with exact shared edit authority and compiler preflight. Do not claim superiority without powered, clustered evidence.
