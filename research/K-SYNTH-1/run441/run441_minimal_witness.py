#!/usr/bin/env python3
"""Run441: no-network production-source witness, urllib3 2.7.0 only."""
import hashlib
import pathlib
import urllib3

EXPECTED_SHA256 = {
    'poolmanager.py': '734ae1d2b7140b5b79b431ae51e188800ce512b6ac3cec16c0b881ebb957f293',
    'util/url.py': '59187e4cc617a2c9a0a7c9bc953e07e6ca681f0e7252395c3027d4e77024a00b',
    'connectionpool.py': 'b0616775d5d8c25c7b282e0908fd602af74d18b34af984c22437460021a3dd8f',
}


def main():
    assert urllib3.__version__ == '2.7.0', 'Different installed release; do not generalize'
    root = pathlib.Path(urllib3.__file__).parent
    for name, digest in EXPECTED_SHA256.items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
    with urllib3.PoolManager() as manager:
        pool_port = manager.connection_from_host('example.com', port=0).port
    with urllib3.ProxyManager('http://proxy:0') as manager:
        proxy_port = manager.proxy.port
    netloc = urllib3.util.parse_url('http://example.com:0').netloc
    assert (pool_port, proxy_port, netloc) == (80, 80, 'example.com')
    print({'expected_explicit_port': 0, 'observed_pool_port': pool_port,
           'observed_proxy_port': proxy_port, 'observed_netloc': netloc,
           'scope': 'SHA-pinned installed urllib3 2.7.0; no network calls'})


if __name__ == '__main__':
    main()
