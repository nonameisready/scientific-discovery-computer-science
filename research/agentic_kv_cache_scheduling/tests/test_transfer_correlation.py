import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from transfer_correlation import correlate_start_complete, transfer_id


class TransferCorrelationTests(unittest.TestCase):
    def test_operation_id_survives_ack_handoff(self):
        self.assertEqual(correlate_start_complete("load_back", 17),
                         ("load_back-17", "load_back-17"))

    def test_direction_is_part_of_id(self):
        self.assertNotEqual(transfer_id("prefetch", 3), transfer_id("backup", 3))

    def test_invalid_direction_rejected(self):
        with self.assertRaises(ValueError):
            transfer_id("unknown", 1)

    def test_negative_operation_rejected(self):
        with self.assertRaises(ValueError):
            transfer_id("load_back", -1)


if __name__ == "__main__":
    unittest.main()
