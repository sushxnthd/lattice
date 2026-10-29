# Run342 post-outcome ABI-only falsifier protocol (exploratory; NOT qualification)

Frozen after recovering original 50 historical outcomes, before executing any compatibility-adapter counterfactual.

Original historical Run342: base 0/4 LF targets and 6/6 controls; A-only (new ReceiveBuffer with old readers/connection) 0/4 targets and 2/6 controls, with `AttributeError: ReceiveBuffer.compress`; B-only (old ReceiveBuffer with new readers/connection) 0/4 targets and 5/6 controls, with `AttributeError: ReceiveBuffer.maybe_extract_next_line` on chunked control; full reference 4/4 targets and 6/6 controls. The original frozen qualification **FAILED** and cannot be rescued.

**Counterfactual A compatibility shim**, added only to the isolated A-only source snapshot: `ReceiveBuffer.compress(self)` returns None because the new ReceiveBuffer already removes consumed bytes in `_extract`; `ReceiveBuffer.maybe_extract_until_next(self, needle)` delegates to `maybe_extract_next_line()` only when `needle == b'\\r\\n'`, otherwise raises a fail-closed exception. These are interface bridges, not a change to LF blank-line detection.

**Counterfactual B compatibility shim**, added only to the isolated B-only snapshot: `ReceiveBuffer.maybe_extract_next_line(self)` delegates to existing `maybe_extract_until_next(b'\\r\\n')`. This bridges only the renamed CRLF chunk-header method, not LF header parsing.

**Predictions:** A+shim may repair all LF targets and controls; B+shim may preserve all controls but fail LF targets. If so, the observed multi-file necessity is explained by API compatibility rather than semantic changes across files. If not, report failure unchanged. Run 4 original arms locally to compare exact event traces with original Python 3.10 cloud, then run both shims. Differentially test base/new CRLF line extraction on at least 2,048 seeded append/extract traces. This is bounded evidence only; do not claim global equivalence or retrospectively promote the failed qualification.

All 89 reserved issues remain sealed; no model inference or IR superiority.
