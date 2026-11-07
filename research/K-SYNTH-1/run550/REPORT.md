# Run550: prospective joint target/control qualification gate

Executed six assertions and exhaustively enumerated 16 two-arm outcome assignments for a one-target/one-control synthetic fixture. Exactly 9/16 pass the **new proposed** joint target-plus-control necessity gate. This is a protocol implementation test, not a qualification of a public-repository repair.

The gate requires a frozen disjoint target/control partition, complete outcome matrix, failing baseline targets, passing baseline controls, full-reference target repair without control regression, and failure of each single-component arm to satisfy both target and control requirements. It deliberately rejects a single component that independently satisfies the entire joint contract.

**Historical integrity:** Werkzeug PR2535 remains unqualified under its ORIGINAL prospectively frozen rules. The synthetic `historical_shape` fixture must not be used to retroactively qualify it. The test illustrates why a *new prospectively declared* joint criterion must not be confused with post-hoc selection.

Limitations: synthetic outcomes, no pinned public-repo source, no isolated independent oracle, no model inference, no IR-vs-Python evidence, no soundness theorem. All 89 reserved issues remain sealed. Next: prospectively freeze an independent real two-production-source candidate before oracle execution.

Local archive SHA256: `8850dbf55c61a771077ef07e9e61b3a6de5d4fb4ea5a7689e039ed464641466d`.
