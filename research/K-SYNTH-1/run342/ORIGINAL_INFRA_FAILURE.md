# Run342 original cloud transport/provenance failure (preserved)

Original workflow [40884219720](https://github.com/sushxnthd/lattice/actions/runs/40884219720), created 2026-10-29 13:41:15 UTC, completed FAILURE. Original artifact ID `12901352294`, ZIP SHA-256 `30a628c2e353967af5ed486688bdbafd5c54bb13d39b04ca0c8f5c8006236c6e`, 698 bytes. The exact frozen oracle and compressed runner were SHA-verified. Historical checkout and reference commit fetch succeeded.

Execution aborted **before any of the five functional arms ran** due to a 39-character typo in the runner's expected ref blob SHA for `h11/_receivebuffer.py`: expected `b32f20ea38136e47f834caf39fe5464f7b804d2` vs actual 40-character `b32f20ea38136e47f834caf39fe5464f7b804d2e`. The actual hash matches the pre-existing independently frozen Run297 source manifest. This is an infrastructure/source-hash transcription error, NOT a model or scientific qualification failure. Do not change the frozen Run342 oracle, target/control cases, base/ref commits, source-group assignment, or criterion. Correct runner SHA-256 after deterministic one-character fix: `438f559a59529210a682ae273457e04b1b0b7bb9bb7dec999a08652ed60cc85a`.

The original failed artifact and GitHub logs must remain available. A corrected cloud run is required before any outcome claim.
