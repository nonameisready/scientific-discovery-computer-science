"""Small deterministic discrete-event reference model for agentic KV scheduling.

This is intentionally a CPU reference model, not an inference-engine emulator.
All decisions are made from state available before a tool returns.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
import math
import random
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Session:
    sid: int
    start: int
    tool_duration: int
    prefix_tokens: int
    reusable_tokens: int
    estimated_reusable_tokens: int
    worker: int
    branch: int = 0
    cancelled: bool = False


@dataclass
class Entry:
    sid: int
    tokens: int
    tier: str = "cpu"
    ready_at: int = 0
    last_touch: int = 0
    generation: int = 0


@dataclass
class Metrics:
    continuation_ttft: List[int] = field(default_factory=list)
    workflow_latency: List[int] = field(default_factory=list)
    prefetches: int = 0
    useful_prefetches: int = 0
    wasted_prefetches: int = 0
    evictions: int = 0
    transfer_bytes: int = 0
    interference: int = 0
    decisions: int = 0

    def summary(self) -> Dict[str, float]:
        xs = sorted(self.continuation_ttft)
        p95 = xs[max(0, math.ceil(.95 * len(xs)) - 1)] if xs else 0
        return {
            "n": len(xs),
            "mean_continuation_ttft": sum(xs) / len(xs) if xs else 0.0,
            "p95_continuation_ttft": p95,
            "mean_workflow_latency": sum(self.workflow_latency) / len(self.workflow_latency) if self.workflow_latency else 0.0,
            "prefetches": self.prefetches,
            "useful_prefetch_rate": self.useful_prefetches / self.prefetches if self.prefetches else 0.0,
            "wasted_prefetches": self.wasted_prefetches,
            "evictions": self.evictions,
            "transfer_bytes": self.transfer_bytes,
            "interference": self.interference,
            "decisions": self.decisions,
        }


class Controller:
    """Policies used by the reference simulator.

    proposed: robust lower-confidence expected benefit minus explicit costs.
    It can wait; at each tick it re-evaluates only with observations so far.
    """

    def __init__(self, policy: str, capacity: int = 4, bandwidth: int = 2,
                 interference_budget: int = 1):
        self.policy = policy
        self.capacity = capacity
        self.bandwidth = bandwidth
        self.interference_budget = interference_budget
        self.cache: Dict[int, Entry] = {}
        self.history: deque[int] = deque(maxlen=32)
        self.completed: Dict[int, int] = {}
        self.pending: Dict[int, Session] = {}
        self.metrics = Metrics()
        self.active_transfers = 0
        self.prefetched_sids: set[int] = set()

    def observe_return(self, s: Session, t: int) -> None:
        self.history.append(t - s.start)
        self.completed[s.sid] = t

    def _mean_duration(self) -> float:
        return sum(self.history) / len(self.history) if self.history else 8.0

    def _p_resume(self, s: Session, now: int) -> float:
        # Empirical survival estimate, with conservative Laplace smoothing.
        if not self.history:
            return 0.5
        h = max(1, now - s.start)
        return sum(d >= h for d in self.history) / (len(self.history) + 2)

    def _p_exact(self, s: Session) -> float:
        # The decision uses an online prefix-survival estimate, not actual future tokens.
        return min(0.99, max(0.05, s.estimated_reusable_tokens / max(1, s.prefix_tokens)))

    def _admit(self, sid: int, now: int, tokens: int, tier: str = "gpu") -> bool:
        gpu = [e for e in self.cache.values() if e.tier == "gpu"]
        if tier == "gpu" and len(gpu) >= self.capacity:
            victim = min(gpu, key=lambda e: (e.last_touch, e.sid))
            del self.cache[victim.sid]
            self.metrics.evictions += 1
        self.cache[sid] = Entry(sid, tokens, tier=tier, ready_at=now, last_touch=now)
        return tier == "gpu"

    def decide(self, s: Session, now: int, active_requests: int) -> str:
        self.metrics.decisions += 1
        p = self._p_resume(s, now) * self._p_exact(s)
        mean = self._mean_duration()
        # Benefit is avoided recomputation. Costs include transfer, residency,
        # displaced-prefix risk, and a queueing/interference charge.
        saved = max(0, s.estimated_reusable_tokens // 50)
        transfer = max(1, s.estimated_reusable_tokens // 800)
        displacement = 2 if len([e for e in self.cache.values() if e.tier == "gpu"]) >= self.capacity else 0
        interference = max(0, active_requests + self.active_transfers - self.interference_budget)
        if self.policy == "lru":
            return "none"
        if self.policy == "ttl":
            return "keep"
        if self.policy == "static":
            return "prefetch"
        if self.policy == "predicted":
            return "prefetch" if mean <= 8 else "none"
        # Robust option-aware rule. A waiting action is selected when current
        # value is negative but the next observation can change the decision.
        robust_p = max(0.0, p - 0.20)  # explicit calibration-error reserve
        score = robust_p * saved - transfer - displacement - 2 * interference
        # Waiting has value, but the reference controller prices one tick of
        # information conservatively; this is the tunable option coefficient.
        option = max(0.0, min(1.0, 0.05 * (1 - robust_p))) * saved
        return "prefetch" if score >= option and score > 0 else "none"

    def start_tool(self, s: Session, now: int, active_requests: int) -> None:
        action = self.decide(s, now, active_requests)
        if action == "keep":
            self._admit(s.sid, now, s.reusable_tokens, "gpu")
        elif action == "prefetch":
            self.metrics.prefetches += 1
            self.prefetched_sids.add(s.sid)
            self.active_transfers += 1
            # Reference units: one bandwidth unit moves 400 tokens per tick.
            delay = max(1, math.ceil(s.reusable_tokens / max(1, self.bandwidth * 400)))
            self.metrics.transfer_bytes += s.reusable_tokens
            ready = now + delay
            self._admit(s.sid, ready, s.reusable_tokens, "gpu")
            self.active_transfers -= 1
        self.pending[s.sid] = s

    def finish(self, s: Session, now: int, cold_cost: int = 10) -> None:
        e = self.cache.get(s.sid)
        # Exact-prefix compatibility: a shorter entry is not treated as a hit
        # for the requested reusable prefix in this conservative model.
        if e and e.tier == "gpu" and e.ready_at <= now and e.tokens == s.reusable_tokens:
            wait = 1
            if self.metrics.prefetches and e.ready_at > s.start + s.tool_duration:
                wait += e.ready_at - (s.start + s.tool_duration)
            self.metrics.useful_prefetches += 1 if s.sid in self.prefetched_sids and e.ready_at <= now else 0
            self.metrics.continuation_ttft.append(wait)
        else:
            self.metrics.continuation_ttft.append(cold_cost)
            if s.sid in self.prefetched_sids:
                self.metrics.wasted_prefetches += 1
        self.observe_return(s, now)
        self.metrics.workflow_latency.append(now - s.start + self.metrics.continuation_ttft[-1])
        if e:
            e.last_touch = now
            e.generation += 1


def generate_trace(seed: int = 7, n: int = 80, regime: str = "mixed") -> List[Session]:
    rng = random.Random(seed)
    out: List[Session] = []
    for sid in range(n):
        start = sid // 2
        if regime == "early": duration = rng.choice([1, 2, 3, 4])
        elif regime == "late": duration = rng.choice([12, 18, 25, 35])
        else: duration = rng.choice([1, 2, 3, 8, 12, 20])
        tokens = rng.choice([400, 800, 1200])
        fraction = rng.choice([0.25, 0.5, 0.75, 1.0])
        if rng.random() < .15: fraction = .05  # context-changing tool output
        forecast_fraction = rng.choice([0.5, 0.75, 1.0])
        out.append(Session(sid, start, duration, tokens, int(tokens * fraction),
                           int(tokens * forecast_fraction), sid % 3,
                           branch=sid % 2, cancelled=(rng.random() < .05)))
    return out


def run(trace: List[Session], policy: str, capacity: int = 4) -> Dict[str, float]:
    c = Controller(policy, capacity=capacity)
    events: Dict[int, List[tuple[str, Session]]] = {}
    for s in trace:
        events.setdefault(s.start, []).append(("start", s))
        events.setdefault(s.start + s.tool_duration, []).append(("finish", s))
    for now in sorted(events):
        for kind, s in sorted(events[now], key=lambda z: z[0]):
            if kind == "start":
                active = sum(1 for x in trace if x.start <= now < x.start + 3 and x.sid != s.sid)
                c.start_tool(s, now, active)
            elif not s.cancelled:
                c.finish(s, now)
            else:
                if s.sid in c.cache: del c.cache[s.sid]
                c.metrics.wasted_prefetches += 1 if s.sid in c.prefetched_sids else 0
    return c.metrics.summary()


if __name__ == "__main__":
    for p in ["lru", "ttl", "static", "predicted", "proposed"]:
        print(p, run(generate_trace(), p))
