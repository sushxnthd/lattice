# K-SYNTH-1 Run313 prospective adversarial parser challenge

Frozen before any historical h11 PR #115 Run313 oracle execution. This is a NEW, non-qualification diagnostic. Original Run312 and Run312B gates and evidence remain immutable.

- Historical BASE: `522b00470b5776dda2dc7e98ff778eb1e418e6ad`; historical REF: `a1197d68630bc37a941b516c7cc74833460fc97c`.
- Four arms: BASE; BUFFER+CONNECTION; READERS_ONLY; FULL. Source files `_receivebuffer.py`, `_connection.py`, `_readers.py`. Execute only in isolated GitHub Actions.
- 22 predeclared HTTP response wire streams: 3 CRLF controls, 4 LF/mixed valid targets, 15 adversarial probes. For each: whole message, every single split boundary, deterministic two-split boundaries, and bytewise fragmentation.
- Deterministic case count: **1191**; four-arm trace count: **4764**. Case manifest SHA256 `c2fffe45a129ce135f8a703f3922f720cb523d633afdae5ac461f44f24cea045`.
- Runner source SHA256 `6b4cbe81082089104fc75f9005aa4789c15ed912b999b317d2f2902b9a1fc58e`. The runner's compressed transport is SHA-verified after decompression before use. Preserve original logs and manifest.
- Outcome = public h11 response status, concatenated body, EOM completion and error class. The independent audit will check fragmentation invariance per stream, cross-arm acceptance differences, and malformed-header acceptance without interpreting parser tolerance as an exploit.
- Modern installed h11 0.16.0 was separately explored BEFORE freezing historical outcomes. It produced 1191/1191 complete traces and 22/22 fragmentation-invariant normalized stream outcomes; 214/857 adversarial variants were accepted by that version, including obsolete folding and equal duplicate CL. Those variants are correlated, and accepted != exploitable.
- No capable-model inference or representation advantage is claimed. No reserved issues may be accessed. One kernel, canonical branch, one draft PR #9.

Any failures in cloud transport, runtime, or historical compatibility are preserved as failures; never alter frozen criteria or relabel them as model failures.
