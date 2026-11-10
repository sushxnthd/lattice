# Run638 — Four-arm descriptor oracle sensitivity

Executed deterministic standard-library 2x2 descriptor-relocation analogue for Werkzeug PR3341. Parent and subclass descriptors toggled independently. Ordinary and subclass/client responses probed before/after backing-data mutation.

Baseline and parent-only subclass responses retain stale `alpha`; full combined variant returns `beta`. Subclass-only yields fresh subclass text but ordinary `Response.text` is absent. Joint ordinary+client API coverage detects the missing parent property; a single-read oracle misses cache staleness. Full raw JSON and SHA-verified local reproducibility ZIP retained. **Not upstream execution, not a qualified repair, not model evidence.** All 89 reserved issues untouched.