# Run449 import-provenance failure and recovery

First execution froze 924 cases with SHA256 `e66a1289fac5d69f8c04a19d9fa81b3309f8f2e943be63b8854f8cd651bc86e9` and staged all eight source variants, but the BASE worker failed before usable API traces: the interpreter had preloaded site-package `urllib3`, triggering the explicit local-import assertion. This was an infrastructure provenance failure, not a scientific negative result.

The worker was corrected to purge `urllib3` and `urllib3.*` from `sys.modules` before importing the SHA-pinned local staged source, while preserving the import-path assertion and network ban. The **same frozen cases and predictions** were then executed without changes, producing 7,392 raw API observations. Independent audit and 21 tests passed. The full corrected archive contains this failure log, source, raw traces and 383 SHA-verified payloads.
