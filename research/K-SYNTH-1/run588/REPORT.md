# Run588: isolated Python execution-phase traces

Twelve deterministic self-authored Python fixtures were executed in separate `python -I -c` processes on Python 3.13.5. All 12 expected traces matched. Definition-time defaults, decorators, class bodies and eager annotations executed during definition; lambda/function bodies and generator elements were deferred; list comprehensions executed eagerly; short-circuit expressions suppressed right operands; postponed annotations did not evaluate annotation calls.

This is bounded functional trace evidence, not a sound general Python call graph, real repair qualification or model comparison. No reserved issues were touched. Qualified real repairs remain two. Full executable, raw per-fixture traces and SHA manifest are in the local Run588 reproducibility archive (ZIP SHA256 f5e0ac9dd364cb6bbb88de263f5d959f802de84c739e175340c61bb4bbb4b028). GitHub executable/raw mirroring remains outstanding.
