"""Run358 real h11 parser ownership counterexample (bounded h11 0.16.0).

Full 1,536-trace source, independent auditor, tests and raw results are in
the SHA-verified local Run358 reproducibility archive. This compact executable
reproduces the central observed counterexample without model-generated code.
"""
import h11

def inspect(kind):
    conn = h11.Connection(h11.CLIENT)
    method = b"CONNECT" if kind == "connect" else b"GET"
    headers = [(b"host", b"example.com")]
    if kind == "upgrade":
        headers += [(b"connection", b"Upgrade"), (b"upgrade", b"websocket")]
    conn.send(h11.Request(method=method, target=b"example.com:443" if kind == "connect" else b"/", headers=headers))
    conn.send(h11.EndOfMessage())
    body = b"abc"
    if kind == "upgrade":
        response = b"HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\n\r\n" + body
    elif kind == "connect":
        response = b"HTTP/1.1 200 Connection Established\r\n\r\n" + body
    else:
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\n" + body
    conn.receive_data(response)
    event = conn.next_event()
    assert isinstance(event, (h11.Response, h11.InformationalResponse))
    buffered, eof = conn.trailing_data
    assert buffered == body and not eof
    switched = conn.their_state is h11.SWITCHED_PROTOCOL
    if kind == "ordinary":
        assert not switched
        following = conn.next_event()
        assert isinstance(following, h11.Data)
        assert bytes(following.data) == body
    else:
        assert switched
    return kind, event.status_code, switched, buffered.hex()

if __name__ == "__main__":
    assert h11.__version__ == "0.16.0", "version-scoped evidence only"
    for case in ("upgrade", "connect", "ordinary"):
        print(inspect(case))
