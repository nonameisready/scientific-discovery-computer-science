"""Deterministic CPU trace harness; outputs are TRACE_SIMULATED, not GPU data."""
from dataclasses import dataclass, replace
from typing import Dict, Iterable, List, Protocol

from .reference_controller import ControllerConfig, Decision, RequestState, ShadowPriceController


@dataclass(frozen=True)
class TraceRequest:
    request_id: str
    arrival: int
    output_tokens: int
    acceptance: float
    deadline: int
    prefix_key: str = ""
    prefix_tokens: int = 0
    prefix_value: float = 0.0


@dataclass
class RuntimeRequest:
    spec: TraceRequest
    remaining: int
    kv_tokens: int
    admitted_at: int
    last_tick: int


@dataclass(frozen=True)
class TraceMetrics:
    policy: str
    completed: int
    goodput: int
    p95_latency: float
    deadline_misses: int
    starvation_events: int
    peak_bytes: int
    evictions: int
    recompute_tokens: int
    accepted_tokens: int
    speculative_tokens: int


class Policy(Protocol):
    name: str

    def choose(self, requests: List[RequestState], used_bytes: int) -> List[Decision]: ...

    def feedback(self, pressure: float, evictions: int, recompute_tokens: int) -> None: ...


class FixedDepth:
    def __init__(self, depth: int, capacity: int, batch: int):
        self.depth, self.capacity, self.batch = depth, capacity, batch
        self.name = f"fixed-{depth}"

    def choose(self, requests, used_bytes):
        out, cur, budget = [], used_bytes, self.batch
        for r in requests:
            k = min(self.depth, r.max_spec_tokens)
            accepted = min(r.waiting_tokens, max(1, round(k * r.acceptance))) if k else 1
            peak = cur + k + accepted
            if k <= budget and peak <= self.capacity:
                out.append(Decision(r.request_id, True, k, 0.0, peak, accepted))
                cur, budget = peak, budget - k
        return out

    def feedback(self, pressure, evictions, recompute_tokens):
        return None


class AcceptanceAdaptive(FixedDepth):
    def __init__(self, depth: int, threshold: float, capacity: int, batch: int):
        super().__init__(depth, capacity, batch)
        self.threshold = threshold
        self.name = f"accept-adaptive-{depth}-{threshold}"

    def choose(self, requests, used_bytes):
        adjusted = [replace(r, max_spec_tokens=(r.max_spec_tokens if r.acceptance >= self.threshold else 0)) for r in requests]
        return super().choose(adjusted, used_bytes)


class MemoryOnly(FixedDepth):
    def __init__(self, depth: int, capacity: int, batch: int):
        super().__init__(depth, capacity, batch)
        self.name = "memory-only"


class SLOPriority(AcceptanceAdaptive):
    def __init__(self, depth: int, capacity: int, batch: int):
        super().__init__(depth, 0.0, capacity, batch)
        self.name = "slo-priority"

    def choose(self, requests, used_bytes):
        ordered = sorted(requests, key=lambda r: (r.slo_debt, -r.age, r.request_id), reverse=True)
        return super().choose(ordered, used_bytes)


class RASPPolicy:
    name = "rasp"

    def __init__(self, config: ControllerConfig):
        self.controller = ShadowPriceController(config)

    def choose(self, requests, used_bytes):
        return self.controller.decide(requests, used_bytes)

    def feedback(self, pressure, evictions, recompute_tokens):
        self.controller.update_feedback(pressure, evictions, recompute_tokens)


def run_trace(trace: Iterable[TraceRequest], policy: Policy, capacity: int = 32,
              batch: int = 16, max_ticks: int = 200) -> TraceMetrics:
    """Run a bounded event trace with no look-ahead into future arrivals."""
    arrivals = sorted(trace, key=lambda r: (r.arrival, r.request_id))
    waiting: List[TraceRequest] = []
    active: Dict[str, RuntimeRequest] = {}
    completed_latencies: List[int] = []
    peak = evictions = recompute = accepted_total = spec_total = misses = starvation = 0
    cache: Dict[str, int] = {}
    cache_bytes = 0
    for tick in range(max_ticks):
        waiting.extend(r for r in arrivals if r.arrival == tick)
        arrivals = [r for r in arrivals if r.arrival != tick]
        for r in list(waiting):
            prefix = 0 if r.prefix_key and r.prefix_key in cache else r.prefix_tokens
            required = prefix
            if required + cache_bytes > capacity:
                continue
            if r.prefix_key and r.prefix_key not in cache:
                cache[r.prefix_key] = r.prefix_tokens
                cache_bytes += r.prefix_tokens
            # Prefix bytes are owned by the shared cache; do not charge them a
            # second time as per-request target KV.
            active[r.request_id] = RuntimeRequest(r, r.output_tokens, 0, tick, tick)
            waiting.remove(r)
        states = []
        for rr in active.values():
            age = tick - rr.admitted_at
            states.append(RequestState(rr.spec.request_id, rr.remaining, rr.kv_tokens,
                                       rr.spec.prefix_value, max(0, tick - rr.spec.deadline),
                                       rr.spec.acceptance, 8, age))
        used = cache_bytes + sum(rr.kv_tokens for rr in active.values())
        decisions = policy.choose(states, used)
        decided = {d.request_id: d for d in decisions if d.admit}
        step_peak = used
        step_evictions = step_recompute = 0
        for rid, rr in list(active.items()):
            d = decided.get(rid)
            if d is None:
                if tick - rr.last_tick >= 3:
                    starvation += 1
                continue
            k = d.speculative_tokens
            accepted = min(rr.remaining, max(1, round(k * rr.spec.acceptance))) if k else 1
            rr.remaining -= accepted
            rr.kv_tokens += accepted
            rr.last_tick = tick
            accepted_total += accepted
            spec_total += k
            step_peak = max(step_peak, used + k + accepted)
            if rr.remaining <= 0:
                completed_latencies.append(tick - rr.admitted_at + 1)
                if tick + 1 > rr.spec.deadline:
                    misses += 1
                del active[rid]
        peak = max(peak, step_peak)
        # Pressure is an observable utilization signal, not only an OOM event;
        # hard admission prevents the latter from occurring by construction.
        policy.feedback(step_peak / max(1, capacity), step_evictions, step_recompute)
        evictions += step_evictions
        recompute += step_recompute
        if not arrivals and not waiting and not active:
            break
    completed = len(completed_latencies)
    ordered = sorted(completed_latencies)
    p95 = float(ordered[min(len(ordered) - 1, max(0, int(0.95 * len(ordered)) - 1))]) if ordered else float("inf")
    return TraceMetrics(policy.name, completed, completed - misses, p95, misses, starvation,
                        peak, evictions, recompute, accepted_total, spec_total)
