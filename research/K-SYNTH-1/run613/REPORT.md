# Run613 — finite dispatch counterexample
Eight exhaustive Boolean configurations of import execution, rebinding and invocation were evaluated with a deterministic Python reproducer. All eight configurations contain a syntactic import edge, but only one dispatches to the original function. Among the four cases where import executes, three do not invoke the original target. This is a finite semantic model, **not eight independently executed real Python modules**. The model is intentionally restricted to three Boolean factors and does not establish a whole-program analyzer result.

Local original executable SHA256: 82e35359ce4395382387de754ded0c12fa2154f3de09ff1c5d5d77f010b94b32
Local raw JSON SHA256: 5c8f18b3eeb67513a1f4275cc2f64e729dac6971c6204d345583badd42014720
Local ZIP SHA256: b88bd914c5b6484cfeb3090ed073f84f65d0f4f806bcdf71e89ea1d8b3fb98cb

The GitHub reproducer is a logically equivalent shorter implementation; hashes above refer to original local artifacts. No production repair or coding-model inference occurred. Qualified real tasks remain two. All 89 reserved issues sealed.