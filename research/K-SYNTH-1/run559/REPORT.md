# Run559: UTF-8 byte-offset atomic transaction counterexample

Executed CPython synthetic compiler experiment. Source has 30 UTF-8 bytes but 25 Python code points. A two-edit transaction using byte coordinates correctly changes both Greek alpha identifiers to `value`, whereas naive Python string slicing using byte offsets silently produces a different result. Compiler rejects split-codepoint endpoints and equal-start edits, and applies disjoint edits atomically in descending source-byte order.

Exhaustive enumeration of all 496 single intervals: 351 valid byte-boundary pairs accepted, 145 invalid boundary pairs rejected. Exhaustive 2713 bounded disjoint two-edit pairs were order-invariant. All assertions passed. The model-facing contract must declare coordinate units and validate them at the shared compiler boundary; no format-specific advantage is inferred.

Local reproducibility archive SHA-256: `dd47a4c3693ad88573ea8783be53bd1c3559f5d95702fde382bfd8653b319c13`; executable SHA-256 `35a30d04acf611c064cabff2d07b09f1d76003281ea42a4b69b93bec4c7076c5`; raw JSON SHA-256 `e4996134c45e962ea77da6c4c5b2e2ffae79df5b200873b66bbe1a5e90f82be6`. Full source/raw GitHub mirroring pending.

No new real repair, model inference, independent evaluator, or powered IR advantage. Two real tasks qualified historically; 89 reserved issues sealed. Synthetic compiler-contract result only.
