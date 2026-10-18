#!/usr/bin/env python3
"""Exercise the event validator with valid and intentionally invalid traces."""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from event_logger import EventLog


def base(event: str, timestamp: int, generation: int = 1, **extra):
    return {"schema": "agentic-kv/events/v1", "event": event,
            "timestamp_ms": timestamp, "session_id": "s1",
            "generation": generation, **extra}


def transfer(event: str, timestamp: int, generation: int = 1, transfer_id: str = "t1"):
    return base(event, timestamp, generation, transfer_id=transfer_id,
                source="remote", destination="gpu", bytes=1024)


def run_case(events, expected_ok: bool):
    log = EventLog()
    log.extend(events)
    audit = log.audit().as_dict()
    if audit["ok"] != expected_ok:
        raise AssertionError(f"unexpected audit result: {audit}")
    return audit


def main() -> None:
    cases = {
        "complete": run_case([
            base("request_start", 0, priority="urgent"),
            transfer("transfer_enqueue", 1),
            transfer("transfer_start", 2),
            transfer("transfer_complete", 5),
            base("ttft_breakdown", 6, queue_wait_ms=1, load_back_wait_ms=3,
                 compute_ms=2, fallback_ms=0),
            base("request_return", 7),
        ], True),
        "cancelled": run_case([
            transfer("transfer_enqueue", 1),
            transfer("transfer_start", 2),
            transfer("transfer_cancel", 3),
        ], True),
        "stale_generation": run_case([
            transfer("transfer_enqueue", 1, generation=1),
            transfer("transfer_cancel", 3, generation=2),
        ], False),
        "unfinished": run_case([
            transfer("transfer_enqueue", 1),
        ], False),
    }
    result = {"protocol": "KV-EVENT-LOG-SMOKE-v1", "cases": cases,
              "all_expected": True}
    out = Path(__file__).parents[1] / "results" / "event_log_smoke.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
