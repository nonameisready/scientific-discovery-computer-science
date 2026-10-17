"""Prespecified CPU trace matrix. All outputs are TRACE_SIMULATED."""
import json

from .reference_controller import ControllerConfig
from .trace_harness import AcceptanceAdaptive, FixedDepth, RASPPolicy, SLOPriority, TraceRequest, run_trace


def make_trace(name):
    if name == "low_pressure":
        return [TraceRequest(f"r{i}", i, 3, .95, 30) for i in range(4)]
    if name == "severe_pressure":
        return [TraceRequest("short", 0, 3, .9, 8), TraceRequest("long", 0, 20, .25, 20), TraceRequest("mid", 0, 8, .6, 15)]
    if name == "burst":
        return [TraceRequest(f"b{i}", 0, 6 + i, .5, 18) for i in range(8)]
    if name == "low_acceptance":
        return [TraceRequest(f"l{i}", i % 2, 8, .1, 20) for i in range(6)]
    if name == "reusable_prefix":
        return [TraceRequest(f"p{i}", i, 5, .8, 20, "shared", 6, 3.0) for i in range(6)]
    if name == "wrong_prefix_value":
        return [TraceRequest(f"w{i}", i, 5, .8, 20, "unique", 6, 3.0) for i in range(6)]
    if name == "strict_slo":
        return [TraceRequest(f"s{i}", i, 5, .7, 5 + i * 2) for i in range(6)]
    if name == "starvation":
        return [TraceRequest("old", 0, 18, .2, 40)] + [TraceRequest(f"new{i}", i + 1, 2, .95, 12) for i in range(8)]
    raise ValueError(name)


def policies():
    return [
        FixedDepth(4, 24, 8),
        AcceptanceAdaptive(4, .5, 24, 8),
        SLOPriority(4, 24, 8),
        RASPPolicy(ControllerConfig(capacity_bytes=24, reserve_bytes=2, max_batch_tokens=8)),
    ]


def main():
    scenarios = ["low_pressure", "severe_pressure", "burst", "low_acceptance",
                 "reusable_prefix", "wrong_prefix_value", "strict_slo", "starvation"]
    rows = []
    for scenario in scenarios:
        for policy in policies():
            m = run_trace(make_trace(scenario), policy, capacity=24, batch=8)
            rows.append({"scenario": scenario, **m.__dict__})
    print(json.dumps({"evidence_level": "TRACE_SIMULATED", "seed": 20261017,
                      "capacity": 24, "batch": 8, "rows": rows}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
