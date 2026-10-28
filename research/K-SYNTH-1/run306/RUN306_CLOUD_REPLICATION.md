# Run306 cloud reproduction and original failure preservation

**First workflow:** [40625128718](https://github.com/sushxnthd/lattice/actions/runs/40625128718), FAILED only at strict SHA comparison because unpinned `python-version: 3.13` selected CPython 3.13.17 rather than local 3.13.5. Its 384 trusted functional outcomes and independent replays nevertheless passed with the same 160 old / 0 corrected false negatives. Original failed artifact 12789525265 was recovered and SHA-verified, ZIP SHA256 `49155e3d39d8fc0dd83d45bb60b1963f953f721949ac6dfa3284ea0352bd14d0`. Do not relabel the original attempt as successful.

**Corrected workflow:** [40625163436](https://github.com/sushxnthd/lattice/actions/runs/40625163436), COMPLETED SUCCESS on exact CPython 3.13.5. Artifact 12788199697 downloaded and independently SHA-verified. ZIP SHA256 `42f048ae7e4c9b22685db1e7990da3e39866a07fbaf821fd6fe8ce0324067a65`, matching GitHub's artifact digest.

All three corrected cloud payloads match original local evidence byte-for-byte:
- Frozen sources SHA256 `1ce234ff74f60224173b6b6d950f62c791b06f0d338d65ca61238525931dfd79`
- Raw functional SHA256 `56d43399ac90e8687427fb30a898d87839c8f8f4408ffb0a9921bc3957ec0496`
- Independent audit SHA256 `c159ab17eb74a6310bf8347aa90b6f0507a9fbf9d23fb192a1b00299a1f4ba82`

Cloud and local results: 384/384 trusted outcomes, 384/384 independent subprocess replays, 160 original false negatives, zero corrected false negatives. Twelve correlated template families, not independent real-repository repairs. No model inference or IR superiority claim. Complete 17-entry local consolidated archive SHA256 `03abc7ef3289af137e43e026b2907af4f314ea5cefe70d3e923fa9fd08919f7c`.
