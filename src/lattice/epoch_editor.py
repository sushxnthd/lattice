"""Immutable epoch-addressed, scope-framed Boolean DAG transactions.

Experimental reference implementation. ``h<epoch>_<root>`` refers to the
immutable root from a *committed* epoch, not the latest mutable root. The
namespace is reserved in input/root names. Callers, not patches, grant scope.
Hashes are tamper-evident commitments, NOT signatures or authorization.
"""
from __future__ import annotations

import ast
import hashlib
import json
import keyword
import re
from dataclasses import dataclass
from typing import Mapping

from .framed_edits import BoundRule, FramedProgram
from .semantic_edits import InvalidProgram, expression

HIST = re.compile(r"^h(0|[1-9][0-9]*)_([A-Za-z_][A-Za-z_0-9]*)$")


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode()).hexdigest()


def state_commit(frame: FramedProgram) -> str:
    """Transitive content commitments, independent of unused historical nodes."""
    identities: list[str] = []
    for node in frame.nodes:
        deps = [(name, identities[idx]) for name, idx in node.bindings]
        identities.append(digest(["lattice.node.v1", node.source, sorted(deps)]))
    return digest(["lattice.state.v1", list(frame.inputs),
                   [(name, identities[idx]) for name, idx in frame.roots]])


@dataclass(frozen=True)
class EpochRecord:
    number: int
    prior: str | None
    state: str
    authority: tuple[str, ...]
    root_ids: tuple[tuple[str, int], ...]
    history: str


class EpochConflict(InvalidProgram):
    """Stale transaction, invalid historical address, or inconsistent history."""


class EpochEditor:
    def __init__(self, initial: FramedProgram):
        names = set(initial.inputs) | {name for name, _ in initial.roots}
        if any(HIST.fullmatch(name) for name in names):
            raise EpochConflict("historical namespace reserved in initial schema")
        state = state_commit(initial)
        roots = tuple(initial.roots)
        genesis = digest(["lattice.epoch.v1", 0, None, state, [], roots])
        self._frames: list[FramedProgram] = [initial]
        self._records: list[EpochRecord] = [EpochRecord(0, None, state, (), roots, genesis)]

    @property
    def tip(self) -> str:
        return self._records[-1].history

    @property
    def records(self) -> tuple[EpochRecord, ...]:
        return tuple(self._records)

    @property
    def current(self) -> FramedProgram:
        return self._frames[-1]

    def at(self, epoch: int) -> FramedProgram:
        if type(epoch) is not int or not 0 <= epoch < len(self._frames):
            raise EpochConflict("unknown epoch")
        return self._frames[epoch]

    def _historical_id(self, ref: str) -> int | None:
        match = HIST.fullmatch(ref)
        if match is None:
            return None
        epoch = int(match.group(1))
        root = match.group(2)
        if epoch >= len(self._frames):
            raise EpochConflict("forward or unknown epoch")
        ids = dict(self._frames[epoch].roots)
        if root not in ids:
            raise EpochConflict("unknown historical root")
        return ids[root]

    def edit(self, replacements: Mapping[str, str], allowed_outputs: set[str],
             expected_tip: str) -> EpochRecord:
        """CAS transaction; changes are atomic if validation succeeds.

        Every root in trusted ``allowed_outputs`` is recompiled (including
        unchanged descendants) so current references bind to new versions.
        Historical names bind directly to the referenced epoch's node ID.
        """
        if expected_tip != self.tip:
            raise EpochConflict("stale history tip")
        before = self.current
        old = dict(before.roots)
        allowed = set(allowed_outputs)
        replacements = dict(replacements)
        if not replacements or not allowed or not set(replacements) <= allowed <= set(old):
            raise InvalidProgram("invalid trusted edit scope")
        if any(type(k) is not str or type(v) is not str for k, v in replacements.items()):
            raise InvalidProgram("patch keys and expressions must be strings")
        sources = dict(before.sources)
        sources.update(replacements)
        dependencies: dict[str, set[str]] = {}
        history_bindings: dict[str, dict[str, int]] = {}
        for root in allowed:
            refs = {n.id for n in ast.walk(expression(sources[root])) if isinstance(n, ast.Name)}
            historical = {}
            for ref in refs:
                historical_id = self._historical_id(ref)
                if historical_id is not None:
                    historical[ref] = historical_id
            current = refs - set(historical)
            if not current <= set(before.inputs) | set(old):
                raise InvalidProgram("unknown reference")
            dependencies[root] = current
            history_bindings[root] = historical
        nodes = list(before.nodes)
        ids = {root: idx for root, idx in before.roots if root not in allowed}
        pending = set(allowed)
        done = set(before.inputs) | set(ids)
        while pending:
            ready = sorted(root for root in pending if dependencies[root] <= done)
            if not ready:
                raise InvalidProgram("cycle among authorized output versions")
            for root in ready:
                bindings = dict(history_bindings[root])
                bindings.update((ref, ids[ref]) for ref in dependencies[root] if ref in ids)
                nodes.append(BoundRule(sources[root], tuple(sorted(bindings.items()))))
                ids[root] = len(nodes) - 1
                done.add(root)
                pending.remove(root)
        after = FramedProgram(before.inputs, tuple(nodes),
                              tuple((name, ids[name]) for name, _ in before.roots),
                              tuple((name, sources[name]) for name, _ in before.sources))
        for name, idx in before.roots:
            if name not in allowed and dict(after.roots)[name] != idx:
                raise EpochConflict("protected root rebound")
        state = state_commit(after)
        number = len(self._records)
        authority = tuple(sorted(allowed))
        roots = tuple(after.roots)
        prior = self.tip
        history = digest(["lattice.epoch.v1", number, prior, state, authority, roots])
        record = EpochRecord(number, prior, state, authority, roots, history)
        # Publish both only after all validation and digest computations finish.
        self._frames.append(after)
        self._records.append(record)
        return record

    def verify(self, pinned_genesis: str | None = None, pinned_tip: str | None = None) -> bool:
        """Verify the local append-only history against optional external pins.

        Without an externally trusted pin/signature, a fully rewritten valid
        history is not distinguishable from an authentic one.
        """
        if not self._records or len(self._frames) != len(self._records):
            return False
        if pinned_genesis is not None and self._records[0].history != pinned_genesis:
            return False
        if pinned_tip is not None and self.tip != pinned_tip:
            return False
        for i, (frame, record) in enumerate(zip(self._frames, self._records)):
            prior = self._records[i - 1].history if i else None
            if record.number != i or record.prior != prior:
                return False
            if record.state != state_commit(frame) or record.root_ids != frame.roots:
                return False
            if record.history != digest(["lattice.epoch.v1", i, prior,
                                         record.state, list(record.authority),
                                         record.root_ids]):
                return False
            if i:
                old = self._frames[i - 1]
                if frame.inputs != old.inputs or tuple(k for k, _ in frame.roots) != tuple(k for k, _ in old.roots):
                    return False
                if frame.nodes[:len(old.nodes)] != old.nodes or len(frame.nodes) <= len(old.nodes):
                    return False
                allowed = set(record.authority)
                if not allowed or not allowed <= set(dict(old.roots)):
                    return False
                if any(dict(frame.roots)[name] != idx for name, idx in old.roots if name not in allowed):
                    return False
        return True
