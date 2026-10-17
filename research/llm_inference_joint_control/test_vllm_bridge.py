import unittest
from types import SimpleNamespace

from .reference_controller import ControllerConfig
from .vllm_bridge import VllmRaspBridge


class FakeKVManager:
    usage = 0.25

    def get_blocks(self, request_id):
        return SimpleNamespace(blocks=((object(), object()),))


class VllmBridgeTests(unittest.TestCase):
    def test_maps_real_vllm_shape_to_rasp(self):
        scheduler = SimpleNamespace(
            kv_cache_manager=FakeKVManager(),
            kv_cache_config=SimpleNamespace(kv_cache_groups=(SimpleNamespace(
                kv_cache_spec=SimpleNamespace(page_size_bytes=10)),)),
            cache_config=SimpleNamespace(num_gpu_blocks=100),
            max_num_scheduled_tokens=8,
            num_spec_tokens=4,
        )
        request = SimpleNamespace(
            request_id='r1', num_tokens_with_spec=20,
            num_output_placeholders=0, num_computed_tokens=10,
            rasp_prefix_reuse_value=2.0, rasp_slo_debt=1.0,
            rasp_acceptance_rate=.75, rasp_age=3,
        )
        bridge = VllmRaspBridge(scheduler, ControllerConfig(
            block_bytes=10, capacity_bytes=1000, reserve_bytes=10, max_batch_tokens=8))
        obs = bridge.observe([request])
        self.assertEqual(obs.requests[0].resident_kv_bytes, 20)
        self.assertEqual(obs.requests[0].waiting_tokens, 10)
        self.assertEqual(obs.used_kv_bytes, 250)
        self.assertEqual(obs.requests[0].acceptance_rate, .75)

    def test_adapter_rejects_mismatched_engine_capacity(self):
        scheduler = SimpleNamespace(
            kv_cache_manager=FakeKVManager(),
            kv_cache_config=SimpleNamespace(kv_cache_groups=(SimpleNamespace(
                kv_cache_spec=SimpleNamespace(page_size_bytes=10)),)),
            cache_config=SimpleNamespace(num_gpu_blocks=100),
            max_num_scheduled_tokens=8, num_spec_tokens=4)
        bridge = VllmRaspBridge(scheduler, ControllerConfig(
            block_bytes=10, capacity_bytes=999, reserve_bytes=10, max_batch_tokens=8))
        with self.assertRaises(ValueError):
            bridge.decide([])


if __name__ == '__main__':
    unittest.main()
