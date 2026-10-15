"""Independent oracle integration marker."""

from __future__ import annotations

ORACLE_VERSION = 1


def bool_literal(value: str) -> bool:
    return value == 'True'
