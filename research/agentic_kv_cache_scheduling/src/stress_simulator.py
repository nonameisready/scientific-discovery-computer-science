"""Bounded stress model for tiers, shared branches, congestion and revisions."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math


@dataclass(frozen=True)
class StressSession:
    sid: int
    start: int
    duration: int
    prefix_group: str
    exact_tokens: int
    forecast_tokens: int
    worker: int
    branch: int = 0
    cancelled: bool = False
    revisions: Tuple[Tuple[int, int], ...] = ()  # (time after start, new forecast)
    forecast_return_ticks: int = 8


@dataclass
class StressEntry:
    group: str
    tokens: int
    tier: str
    worker: int
    ready: int
    last: int


@dataclass
class Transfer:
    group: str
    tokens_left: int
    target: str
    worker: int
    cancelled: bool = False


@dataclass
class StressMetrics:
    ttft: List[int] = field(default_factory=list)
    wasted_transfers: int = 0
    completed_transfers: int = 0
    cancelled_transfers: int = 0
    transfer_tokens: int = 0
    interference_ticks: int = 0
    evictions: int = 0
    revisions: int = 0
    shared_hits: int = 0
    cpu_hits: int = 0
    remote_hits: int = 0
    recompute_misses: int = 0

    def summary(self):
        xs = sorted(self.ttft)
        return {
            "n": len(xs), "mean_ttft": sum(xs) / len(xs) if xs else 0.0,
            "p95_ttft": xs[max(0, math.ceil(.95 * len(xs)) - 1)] if xs else 0,
            "wasted_transfers": self.wasted_transfers,
            "completed_transfers": self.completed_transfers,
            "cancelled_transfers": self.cancelled_transfers,
            "transfer_tokens": self.transfer_tokens,
            "interference_ticks": self.interference_ticks,
            "evictions": self.evictions,
            "revisions": self.revisions,
            "shared_hits": self.shared_hits,
            "cpu_hits": self.cpu_hits,
            "remote_hits": self.remote_hits,
            "recompute_misses": self.recompute_misses,
        }


class StressEngine:
    def __init__(self, policy: str, gpu_tokens=2400, cpu_tokens=4800,
                 remote_tokens=9600, bandwidth=400):
        self.policy = policy
        self.cap = {"gpu": gpu_tokens, "cpu": cpu_tokens, "remote": remote_tokens}
        self.used = {k: 0 for k in self.cap}
        self.bandwidth = bandwidth
        self.cache: Dict[str, StressEntry] = {}
        self.transfers: List[Transfer] = []
        self.metrics = StressMetrics()
        self.forecasts: Dict[int, int] = {}

    def _place(self, group, tokens, tier, worker, now):
        old = self.cache.get(group)
        if old:
            self.used[old.tier] -= old.tokens
        while self.used[tier] + tokens > self.cap[tier]:
            victims = [e for e in self.cache.values() if e.tier == tier]
            if not victims:
                return False
            victim = min(victims, key=lambda e: (e.last, e.group))
            del self.cache[victim.group]
            self.used[tier] -= victim.tokens
            self.metrics.evictions += 1
        self.cache[group] = StressEntry(group, tokens, tier, worker, now, now)
        self.used[tier] += tokens
        return True

    def _start(self, s: StressSession, now, active):
        self.forecasts[s.sid] = s.forecast_tokens
        for dt, forecast in s.revisions:
            if dt == 0:
                self.forecasts[s.sid] = forecast
        if self.policy == "lru":
            return
        estimate = self.forecasts[s.sid]
        if self.policy == "ttl":
            self._place(s.prefix_group, s.exact_tokens, "gpu", s.worker, now)
            return
        if self.policy == "tier_aware":
            # The forecast is the only length available at admission. If a
            # GPU prefetch cannot finish in the forecast return window, retain
            # the predicted prefix in the cheapest available lower tier.
            estimate = max(0, min(estimate, s.forecast_tokens))
            transfer_ticks = max(1, math.ceil(estimate / self.bandwidth))
            gpu_room = self.used["gpu"] + estimate <= self.cap["gpu"]
            completion_prob = 0.85 if transfer_ticks <= s.forecast_return_ticks else 0.15
            robust = max(0, .65 * min(.99, estimate / max(1, s.exact_tokens)) - .2)
            score = robust * completion_prob * (estimate / 50) - transfer_ticks
            if (gpu_room and completion_prob >= .60 and
                    score > .05 * (1 - robust) * (estimate / 50) and active < 3):
                self.transfers.append(Transfer(s.prefix_group, estimate, "gpu", s.worker))
            else:
                lower_tier = "cpu" if self.used["cpu"] + estimate <= self.cap["cpu"] else "remote"
                self._place(s.prefix_group, estimate, lower_tier, s.worker, now)
            return
        if self.policy == "static":
            action = True
        else:
            q = min(.99, estimate / max(1, s.exact_tokens))
            p = .5 if not self.cache else .65
            robust = max(0, p * q - .2)
            transfer_ticks = max(1, math.ceil(estimate / self.bandwidth))
            # Revision 2: price whether the transfer can finish before the
            # forecast return window. This is an observable forecast, not the
            # realized duration. It directly targets the bandwidth failure.
            completion_prob = 0.85 if transfer_ticks <= s.forecast_return_ticks else 0.15
            score = robust * completion_prob * (estimate / 50) - transfer_ticks
            action = (score > .05 * (1 - robust) * (estimate / 50)
                      and completion_prob >= .60 and active < 3)
        if action:
            self.transfers.append(Transfer(s.prefix_group, estimate, "gpu", s.worker))

    def run(self, sessions: List[StressSession]):
        events: Dict[int, List[Tuple[str, StressSession]]] = {}
        for s in sessions:
            events.setdefault(s.start, []).append(("start", s))
            events.setdefault(s.start + s.duration, []).append(("return", s))
            for dt, _ in s.revisions:
                events.setdefault(s.start + dt, []).append(("revision", s))
        end = max(events) if events else 0
        for now in range(end + 1):
            # Transfer bandwidth is shared by all in-flight transfers.
            active_transfers = [x for x in self.transfers if not x.cancelled]
            active_requests = sum(1 for s in sessions if s.start <= now < s.start + 2)
            if active_transfers and active_requests:
                self.metrics.interference_ticks += 1
            share = max(1, self.bandwidth // max(1, len(active_transfers)))
            for x in list(active_transfers):
                moved = min(share, x.tokens_left)
                x.tokens_left -= moved
                self.metrics.transfer_tokens += moved
                if x.tokens_left == 0:
                    self._place(x.group, self._tokens_for(x.group, sessions), x.target, x.worker, now)
                    self.metrics.completed_transfers += 1
                    self.transfers.remove(x)
            for kind, s in events.get(now, []):
                if kind == "start":
                    self._start(s, now, active_requests)
                elif kind == "revision":
                    self.metrics.revisions += 1
                    if s.cancelled or s.forecast_tokens != self.forecasts.get(s.sid):
                        for x in self.transfers:
                            if x.group == s.prefix_group:
                                x.cancelled = True
                                self.metrics.cancelled_transfers += 1
                elif kind == "return":
                    for x in self.transfers:
                        if x.group == s.prefix_group:
                            x.cancelled = True
                            self.metrics.cancelled_transfers += 1
                    if s.cancelled:
                        self.metrics.wasted_transfers += 1
                        continue
                    e = self.cache.get(s.prefix_group)
                    if e and e.tier == "gpu" and e.tokens == s.exact_tokens and e.ready <= now:
                        self.metrics.ttft.append(1 if e.worker == s.worker else 3)
                        self.metrics.shared_hits += int(s.branch > 0)
                        e.last = now
                    elif e and e.tier == "cpu" and e.tokens == s.exact_tokens:
                        self.metrics.ttft.append(4 if e.worker == s.worker else 6)
                        self.metrics.cpu_hits += 1
                        self.metrics.transfer_tokens += s.exact_tokens
                        self.metrics.shared_hits += int(s.branch > 0)
                        e.last = now
                    elif e and e.tier == "remote" and e.tokens == s.exact_tokens:
                        self.metrics.ttft.append(7 if e.worker == s.worker else 9)
                        self.metrics.remote_hits += 1
                        self.metrics.transfer_tokens += s.exact_tokens
                        self.metrics.shared_hits += int(s.branch > 0)
                        e.last = now
                    else:
                        self.metrics.ttft.append(10)
                        self.metrics.recompute_misses += 1
                        if s.prefix_group in self.cache:
                            self.metrics.wasted_transfers += 1
        self.metrics.wasted_transfers += sum(1 for x in self.transfers if x.cancelled)
        return self.metrics.summary()

    def _tokens_for(self, group, sessions):
        return max(s.exact_tokens for s in sessions if s.prefix_group == group)
