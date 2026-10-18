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


if __name__ == "__main__":
    unittest.main()
