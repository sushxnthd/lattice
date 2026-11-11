# Run643 — Cluster dependence in planned paired repair evaluation

Synthetic, seeded sensitivity experiment; not model or production-repair evidence. Simulated 2,000 trials per cell at n=306/681/800, repository counts 100/150/200, 30% discordance and conditional IR win 65%. Beta-binomial repository latent win probabilities had rho 0, 0.1, 0.3, 0.5. Naive exact McNemar rejection proportions: n306 0.806/0.8085/0.776/0.774; n681 0.986/0.986/0.969/0.9685; n800 0.9925/0.995/0.991/0.9855. These are NOT calibrated cluster-aware powers.

Counterexample: 4 repositories with 10 discordant issues each, 3 all favor IR, 1 all favor Python. Naive issue-level exact McNemar p=0.00222; two-sided repo-level sign test p=0.625. Independent sampling unit changes inference. Pre-register repo-aware effect and uncertainty; do not assume n306/n681 guaranteed powered.

Executable local artifact SHA256 ZIP 44ec3d2ce137aecdcf204d14ded27328fd4c05db8d40a436a6997f2700107569; includes reproduce.py, raw.json, stdout.txt and SHA256 manifest. GitHub executable/raw mirroring pending. No upstream execution, model calls, new qualified tasks or access to 89 sealed issues. Qualified count remains two.