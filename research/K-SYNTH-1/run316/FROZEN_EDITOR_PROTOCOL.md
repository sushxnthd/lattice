# Run316 secondary structural compiler protocol (frozen before execution)

Separate bounded synthetic engineering study, not a model benchmark or production repair qualification. Source SHA256: `run316_structural_compiler.py` 005fb330be56bc94ba4e7c8c400a609092e6aa9452a2089e8218f13b7601331f; `run316_structural_experiment.py` 2206e8e7b696e1185718776b9c3f599d8405494ca7767f55bfcecff2c2736144.

Primary predeclared test: 128 deterministic correlated three-module fixtures, each with 4 SHA-preconditioned AST structural operations (statement insertion, expression replacement, statement replacement, statement deletion). Require byte-identical outputs against independently specified expected bytes, and 128/128 isolated trusted CPython functional replays. Require 8/8 negative controls rejected. All 512 edits must be verified by exact AST node digest and UTF-8 byte span. Any exception or mismatch is a failed test; preserve raw output and errors.

Bounded editor supports no arbitrary top-level file replacement and does not execute untrusted model code. It is not yet demonstrated to express the complete h11 PR #115 or other historical reference repairs. It is not proof of semantic soundness, secure filesystem transactions, or IR superiority. Six historical repairs remain six; 89 reserved boundary issues remain sealed.
