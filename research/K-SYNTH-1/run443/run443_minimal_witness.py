#!/usr/bin/env python3
"""Run443 standalone semantic witness; does not execute generated patches."""
CASES = {
    "example.com": "example.com",
    "example.com:5000": "example.com",
    "127.0.0.1": "127.0.0.1",
    "127.0.0.1:8080": "127.0.0.1",
    "localhost": "localhost",
    "localhost:8080": "localhost",
    "[::1]": "[::1]",
    "[::1]:5000": "[::1]",
    "[2001:db8::1]": "[2001:db8::1]",
    "[2001:db8::1]:443": "[2001:db8::1]",
}
def audit():
    old = new = 0
    for host, expected in CASES.items():
        baseline = host.partition(":")[0]
        model = host.rpartition(":")[0]
        old += baseline == expected
        new += model == expected
        print(repr(host), "expected", repr(expected),
              "baseline", repr(baseline), "model", repr(model))
    assert (old, new) == (6, 5)
    assert "example.com".rpartition(":")[0] == ""
    assert "[::1]".rpartition(":")[0] == "[:"
    for port in (None, 0, 1, 80):
        assert not (port is None and port == 0)
    print("10 cases, partition 6/10, rpartition 5/10; zero elif unreachable")
if __name__ == "__main__":
    audit()
