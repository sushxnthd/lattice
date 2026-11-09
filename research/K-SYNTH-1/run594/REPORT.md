# K-SYNTH-1 Run594 — anytime-valid repository confidence sequence

Run593 showed optional-stopping failure for repeated fixed-time intervals. This run computes a conservative time-uniform alternative. For independent repository-level paired effects X_i in [-1,1] with a common mean μ, allocate alpha_t=0.05*6/(π² t²). Hoeffding plus a union bound guarantees simultaneous 95% coverage at every integer t, including data-dependent stopping. Halfwidth: sqrt(2 log(2/alpha_t)/t), clipped to [-1,1].

Computed fixed-time / anytime halfwidths: n=100: 0.2716/0.5176; n=400: 0.1358/0.2843; n=800: 0.0960/0.2095; n=2000: 0.0607/0.1392. This is analytic, conservative, and not observed coding-model evidence. Nonidentically distributed repositories, adaptive repository selection, and other estimands require separate assumptions.

Local executed reproducer and raw data archived in lattice_run594.zip, SHA256 711a6633d3037cd1285888046aeabe02c6f45fa282e5aeae200cf79c6a913fd6. Full raw archive GitHub mirroring pending. Two qualified production repairs only; 89 boundary issues sealed; no superiority claim.
