#!/usr/bin/env python3
"""Find the capacity/bandwidth regime where migration can beat TTL."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from stress_simulator import StressEngine
from run_stochastic_bandwidth_sweep import SEEDS, make_trace, POLICIES


GPU_CAPACITIES = (600, 1000, 1600, 2400)
BANDWIDTHS = (50, 100, 200, 400)


def main() -> None:
    rows = []
    for gpu_tokens in GPU_CAPACITIES:
        for bandwidth in BANDWIDTHS:
            for seed in SEEDS:
                sessions, schedule = make_trace(seed)
                # The pressure protocol replaces the random initial bandwidth
                # with a fixed regime while retaining each paired trace's
                # arrivals and exact/forecast mismatch.
                schedule = {0: bandwidth}
                for policy in POLICIES:
                    metrics = StressEngine(
                        policy,
                        gpu_tokens=gpu_tokens,
                        cpu_tokens=4000,
                        remote_tokens=8000,
                        bandwidth=bandwidth,
                        bandwidth_schedule=schedule,
                    ).run(sessions)
                    rows.append({
                        "gpu_tokens": gpu_tokens,
                        "bandwidth": bandwidth,
                        "seed": seed,
                        "policy": policy,
                        **metrics,
                    })

    cells = []
    for gpu_tokens in GPU_CAPACITIES:
        for bandwidth in BANDWIDTHS:
            cell = {"gpu_tokens": gpu_tokens, "bandwidth": bandwidth}
            for policy in POLICIES:
                group = [r for r in rows if r["gpu_tokens"] == gpu_tokens
                         and r["bandwidth"] == bandwidth and r["policy"] == policy]
                cell[policy] = {
                    "mean_ttft": statistics.mean(r["mean_ttft"] for r in group),
                    "mean_p95_ttft": statistics.mean(r["p95_ttft"] for r in group),
                    "mean_transfer_tokens": statistics.mean(r["transfer_tokens"] for r in group),
                    "mean_recompute_misses": statistics.mean(r["recompute_misses"] for r in group),
                }
            ttl = cell["ttl"]
            unified = cell["unified_aware"]
            cell["unified_beats_ttl_mean_ttft"] = unified["mean_ttft"] < ttl["mean_ttft"]
            cell["unified_beats_ttl_p95_ttft"] = unified["mean_p95_ttft"] < ttl["mean_p95_ttft"]
            cells.append(cell)

    result = {
        "protocol": "MULTI-TIER-CAPACITY-PRESSURE-v1",
        "question": "Does migration beat TTL when GPU retention capacity is deliberately insufficient?",
        "falsification_gate": "A promising regime must improve both mean and mean-P95 TTFT against TTL on the same paired traces; isolated traffic savings are not sufficient.",
        "gpu_capacities": list(GPU_CAPACITIES),
        "bandwidths": list(BANDWIDTHS),
        "seeds": list(SEEDS),
        "cells": cells,
        "rows": rows,
    }
    out = Path(__file__).parents[1] / "results" / "capacity_pressure_sweep.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    hits = [c for c in cells if c["unified_beats_ttl_mean_ttft"] and c["unified_beats_ttl_p95_ttft"]]
    print(json.dumps({"protocol": result["protocol"], "cells": len(cells),
                      "unified_beats_ttl_on_both_latency_metrics": len(hits),
                      "hits": [(c["gpu_tokens"], c["bandwidth"]) for c in hits]}, indent=2))


if __name__ == "__main__":
    main()
