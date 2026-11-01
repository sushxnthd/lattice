# Reproduce K-SYNTH-1 Run416 (Python 3.11+)

From the clean extracted directory, without network access:

```
python -m unittest -v test_run416 test_run416_httpx_oracle
python run416_experiment.py
python run416_independent_audit.py
```

These commands use only trusted, deterministic, locally constructed Python fixtures; model-generated code is never executed. Run416's frozen HTTPX issue oracle is **not** run here: it requires an isolated historical Python 3.9/httpx 0.16.1 source environment and remains unqualified. Do not substitute installed modern HTTPX for historical source attestation.

The SHA-256 manifest verifies all archived payload bytes. `run416_lossless_compiler.py` uses the exact included `run402_dual_edit.py` dependency. All 89 reserved boundary issues are sealed.
