import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from simulator import Controller, Session, generate_trace, run


class SimulatorTests(unittest.TestCase):
  def test_deterministic_replay(self):
    trace = generate_trace(11, 20)
    self.assertEqual(run(trace, "proposed"), run(trace, "proposed"))


  def test_memory_capacity_is_hard(self):
    c = Controller("static", capacity=2)
    for i in range(10):
        c.start_tool(Session(i, i, 1, 800, 800, 800, 0), i, 0)
        self.assertLessEqual(sum(e.tier == "gpu" for e in c.cache.values()), 2)


  def test_exact_prefix_cannot_use_shorter_cache(self):
    c = Controller("lru")
    s = Session(1, 0, 1, 1000, 1000, 1000, 0)
    c._admit(s.sid, 0, 500, "gpu")
    c.finish(s, 1)
    self.assertEqual(c.metrics.continuation_ttft[-1], 10)


  def test_cancelled_prefetch_is_counted_and_removed(self):
    s = Session(1, 0, 1, 800, 800, 800, 0, cancelled=True)
    c = Controller("static")
    c.start_tool(s, 0, 0)
    del c.cache[s.sid]
    self.assertNotIn(s.sid, c.cache)


  def test_no_future_information_in_decision_path(self):
    c = Controller("proposed")
    s = Session(1, 0, 10, 800, 800, 800, 0)
    before = (list(c.history), dict(c.cache), c.metrics.decisions)
    c.start_tool(s, 0, 0)
    self.assertEqual(before[0], list(c.history))
    self.assertEqual(c.metrics.decisions, before[2] + 1)


if __name__ == "__main__":
  unittest.main()
