# Prospective external issue candidates (not a frozen evaluation)

Selected from currently open upstream issues on 2026-10-12. These are candidate tasks only: no task solutions, hidden tests, model runs, or holdout results are claimed.

- pytest-dev/pluggy #760: plugin registry identity vs equality. Issue opened 2026-10-08. Base commit 87f130aa18d8fdf9c92585e72423eca7f3de727d.
- pytest-dev/pluggy #761: rollback after hook registration or historic replay failures. Issue opened 2026-10-08. Same base commit; count as one repository cluster.
- pallets/itsdangerous #429: unexpected max_age accepted by untimed serializer. Issue opened 2026-07-08. Base commit 672971d66a2ef9f85151e53283113f33d642dabd.
- pallets/click #3652: multiple-option help metavar convention. Issue opened 2026-06-29. Base commit 2247b35ea1c47c727d7a06e51fa280e12a863ff6.

All tasks require independent failing tests, clean environments, source-hash capture, prompt parity, hidden-test separation, and prospective freeze before model inference. These tasks may already be known to pretrained models. Two pluggy issue reports explicitly acknowledge model assistance, which is a contamination consideration.

The previous negative Lattice-versus-Python result remains unchanged.