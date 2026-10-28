# Reproduce Run305 on CPython 3.13.5

Use the Run305 source files in this folder and these pinned predecessor files on the same branch:

- `../run293/run293_conservative_transfer.py`
- `../run301/run301_decorator_transfer.py`
- `../run304/run304_shadowing_transfer.py`

Copy those three files beside the Run305 scripts, then run:

```sh
python run305_experiment.py freeze
sha256sum RUN305_FROZEN_SOURCES.json
# expected: 84b15919cf471ad4feda642d535718644f9ba37816fd1e3cd71585a9ffa65933
python run305_experiment.py execute
sha256sum RUN305_RAW_FUNCTIONAL.json
# expected: 7dae49e0ca7d354ecbe60b73d972452070277500eeaa702f0ca22adcd0096e25
python run305_independent_audit.py
```

The complete local evidence archive additionally preserves the exact original
predecessor snapshots, original runner, frozen sources, raw 1,024 functional
records, independent audit and SHA-256 manifest. A GitHub-side reproduction
has not yet been independently verified. No real-repository model success
or general Python soundness is claimed.
