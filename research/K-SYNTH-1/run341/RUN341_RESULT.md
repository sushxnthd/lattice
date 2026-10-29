# K-SYNTH-1 Run341: casewise interaction and cancellation falsifier

Date: 2026-10-29 UTC. Canonical branch `research/exp003-context-order`, sole OPEN/DRAFT/UNMERGED PR #9; all 89 reserved boundary issues SEALED.

## Evidence and reproducibility
Read-only post-outcome reanalysis of the ORIGINAL prospectively frozen HTTPcore PR #882 Run340 four-arm historical public-API results. Parent archive SHA-256: `14b014089ce43c6b22daa8343115d334e5c0e3268a9316089903f1274cfb33b8`. All 17 parent SHA-256 manifest entries independently reverified, including 40 original functional records, frozen oracle, source manifests, original GitHub artifact `d1ebbc8393f5cd5e6077b4d48ac94473007307a904806c8e6d2acbcde6f2664a`, and audit-only corrected artifact `6a28444a170e572f5b20143a2ccbcbbfaac5c5a8d7d92556aca9c18e791bc7b9`. Original Run340 qualification is unchanged.

## Executed causal diagnostic
New independent local analyzer `run341_interaction_gate.py` verifies all 40 immutable functional outcomes and calculates each case's 2x2 contrast `D_i = Y11_i - Y10_i - Y01_i + Y00_i`, rather than relying on aggregate contrast.

- All 10 cases have `D_i=0`; `sum(D_i)=0` and `sum(abs(D_i))=0`.
- Two sync cases have pattern `(0,1,0,1)`, two async cases `(0,0,1,1)`, and six controls `(1,1,1,1)`. Original counts remain baseline 6/10, sync-only 8/10, async-only 8/10, full 10/10.
- Five local tests passed, including 4,096 seeded order-invariance trials and 24 adversarial record corruptions rejected. The exhaustive 16-function Boolean theorem checker also passed.

## Formal result
For binary `f:{0,1}^2 -> {0,1}`, exactly 6 of the 16 functions are coordinatewise monotone. Under monotonicity, `D=+1` only for conjunction (AND), `D=-1` only for disjunction (OR), and `D=0` for constants or single-factor functions. Exhaustive truth-table evidence is included.

**Cancellation falsifier:** two cases with potential-outcome vectors `(0,0,0,1)` and `(0,1,1,1)` have contrasts +1 and -1, so their aggregate contrast is zero despite two nonzero casewise interactions. Thus aggregate zero is insufficient to establish even absence of observed outcome interaction. HTTPcore #882 satisfies the stronger *casewise* zero condition on its finite oracle, but this cannot prove absence of global semantic interaction.

## Scientific boundary and next step
A positive outcome interaction does not prove cross-file dataflow (ABI mismatches and oracle effects can mimic it); a zero observed interaction does not prove global noninteraction. Analyzer conservatively marks `mechanistic_semantic_interaction=UNKNOWN` and `abi_compatibility=UNKNOWN` for every case. Future independently qualified tasks must prospectively register source-level cross-file hypotheses and ABI controls, retain PARALLEL/INTERACTING/UNKNOWN strata without post-outcome filtering, and use matched IR versus Python/AST model arms. No new model inference, new qualified repository, powered IR advantage, or breakthrough claimed.

Local reproducibility archive: `lattice_run341_casewise_interaction_gate.zip`, SHA-256 `f0275e30df8a9343ceb9947d35cdb2bb50b11bf8dc0cde3573712e674664c7fb`; 18 SHA-verified evidence payloads, original Run340 raw records, executable code/tests, theorem truth table and protocol. All 89 reserved issues untouched.
