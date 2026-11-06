# K-SYNTH-1 Run532 — runtime binding stability counterexample

2026-11-06 UTC. This is a bounded compiler-precondition falsification, not a production repair qualification.

Executed local Python experiment on 16 adversarial source programs; 8 directed assertions passed. Five programs satisfied the narrow unique-direct-top-level-assignment syntactic candidate predicate. The counterexample `x = 1; def f(): global x; x = 2` has one direct module assignment, but invoking `f` can rebind module `x`. Conversely `x = 1; def f(): x = 2` does not itself add another module binding. This disproves runtime uniqueness from direct top-level syntactic uniqueness. No untrusted source executed.

Scanner labels hazards for global declarations, conditional/loop/try structures, dynamic `exec`, `globals`, `setattr`, star imports, augmented assignments, deletion and assignment expressions. It is NOT a soundness certificate: alias mutation, import hooks, external calls and metaclass effects remain outside the modeled scope. Lexical `symtable` facts do not establish runtime stability. The shared IR/Python compiler contract must distinguish unique direct syntactic assignment from runtime UNKNOWN.

Local SHA-verified archive: run532.zip SHA256 a4a2e4151208c23d0bbf6051227b5751c692dcb9120e90f754f7349767452cee. Local files experiment.py SHA256 2e12e7bd9a79b71cf506be7eb15c6e26a62c5cd62517ab1a0ca46df90331f7ed; raw.json SHA256 cb3f4097ebf012cc8180a2fa4459372840a760f368ac2aac755661a11f5df2c9; REPORT.md SHA256 a3862eb4607d2f38ebfdc675ea45f6944b7f6683ed163694d2d5cdfa873a4d97. Direct Git transport DNS failed; executable and raw JSON GitHub mirroring pending.

No newly qualified real multi-source repair, no coding-model inference, no superiority claim. Exactly two independent qualified repairs remain (Flask PR6096 and urllib3 PR5071); all 89 reserved issues remain SEALED. Next priority: prospective independent real repair qualification and blinded paired coding-model pilot.
