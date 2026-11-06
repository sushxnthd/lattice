# K-SYNTH-1 Run539: transitive Python import provenance

Six deterministic local subprocess executions; 3/3 assertions passed. Identical entrypoint SHA-256 with helper module A versus B yielded outputs A versus B. Removing helper caused import failure; snapshotting entrypoint alone also failed; snapshotting entrypoint plus helper restored output A. Thus entrypoint-only immutable snapshots do not suffice for deterministic Python oracle replay.

Initial execution using Python -I failed because isolated mode excludes the script directory from module lookup. Reproducible experiment corrected to -B. This was an experimental harness issue, not model failure.

Limitations: synthetic fixtures, no OS-level isolation, no independent oracle, no new qualified real production repair, no coding-model inference, no IR superiority. Full transitive dependency closure, native imports, import hooks and environment remain unverified. Raw code/results and SHA-verified local ZIP remain to be mirrored. Local archive SHA256 52382eaf7b704857d1fe3e66c2d23899f5daa80a3f155b4baac1fa2c2fbae97f. Two real qualified tasks, all 89 sealed.
