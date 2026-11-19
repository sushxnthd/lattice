# Run750 — bounded alpha CLI release-gate regression

2026-11-19 UTC; CPython 3.13.5; archived Run749 compiler snapshot. Twelve subprocess-level tests passed (12/12): inventory, API, certification, import/future-import/decorator/syntax refusals, same-path/hardlink/symlink output alias refusal, oversized input refusal, and valid UTF-8 source. Every case checked input-byte preservation. No candidate source execution or model inference. This does not prove race-free filesystem behavior, general soundness, or IR superiority. Only two qualified independent real repair tasks; all 89 reserved issues sealed.

Local SHA-verified archive: `run750.zip`, SHA256 `0f707af6271188ac094db12b3cbdd6f8edcabd96681195b4d46de6d9d53fa9b0`. Archive mirroring pending.
