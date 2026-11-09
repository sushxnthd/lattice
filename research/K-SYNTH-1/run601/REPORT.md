# Run601: bounded AST-versus-runtime call traces

Executed 2026-11-09 UTC. Eight hand-authored Python programs were parsed with Python ast and independently executed using isolated `python -I` subprocesses with `sys.setprofile` call-event capture.

Observed: **8/8 subprocesses succeeded**, **13 syntactic AST Call nodes**, **17 interpreter Python call events** (including module execution and nested functions). These are non-comparable counting units; neither quantity is a repair success metric. Cases: dynamic getattr, alias rebinding, exec injection, decorator replacement, short circuit, deferred generator, eager default, globals reflection.

The central soundness boundary is that AST presence does not imply execution, and call-target syntax alone does not uniquely determine the runtime target under reflection, rebinding, exec or decorators. A soundness-scoped representation must retain UNKNOWN and distinguish MAY from MUST. This is bounded illustration, **not** a sound whole-program analysis.

Local executable files `reproduce.py`, `functional.py`, `raw.json`, `functional.json` and stdout are preserved in the SHA-manifested Run601 archive. GitHub raw artifact mirroring is outstanding.

No new qualified production repair, no coding-model comparison, no evidence of semantic IR superiority. Exactly two independent real production tasks remain qualified. All 89 reserved issues sealed. Next highest-information experiment: prospectively frozen real multi-production-source repair qualification, not additional synthetic call-count demonstrations.
