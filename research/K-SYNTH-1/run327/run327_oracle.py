#!/usr/bin/env python3
"""Frozen urllib3 PR2482 fault-injection oracle. No external network or reference introspection.

Run: python -I -B run327_oracle.py /candidate
All fault injection uses the public ConnectionPool.urlopen() entrypoint. No model code runs.
"""
import http.client
import json
import pathlib
import ssl
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "src"))
import urllib3
from urllib3.connectionpool import HTTPSConnectionPool
from urllib3.exceptions import MaxRetryError, ProxyError
from urllib3.util.retry import Retry
from urllib3.util.url import parse_url
from urllib3.util.ssl_match_hostname import CertificateError

class InjectedConnection:
    sock = None
    timeout = None
    def __init__(self, proxy):
        self._connecting_to_proxy = proxy
    def close(self):
        pass

CASES = (
    ("target_proxy_tls", True, "tls", "ProxyError", True),
    ("target_proxy_certificate", True, "certificate", "ProxyError", True),
    ("target_proxy_http_exception", True, "http_exception", "ProxyError", True),
    ("control_direct_tls", False, "tls", "SSLError", False),
    ("control_direct_certificate", False, "certificate", "SSLError", False),
    ("control_direct_http_exception", False, "http_exception", "ProtocolError", False),
    ("control_direct_oserror", False, "oserror", "ProtocolError", False),
    ("control_proxy_valueerror", True, "valueerror", "ValueError", False),
    ("control_direct_valueerror", False, "valueerror", "ValueError", False),
)

def error(kind):
    if kind == "tls":
        return ssl.SSLError("injected TLS negotiation failure")
    if kind == "certificate":
        return CertificateError("injected certificate failure")
    if kind == "http_exception":
        return http.client.HTTPException("injected HTTP parser failure")
    if kind == "oserror":
        return OSError("injected connection failure")
    if kind == "valueerror":
        return ValueError("injected invalid parameter")
    raise AssertionError(kind)

def run_case(case):
    name, proxy, kind, expected, target = case
    pool = HTTPSConnectionPool("example.invalid", port=443, maxsize=1)
    pool.proxy = parse_url("https://proxy.invalid:443") if proxy else None
    pool.proxy_headers = {}
    pool._get_conn = lambda timeout=None: InjectedConnection(proxy)
    pool._prepare_proxy = lambda conn: None
    def fail_validation(conn):
        raise error(kind)
    pool._validate_conn = fail_validation
    observed = None
    outer = None
    original = None
    detail = None
    try:
        pool.urlopen("GET", "/", retries=Retry(total=0, connect=0, read=0, redirect=0))
        observed = "NO_EXCEPTION"
    except BaseException as exc:
        root = exc.reason if isinstance(exc, MaxRetryError) else exc
        observed = type(root).__name__
        outer = type(exc).__name__
        detail = str(root)[:300]
        if isinstance(root, ProxyError):
            original = type(root.original_error).__name__
    return {
        "case": name, "target": target, "proxy": proxy, "injection": kind,
        "expected": expected, "observed": observed, "outer": outer,
        "proxy_original": original, "exception_detail": detail,
        "pass": observed == expected,
    }

rows = [run_case(c) for c in CASES]
result = {
    "oracle_version": "run327-frozen-v1",
    "candidate_git": (ROOT / "PINNED_COMMIT").read_text().strip()
        if (ROOT / "PINNED_COMMIT").exists() else None,
    "python": sys.version.split()[0],
    "urllib3_version": str(urllib3.__version__),
    "targets": sum(r["pass"] for r in rows if r["target"]),
    "controls": sum(r["pass"] for r in rows if not r["target"]),
    "rows": rows,
}
print(json.dumps(result, sort_keys=True, indent=2))
