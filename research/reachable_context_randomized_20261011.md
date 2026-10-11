# Reachable context randomized property probe (2026-10-11)

Classification: CAPABILITY-BUILDING / DISCRIMINATION. Belief: BELIEVED (synthetic only).

Independent implementation, **not canonical Lattice execution**. Seed 20261011, 250 random Boolean DAGs, 40 sequential edits per graph, 3 checkpoints per graph, 10,920 exhaustive input-valuation comparisons. No mismatches between full-history and reachable-only serializations. Max byte reduction 16.76x; mean full view 1328.01 bytes, mean compact view 531.40 bytes. Original script SHA256 dbcc76a51d3da72a93cadf9f6225178b2b14f22e70e75b251dd0b7b9788cef20; result SHA256 697cc9638c92efcaa1f74b954d46c6e9a005f94d5c1655cc4b4340df3c816114. Raw script and result are preserved as conversation artifacts, not repository artifacts.

Prediction: reachable-only serialization can reduce agent context while preserving bound DAG meaning. Competing explanation: reductions are specific to synthetic graphs and do not generalize to real repository histories or tokenization.

Next discriminator: add opt-in reachable_context API and property tests against canonical FramedProgram; preserve legacy context API and frozen benchmarks. Measure actual model token counts; do not claim LLM advantage.
