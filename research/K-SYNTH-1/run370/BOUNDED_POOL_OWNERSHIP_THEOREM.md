# Run370 bounded ownership counterexamples

**Scope:** finite two-request, one-connection transition system, not full Python or historical HTTPcore. No spontaneous external network transition; `connecting` is unavailable, not idle and not closed. Transitions are defined in [the executable model](run370_minimal_bounded_witness.py).

**Proposition 1 (orphan capacity).** If a request owns the sole connecting pool entry and times out, dequeue-only cleanup can remove the sole owner while leaving the connection. A subsequent queued request cannot reuse (not available), evict (not idle) or create (pool at capacity). Without an external state transition, progress is blocked. Shortest witness: enqueue 0, assign new 0, timeout/dequeue 0, enqueue 1.

**Proposition 2 (unsafe naive close).** If request 0 is active on a multiplexed connection and request 1 is assigned that same connection, unconditional close on request 1's timeout closes a transport still owned by request 0. Shortest witness: enqueue 0, assign new 0, start 0, enqueue 1, assign shared 1, timeout/close 1.

**Exhaustive model results:** dequeue-only 42 states/70 edges/orphan witness; unconditional-close 46 states/74 edges/shared-close witness; close-if-unowned 42 states/72 edges/neither witness. Independent interpreter reproduces all counts and validates witnesses. Absence of a witness is only bounded-model evidence, **not** production soundness.

**Proposition 3 (pre-wait guard insufficiency).** A guard `if status.connection is None: wait(...)` can be evaluated before the wait times out. Another actor can assign a connection after timeout is decided but before the exception handler acquires the pool lock and dequeues. The guard has already been passed. A controlled CPython source-excerpt interleaving reproduces the orphan. This does not prove the full merged upstream PR fails on a historical workload.

**Key timing distinction:** sync `threading.Event` already set before `wait(0)` succeeds in 1,024/1,024 tests. In modern installed AnyIO, an already-set event under `fail_after(0)` can still time out (128/128), and the post-reference guard avoids that specific outcome (128/128). Neither observation is a historical full-tree qualification.

**Implication:** aggregate two-file necessity, timeout guards and AST-level MAY edges do not establish unique semantic mechanisms. A soundness-scoped semantic IR must explicitly represent unknown cancellation timing and shared ownership rather than claiming general noninterference.
