# K-SYNTH-1 Run308: imported builtin identity and deletion counterexample

**Result:** Original Run307 source-only analyzer produced **128/384 definite-negative false negatives** on prospectively frozen trusted CPython 3.13.5 fixtures. A bounded module-binding provenance correction produced **0/384 definite-negative false negatives**. Independent read-only subprocess replay matched all **384/384** original observations, with **0 discrepancies**. This is a semantic-analysis correction, not a real-repository repair or representation advantage.

## Freeze and provenance
- Protocol `PROTOCOL_RUN308.md` committed before functional execution at `7f467c0620be2fa2511b7162b0fed798e7cb0a8e`.
- 384-source manifest SHA-256 `d0f9a6e07cdcb09b7a1e1db7ce2e71e06cf4de6a53d1259110afcf4672d0f4f8`, frozen on GitHub at `d9db7f5d5094810778bf6d82e450a17c883e1009` before execution.
- Original functional results SHA-256 `f6ddea2d9953f62a7a66d621aae20681c09cdd962a12638df9ebaa82a3850649`.
- Independent replay SHA-256 `f5f13f374d01e6f468e024f26b012d0c69cc45926592ab21042d904539d649c1`.
- Runtime: CPython 3.13.5; 12 prespecified scenarios x 32 correlated syntactic variants; no model-generated code executed.

## Mechanism

```python
len = lambda xs: 2
from builtins import len
observed = len([1, 2, 3])  # genuine builtin returns 3
```

The original analyzer ignored import binding effects. It retained the earlier local lambda identity and classified the final call as `NOT_KNOWN_TARGET`, even though CPython called `builtins.len`. The same failure occurred for `from builtins import len as len`, import-through-alias rebinding, and wildcard import. Deleting the local shadow also exposes the builtin, but the old analyzer already returned UNKNOWN for that case.

## Frozen results

| Scenario class | Cases | Builtin actually called | Old definite-negative false negatives | Corrected definite-negative false negatives | Corrected UNKNOWN |
|---|---:|---:|---:|---:|---:|
| Direct/aliased builtin import, intermediary alias | 96 | 96 | 96 | 0 | 0 |
| Delete local shadow | 32 | 32 | 0 | 0 | 0 |
| Wildcard import | 32 | 32 | 32 | 0 | 32 |
| Seven negative/control classes | 224 | 0 | 0 | 0 | 0 |
| **Total** | **384** | **160** | **128** | **0** | **32** |

The corrected transfer tracks trusted import aliases and assignment identities, handles deletion fallback, and explicitly marks wildcard import UNKNOWN. It preserved all 224 negative controls. No original CPython execution failed. The independent auditor verified all source hashes and reproduced all original stdout/stderr/return codes byte-for-byte.

## Limits

This is a **bounded trusted subset**, not proof of soundness for Python as a whole. The experiments assume genuine unmodified builtins, standard import hooks, no reflection or concurrent mutation, and no side-effecting decorators/defaults. Imported modules and runtime effects outside the subset must invalidate knowledge to UNKNOWN. The 384 variants are correlated, not independent repair tasks, and do not support McNemar superiority claims.

The original Run307 Python 3.14 cloud workflows `40634632773` and `40634738705` were still **queued** at this check; no Python 3.14 outcome was inferred. GitHub queue delays were not treated as model or scientific failures. No sixth independent production-repository repair was qualified; wsproto PR #6 remains a screened candidate only.

**Research state:** Five independently qualified real repairs per Run307 handoff; no powered IR-versus-Python benefit, no breakthrough. Canonical branch `research/exp003-context-order`, one open/draft/unmerged PR #9, all 89 reserved boundary issues SEALED.
