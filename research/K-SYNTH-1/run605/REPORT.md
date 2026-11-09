# Run605: bounded cross-file import resolution with explicit UNKNOWN

Eight deterministic AST cases executed locally: 8/8 passed; four MAY_STATIC_IMPORT_BINDING, four UNKNOWN. Cases cover named import, alias, rebinding, missing export, attribute call, unreachable conditional, deferred body, wildcard import.

MAY_STATIC_IMPORT_BINDING indicates only that a matching top-level definition exists in the named source file without detected top-level rebinding. It does not certify runtime binding, execution, callee identity, or sound whole-program call graph. Dynamic imports, hooks, local shadowing and monkeypatching remain unresolved. Conditional and deferred calls are never promoted to MUST.

Local reproducibility archive SHA-256: 239fe50d4a94bf30c89fa743fe1815fcbcd1a50d4a081f09fd4ed60ba7fe5225. Eight raw source-hashed outcomes, executable Python and checksum manifest are in local archive. No model inference, production qualification or superiority claim. 89 reserved issues untouched.
