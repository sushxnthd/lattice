"""Frozen, deterministic, network-free HTTPX PR1183 public-API oracle.

Runs inside a separately pinned historical checkout; never executes model output.
All cases are fixed before reading the historical reference source/diff.
"""
import json
import socket
import traceback
from unittest.mock import patch
from urllib.parse import urlsplit

import httpx

ROUTES = {"/one": "/done", "/two": "/mid", "/mid": "/done"}
BASE_URL = "http://lattice.invalid"
# (id, arm, method, starting path, explicit redirect value or None,
#  expected HTTP status, expected request paths)
CASES = [
    ("target_api_head_one", "api", "head", "/one", None, 200, ["/one", "/done"]),
    ("target_client_head_one", "client", "head", "/one", None, 200, ["/one", "/done"]),
    ("heldout_client_head_two", "client", "head", "/two", None, 200, ["/two", "/mid", "/done"]),
    ("control_api_head_false", "api", "head", "/one", False, 302, ["/one"]),
    ("control_client_head_false", "client", "head", "/one", False, 302, ["/one"]),
    ("control_api_get_default", "api", "get", "/one", None, 200, ["/one", "/done"]),
    ("control_client_get_default", "client", "get", "/one", None, 200, ["/one", "/done"]),
    ("control_api_head_true", "api", "head", "/one", True, 200, ["/one", "/done"]),
    ("control_client_head_true", "client", "head", "/one", True, 200, ["/one", "/done"]),
]


def forbid_connect(*args, **kwargs):
    raise AssertionError("REAL_NETWORK_FORBIDDEN")


def run_case(case):
    name, entry, method, path, explicit, expected_status, expected_paths = case
    trace = []

    def fake_send(self, request, timeout):
        url = urlsplit(str(request.url))
        assert url.hostname == "lattice.invalid", "UNAUTHORIZED_HOST"
        assert request.method == method.upper(), "METHOD_NOT_PRESERVED"
        trace.append({"method": request.method, "path": url.path})
        next_path = ROUTES.get(url.path)
        if next_path is not None:
            return httpx.Response(302, request=request, headers={"location": next_path})
        if url.path == "/done":
            return httpx.Response(200, request=request)
        raise AssertionError("UNEXPECTED_ROUTE:" + url.path)

    kwargs = {} if explicit is None else {"allow_redirects": explicit}
    expected = {"status": expected_status,
                "trace": [{"method": method.upper(), "path": p} for p in expected_paths],
                "history_len": len(expected_paths) - 1 if expected_status == 200 else 0}
    try:
        with patch.object(socket.socket, "connect", forbid_connect), patch.object(
            httpx.Client, "_send_single_request", fake_send
        ):
            if entry == "api":
                response = getattr(httpx, method)(BASE_URL + path, trust_env=False, **kwargs)
            else:
                with httpx.Client(trust_env=False) as client:
                    response = getattr(client, method)(BASE_URL + path, **kwargs)
        observed = {"status": response.status_code, "trace": trace,
                    "history_len": len(response.history)}
        return {"id": name, "passed": observed == expected,
                "observed": observed, "expected": expected, "error": None}
    except Exception as exc:
        return {"id": name, "passed": False,
                "observed": {"trace": trace}, "expected": expected,
                "error": type(exc).__name__ + ":" + str(exc),
                "traceback": traceback.format_exc(limit=3)}


def main():
    results = [run_case(case) for case in CASES]
    print(json.dumps({"schema": "lattice-run328-oracle-v1", "cases": results,
                      "passed": sum(x["passed"] for x in results),
                      "total": len(results)}, sort_keys=True))


if __name__ == "__main__":
    main()
