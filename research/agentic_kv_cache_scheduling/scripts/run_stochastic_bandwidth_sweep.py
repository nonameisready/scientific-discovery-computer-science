#!/usr/bin/env python3
"""Run a paired random-trace stress test for multi-tier KV migration policies."""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from stress_simulator import StressEngine, StressSession


POLICIES = ("ttl", "queue_aware", "budget_aware", "fallback_aware", "unified_aware")
SEEDS = tuple(range(2026101701, 2026101721))
HORIZON = 44


def make_trace(seed: int) -> tuple[list[StressSession], dict[int, int]]:
    rng = random.Random(seed)
    schedule = {0: rng.choice((400, 800, 1200))}
    for tick in range(2, HORIZON, 2):
        if rng.random() < 0.34:
            previous = schedule[max(schedule)]
            schedule[tick] = rng.choice((50, 100, 200, 400, 800, 1200))
            if schedule[tick] == previous:
                schedule[tick] = 50 if previous >= 400 else 800

    sessions = [StressSession(
        sid=seed,
        start=0,
        duration=rng.randint(18, 30),
        prefix_group=f"long-{seed}",
        exact_tokens=rng.choice((1600, 2400, 3200)),
        forecast_tokens=rng.choice((1600, 2400, 3200)),
        worker=0,
        forecast_return_ticks=rng.choice((8, 12, 16)),
        prefix_survival_probability=rng.choice((0.65, 0.75, 0.85, 0.95)),
    )]
    for i in range(rng.randint(3, 8)):
        start = rng.randint(2, HORIZON - 8)
        forecast = rng.choice((200, 400, 600, 800, 1000))
        exact = max(100, min(1200, forecast + rng.choice((-200, -100, 0, 0, 100))))
        duration = rng.randint(2, 8)
        sessions.append(StressSession(
            sid=seed + i + 1,
            start=start,
            duration=duration,
            prefix_group=f"urgent-{seed}-{i}",
            exact_tokens=exact,
            forecast_tokens=forecast,
            worker=rng.randrange(2),
            branch=int(rng.random() < 0.2),
            forecast_return_ticks=rng.choice((4, 6, 8)),
            prefix_survival_probability=rng.choice((0.55, 0.75, 0.95)),
        ))
    return sessions, schedule


def percentile(values: list[float], q: float) -> float:
    xs = sorted(values)
    if not xs:
        return 0.0
    return xs[max(0, min(len(xs) - 1, round(q * (len(xs) - 1))))]


def main() -> None:
    rows = []
    for seed in SEEDS:
        sessions, schedule = make_trace(seed)
        for policy in POLICIES:
            metrics = StressEngine(
                policy,
                gpu_tokens=4000,
                cpu_tokens=4000,
                remote_tokens=8000,
                bandwidth=800,
                bandwidth_schedule=schedule,
            ).run(sessions)
            rows.append({"seed": seed, "policy": policy, "schedule": schedule, **metrics})

    aggregate = {}
    for policy in POLICIES:
        group = [row for row in rows if row["policy"] == policy]
        aggregate[policy] = {
            "traces": len(group),
            "mean_ttft": statistics.mean(row["mean_ttft"] for row in group),
            "p95_trace_mean_ttft": percentile([row["mean_ttft"] for row in group], 0.95),
            "mean_p95_ttft": statistics.mean(row["p95_ttft"] for row in group),
            "p95_trace_p95_ttft": percentile([row["p95_ttft"] for row in group], 0.95),
            "mean_transfer_tokens": statistics.mean(row["transfer_tokens"] for row in group),
            "mean_recompute_misses": statistics.mean(row["recompute_misses"] for row in group),
            "mean_cancelled_transfer_tokens": statistics.mean(row["cancelled_transfer_tokens"] for row in group),
            "mean_fallback_demotions": statistics.mean(row["fallback_demotions"] for row in group),
        }

    result = {
        "protocol": "MULTI-TIER-STOCHASTIC-BANDWIDTH-v1",
        "hypothesis": "unified_aware is a stable compromise under paired random bandwidth and arrival traces",
        "falsification_gate": "Reject stability if unified_aware is not within 10% of the best policy on both mean TTFT and P95 TTFT, or if it is not within 10% of the lowest transfer traffic.",
        "policies": list(POLICIES),
        "seeds": list(SEEDS),
        "horizon": HORIZON,
        "aggregate": aggregate,
        "rows": rows,
    }
    out = Path(__file__).parents[1] / "results" / "stochastic_bandwidth_sweep.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"protocol": result["protocol"], "seeds": len(SEEDS), "aggregate": aggregate}, indent=2))


if __name__ == "__main__":
    main()
