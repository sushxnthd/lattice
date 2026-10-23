# K-SYNTH-1 Run198 — persistent epoch-addressed semantic editing

Date: 2026-10-23. **Compiler correctness evidence, not a capable-model or representation-superiority experiment.**

## Implemented

`src/lattice/epoch_editor.py` adds an append-only `EpochEditor` with immutable `h<epoch>_<root>` references, optimistic compare-and-swap transaction tips, trusted caller-supplied edit scope, protected-root identity preservation, content-addressed transitive node identities, and epoch-linked state/authority commitments. Historical references bind to a committed node ID even when an authorized descendant is recompiled in later transactions. The prior one-transaction snapshot adapter did not support this case.

`tests/test_epoch_editor.py` covers historical references across three edits, stale fork rejection, atomic rejection of invalid edits, divergent fork commitments, authority forgery under self-consistent hash chains, and a 258-case exhaustive stress test. A separate independent evaluator replayed all **258 unchanged Run186 frozen public tasks** across **four epochs** and **64 Boolean assignments** per epoch, producing **66,048 epoch/input traces** and **462,336 root-output comparisons** with **zero observed oracle disagreements**. It independently evaluated expressions using an AST interpreter; production-framed evaluation was cross-checked on 16 input assignments per epoch (16,512 framed-versus-oracle output dictionaries). This remains a four-family synthetic benchmark, not 258 independent issue samples.

Frozen public-task SHA-256: `75a29941a8802ab6b1c8a55e501d25e2273267839eb965fe303698d164c0cc94`. Raw trace SHA-256: `072f7019c08aa5d50ed6fc2cb511a604c392917130ac65e0bfdf193ab8c7e0ad`. The raw 17 MB JSONL and standalone replay script are retained in the local reproducibility archive.

## Security boundary and falsification

**A hash-chain authority commitment is not authentication.** An attacker can create a different self-consistent ledger and claim an unauthorized edit. The `verify()` routine detects this substitution only when compared with an independently trusted tip or an authenticated external checkpoint. It does not provide signatures, durable storage, distributed concurrency, or a multi-user trust model. Treat it as a prototype.

## Research status

No new capable-model inference occurred in Run198. The Run197 negative/ambiguous IR-versus-Python results remain unchanged. The decisive next experiment is an independently sampled, prospectively frozen real multi-file issue benchmark with identical compiler/verifier/edit authority for semantic IR, ordinary Python, and AST-action baselines. The Run197 power sensitivity suggests 480 paired issues across 120 repositories for a relatively large effect under some heterogeneity assumptions; 258 synthetic seeds are not adequately powered for that claim. Do not claim world-class completion or representation superiority from this run.
