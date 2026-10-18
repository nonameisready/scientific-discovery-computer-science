#!/usr/bin/env python3
"""Sweep repeated bandwidth changes and urgent-arrival intensity."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from stress_simulator import StressEngine, StressSession


SCHEDULES = {
    "single_drop": {2: 50},
    "drop_recover": {2: 50, 8: 800},
    "double_drop": {2: 50, 8: 400, 12: 50},
    "oscillating": {2: 50, 6: 400, 10: 50, 14: 800},
}
URGENT_COUNTS = (1, 3, 5)
SEEDS = (20261017, 20261018, 20261019)


def trace(seed: int, urgent_count: int) -> list[StressSession]:
    sessions = [StressSession(seed, 0, 30, f"long-{seed}", 3200, 3200, 0,
                              forecast_return_ticks=16)]
    for i in range(urgent_count):
        tokens = 400 + 200 * (i % 3)
        sessions.append(StressSession(
            seed + i + 1, 4 + i, 3 + (i % 2), f"urgent-{seed}-{i}",
            tokens, tokens, i % 2, forecast_return_ticks=8,
        ))
    return sessions


def main() -> None:
    rows = []
    for seed in SEEDS:
        for urgent_count in URGENT_COUNTS:
            for schedule_name, schedule in SCHEDULES.items():
                for policy in ("queue_aware", "budget_aware", "fallback_aware", "unified_aware"):
                    metrics = StressEngine(
                        policy,
                        gpu_tokens=4000,
                        cpu_tokens=4000,
                        remote_tokens=8000,
                        bandwidth=800,
                        bandwidth_schedule=schedule,
                    ).run(trace(seed, urgent_count))
                    rows.append({
                        "seed": seed,
                        "urgent_count": urgent_count,
                        "schedule": schedule_name,
                        "policy": policy,
                        **metrics,
                    })
    result = {
        "protocol": "MULTI-TIER-BANDWIDTH-FLUCTUATION-v1",
        "schedules": SCHEDULES,
        "urgent_counts": list(URGENT_COUNTS),
        "seeds": list(SEEDS),
        "rows": rows,
    }
    out = Path(__file__).parents[1] / "results" / "bandwidth_fluctuation_sweep.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
