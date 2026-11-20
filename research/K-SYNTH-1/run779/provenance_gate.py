"""Fail-closed release approval boundary (Run779); standard library only.

The approval must be provided by an independently trusted caller, not read from
the wheel or the CI producer's generated digest.
"""
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

HEX = re.compile(r'[0-9a-f]{64}\Z')
SHA = re.compile(r'[0-9a-f]{40}\Z')

@dataclass(frozen=True)
class Approval:
    source_commit: str
    wheel_sha256: str
    trusted_channel: str

def verify(wheel: Path, approval: Approval, source_commit: str,
           trusted_channels=frozenset({'independent-release-approval'})) -> str:
    if approval.trusted_channel not in trusted_channels:
        raise ValueError('UNKNOWN: approval channel not independently trusted')
    if not SHA.fullmatch(approval.source_commit) or not SHA.fullmatch(source_commit):
        raise ValueError('UNKNOWN: invalid source commit')
    if approval.source_commit != source_commit:
        raise ValueError('UNKNOWN: source commit mismatch')
    if not HEX.fullmatch(approval.wheel_sha256):
        raise ValueError('UNKNOWN: malformed approved digest')
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    if digest != approval.wheel_sha256:
        raise ValueError('UNKNOWN: artifact digest mismatch')
    return digest
