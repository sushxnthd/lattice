#!/usr/bin/env python3
"""Prospectively frozen Flask #5928 public API oracle; each case isolated."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from dataclasses import dataclass

@dataclass(frozen=True)
class Expectation:
    events: tuple[str, ...]
    errors: tuple[str, ...] = ()
    ordered: bool = True

CASES: dict[str, Expectation] = {
    "T01_request_one_error": Expectation(("c", "b", "a"), ("ValueError",)),
    "T02_request_two_errors": Expectation(("c", "b", "a"), ("RuntimeError", "ValueError")),
    "T03_app_one_error": Expectation(("c", "b", "a"), ("ValueError",)),
    "T04_app_two_errors": Expectation(("c", "b", "a"), ("RuntimeError", "ValueError")),
    "T05_request_callback_signal": Expectation(("callback", "signal"), ("ValueError", "RuntimeError"), False),
    "T06_app_callback_signal": Expectation(("callback", "signal"), ("ValueError", "RuntimeError"), False),
    "C01_request_clean": Expectation(("c", "b", "a")),
    "C02_app_clean": Expectation(("c", "b", "a")),
    "C03_request_exc_argument": Expectation(("ValueError",)),
    "C04_app_exc_argument": Expectation(("ValueError",)),
    "C05_nested_app_contexts": Expectation(("teardown", "teardown")),
    "C06_empty_request": Expectation(()),
}

def flatten_error_types(error: BaseException | None) -> list[str]:
    if error is None:
        return []
    if isinstance(error, BaseExceptionGroup):
        return [n for sub in error.exceptions for n in flatten_error_types(sub)]
    return [type(error).__name__]

def assess(case: str, events: list[str], errors: list[str]) -> dict:
    spec = CASES[case]
    observed_events = tuple(events)
    events_ok = observed_events == spec.events if spec.ordered else sorted(events) == sorted(spec.events)
    errors_ok = sorted(errors) == sorted(spec.errors)
    return {"case": case, "events": events, "errors": errors, "events_ok": events_ok,
            "errors_ok": errors_ok, "pass": events_ok and errors_ok}

def execute_one(case: str) -> dict:
    from flask import Flask, appcontext_tearing_down, request_tearing_down
    app = Flask("run363_oracle")
    events: list[str] = []
    mode = "request" if "request" in case or case == "C06_empty_request" else "app"
    if mode == "request":
        register = app.teardown_request
        context_factory = app.test_request_context
    else:
        register = app.teardown_appcontext
        context_factory = app.app_context
    if case in ("T01_request_one_error", "T02_request_two_errors", "T03_app_one_error",
                "T04_app_two_errors", "C01_request_clean", "C02_app_clean"):
        for name in ("a", "b", "c"):
            def callback(exc, name=name):
                events.append(name)
                if case.startswith("T") and name == "b":
                    raise ValueError("frozen b failure")
                if case in ("T02_request_two_errors", "T04_app_two_errors") and name == "c":
                    raise RuntimeError("frozen c failure")
            register(callback)
    elif case in ("T05_request_callback_signal", "T06_app_callback_signal"):
        def callback(exc):
            events.append("callback")
            raise ValueError("frozen callback failure")
        register(callback)
        signal = request_tearing_down if mode == "request" else appcontext_tearing_down
        def receiver(sender, **kwargs):
            events.append("signal")
            raise RuntimeError("frozen signal failure")
        signal.connect(receiver, app, weak=False)
    elif case in ("C03_request_exc_argument", "C04_app_exc_argument"):
        def callback(exc):
            events.append(type(exc).__name__ if exc is not None else "None")
        register(callback)
    elif case == "C05_nested_app_contexts":
        def callback(exc):
            events.append("teardown")
        register(callback)
    error: BaseException | None = None
    try:
        if case == "C05_nested_app_contexts":
            with app.app_context():
                with app.app_context():
                    pass
        else:
            ctx = context_factory()
            ctx.push()
            passed_exc = ValueError("frozen view failure") if case in ("C03_request_exc_argument", "C04_app_exc_argument") else None
            ctx.pop(passed_exc)
    except BaseException as exc:
        error = exc
    return assess(case, events, flatten_error_types(error))

def run_all() -> dict:
    results = []
    for case in CASES:
        p = subprocess.run([sys.executable, __file__, "--case", case], capture_output=True, text=True, timeout=25)
        if p.returncode != 0:
            results.append({"case": case, "pass": False, "error": "SUBPROCESS_FAILURE",
                            "returncode": p.returncode, "stdout": p.stdout[-3000:], "stderr": p.stderr[-3000:]})
            continue
        try:
            row = json.loads(p.stdout)
            if row.get("case") != case:
                raise ValueError("case identity mismatch")
            results.append(row)
        except (ValueError, json.JSONDecodeError) as exc:
            results.append({"case": case, "pass": False, "error": "MALFORMED_OUTPUT", "detail": str(exc), "raw": p.stdout[-3000:]})
    return {"schema": "run363.flask.oracle.v1", "python": sys.version.split()[0], "results": results,
            "targets_pass": sum(r.get("pass", False) for r in results if r["case"].startswith("T")),
            "controls_pass": sum(r.get("pass", False) for r in results if r["case"].startswith("C"))}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES)
    args = parser.parse_args()
    print(json.dumps(execute_one(args.case) if args.case else run_all(), sort_keys=True))

if __name__ == "__main__":
    main()
