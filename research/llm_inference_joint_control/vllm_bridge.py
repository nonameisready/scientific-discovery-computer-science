"""Duck-typed vLLM V1 bridge for the pinned v0.13.0 scheduler surface.

The bridge is importable without vLLM. In production it is called from a
small scheduler fork immediately before allocate_slots().
"""
from typing import Any, Iterable

from .engine_adapter import EngineRequestObservation, EngineStepObservation, RaspEngineAdapter
from .reference_controller import ControllerConfig, Decision


class VllmRaspBridge:
    def __init__(self, scheduler: Any, controller_config: ControllerConfig):
        self.scheduler = scheduler
        self.adapter = RaspEngineAdapter(controller_config)

    def _page_bytes(self, group: Any) -> int:
        return int(group.kv_cache_spec.page_size_bytes)

    def request_kv_bytes(self, request: Any) -> int:
        blocks = self.scheduler.kv_cache_manager.get_blocks(request.request_id).blocks
        groups = self.scheduler.kv_cache_config.kv_cache_groups
        return sum(len(block_group) * self._page_bytes(group)
                   for block_group, group in zip(blocks, groups))

    def _capacity_bytes(self) -> int:
        groups = self.scheduler.kv_cache_config.kv_cache_groups
        blocks = int(self.scheduler.cache_config.num_gpu_blocks)
        return blocks * sum(self._page_bytes(group) for group in groups)

    def observe(self, requests: Iterable[Any]) -> EngineStepObservation:
        capacity = self._capacity_bytes()
        usage = float(self.scheduler.kv_cache_manager.usage)
        observations = []
        for request in requests:
            observations.append(EngineRequestObservation(
                request_id=request.request_id,
                waiting_tokens=max(0, int(getattr(request, "num_tokens_with_spec", 0)
                                           + getattr(request, "num_output_placeholders", 0)
                                           - getattr(request, "num_computed_tokens", 0))),
                resident_kv_bytes=self.request_kv_bytes(request),
                prefix_reuse_value=float(getattr(request, "rasp_prefix_reuse_value", 0.0)),
                slo_debt=float(getattr(request, "rasp_slo_debt", 0.0)),
                acceptance_rate=float(getattr(request, "rasp_acceptance_rate", 1.0)),
                max_spec_tokens=int(getattr(self.scheduler, "num_spec_tokens", 0)),
                age=max(0, int(getattr(request, "rasp_age", 0))),
            ))
        return EngineStepObservation(
            requests=tuple(observations),
            used_kv_bytes=int(round(usage * capacity)),
            capacity_bytes=capacity,
            batch_token_budget=int(self.scheduler.max_num_scheduled_tokens),
            pressure_signal=usage,
            evictions=0,
            recompute_tokens=0,
        )

    def decide(self, requests: Iterable[Any]) -> list[Decision]:
        return self.adapter.decide(self.observe(requests))
