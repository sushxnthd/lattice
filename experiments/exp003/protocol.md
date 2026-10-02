# Experiment 003: diagnose the 0.5B floor

Experiment 002 Qwen2.5-Coder 0.5B completed zero checkpoints in all arms. Full
Python frequently echoed the old policy; patch formats frequently copied `auth`
and `blocked` from the generic example into tasks with different input names.

Do not silently replace that negative result. Register a separate 2x2 diagnostic:
request before vs after current source, and generic vs task-named format example.
Test all three representations on the first request from Release, Ticket and Model
(one task per semantic family), one call each, all 64 Boolean inputs checked.
Same 0.5B model, greedy decoding, 220 generated-token budget. No repair or selection.

These tasks were already evaluated. This is mechanism diagnosis, not a fresh
hold-out confirmation. Even if prompt order raises accuracy, that is evidence about
prompt placement and must not be credited to new-language semantics. Freeze code
and protocol before examining these results. Preserve all prompts and outputs.
