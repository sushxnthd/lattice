#!/usr/bin/env python3
"""Executable Run257 model-output counterexample; no third-party dependencies."""
from urllib.parse import urlsplit

def model_server_parse(server_name):
    sn_host, _, sn_port = server_name.partition(":")
    if sn_host.startswith("[") and sn_host.endswith("]"):
        sn_host = sn_host[1:-1]
    return sn_host, int(sn_port) if sn_port else 5000

def model_session_parse(host):
    return host.partition(":")[0].replace("[", "").replace("]", "")

def check():
    for address in ("[::1]:8080", "[2001:db8::1]:8080"):
        try:
            model_server_parse(address)
        except ValueError:
            pass
        else:
            raise AssertionError("model server parser unexpectedly accepted IPv6")
        parsed = urlsplit("//" + address)
        assert (parsed.hostname, parsed.port) == (address[1:address.index("]")], 8080)
    assert model_session_parse("[::1]:8000") == ""
    assert urlsplit("http://[::1]:8000/").hostname == "::1"
    return "4 model/reference IPv6 counterexample checks passed"

if __name__ == "__main__":
    print(check())
