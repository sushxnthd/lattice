# Run651: target/control confounding in Run650

Run650 requires each non-full arm to fail any of four cells, allowing a target-successful arm that fails only controls to be labeled necessary. Exhaustive enumeration of 4096 synthetic Boolean matrices with the full arm correct: original predicate accepts 3375, target-necessity predicate accepts 1728, and 1647 original candidates are rejected by the stricter condition. In 27 original candidates, all three non-full arms pass both targets and fail only controls.

These are combinatorial counts, not empirical rates or upstream oracle evidence. Strict target necessity is necessary but not sufficient for qualification; heldout/nonregression oracle, pinned upstream execution and prospective freeze remain absent. Qualified production repairs: 2. Reserved boundary issues: 89 sealed.
