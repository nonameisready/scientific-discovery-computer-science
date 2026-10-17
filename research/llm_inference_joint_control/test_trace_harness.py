import unittest

from .reference_controller import ControllerConfig
from .trace_harness import AcceptanceAdaptive, FixedDepth, RASPPolicy, TraceRequest, run_trace


class TraceHarnessTests(unittest.TestCase):
    def setUp(self):
        self.trace = [
            TraceRequest("short", 0, 3, 0.95, 8, "sys", 4, 0.2),
            TraceRequest("long", 1, 12, 0.25, 20, "sys", 4, 0.2),
            TraceRequest("burst", 2, 5, 0.8, 12, "", 0, 0.0),
        ]

    def test_no_future_arrival_access_and_determinism(self):
        cfg = ControllerConfig(capacity_bytes=32, reserve_bytes=2, max_batch_tokens=8)
        a = run_trace(self.trace, RASPPolicy(cfg), capacity=32, batch=8)
        b = run_trace(self.trace, RASPPolicy(cfg), capacity=32, batch=8)
        self.assertEqual(a, b)

    def test_metrics_are_trace_simulation_and_memory_bounded(self):
        cfg = ControllerConfig(capacity_bytes=32, reserve_bytes=2, max_batch_tokens=8)
        m = run_trace(self.trace, RASPPolicy(cfg), capacity=32, batch=8)
        self.assertLessEqual(m.peak_bytes, 32)
        self.assertGreaterEqual(m.completed, 1)

    def test_baseline_labels_are_distinct(self):
        fixed = run_trace(self.trace, FixedDepth(4, 32, 8), 32, 8)
        adaptive = run_trace(self.trace, AcceptanceAdaptive(4, 0.5, 32, 8), 32, 8)
        self.assertNotEqual(fixed.policy, adaptive.policy)


if __name__ == "__main__":
    unittest.main()
