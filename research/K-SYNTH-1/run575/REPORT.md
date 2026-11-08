# Run575: multi-file atomicity counterexample

Executed four deterministic injected-failure phases for a two-file Python edit using staged files and `os.replace`. The failure immediately after replacing the first file leaves a partially committed transaction (one file new, one old). Exactly one of four phases exhibited this state. Thus atomic per-file rename does not establish atomic multi-file edit transactions. This does not test power loss, concurrent mutation, durable fsync ordering, or recovery journal correctness. A production editor must either specify weaker per-file semantics, or implement and verify a transaction/recovery protocol. No model inference, qualified repair, or IR advantage is claimed. All reserved issues remain sealed.

Local ZIP SHA256 `21327aa291057aea1014517aaade4271adf6ea5d6b5decb4c6bc4eff57df0ea8`.
