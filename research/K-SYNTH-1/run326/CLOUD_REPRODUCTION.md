# Run326 original cloud counterexample reproduction

Original [GitHub Actions run 40778830419](https://github.com/sushxnthd/lattice/actions/runs/40778830419): **completed SUCCESS**. The `counterexample` job passed and uploaded original artifact ID `12855174121` (`lattice-run326-semantic-counterexamples`).

The independently downloaded original ZIP had SHA-256 `89ef603b0cc471bc92e3910cc029857c1485396633e7b334250b40383a14a0c9`, passed ZIP CRC, and contained three entries. The original `commit.txt` pinned `479555dce75666fb2b1579cdc2fb54c65ba199f2`. Original `SHA256SUMS.txt` matched both source script SHA-256 `75cf87e3ab899c49d29615ebdf380ab5e30df6890aee34e405fb952b48c746da` and `witness.json` SHA-256 `081cac1b48a2788bd20dfdae6d491066ffb431810c084fc300efefd715119654`.

The cloud witness reproduced three bounded semantic counterexamples: hidden `__bool__` side effect, short-circuit skipping a syntactic Name in 2/4 assignments, and `eval` reading a name absent from the lexical AST. This validates the **minimal counterexample reproduction only**, not the separate 16,384-evaluation local audit, model inference, or real repository repair. The full local archive retains both original failed audits and the postfreeze-corrected primary/independent results.
