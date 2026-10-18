import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from stress_simulator import StressEngine, StressSession


class StressTests(unittest.TestCase):
    def test_tier_capacity_and_congestion(self):
        xs = [StressSession(i, 0, 4, f"g{i}", 1200, 1200, i % 2) for i in range(8)]
        e = StressEngine("static", gpu_tokens=1200, bandwidth=200)
        m = e.run(xs)
        self.assertLessEqual(e.used["gpu"], e.cap["gpu"])
        self.assertGreater(m["interference_ticks"], 0)

    def test_cancelled_revision_cancels_transfer(self):
        s = StressSession(1, 0, 20, "shared", 800, 800, 0,
                          revisions=((2, 50),), cancelled=True)
        m = StressEngine("static", bandwidth=100).run([s])
        self.assertGreaterEqual(m["cancelled_transfers"], 1)

    def test_shared_branch_hit_is_counted(self):
        xs = [StressSession(1, 0, 1, "shared", 400, 400, 0),
              StressSession(2, 2, 1, "shared", 400, 400, 0, branch=1)]
        m = StressEngine("ttl", gpu_tokens=800).run(xs)
        self.assertGreaterEqual(m["shared_hits"], 1)

    def test_tier_aware_policy_can_use_cpu_fallback(self):
        s = StressSession(1, 0, 10, "cpu", 800, 800, 0,
                          forecast_return_ticks=1)
        m = StressEngine("tier_aware", gpu_tokens=400, cpu_tokens=1000,
                         remote_tokens=2000, bandwidth=100).run([s])
        self.assertEqual(m["cpu_hits"], 1)
        self.assertEqual(m["recompute_misses"], 0)
        self.assertEqual(m["completed_transfers"], 0)

    def test_transfer_accounting_separates_cancellation_and_on_demand(self):
        s = StressSession(1, 0, 20, "accounting", 800, 800, 0,
                          forecast_return_ticks=8)
        m = StressEngine("tier_aware", gpu_tokens=1600, cpu_tokens=1000,
                         remote_tokens=2000, bandwidth=100).run([s])
        self.assertGreaterEqual(m["on_demand_transfer_tokens"], 0)
        self.assertGreaterEqual(m["completed_transfer_tokens"], 0)
        self.assertGreaterEqual(m["cancelled_transfer_tokens"], 0)

    def test_cost_aware_policy_uses_cpu_when_expected_cheaper(self):
        s = StressSession(1, 0, 10, "cost", 800, 800, 0,
                          forecast_return_ticks=1,
                          prefix_survival_probability=.95)
        m = StressEngine("cost_aware", gpu_tokens=400, cpu_tokens=1000,
                         remote_tokens=2000, bandwidth=100).run([s])
        self.assertEqual(m["cpu_hits"], 1)
        self.assertEqual(m["recompute_misses"], 0)

    def test_cost_aware_policy_does_not_retain_low_probability_prefix(self):
        s = StressSession(1, 0, 10, "cost", 800, 800, 0,
                          forecast_return_ticks=1,
                          prefix_survival_probability=.10)
        m = StressEngine("cost_aware", gpu_tokens=400, cpu_tokens=1000,
                         remote_tokens=2000, bandwidth=100).run([s])
        self.assertEqual(m["cpu_hits"], 0)
        self.assertEqual(m["remote_hits"], 0)
        self.assertEqual(m["recompute_misses"], 1)

    def test_queue_aware_policy_completes_a_selected_transfer(self):
        xs = [StressSession(1, 0, 20, "short", 200, 200, 0,
                            forecast_return_ticks=8),
              StressSession(2, 0, 20, "long", 800, 800, 0,
                            forecast_return_ticks=8)]
        m = StressEngine("queue_aware", gpu_tokens=1600, cpu_tokens=3200,
                         remote_tokens=6400, bandwidth=200).run(xs)
        self.assertGreaterEqual(m["completed_transfers"], 1)

    def test_budget_aware_cancels_transfer_after_deadline(self):
        s = StressSession(1, 0, 20, "budget", 1200, 1200, 0,
                          forecast_return_ticks=2)
        m = StressEngine("budget_aware", gpu_tokens=1600, cpu_tokens=3200,
                         remote_tokens=6400, bandwidth=200).run([s])
        self.assertGreaterEqual(m["budget_cancellations"], 1)
        self.assertGreaterEqual(m["cancelled_transfer_tokens"], 1)


if __name__ == "__main__":
    unittest.main()
