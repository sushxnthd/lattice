# Run629: repository clustering counterexample

Executed a deterministic exact-test counterexample: 30 paired synthetic tasks from six repositories, five IR-winning repositories and one Python-winning repository. Task-independent exact McNemar p = 0.00032491423189640045; exact repository sign-flip p = 0.21875. Tripling each repository's observations does not change the repository sign-flip p-value. This demonstrates that nominal task count alone cannot justify powered inference under repository dependence. The cluster test additionally requires independent, sign-symmetric repository effects under the null; it is not a universal replacement for a hierarchical design.

No new production repair or model inference. All 89 sealed issues untouched.

Reproducibility: local SHA-verified archive lattice_run629.zip, SHA-256 b1fea23ce5bbd3f9ca4e1b6a3101a2e8d94072f5e76ea662de998fe8c7c553ec. Includes reproduce.py, raw.json, REPORT.md, manifest.json. GitHub executable/raw mirroring pending.
