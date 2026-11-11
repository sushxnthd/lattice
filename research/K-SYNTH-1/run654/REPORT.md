# K-SYNTH-1 Run654 — target/control separation audit

Exhaustively enumerated 65,536 synthetic four-arm × two-target × two-control Boolean configurations. Exactly 768 meet base target failure, base/full control preservation, and full target repair. Of these 336 lack target-level component necessity, 336 have a common target failed by both omissions, and 96 have disjoint target-failure witnesses. Disjoint witness is suite-level necessity, not per-target synergy. Counts are exact synthetic combinatorics, not empirical repair rates or causal effects.

No new upstream execution, heldout validation, or coding-model comparison. Qualified real repairs remain two; 89 reserved issues sealed. Original Run641 oracle still lacks independent heldout/nonregression qualification. Local archive SHA256 913cd3399bce175fdcceb0de3f70a150a66caa0f46d1b980e21d3663d3493bff. Next: execute pinned upstream four-arm oracle in isolated CI and independently adjudicate.
