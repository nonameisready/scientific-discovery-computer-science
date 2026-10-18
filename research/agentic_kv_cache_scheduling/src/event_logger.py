"""Engine-neutral event log validator for KV-cache experiments."""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, Iterable

TRANSFER_EVENTS = {"transfer_enqueue", "transfer_start", "transfer_complete", "transfer_cancel"}
TERMINAL_TRANSFER_EVENTS = {"transfer_complete", "transfer_cancel"}


def validate_event(event: Dict[str, Any]) -> None:
    required = {"schema", "event", "timestamp_ms", "session_id", "generation"}
    missing = required - event.keys()
    if missing:
        raise ValueError(f"missing event fields: {sorted(missing)}")
    if event["schema"] != "agentic-kv/events/v1":
        raise ValueError("unsupported event schema")
    if int(event["timestamp_ms"]) < 0 or int(event["generation"]) < 0:
        raise ValueError("timestamp and generation must be non-negative")
    if event["event"] in TRANSFER_EVENTS:
        for key in ("transfer_id", "source", "destination"):
            if not event.get(key):
                raise ValueError(f"transfer event missing {key}")
        if int(event.get("bytes", 0)) < 0:
            raise ValueError("transfer bytes must be non-negative")


@dataclass
class EventAudit:
    errors: list[str] = field(default_factory=list)
    transfer_count: int = 0
    completed_transfers: int = 0
    cancelled_transfers: int = 0

    def as_dict(self) -> Dict[str, Any]:
        return {"ok": not self.errors, "errors": list(self.errors),
                "transfer_count": self.transfer_count,
                "completed_transfers": self.completed_transfers,
                "cancelled_transfers": self.cancelled_transfers}


class EventLog:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else None
        self._events: list[Dict[str, Any]] = []

    def append(self, event: Dict[str, Any]) -> None:
        validate_event(event)
        if self._events and int(event["timestamp_ms"]) < int(self._events[-1]["timestamp_ms"]):
            raise ValueError("event timestamps must be non-decreasing")
        self._events.append(dict(event))
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, sort_keys=True) + "\n")

    def extend(self, events: Iterable[Dict[str, Any]]) -> None:
        for event in events:
            self.append(event)

    def events(self) -> list[Dict[str, Any]]:
        return list(self._events)

    def audit(self) -> EventAudit:
        result = EventAudit()
        transfers: Dict[str, Dict[str, Any]] = {}
        last_generation: Dict[str, int] = {}
        for event in self._events:
            session = str(event["session_id"])
            generation = int(event["generation"])
            if generation < last_generation.get(session, generation):
                result.errors.append(f"generation regressed for session {session}")
            last_generation[session] = max(last_generation.get(session, generation), generation)
            if event["event"] == "transfer_enqueue":
                transfer_id = str(event["transfer_id"])
                if transfer_id in transfers:
                    result.errors.append(f"duplicate transfer enqueue: {transfer_id}")
                else:
                    transfers[transfer_id] = event
                    result.transfer_count += 1
            elif event["event"] in TERMINAL_TRANSFER_EVENTS:
                transfer_id = str(event["transfer_id"])
                original = transfers.get(transfer_id)
                if original is None:
                    result.errors.append(f"terminal event without enqueue: {transfer_id}")
                    continue
                if generation != int(original["generation"]):
                    result.errors.append(f"stale transfer generation: {transfer_id}")
                if event["event"] == "transfer_complete":
                    result.completed_transfers += 1
                else:
                    result.cancelled_transfers += 1
                del transfers[transfer_id]
        for transfer_id in sorted(transfers):
            result.errors.append(f"unfinished transfer: {transfer_id}")
        return result
