"""Engine-neutral adapter contract for a future vLLM integration.

This module intentionally does not import vLLM. It freezes the observation and
decision boundary that an engine-specific patch must implement.
"""
from dataclasses import dataclass
from typing import Dict, Iterable, List

from .reference_controller import ControllerConfig, Decision, RequestState, ShadowPriceController


@dataclass(frozen=True)
class EngineRequestObservation:
    request_id: str
    waiting_tokens: int
    resident_kv_bytes: int
    prefix_reuse_value: float
    slo_debt: float
    acceptance_rate: float
    max_spec_tokens: int
    age: int


@dataclass(frozen=True)
class EngineStepObservation:
    requests: tuple[EngineRequestObservation, ...]
    used_kv_bytes: int
    capacity_bytes: int
    batch_token_budget: int
    pressure_signal: float
    evictions: int
    recompute_tokens: int


class RaspEngineAdapter:
    """Translate an engine observation into a safe RASP decision.

    The engine remains responsible for allocation, preemption, and executing
    target verification. The adapter only supplies candidate decisions and
    must reject any decision that exceeds the engine-reported hard budget.
    """

    def __init__(self, config: ControllerConfig):
        self.controller = ShadowPriceController(config)

    def decide(self, obs: EngineStepObservation) -> List[Decision]:
        self.controller.update_feedback(obs.pressure_signal, obs.evictions, obs.recompute_tokens)
        requests = [RequestState(
            request_id=r.request_id,
            waiting_tokens=r.waiting_tokens,
            kv_tokens=r.resident_kv_bytes,
            prefix_reuse_value=r.prefix_reuse_value,
            slo_debt=r.slo_debt,
            acceptance=r.acceptance_rate,
            max_spec_tokens=r.max_spec_tokens,
            age=r.age,
        ) for r in obs.requests]
        config = self.controller.config
        if config.capacity_bytes != obs.capacity_bytes or config.max_batch_tokens != obs.batch_token_budget:
            raise ValueError('controller configuration does not match engine hard budgets')
        return self.controller.decide(requests, obs.used_kv_bytes)
