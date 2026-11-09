# Run610 — bounded cross-file binding safety regressions

Ten deterministic AST fixtures executed, all passing. Cases: plain import (MAY), conditional false/true/unknown imports (UNKNOWN), overwrite (UNKNOWN), delete (UNKNOWN), globals mutation (UNKNOWN), exec mutation (UNKNOWN), after-call rebinding (MAY), and function-local shadow (UNKNOWN).

This is a syntactic MAY-versus-UNKNOWN regression contract, not whole-program soundness, a production repair qualification, or model evidence. The analyzer restricts direct top-level calls and does not claim that MAY implies execution or unique target resolution.

Initial execution failed two assertions: conservative UNKNOWN for a conditional-true import, and missing detection of globals-subscript assignment. The expectation and detector were corrected before final execution. All 10 final tests passed. No reserved issues accessed.

Local original executed archive: SHA256 `2ea6b4917c489c5ceefceb195c06848ecf5299192ee67ca360690295cb04522a`. Archive contains executable Python, complete raw classifications and SHA manifest. Full archive mirroring to GitHub remains pending.

Only two independently qualified real production repairs remain. No semantic IR superiority claim.