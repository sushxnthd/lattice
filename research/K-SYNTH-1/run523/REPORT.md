# Run523 — descriptor-relative reads do not guarantee a coherent file snapshot

A deterministic local experiment opened one regular file by descriptor, read its first 4096-byte block, overwrote both blocks in place, restored atime/mtime, then read its second block through the original descriptor. Six directed assertions passed. The reader returned A×4096 || B×4096, which equals neither the original A×8192 nor the final B×8192. File size, inode, and mtime remained equal; ctime changed on the tested filesystem.

SHA256 initial: `f8ca02c69621dd84cd1212ebfd7d6cdc9ba6ad658854f29567723531912d1a35`.
SHA256 final: `766c00ba277e84ef9550596c7eda86bad4d66a3fee2255924e6388ee9c272792`.
SHA256 torn read: `54f624253436dcd5fe656688f7ddb3a314b4524453ce553a5b39a62ce0de4ee5`.

This is a controlled filesystem counterexample, not a production benchmark result. It shows that descriptor-relative no-symlink traversal (Run522) addresses pathname substitution but not concurrent in-place mutation. A freeze verifier must operate on immutable content-addressed snapshots or otherwise establish exclusive mutation-free access. Metadata checks alone are not a proof of immutability. Local runnable source and raw JSON were produced; GitHub source/raw mirroring remains pending. No new qualified repair, model inference, or IR superiority claim. All 89 reserved issues remain sealed.