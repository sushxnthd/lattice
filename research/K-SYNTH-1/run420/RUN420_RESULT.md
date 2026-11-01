# K-SYNTH-1 Run420: conditional SSA certificate and real-source coverage kill test

Date: 2026-11-01 UTC / 2026-11-02 IST. All 89 reserved issues remain sealed.

Implemented a conservative typed def-use certificate for pure, straight-line, single-assignment integer Python functions. It rejects dynamic dispatch, calls, attributes, imports, closures, branching, rebinding and other unknown effects. The positive result is **conditional** on `type(arg) is int` for every argument; annotations are not proof. The lemma concerns returned values under normal termination, not exception, trace or resource noninterference.

**Functional experiments:** 192 generated programs; 192 semantic/dataflow binding-action versus ordinary AST-index-action transactions lowered through the same Run419 atomic compiler with byte-identical outputs. 768 exact-int input pairs preserved return values (1,536 function evaluations). 192 stateful `int` subclass pairs changed the return value after a syntactically dead assignment edit (384 evaluations), falsifying any unconditional interpretation of the `int` annotation. Independent subprocess replay: 192 cases, 2,880 checks, zero disagreements; 24/24 adversarial tests pass.

**Production applicability kill test:** Read-only scan of installed urllib3 2.7.0, httpx 0.28.1, requests 2.32.5 and click 8.1.8: 1,700 Python functions. 1,698 UNKNOWN; two conditional certificates were context-manager `__enter__` methods in requests, neither with a dead assignment. **0/1,700 eligible certified dead-assignment edits.** Independent SHA audit: 84 function-bearing source files, 3,687 checks, zero disagreements. These are installed snapshots, not pinned historical PR bases, and do not support population-wide statistical inference.

**Decision:** Do not scale this narrow certificate as the production repair editor. Next use a conservative MAY graph with explicit UNKNOWN but full equal Python/AST edit authority, then exact pinned historical reference expressibility, new prospectively qualified real repairs, and matched capable open-model inference. The ordinary baseline must receive identical source and dataflow facts.

Still only two qualified historical real multi-source repairs (Flask PR6096, urllib3 PR5071); no new model inference, no representation-superiority claim, no breakthrough. Complete raw traces, code, independent audits, SHA manifest and reproducible ZIP retained locally in Run420; full GitHub ZIP mirroring remains incomplete.
