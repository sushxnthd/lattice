# K-SYNTH-1 Run571 — atomic compiler adversarial contract

Synthetic deterministic CPython byte compiler tests: 6,000 assertions passed, including 400 valid transactions and 5,600 adversarial rejections. Rejections: 3,200 unsafe paths; 400 each stale source hash, Boolean offset, UTF-8 split, invalid syntax, overlapping edits, and invalid second-file transaction. Atomic output is returned only after validation. No filesystem access or untrusted model-code execution.

Run570's pure dictionary-key path handling did not establish a filesystem-safe path contract. This prototype rejects traversal, absolute and drive paths, backslashes, empty/dot components and NUL. Not a general filesystem safety proof: symlinks, case-folding, normalization, TOCTOU and platform differences are out of scope.

Locally executed code and complete 6,000-case JSON preserved in SHA-verified archive; GitHub raw-source/result mirroring is outstanding. No production repair qualification, no model inference, no semantic-IR superiority. Only two historically qualified real repairs; 89 reserved issues sealed.