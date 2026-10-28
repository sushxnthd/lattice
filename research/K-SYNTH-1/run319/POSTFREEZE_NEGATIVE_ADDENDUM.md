# Run319 postfreeze negative-control correction (not a primary protocol change)

The first negative-control execution stopped on the predeclared 'trailing statement on same line' case, constructed as `@marker\ndef disposable(): return 1; x=2`. CPython parses `x=2` **inside the disposable function suite**, so deleting the whole decorated function is semantically valid and is not a trailing sibling statement. The compiler's acceptance is therefore not a security failure. Original failure is preserved in the local log.

The frozen 256-case primary matrix and 128 plain controls were already completed and are unchanged. The independent auditor passed 256 byte reconstructions and 768 trusted subprocess evaluations. For the separately labelled postfreeze negative-control rerun, replace only this malformed negative fixture with `@marker\ndef disposable(): return 1 # trailing comment`, which must be conservatively rejected because the original node span ends before the trailing comment. Do not count the original malformed negative fixture as a passed test or silently modify the frozen protocol.

This is a test-design correction, not new model evidence or a seventh repair.
