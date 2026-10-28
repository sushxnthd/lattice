# Run315 postfreeze hardening and negative result

The frozen primary experiment remains unchanged. A separate exploratory adversarial test discovered a **pre-existing ancestor-symlink escape** in the original snapshot publisher. A bounded revised publisher now uses a private random staging directory, verified content-addressed snapshots, and one CURRENT pointer replacement.

Postfreeze trusted results: **256/256** ordinary publications, **256/256** prepublication failure injections preserving the previous pointer, and **2/2** pre-existing symlink attacks rejected without writing outside the store.

The first hardening attempt failed with an uncaught FileNotFoundError when an attacker-controlled snapshot directory lacked MANIFEST.json. That failure was preserved, and the implementation was corrected to return PatchRejected. The hardened source is committed and Git-blob-verified against the local evidence.

This does **not** establish safety against malicious concurrent writers, time-of-check/time-of-use races, hostile shared storage, crashes, power loss or network filesystems. A production security review and further adversarial tests are necessary.

Complete local postfreeze evidence ZIP SHA-256: `50bd6446ab850fff5e23a5f5b4dc2aac63119b05065aa84e954988e4dec7f64d`. GitHub ZIP mirroring remains incomplete.