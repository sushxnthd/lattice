# Run577: recovery versus concurrent external writes

Deterministic eight-case abstract state-machine experiment. Blind rollback overwrites an external writer in 2/2 concurrent-write cases. Conservative compare-and-swap preserves external values and reports UNKNOWN/CONFLICT in 2/2 cases. Four assertions passed. This disproves noninterference of blind journal rollback in this abstract model, not physical crash safety. ABA, filesystem aliases, TOCTOU and crash durability remain open. No real task qualified; no model inference; 89 reserved issues sealed.

Local SHA-verified archive: lattice_run577.zip; SHA256 `5f61a01e095d80c947dcfb165e65cf44e5a11c681afebe6ff1d2d0bc6de49a8c`.
