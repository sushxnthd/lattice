# Run611: import binding is not execution identity

Executed 8 isolated Python `-I` subprocess cases using synthetic in-memory modules; all returned code 0 and matched prospectively coded expected stdout.

| Case | Direct ImportFrom syntax | Actual stdout |
|---|---|---|
| plain | yes | ORIGINAL |
| rebound | yes | REBOUND |
| conditional_false | yes | NAME_ERROR |
| star_import | yes | ORIGINAL |
| module_getattr | yes | DYNAMIC |
| dynamic_exec | no | ORIGINAL |
| globals_mutation | yes | REBOUND |
| module_replacement | yes | REPLACED |

Seven cases have syntactic `ImportFrom(provider)`; only two of those execute the original `target` function. The eighth case dynamically imports through `exec` and executes the original target without direct import syntax. This is a bounded counterexample to treating syntactic imports as a sound binding/execution identity; not a statistical sample or model repair result. AST analysis must preserve explicit UNKNOWN for rebinding, dynamic module attributes, globals mutation, import cache substitution and dynamic code. The exact executable is `reproduce.py`, with expected outputs asserted; execute with `python reproduce.py`. Each source string's SHA256 is emitted in JSON.

Local original executable SHA256 f4cd3f5031451e48552fc536e30a974e604ca01e7a560900b0f9c950916d8f60; local raw JSON SHA256 f654d4791416f23b06a24a7501f6b3b50cf08040d33b328cae462b343a1ed1e1. The GitHub executable is equivalent but its bytes may differ; do not conflate hashes.

No real repair qualification, model inference, or IR superiority. Only two qualified production tasks remain; 89 sealed boundary issues untouched.