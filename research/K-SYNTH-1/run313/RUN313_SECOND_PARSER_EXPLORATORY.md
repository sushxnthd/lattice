# Run313 post-hoc second-parser differential (exploratory, NOT prospective)

After the frozen four-arm historical h11 replay, the same 22 fixed wire streams were independently parsed by Python's trusted `http.client.HTTPResponse` using an in-memory fake socket, without network access. This experiment was **not** part of the prospectively frozen Run313 primary protocol. No source or acceptance gate was retuned.

Compared to the historical h11 FULL arm's unfragmented `whole` outcomes, `http.client` completed 19/22 streams while h11 FULL completed 10/22. The nine **distinct adversarial wire streams** accepted by `http.client` but rejected by h11 were:

- `bare_cr`
- `double_cr`
- `nul_header_value`
- `space_before_colon`
- `leading_space_header`
- `conflicting_cl`
- `embedded_bare_lf`
- `missing_final_crlf`
- `empty_field_name`

The clearest bounded witness is `conflicting_cl`: `HTTP/1.1 200 OK\r\nContent-Length: 0\r\nContent-Length: 3\r\n\r\nabc`. Historical h11 FULL raises `RemoteProtocolError`; stdlib `http.client` returns status 200 and an empty body, following the first length. The two parsers disagree about validity and body framing on identical bytes.

This is a **response-parser differential**, not a demonstrated request-smuggling exploit, security vulnerability, or proof of a deployed proxy desynchronization. No network request or second real server was involved. These are 9 distinct wire streams, not 9 independent repair tasks; fragmentation variants remain correlated. Additional end-to-end testing would be required before a security conclusion.

The trusted standalone [second-parser runner](run313_second_parser_exploratory.py) and its raw JSONL are included in the complete local SHA-verified Run313 archive. The historical original cloud artifact and qualification gates are unchanged.
