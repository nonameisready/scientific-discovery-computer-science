"""Small, dependency-free reference controller for the LLM serving study.

This is a trace-level policy model, not a serving engine.  It deliberately
separates transient speculative workspace from persistent accepted-token KV.
"""
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class RequestState:
    request_id: str
    waiting_tokens: int
    kv_tokens: int
    prefix_reuse_value: float
    slo_debt: float
    acceptance: float
    max_spec_tokens: int
    age: int = 0


@dataclass(frozen=True)
class ControllerConfig:
    block_bytes: int = 1
    capacity_bytes: int = 64
    reserve_bytes: int = 4
    max_batch_tokens: int = 32
    pressure_weight: float = 1.0
    eviction_weight: float = 1.0
    slo_weight: float = 1.0
    acceptance_floor: float = 0.05
    hysteresis: float = 0.0
    age_weight: float = 0.1
    utilization_weight: float = 1.0


@dataclass(frozen=True)
class Decision:
    request_id: str
    admit: bool
    speculative_tokens: int
    score: float
    peak_bytes: int
    persistent_bytes: int


class ShadowPriceController:
    """Greedy, hard-feasible admission/speculation controller.

    The controller scores each candidate independently, then admits in score
    order subject to batch and peak-memory constraints.  A candidate's peak
    cost includes all draft tokens, while its persistent cost includes only
    expected accepted tokens.  The prefix value is subtracted from eviction
    pressure, making reusable prefixes harder to evict than ordinary blocks.
    """

    def __init__(self, config: ControllerConfig):
        self.config = config
        self.pressure_shadow = 0.0
        self.eviction_shadow = 0.0

    def update_feedback(self, pressure: float, evictions: int, recompute_tokens: int) -> None:
        """Update prices from observable runtime feedback only."""
        self.pressure_shadow = max(0.0, 0.8 * self.pressure_shadow + 0.2 * pressure)
        event_cost = evictions + recompute_tokens / max(1, self.config.block_bytes)
        self.eviction_shadow = max(0.0, 0.8 * self.eviction_shadow + 0.2 * event_cost)

    def _candidate(self, r: RequestState, k: int, used: int) -> Decision:
        c = self.config
        acceptance = max(c.acceptance_floor, min(1.0, r.acceptance))
        accepted = min(r.waiting_tokens, max(1, int(round(k * acceptance)))) if k else 1
        persistent = accepted * c.block_bytes
        transient = k * c.block_bytes
        peak = used + transient + persistent
        safe_capacity = max(1, c.capacity_bytes - c.reserve_bytes)
        utilization = peak / safe_capacity
        # Hard feasibility is checked separately.  This soft term makes the
        # policy react before the allocator reaches the hard cap.
        pressure_term = max(0.0, utilization - 0.5) * transient / max(1, c.block_bytes)
        eviction_term = max(0.0, persistent - r.prefix_reuse_value)
        useful = accepted + 0.25 * r.prefix_reuse_value + 0.5 * r.slo_debt + c.age_weight * r.age
        score = useful - c.pressure_weight * (pressure_term + self.pressure_shadow * transient)
        score -= c.eviction_weight * (eviction_term + self.eviction_shadow * persistent)
        score -= c.slo_weight * max(0.0, -r.slo_debt)
        return Decision(r.request_id, False, k, score, peak, persistent)

    def decide(self, requests: Iterable[RequestState], used_bytes: int) -> List[Decision]:
        """Return deterministic decisions; no request is admitted if hard-fit fails."""
        c = self.config
        candidates: List[Decision] = []
        for r in requests:
            best: Optional[Decision] = None
            for k in range(0, min(r.max_spec_tokens, c.max_batch_tokens) + 1):
                d = self._candidate(r, k, used_bytes)
                if d.peak_bytes <= c.capacity_bytes - c.reserve_bytes:
                    if best is None or (d.score, d.speculative_tokens) > (best.score, best.speculative_tokens):
                        best = d
            if best is not None:
                candidates.append(best)
        candidates.sort(key=lambda d: (-d.score, d.request_id))
        out: List[Decision] = []
        batch = 0
        current = used_bytes
        for d in candidates:
            if batch + d.speculative_tokens > c.max_batch_tokens:
                continue
            if current + d.persistent_bytes + d.speculative_tokens * c.block_bytes > c.capacity_bytes - c.reserve_bytes:
                continue
            out.append(Decision(d.request_id, True, d.speculative_tokens, d.score,
                                current + d.persistent_bytes + d.speculative_tokens * c.block_bytes,
                                d.persistent_bytes))
            batch += d.speculative_tokens
            current += d.persistent_bytes + d.speculative_tokens * c.block_bytes
        return out
