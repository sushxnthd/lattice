# Run552: qualification gate causal-identifiability counterexample

Constructive falsification: two mechanisms yield identical observed base=fail, A=fail, B=fail, AB=pass. Mechanism 1: outcome = A AND B. Mechanism 2: outcome = unrecorded environment flag, set only in AB execution. Under a fixed environment flag=0, only mechanism 1 repairs the target. Thus the observed 2x2 gate alone cannot certify joint causal necessity unless the execution environment is fixed and independently verified across all four cells.

A second explicit counterexample passes 100 controls (inputs 0..99) but regresses at input 1000. Nonregression is limited to tested controls.

Local executable experiment and raw traces: SHA-verified run552.zip SHA256 a3d95dae9d3b44ba53121173b5c07a90b0ab3ba6c3cdef33fcff9a686d0b16be. GitHub source/raw mirroring outstanding. No real repair newly qualified; no coding-model inference or semantic IR advantage. All 89 reserved issues sealed.
