#!/usr/bin/env python3
"""Vary GPU capacity, bandwidth, and return window for migration boundaries."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from stress_simulator import StressEngine, StressSession


SEEDS = (20261017, 20261018, 20261019)
BANDWIDTHS = (50, 200, 800)
GPU_CAPACITIES = (800, 1600, 3200)
RETURN_WINDOWS = (2, 8, 16)
POLICIES = ("lru", "ttl", "proposed", "tier_aware", "cost_aware", "queue_aware")


def sessions(seed: int, return_window: int) -> list[StressSession]:
    rng = random.Random(seed)
    output = []
    for i in range(16):
        exact = rng.choice((400, 800, 1200))
        output.append(StressSession(
            sid=i,
            start=i // 2,
            duration=rng.choice((1, 3, 8, 20)),
            prefix_group="shared" if i % 3 == 0 else f"g{seed}-{i}",
            exact_tokens=exact,
            forecast_tokens=max(100, min(1400, exact + rng.choice((-400, -100, 0, 100)))),
            worker=i % 2,
            branch=i % 2,
            cancelled=(i == 7),
            revisions=((2, 100),) if i == 5 else (),
            forecast_return_ticks=return_window,
            prefix_survival_probability=.75,
        ))
    return output


def main() -> None:
    rows = []
    for seed in SEEDS:
        for return_window in RETURN_WINDOWS:
            trace = sessions(seed, return_window)
            for gpu_capacity in GPU_CAPACITIES:
                for bandwidth in BANDWIDTHS:
                    for policy in POLICIES:
                        metrics = StressEngine(
                            policy,
                            gpu_tokens=gpu_capacity,
                            cpu_tokens=3200,
                            remote_tokens=6400,
                            bandwidth=bandwidth,
                        ).run(trace)
                        rows.append({
                            "seed": seed,
                            "return_window": return_window,
                            "gpu_capacity_tokens": gpu_capacity,
                            "bandwidth_tokens_per_tick": bandwidth,
                            "policy": policy,
                            **metrics,
                        })
    result = {
        "protocol": "MULTI-TIER-MIGRATION-BOUNDARY-CPU-v1",
        "seeds": list(SEEDS),
        "bandwidths": list(BANDWIDTHS),
        "gpu_capacities": list(GPU_CAPACITIES),
        "return_windows": list(RETURN_WINDOWS),
        "policies": list(POLICIES),
        "rows": rows,
    }
    out = Path(__file__).parents[1] / "results" / "migration_boundary_sweep.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
