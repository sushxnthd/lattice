# Run603: exact sign-flip failure under asymmetric mean-zero effects

Eight independent repository effects take +1 with probability 0.9 and -9 with probability 0.1. Their population mean is exactly zero. Exhaustive enumeration of all 256 observed vectors and all 256 sign flips per vector gives a nominal 5% two-sided sign-flip rejection probability **21524531/50000000 = 0.43049062**. The all-positive observation alone has probability 0.9^8 = 0.43046721 and sign-flip p=1/128. Thus zero mean alone does not justify sign-flip inference: joint sign symmetry or an actual randomization mechanism is required.

Exact standard-library Python reproducer and all 256 weighted outcomes were executed locally. SHA-256 of local archive: `cd18b510b86406e11f64cadf8943a33899d226f29533a345d9637fbd59317893`. This is a synthetic counterexample, not production-repair/model evidence. The 89 reserved issues remain sealed. No semantic-IR superiority claim.
