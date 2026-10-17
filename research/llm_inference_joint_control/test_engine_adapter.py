import unittest

from .engine_adapter import EngineRequestObservation, EngineStepObservation, RaspEngineAdapter
from .reference_controller import ControllerConfig


class EngineAdapterTests(unittest.TestCase):
    def test_maps_observation_without_future_information(self):
        cfg = ControllerConfig(capacity_bytes=24, reserve_bytes=2, max_batch_tokens=8)
        adapter = RaspEngineAdapter(cfg)
        obs = EngineStepObservation(
            requests=(EngineRequestObservation('r1', 8, 4, 0.0, 0.0, 0.8, 4, 2),),
            used_kv_bytes=4, capacity_bytes=24, batch_token_budget=8,
            pressure_signal=0.5, evictions=0, recompute_tokens=0)
        decisions = adapter.decide(obs)
        self.assertTrue(decisions)
        self.assertEqual(decisions[0].request_id, 'r1')

    def test_rejects_budget_mismatch(self):
        adapter = RaspEngineAdapter(ControllerConfig(capacity_bytes=24, reserve_bytes=2, max_batch_tokens=8))
        obs = EngineStepObservation((), 0, 32, 8, 0.0, 0, 0)
        with self.assertRaises(ValueError):
            adapter.decide(obs)


if __name__ == '__main__':
    unittest.main()
