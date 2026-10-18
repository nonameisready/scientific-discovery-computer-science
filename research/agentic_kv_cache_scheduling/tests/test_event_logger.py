import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from event_logger import EventLog


def transfer(event, timestamp, generation=1, transfer_id="t1"):
    return {"schema": "agentic-kv/events/v1", "event": event,
            "timestamp_ms": timestamp, "session_id": "s1",
            "generation": generation, "transfer_id": transfer_id,
            "source": "remote", "destination": "gpu", "bytes": 1024}


class EventLogTests(unittest.TestCase):
    def test_complete_transfer_is_a_valid_lifecycle(self):
        log = EventLog()
        log.extend([transfer("transfer_enqueue", 1), transfer("transfer_start", 2),
                    transfer("transfer_complete", 3)])
        self.assertEqual(log.audit().as_dict(),
                         {"ok": True, "errors": [], "transfer_count": 1,
                          "completed_transfers": 1, "cancelled_transfers": 0})

    def test_stale_generation_is_rejected(self):
        log = EventLog()
        log.extend([transfer("transfer_enqueue", 1, generation=1),
                    transfer("transfer_cancel", 2, generation=2)])
        audit = log.audit().as_dict()
        self.assertFalse(audit["ok"])
        self.assertIn("stale transfer generation", audit["errors"][0])

    def test_unfinished_transfer_is_rejected(self):
        log = EventLog()
        log.append(transfer("transfer_enqueue", 1))
        audit = log.audit().as_dict()
        self.assertFalse(audit["ok"])
        self.assertIn("unfinished transfer", audit["errors"][0])

    def test_global_time_cannot_go_backwards(self):
        log = EventLog()
        log.append(transfer("transfer_enqueue", 10))
        with self.assertRaises(ValueError):
            log.append(transfer("transfer_start", 9))


if __name__ == "__main__":
    unittest.main()
