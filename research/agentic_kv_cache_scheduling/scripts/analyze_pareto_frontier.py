#!/usr/bin/env python3
"""Compute per-trace Pareto frontiers for migration policies."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]
INPUT = ROOT / "results" / "bandwidth_fluctuation_sweep.json"
OUTPUT = ROOT / "results" / "migration_pareto_frontier.json"
METRICS = ("mean_ttft", "transfer_tokens", "recompute_misses")


def dominates(a: dict, b: dict) -> bool:
    no_worse = all(a[m] <= b[m] for m in METRICS)
    strictly_better = any(a[m] < b[m] for m in METRICS)
    return no_worse and strictly_better


def main() -> None:
    rows = json.loads(INPUT.read_text(encoding="utf-8"))["rows"]
    grouped = defaultdict(list)
    for row in rows:
        key = (row["seed"], row["schedule"], row["urgent_count"])
        grouped[key].append(row)

    frontiers = []
    frontier_counts = Counter()
    for key, candidates in sorted(grouped.items()):
        frontier = [
            row for row in candidates
            if not any(dominates(other, row) for other in candidates if other is not row)
        ]
        for row in frontier:
            frontier_counts[row["policy"]] += 1
        frontiers.append({
            "seed": key[0],
            "schedule": key[1],
            "urgent_count": key[2],
            "policies": [
                {"policy": row["policy"], **{m: row[m] for m in METRICS}}
                for row in sorted(frontier, key=lambda x: (x["mean_ttft"], x["policy"]))
            ],
        })

    result = {
        "protocol": "MULTI-TIER-PARETO-FRONTIER-v1",
        "metrics_minimized": list(METRICS),
        "unit": "one fixed seed x bandwidth schedule x urgent-arrival count",
        "frontier_counts": dict(sorted(frontier_counts.items())),
        "frontiers": frontiers,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "frontiers"}, indent=2))


if __name__ == "__main__":
    main()
