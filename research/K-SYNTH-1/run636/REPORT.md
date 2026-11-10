# Run636: descriptor shadowing and state-transition oracle

Original Werkzeug PR #3341 patches remove `TestResponse.text` (`cached_property`) in `src/werkzeug/test.py` and add `Response.text` (`property`) in `src/werkzeug/wrappers/response.py`. These original patches were fetched directly from GitHub during this run.

An executed four-arm Python descriptor analogue shows the parent-only arm leaves the subclass's cached text stale after mutating backing bytes, while the combined arm returns updated text. Both return the same first-read text. The removal-only arm raises AttributeError; the baseline retains stale text. Thus an initial-read oracle is insufficient to establish component necessity. A semantic/dataflow IR must represent MRO shadowing and distinguish caching; otherwise emit UNKNOWN.

Seven executable assertions passed. This is a Python analogue, **not upstream Werkzeug execution**, a prospectively frozen qualification, or model evidence. Qualified real repairs remain two; 89 reserved issues remain sealed.

Reproducer and raw JSON are in the SHA-verified local Run636 archive; full artifact mirroring is pending.