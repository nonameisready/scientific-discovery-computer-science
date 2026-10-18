#!/usr/bin/env python3
"""Compare queue policies under a mid-flight bandwidth shock and urgent arrival."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from stress_simulator import StressEngine, StressSession


def trace(seed: int) -> list[StressSession]:
    return [
        StressSession(seed, 0, 30, f"long-{seed}", 3200, 3200, 0,
                      forecast_return_ticks=16),
        StressSession(seed + 1, 4, 3, f"urgent-{seed}", 400, 400, 0,
                      forecast_return_ticks=8),
        StressSession(seed + 2, 5, 8, f"urgent2-{seed}", 800, 800, 1,
                      forecast_return_ticks=8),
    ]


def main() -> None:
    rows = []
    for seed in (20261017, 20261018, 20261019):
        for policy in ("queue_aware", "budget_aware"):
            metrics = StressEngine(
                policy,
                gpu_tokens=4000,
                cpu_tokens=4000,
                remote_tokens=8000,
                bandwidth=800,
                bandwidth_schedule={2: 50},
            ).run(trace(seed))
            rows.append({"seed": seed, "policy": policy, **metrics})
    result = {
        "protocol": "MULTI-TIER-BANDWIDTH-SHOCK-v1",
        "bandwidth_schedule": {"0": 800, "2": 50},
        "urgent_arrivals": [4, 5],
        "rows": rows,
    }
    out = Path(__file__).parents[1] / "results" / "bandwidth_shock.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
