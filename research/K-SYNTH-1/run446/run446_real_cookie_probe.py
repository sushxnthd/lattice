#!/usr/bin/env python3
"""Run446 isolated real Flask cookie diagnostic. Historical source, no model code."""
import hashlib
import importlib.metadata
import json
import pathlib
import platform
import sys
from urllib.parse import urlsplit
import flask

def safe_cookies(client):
    jar = getattr(client, "_cookies", None)
    if jar is None:
        return None
    return [
        {"key": repr(key), "domain": getattr(cookie, "domain", None),
         "path": getattr(cookie, "path", None), "key_name": getattr(cookie, "key", None),
         "value_length": len(str(getattr(cookie, "value", "")))}
        for key, cookie in sorted(jar.items(), key=lambda pair: repr(pair[0]))
    ]

def run(cases_path, output_path, variant):
    cases_path = pathlib.Path(cases_path)
    cases = json.loads(cases_path.read_text())
    assert len(cases) == 128 and len({x["case_id"] for x in cases}) == 128
    rows = []
    for case in cases:
        authority = case["authority"]
        app = flask.Flask("run446_real_cookie_probe")
        app.secret_key = "run446-isolated-fixed-test-only"
        @app.get("/")
        def index():
            return str(flask.session.get("value"))
        client = app.test_client()
        base_url = "http://" + authority + "/"
        record = {"case_id": case["case_id"], "family": case["family"],
                  "authority": authority, "variant": variant, "base_url": base_url,
                  "cookie_update_calls": []}
        original = client._update_cookies_from_response
        def trace_update(domain, path, headers):
            record["cookie_update_calls"].append({
                "domain": domain, "path": path, "set_cookie_count": len(headers),
                "headers_have_session": any("session=" in x for x in headers)})
            return original(domain, path, headers)
        client._update_cookies_from_response = trace_update
        try:
            with app.test_request_context(base_url=base_url) as ctx:
                host = ctx.request.host
                host_url = ctx.request.host_url
                record["request_host"] = host
                record["request_host_url"] = host_url
                record["old_extraction"] = host.partition(":")[0]
                record["new_extraction"] = urlsplit(host_url).hostname or "localhost"
                record["host_extractions_equal"] = (
                    record["old_extraction"] == record["new_extraction"])
            with client.session_transaction(base_url=base_url) as sess:
                sess["value"] = 42
            record["cookies_after_transaction"] = safe_cookies(client)
            response = client.get("/", base_url=base_url)
            record["response_text"] = response.get_data(as_text=True)
            record["response_status"] = response.status_code
            record["success"] = (
                record["response_text"] == "42" and response.status_code == 200)
            record["cookies_after_get"] = safe_cookies(client)
        except Exception as exc:
            record["error"] = type(exc).__name__ + ":" + str(exc)[:200]
            record["success"] = False
        rows.append(record)
    output_path = pathlib.Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    meta = {"variant": variant, "python": sys.version,
            "platform": platform.platform(),
            "flask_version": importlib.metadata.version("flask"),
            "werkzeug_version": importlib.metadata.version("werkzeug"),
            "cases_sha256": hashlib.sha256(cases_path.read_bytes()).hexdigest(),
            "observations": len(rows),
            "session_success": sum(x["success"] for x in rows),
            "unequal_host_extractions": sum(
                not x.get("host_extractions_equal", False) for x in rows),
            "port_zero": [
                {k: r.get(k) for k in (
                    "case_id", "request_host", "request_host_url", "old_extraction",
                    "new_extraction", "host_extractions_equal", "success",
                    "cookie_update_calls", "cookies_after_transaction",
                    "response_text", "error")}
                for r in rows
                if r["family"] == "dns_with_port" and r["authority"].endswith(":0")]}
    output_path.with_suffix(".meta.json").write_text(
        json.dumps(meta, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: meta[k] for k in (
        "variant", "observations", "session_success", "unequal_host_extractions")},
        sort_keys=True), flush=True)
    assert len(rows) == 128

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
