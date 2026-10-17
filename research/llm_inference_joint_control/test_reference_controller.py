import unittest

from .reference_controller import ControllerConfig, RequestState, ShadowPriceController


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.cfg = ControllerConfig(capacity_bytes=20, reserve_bytes=2, max_batch_tokens=8)

    def test_peak_memory_is_hard_bounded(self):
        ctl = ShadowPriceController(self.cfg)
        reqs = [RequestState("a", 20, 4, 0, 0, 1.0, 8), RequestState("b", 20, 4, 0, 0, 1.0, 8)]
        for d in ctl.decide(reqs, used_bytes=8):
            self.assertLessEqual(d.peak_bytes, 18)

    def test_rejected_speculation_does_not_become_persistent_kv(self):
        ctl = ShadowPriceController(self.cfg)
        low = RequestState("low", 20, 4, 0, 0, 0.1, 6)
        high = RequestState("high", 20, 4, 0, 0, 1.0, 6)
        low_candidate = ctl._candidate(low, 6, used=0)
        high_candidate = ctl._candidate(high, 6, used=0)
        self.assertLessEqual(low_candidate.persistent_bytes, low_candidate.speculative_tokens)
        self.assertLessEqual(high_candidate.persistent_bytes, high_candidate.speculative_tokens)

    def test_feedback_changes_future_pressure_price(self):
        ctl = ShadowPriceController(self.cfg)
        before = ctl.decide([RequestState("a", 20, 0, 0, 0, 1, 6)], 0)[0].score
        ctl.update_feedback(pressure=4, evictions=3, recompute_tokens=4)
        after = ctl.decide([RequestState("a", 20, 0, 0, 0, 1, 6)], 0)[0].score
        self.assertLess(after, before)

    def test_deterministic_tie_break(self):
        ctl = ShadowPriceController(self.cfg)
        reqs = [RequestState("z", 2, 0, 0, 0, 1, 0), RequestState("a", 2, 0, 0, 0, 1, 0)]
        self.assertEqual([d.request_id for d in ctl.decide(reqs, 0)], ["a", "z"])


if __name__ == "__main__":
    unittest.main()
