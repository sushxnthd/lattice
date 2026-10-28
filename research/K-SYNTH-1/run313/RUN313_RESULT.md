# K-SYNTH-1 Run313: independently verified historical h11 adversarial fragmentation challenge

**2026-10-28 UTC.** Canonical `sushxnthd/lattice`; branch `research/exp003-context-order`; PR #9 open/draft/unmerged; all 89 reserved issues sealed.

## Prospective evidence

Protocol commit `faab907992cca9f1884091aaeb406e09ea72c4c0` and frozen runner commit `74995a9a45cad684302ef21b8d02506540151b13` preceded original historical execution. Runner SHA256 `6b4cbe81082089104fc75f9005aa4789c15ed912b999b317d2f2902b9a1fc58e`; frozen case-manifest SHA256 `c2fffe45a129ce135f8a703f3922f720cb523d633afdae5ac461f44f24cea045`. Isolated workflow commit `3bc60ea841c6c5367df6530049a67cf89a32126f` triggered [Actions run 40673866449](https://github.com/sushxnthd/lattice/actions/runs/40673866449), completed SUCCESS.

Original artifact `12809323142`, ZIP SHA256 `f6c78c0f9302d944684c536483e41162e3a2f42f951e78a34d58c8eb89afcd83`. Independent audit checked 9/9 original manifest payloads, all 4,764 functional JSONL traces, original runner and case SHA, source-arm hash relationships and the BASE-to-FULL differential. Zero SHA or outcome discrepancies. Historical h11 base `522b00470b5776dda2dc7e98ff778eb1e418e6ad`, reference `a1197d68630bc37a941b516c7cc74833460fc97c`.

## Original four-arm results

22 predeclared response streams (3 CRLF valid controls, 4 LF/mixed targets, 15 adversarial probes), fragmented as whole, at every one-boundary split, deterministic two-boundary splits and bytewise: **1,191 correlated variants per arm, 4,764 traces total**.

| Arm | CRLF controls | LF/mixed targets | Adversarial complete parses |
|---|---:|---:|---:|
| BASE | 163/163 | 0/171 | 214/857 |
| BUFFER+CONNECTION | 93/163 | 171/171 | 132/857 |
| READERS_ONLY | 93/163 | 0/171 | 132/857 |
| FULL | 163/163 | 171/171 | 214/857 |

**Fragmentation invariance: 22/22 streams in all four arms.** BASE versus FULL differed on exactly 171/1,191 normalized outcomes, all intended LF/mixed targets. No BASE-to-FULL change in the adversarial or CRLF control streams. Partial arms lose 70 valid-control variants; full integration restores them. This is a new bounded adversarial validation of the previously qualified historical repair, **not a new independent repair**.

FULL accepted 214/857 adversarial variants, specifically folded headers (62), equal duplicate Content-Length (70), and Transfer-Encoding plus Content-Length (82). BASE accepted exactly those same 214. These are parser-tolerance observations, **not a demonstrated regression or security exploit**. End-to-end smuggling would require a second parser and a concrete disagreement witness.

An exploratory local CPython 3.13.5 comparison against modern `h11==0.16.0` produced **0/1,191** normalized differences versus the historical FULL arm on CPython 3.9. The modern comparison was performed before the historical Run313 replay and is not unseen confirmatory evidence.

## Decision

Original Run312 and Run312B frozen qualification criteria remain unchanged. Six historical real-repository repairs remain six; 1,191 fragmentation variants are not independent issues. No new coding-model inference, powered IR advantage or breakthrough. No untrusted model-generated code was executed on host.

Reproducibility: [original workflow](https://github.com/sushxnthd/lattice/actions/runs/40673866449), [independent read-only auditor](run313_independent_audit.py), [frozen protocol](PROTOCOL_RUN313_ADVERSARIAL.md), and the local complete SHA-verified archive. Full historical GitHub artifact mirroring remains incomplete.

Next priority: genuine paired capable-model IR versus information-equivalent ordinary Python/AST repair inference with model SHA, exact prompts, seeds, token budgets, raw completions, shared compiler and isolated oracle, followed by recruitment across many independent repositories.
