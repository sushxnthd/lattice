# Run320 postfreeze harness correction (registered before rerun)

The original frozen run320_experiment.py failed before the first scientific case completed. This was a test-harness type-identity error, not a model or compiler outcome: the old and hardened compiler modules define distinct Action dataclasses, and the harness passed the old Action to the hardened compiler, triggering PatchRejected("unauthorized action"). The exact traceback is preserved in the local archive.

The separately labelled corrected harness run320_experiment_corrected.py converts action fields into the hardened module's Action class before each hardened call. No changes to fixture families, 32 variants, operation payloads, test success criteria or compiler implementation.

Original frozen experiment SHA256: e065179a87ee9f93e1a137f43724764bb7b9574128ea849659ad251f708ffb4f
Corrected harness SHA256: 8cca424f3f3208f801570228ecf4b05a4d17c5974ea7c40078619fa993d72739

The original attempt remains a failed precompletion harness attempt; all subsequent outcomes are POSTFREEZE CORRECTED, never retroactively original-prospective outcomes.
