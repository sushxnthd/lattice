# Run307 frozen source manifest (before functional execution)

Frozen protocol commit: f4e506e942bc6c919d8d15f8679127fce80ac033.

Generated deterministic 256 trusted fixtures from `run307_build_frozen.py`: 2 future-import modes x 2 effect functions (restore/no-op) x 4 annotation access patterns (none/direct/alias/repeat) x 16 syntactic name variants.

SHA-256 of canonical UTF-8 JSON file `RUN307_FROZEN_SOURCES.json` (json.dumps(sort_keys=True,indent=2) + newline): `f2646b6dd96169c19cdb3474d3011354124b893e5829fd719ea02d06075da95b`.

Expected Python 3.13: eager annotation effect at definition unless future import; expected Python 3.14: lazy first annotation access unless future import. Only effect='restore' can restore builtin len; repeated accesses expected cached (one annotation side effect). No source fixtures executed when this manifest was committed.

If interpreter 3.14 is unavailable, do not label predictions as empirical 3.14 results. All cases are correlated fixtures, not independent repair tasks.
