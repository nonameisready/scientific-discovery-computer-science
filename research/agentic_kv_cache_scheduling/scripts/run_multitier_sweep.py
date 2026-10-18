#!/usr/bin/env python3
"""Run the frozen CPU-only multi-tier migration sweep."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from stress_simulator import StressEngine, StressSession


SEEDS = (20261017, 20261018, 20261019)
BANDWIDTHS = (50, 100, 200, 400, 800)
POLICIES = ("lru", "ttl", "proposed", "tier_aware", "cost_aware")


def sessions(seed: int) -> list[StressSession]:
    rng = random.Random(seed)
    output = []
    for i in range(16):
        duration = rng.choice((1, 3, 8, 20))
        exact = rng.choice((400, 800, 1200))
        forecast = max(100, min(1400, exact + rng.choice((-400, -100, 0, 100))))
        output.append(StressSession(
            sid=i,
            start=i // 2,
            duration=duration,
            prefix_group="shared" if i % 3 == 0 else f"g{seed}-{i}",
            exact_tokens=exact,
            forecast_tokens=forecast,
            worker=i % 2,
            branch=i % 2,
            cancelled=(i == 7),
            revisions=((2, 100),) if i == 5 else (),
            forecast_return_ticks=8,
            prefix_survival_probability=.75,
        ))
    return output


def main() -> None:
    rows = []
    for seed in SEEDS:
        trace = sessions(seed)
        for bandwidth in BANDWIDTHS:
            for policy in POLICIES:
                metrics = StressEngine(
                    policy,
                    gpu_tokens=1600,
                    cpu_tokens=3200,
                    remote_tokens=6400,
                    bandwidth=bandwidth,
                ).run(trace)
                rows.append({
                    "seed": seed,
                    "bandwidth_tokens_per_tick": bandwidth,
                    "policy": policy,
                    **metrics,
                })
    result = {
        "protocol": "MULTI-TIER-MIGRATION-CPU-SWEEP-v1",
        "seeds": list(SEEDS),
        "bandwidths": list(BANDWIDTHS),
        "policies": list(POLICIES),
        "capacity_tokens": {"gpu": 1600, "cpu": 3200, "remote": 6400},
        "rows": rows,
    }
    out = Path(__file__).parents[1] / "results" / "multitier_bandwidth_sweep.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
