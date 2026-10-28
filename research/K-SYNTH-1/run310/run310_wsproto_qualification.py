#!/usr/bin/env python3
"""Frozen Run310 wsproto PR #6 historical public API oracle. Trusted tests only."""
import hashlib
import json
import os
import sys
import traceback

sys.path.insert(0, os.getcwd())
from wsproto.connection import WSConnection, SERVER
from wsproto.events import ConnectionRequested, ConnectionFailed

KEY = b"dGhlIHNhbXBsZSBub25jZQ=="
def request(extra=(), method=b"GET", connection=b"Upgrade", upgrade=b"WebSocket", version=True):
    lines = [
        method + b" /chat HTTP/1.1",
        b"Host: example.org",
        b"Connection: " + connection,
        b"Upgrade: " + upgrade,
    ]
    if version:
        lines.append(b"Sec-WebSocket-Version: 13")
    lines.append(b"Sec-WebSocket-Key: " + KEY)
    lines.extend(extra)
    return b"\r\n".join(lines) + b"\r\n\r\n"

def handshake(extra=(), **kwargs):
    ws = WSConnection(SERVER)
    ws.receive_bytes(request(extra, **kwargs))
    return ws, next(ws.events())

def public_single():
    ws, event = handshake([b"Sec-WebSocket-Protocol: chat"])
    return isinstance(event, ConnectionRequested) and event.proposed_subprotocols == [b"chat"]

def public_duplicate():
    ws, event = handshake([b"Sec-WebSocket-Protocol: chat", b"Sec-WebSocket-Protocol: superchat"])
    return isinstance(event, ConnectionRequested) and event.proposed_subprotocols == [b"chat", b"superchat"]

def public_accept():
    ws, event = handshake([b"Sec-WebSocket-Protocol: chat"])
    ws.accept(event, subprotocol=b"chat")
    return b"sec-websocket-protocol: chat" in ws.bytes_to_send().lower()

def heldout_reject_unoffered():
    ws, event = handshake([b"Sec-WebSocket-Protocol: chat"])
    try:
        ws.accept(event, subprotocol=b"unoffered")
    except ValueError:
        return True
    return False

def heldout_select_second():
    ws, event = handshake([b"Sec-WebSocket-Protocol: chat", b"Sec-WebSocket-Protocol: superchat"])
    ws.accept(event, subprotocol=b"superchat")
    return b"sec-websocket-protocol: superchat" in ws.bytes_to_send().lower()

def control_no_protocol():
    ws, event = handshake()
    return isinstance(event, ConnectionRequested)

def control_accept_default():
    ws, event = handshake()
    ws.accept(event)
    response = ws.bytes_to_send().lower()
    return b"101 switching protocols" in response and b"sec-websocket-protocol:" not in response

def control_bad_connection():
    ws, event = handshake(connection=b"Wrong")
    return isinstance(event, ConnectionFailed)

def control_bad_upgrade():
    ws, event = handshake(upgrade=b"Wrong")
    return isinstance(event, ConnectionFailed)

def control_missing_version():
    ws, event = handshake(version=False)
    return isinstance(event, ConnectionFailed)

def control_wrong_method():
    ws, event = handshake(method=b"POST")
    return isinstance(event, ConnectionFailed)

TESTS = [
    ("PUBLIC", "single_protocol", public_single),
    ("PUBLIC", "duplicate_protocol", public_duplicate),
    ("PUBLIC", "accept_selected", public_accept),
    ("HELDOUT", "reject_unoffered", heldout_reject_unoffered),
    ("HELDOUT", "select_second", heldout_select_second),
    ("CONTROL", "no_protocol", control_no_protocol),
    ("CONTROL", "accept_default", control_accept_default),
    ("CONTROL", "bad_connection", control_bad_connection),
    ("CONTROL", "bad_upgrade", control_bad_upgrade),
    ("CONTROL", "missing_version", control_missing_version),
    ("CONTROL", "wrong_method", control_wrong_method),
]
results = []
for group, name, fn in TESTS:
    try:
        passed = bool(fn())
        error = None
    except Exception as exc:
        passed = False
        error = type(exc).__name__ + ": " + str(exc)
    results.append({"group": group, "name": name, "passed": passed, "error": error})
summary = {
    "schema": "run310-wsproto-pr6-v1",
    "arm": os.environ.get("RUN310_ARM", "unknown"),
    "runtime": sys.version,
    "results": results,
    "passed": sum(row["passed"] for row in results),
    "total": len(results),
}
with open("run310_wsproto_results.json", "w") as f:
    json.dump(summary, f, indent=2, sort_keys=True)
    f.write("\n")
print(json.dumps(summary, sort_keys=True))
