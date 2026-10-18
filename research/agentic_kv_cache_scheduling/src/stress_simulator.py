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
    prefix_survival_probability: float = 0.75


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
    total_tokens: int = 0
    deadline: int = 0


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
    gpu_prefetch_tokens: int = 0
    completed_transfer_tokens: int = 0
    cancelled_transfer_tokens: int = 0
    on_demand_transfer_tokens: int = 0
    stale_cache_misses: int = 0
    deadline_misses: int = 0
    budget_cancellations: int = 0
    fallback_demotions: int = 0
    unified_continuations: int = 0

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
            "gpu_prefetch_tokens": self.gpu_prefetch_tokens,
            "completed_transfer_tokens": self.completed_transfer_tokens,
            "cancelled_transfer_tokens": self.cancelled_transfer_tokens,
            "on_demand_transfer_tokens": self.on_demand_transfer_tokens,
            "stale_cache_misses": self.stale_cache_misses,
            "deadline_misses": self.deadline_misses,
            "budget_cancellations": self.budget_cancellations,
            "fallback_demotions": self.fallback_demotions,
            "unified_continuations": self.unified_continuations,
        }


class StressEngine:
    def __init__(self, policy: str, gpu_tokens=2400, cpu_tokens=4800,
                 remote_tokens=9600, bandwidth=400, recompute_cost=10,
                 cpu_fetch_cost=4, remote_fetch_cost=7,
                 bandwidth_schedule: Dict[int, int] | None = None):
        self.policy = policy
        self.cap = {"gpu": gpu_tokens, "cpu": cpu_tokens, "remote": remote_tokens}
        self.used = {k: 0 for k in self.cap}
        self.bandwidth = bandwidth
        self.bandwidth_schedule = bandwidth_schedule or {}
        self.recompute_cost = recompute_cost
        self.cpu_fetch_cost = cpu_fetch_cost
        self.remote_fetch_cost = remote_fetch_cost
        self.cache: Dict[str, StressEntry] = {}
        self.transfers: List[Transfer] = []
        self.metrics = StressMetrics()
        self.forecasts: Dict[int, int] = {}

    def _bandwidth_at(self, now: int) -> int:
        applicable = [t for t in self.bandwidth_schedule if t <= now]
        if not applicable:
            return max(1, int(self.bandwidth))
        return max(1, int(self.bandwidth_schedule[max(applicable)]))

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
        if self.policy in {"tier_aware", "queue_aware", "budget_aware", "fallback_aware", "unified_aware"}:
            # The forecast is the only length available at admission. If a
            # GPU prefetch cannot finish in the forecast return window, retain
            # the predicted prefix in the cheapest available lower tier.
            estimate = max(0, min(estimate, s.forecast_tokens))
            transfer_ticks = max(1, math.ceil(estimate / self._bandwidth_at(now)))
            gpu_room = self.used["gpu"] + estimate <= self.cap["gpu"]
            completion_prob = 0.85 if transfer_ticks <= s.forecast_return_ticks else 0.15
            robust = max(0, min(.99, s.prefix_survival_probability) - .2)
            value_completion = 1.0 if self.policy == "budget_aware" else completion_prob
            score = robust * value_completion * (estimate / 50) - transfer_ticks
            if (gpu_room and (completion_prob >= .60 or self.policy == "budget_aware") and
                    score > .05 * (1 - robust) * (estimate / 50) and active < 3):
                self.transfers.append(Transfer(
                    s.prefix_group, estimate, "gpu", s.worker,
                    total_tokens=estimate,
                    deadline=now + s.forecast_return_ticks,
                ))
            else:
                lower_tier = "cpu" if self.used["cpu"] + estimate <= self.cap["cpu"] else "remote"
                self._place(s.prefix_group, estimate, lower_tier, s.worker, now)
            return
        if self.policy == "cost_aware":
            # Only the explicit prefix-survival forecast is used here. The
            # realized exact length remains outcome-only and is never read for
            # admission scoring.
            robust = max(0, min(.99, s.prefix_survival_probability) - .2)
            transfer_ticks = max(1, math.ceil(estimate / self._bandwidth_at(now)))
            candidates = [(self.recompute_cost, "recompute")]
            if (self.used["gpu"] + estimate <= self.cap["gpu"] and
                    transfer_ticks <= s.forecast_return_ticks and active < 3):
                gpu_cost = robust * (1 + transfer_ticks) + (1 - robust) * self.recompute_cost
                candidates.append((gpu_cost, "gpu"))
            if self.used["cpu"] + estimate <= self.cap["cpu"]:
                cpu_cost = robust * self.cpu_fetch_cost + (1 - robust) * self.recompute_cost
                candidates.append((cpu_cost, "cpu"))
            if self.used["remote"] + estimate <= self.cap["remote"]:
                remote_cost = robust * self.remote_fetch_cost + (1 - robust) * self.recompute_cost
                candidates.append((remote_cost, "remote"))
            best_cost, best_tier = min(candidates, key=lambda x: (x[0], x[1]))
            if best_tier == "gpu" and best_cost < self.recompute_cost:
                self.transfers.append(Transfer(s.prefix_group, estimate, "gpu", s.worker,
                                               total_tokens=estimate))
            elif best_tier in {"cpu", "remote"} and best_cost < self.recompute_cost:
                self._place(s.prefix_group, estimate, best_tier, s.worker, now)
            return
        if self.policy == "static":
            action = True
        else:
            q = min(.99, s.prefix_survival_probability)
            p = .5 if not self.cache else .65
            robust = max(0, p * q - .2)
            transfer_ticks = max(1, math.ceil(estimate / self._bandwidth_at(now)))
            # Revision 2: price whether the transfer can finish before the
            # forecast return window. This is an observable forecast, not the
            # realized duration. It directly targets the bandwidth failure.
            completion_prob = 0.85 if transfer_ticks <= s.forecast_return_ticks else 0.15
            score = robust * completion_prob * (estimate / 50) - transfer_ticks
            action = (score > .05 * (1 - robust) * (estimate / 50)
                      and completion_prob >= .60 and active < 3)
        if action:
            self.transfers.append(Transfer(s.prefix_group, estimate, "gpu", s.worker,
                                           total_tokens=estimate))

    def _cancel_group_transfers(self, group: str) -> None:
        for transfer in self.transfers:
            if transfer.group == group and not transfer.cancelled:
                transfer.cancelled = True
                self.metrics.cancelled_transfers += 1
                self.metrics.cancelled_transfer_tokens += transfer.tokens_left

    def _active_transfers(self) -> List[Transfer]:
        active = [x for x in self.transfers if not x.cancelled]
        if self.policy not in {"queue_aware", "budget_aware", "fallback_aware", "unified_aware"} or len(active) <= 1:
            return active
        # Finish the most urgent small transfer first. This is intentionally a
        # simple, auditable queue policy rather than an optimal scheduler.
        return [min(active, key=lambda x: (x.deadline, x.tokens_left, x.group))]

    def _cancel_overdue_transfers(self, now: int) -> None:
        if self.policy not in {"budget_aware", "fallback_aware", "unified_aware"}:
            return
        for transfer in self.transfers:
            if (not transfer.cancelled and transfer.tokens_left > 0
                    and transfer.deadline and now > transfer.deadline):
                fallback_tier = (
                    "cpu" if self.used["cpu"] + transfer.total_tokens <= self.cap["cpu"]
                    else "remote"
                )
                if self.policy == "unified_aware":
                    current_bandwidth = self._bandwidth_at(now)
                    continue_cost = math.ceil(transfer.tokens_left / current_bandwidth) + 1
                    fallback_cost = (
                        self.cpu_fetch_cost if fallback_tier == "cpu"
                        else self.remote_fetch_cost
                    )
                    options = [(self.recompute_cost, "recompute"),
                               (fallback_cost, fallback_tier),
                               (continue_cost, "continue")]
                    best_cost, best_action = min(options, key=lambda x: (x[0], x[1]))
                    if best_action == "continue":
                        self.metrics.unified_continuations += 1
                        continue
                transfer.cancelled = True
                self.metrics.cancelled_transfers += 1
                self.metrics.cancelled_transfer_tokens += transfer.tokens_left
                self.metrics.budget_cancellations += 1
                if self.policy in {"fallback_aware", "unified_aware"}:
                    if self._place(
                        transfer.group, transfer.total_tokens, fallback_tier,
                        transfer.worker, now
                    ):
                        self.metrics.fallback_demotions += 1

    def run(self, sessions: List[StressSession]):
        events: Dict[int, List[Tuple[str, StressSession]]] = {}
        for s in sessions:
            events.setdefault(s.start, []).append(("start", s))
            events.setdefault(s.start + s.duration, []).append(("return", s))
            for dt, _ in s.revisions:
                events.setdefault(s.start + dt, []).append(("revision", s))
        end = max(events) if events else 0
        for now in range(end + 1):
            self._cancel_overdue_transfers(now)
            # Transfer bandwidth is shared by all in-flight transfers.
            active_transfers = self._active_transfers()
            active_requests = sum(1 for s in sessions if s.start <= now < s.start + 2)
            if active_transfers and active_requests:
                self.metrics.interference_ticks += 1
            bandwidth = self._bandwidth_at(now)
            share = (bandwidth if self.policy in {"queue_aware", "budget_aware", "fallback_aware", "unified_aware"}
                     else max(1, bandwidth // max(1, len(active_transfers))))
            for x in list(active_transfers):
                moved = min(share, x.tokens_left)
                x.tokens_left -= moved
                self.metrics.transfer_tokens += moved
                if x.tokens_left == 0:
                    self._place(x.group, self._tokens_for(x.group, sessions), x.target, x.worker, now)
                    self.metrics.completed_transfers += 1
                    self.metrics.completed_transfer_tokens += x.total_tokens or x.tokens_left
                    self.metrics.deadline_misses += int(x.deadline and now > x.deadline)
                    self.transfers.remove(x)
            for kind, s in events.get(now, []):
                if kind == "start":
                    self._start(s, now, active_requests)
                elif kind == "revision":
                    self.metrics.revisions += 1
                    if s.cancelled or s.forecast_tokens != self.forecasts.get(s.sid):
                        self._cancel_group_transfers(s.prefix_group)
                elif kind == "return":
                    self._cancel_group_transfers(s.prefix_group)
                    if s.cancelled:
                        self.metrics.wasted_transfers += 1
                        continue
                    e = self.cache.get(s.prefix_group)
                    if e and e.tier == "gpu" and e.tokens == s.exact_tokens and e.ready <= now:
                        self.metrics.ttft.append(1 if e.worker == s.worker else 3)
                        self.metrics.shared_hits += int(s.branch > 0)
                        e.last = now
                    elif e and e.tier == "cpu" and e.tokens == s.exact_tokens:
                        self.metrics.ttft.append(self.cpu_fetch_cost if e.worker == s.worker else self.cpu_fetch_cost + 2)
                        self.metrics.cpu_hits += 1
                        self.metrics.transfer_tokens += s.exact_tokens
                        self.metrics.on_demand_transfer_tokens += s.exact_tokens
                        self.metrics.shared_hits += int(s.branch > 0)
                        e.last = now
                    elif e and e.tier == "remote" and e.tokens == s.exact_tokens:
                        self.metrics.ttft.append(self.remote_fetch_cost if e.worker == s.worker else self.remote_fetch_cost + 2)
                        self.metrics.remote_hits += 1
                        self.metrics.transfer_tokens += s.exact_tokens
                        self.metrics.on_demand_transfer_tokens += s.exact_tokens
                        self.metrics.shared_hits += int(s.branch > 0)
                        e.last = now
                    else:
                        self.metrics.ttft.append(self.recompute_cost)
                        self.metrics.recompute_misses += 1
                        if s.prefix_group in self.cache:
                            self.metrics.wasted_transfers += 1
                            self.metrics.stale_cache_misses += 1
        self.metrics.wasted_transfers += sum(1 for x in self.transfers if x.cancelled)
        return self.metrics.summary()

    def _tokens_for(self, group, sessions):
        return max(s.exact_tokens for s in sessions if s.prefix_group == group)
