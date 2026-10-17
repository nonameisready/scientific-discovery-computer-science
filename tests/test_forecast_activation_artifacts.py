import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_forecast_activation_artifacts as activation


class ForecastActivationArtifactTests(unittest.TestCase):
    def test_reviewed_baseline_yields_no_unjustified_forecast(self):
        prospective, monitoring, summary = activation.build_activation("2026-10-17T01:00:50Z")
        self.assertEqual(summary["radar_directions_reviewed"], 12)
        self.assertEqual(summary["candidate_endpoints_assessed"], 12)
        self.assertEqual(prospective["events"], [])
        self.assertEqual(prospective["activation_result"]["prospective_forecasts_frozen"], 0)
        self.assertEqual(prospective["activation_result"]["numeric_forecasts_created"], 0)
        self.assertTrue(all(row["activation_decision"] == "NOT_FROZEN"
                            for row in prospective["candidate_assessments"]))
        self.assertEqual(monitoring["active_monitor_count"], 0)
        self.assertTrue(all(row["status"] == "PREPARATORY_NOT_ACTIVE_FORECAST"
                            for row in monitoring["monitoring_specs"]))
        self.assertTrue(all(len(row["exact_search_phrases_from_frozen_radar"]) == 3
                            for row in monitoring["monitoring_specs"]))
        self.assertTrue(all(row["missing_definition_fields"]
                            for row in prospective["candidate_assessments"]))
        adaptive_ivm = next(row for row in prospective["candidate_assessments"]
                            if row["parent_candidate_id"] == "ADAPTIVE_IVM_WORKLOAD_SHIFT")
        self.assertIn("REFRAME_REQUIRED", adaptive_ivm["status"])

    def test_historical_packets_are_frozen_source_bound_and_candidate_only(self):
        packets = activation.build_historical_packets()
        self.assertEqual(len(packets), 6)
        self.assertEqual(sum(row["track"].endswith("TARGET_A_DIRECT_RESOLUTION") for row in packets), 3)
        self.assertEqual(sum(row["track"].endswith("TARGET_B_SUBSTANTIVE_EVIDENCE_GROWTH") for row in packets), 3)
        for packet in packets:
            self.assertTrue(packet["source_question_id"].endswith(("v1", "v2", "v3")))
            self.assertLessEqual(packet["historical_window"]["cutoff"], packet["historical_window"]["followup_end"])
            self.assertEqual(packet["human_review"]["status"], "PENDING_TWO_INDEPENDENT_HUMAN_REVIEWERS")
            self.assertIsNone(packet["human_review"]["target_a_label"])
            self.assertIsNone(packet["human_review"]["target_b_label"])
            self.assertIsNone(packet["human_review"]["trajectory_label"])
            for evidence in packet["documented_later_evidence"]:
                self.assertEqual(evidence["evidence_status"], "CANDIDATE_OUTCOME_EVIDENCE")
                self.assertEqual(len(evidence["citation_record_sha256"]), 64)
            self.assertFalse(packet["matching_analysis"].get("search_absence_is_negative", False))
        # Target A's selected round-6 cohort keeps its own source task ID rather
        # than being relabeled as the older observable-16 cohort.
        round6 = [row for row in packets if row["track"].endswith("TARGET_A_DIRECT_RESOLUTION")]
        self.assertTrue(all(row["cohort_id"] == "PAPER3-DIRECT-ENDPOINT-COHORT-ROUND6-001"
                            for row in round6))

    def test_builder_creates_new_records_and_refuses_overwrite(self):
        protected = [
            ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json",
            ROOT / "data/forecast_engine/qualitative_editorial_baseline_20261016.json",
            ROOT / "research/paper3_target_b_protocol_v1.json",
            ROOT / "research/historical_evidence_trajectory_protocol_v1.json",
            ROOT / "docs/paper3_methodology.md",
            ROOT / "docs/paper4_methodology.md",
        ]
        before = {path: path.read_bytes() for path in protected}
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            result = activation.build(output, "2026-10-17T01:00:50Z")
            self.assertEqual(result["historical_packets_prepared"], 6)
            event_path = output / "data/forecast_engine/prospective_forecast_events.json"
            data = json.loads(event_path.read_text(encoding="utf-8"))
            self.assertEqual(data["events"], [])
            self.assertEqual(len(list((output / "data/forecast_engine/historical_packets").glob("*.json"))), 6)
            with self.assertRaises(FileExistsError):
                activation.build(output, "2026-10-17T01:00:50Z")
        self.assertEqual(before, {path: path.read_bytes() for path in protected})


if __name__ == "__main__":
    unittest.main()
