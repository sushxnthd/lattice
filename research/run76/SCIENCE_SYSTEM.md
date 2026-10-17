# Run 76: paired repair development pilot

SCIENCE: No capable-model inference and no representation-specific result. Eight development-only task contracts and sixteen paired prompts prepared; unseen holdout untouched. Same-compiler evaluation script requires production compiler and independent Run62 oracle. A token-matching gate must run before model inference.

SYSTEM: Existing Run62 independent-oracle tests remain excluded from default CI discovery (`testpaths = ["tests"]`). Attempt to update pyproject.toml on this branch was blocked by connector safety checks. No production code changed.

Branch: build/run76-oracle-ci-repair-20261017. Blocker: GitHub update_file rejected by safety checks. Local files: prepare_pilot.py, paired_repair_eval.py, dev_pilot_manifest.json, prompts.json. Smallest supported claim: eight development contracts pass 128 exhaustive Boolean rows and the paired prompts share identical semantic-information context; no model gain measured.
