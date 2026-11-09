# Run608: frozen qualification gate audit

Exhaustively evaluated 256 paired two-component ablation configurations with two frozen targets and two controls. Joint target-plus-control necessity accepted 225; target-only necessity accepted 144; joint-only accepted 81; neither accepted 31. This establishes that joint necessity is logically weaker than target-only necessity: a component ablation may fail only on controls and nevertheless pass joint necessity. Control regression does not by itself demonstrate the target repair mechanism. Future prospective qualification must record target rescue and control preservation separately for each component ablation.

The original local hard-coded target-only expectation was wrong (49 instead of 144); the executable assertion failed and was corrected. Synthetic exhaustive result only, no new real qualified repair, no model comparison. All 89 reserved issues sealed.

Local ZIP SHA256 `0c566c9b4c0815c8622328f6c23a6c58718f27c60f0bcdca9cf952bf5e5cedc6`; complete raw dataset in local archive, GitHub raw mirror pending.
