# Run 30 — prospective factorial-integrity gate

The existing Run 29 independent checker required complete A/B/C/D outcomes for each observed task/model/seed combination. That alone does **not** guarantee that every task was evaluated with every model and seed. Selectively omitting a difficult task/model combination can bias the aggregate C-minus-B estimate even though each retained four-arm group is complete.

**Required Run 30 change:** reject evidence unless all tasks share the identical set of `(model_id, model_revision, seed)` combinations; also reject more than one revision under the same model identifier. This is a research-design integrity check, not a Lattice representation advantage. In local synthetic tests, balanced multiple-model/seed designs passed, while selective task/model omissions, selective task/seed omissions, and mixed revisions were rejected. No coding-model inference occurred.

The full Run 30 implementation additionally includes raw-transcript attestation and deterministic static dependency-path diagnostics. Those implementations are locally validated but **not committed to this branch**. Prior negative Qwen comparisons and all frozen evidence remain unchanged.
