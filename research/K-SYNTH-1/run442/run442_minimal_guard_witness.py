#!/usr/bin/env python3
"""K-SYNTH-1 Run442: algebraic guard witness (real API traces in local archive).

This is an extracted guard-level witness, not an execution of the upstream
urllib3 package. The full SHA-locked production-source experiment, independent
replay and 216-case freeze are in the Run442 reproducibility archive.
"""

def original_same_host(pool_port, url_port, default_port):
    port = url_port
    if pool_port and not port:
        port = default_port
    elif not pool_port and port == default_port:
        port = None
    return port == pool_port

def corrected_same_host(pool_port, url_port, default_port):
    port = url_port
    if pool_port is not None and port is None:
        port = default_port
    elif pool_port is None and port == default_port:
        port = None
    return port == pool_port

if __name__ == "__main__":
    for scheme, default in (("http", 80), ("https", 443)):
        original = original_same_host(default, 0, default)
        corrected = corrected_same_host(default, 0, default)
        assert original is True and corrected is False
        print(f"{scheme} pool={default} URL-port=0: baseline={original}, corrected={corrected}")
