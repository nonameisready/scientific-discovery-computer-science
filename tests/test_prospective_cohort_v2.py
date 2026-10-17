import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from research_platform.forecast_engine.core import (
    canonical_json, hash_file, sha256_bytes, validate_prospective_forecast, verify_snapshot_hash,
)


class ProspectiveCohortV2Tests(unittest.TestCase):
    def setUp(self):
        self.cohort = json.loads((ROOT / "data/forecast_engine/prospective_cohort_v2.json").read_text())
        self.monitor = json.loads((ROOT / "data/forecast_engine/prospective_cohort_v2_monitoring.json").read_text())
        self.manifest = json.loads((ROOT / "data/forecast_engine/prospective_cohort_v2_manifest.json").read_text())
        self.report = json.loads((ROOT / "reports/CS_PROSPECTIVE_COHORT_EXPANSION.json").read_text())
        self.activation = json.loads((ROOT / "data/forecast_engine/activated_forecasts.json").read_text())
        self.original_monitor = json.loads((ROOT / "data/forecast_engine/activated_forecast_monitoring.json").read_text())

    def test_frozen_forecast_ids_and_records_are_valid_and_unique(self):
        rows = self.cohort["new_forecasts"]
        self.assertEqual(len(rows), 7)
        self.assertEqual(len({r["event_id"] for r in rows}), 7)
        for row in rows:
            validate_prospective_forecast(row)
            self.assertTrue(row["qualitative_only"])
            self.assertNotIn("probability", row)
            self.assertEqual(row["outcome_status"], "NOT_YET_DUE")
        old = self.cohort["original_cohort"]["records"]
        self.assertEqual(old, self.activation["forecasts"])
        self.assertEqual(self.cohort["forecast_count_total"], 10)
        self.assertEqual(self.cohort["original_cohort"]["source_sha256"], hash_file(ROOT / "data/forecast_engine/activated_forecasts.json"))

    def test_snapshot_and_manifest_hashes(self):
        snapshot = self.cohort["prospective_snapshot"]
        self.assertTrue(verify_snapshot_hash(snapshot))
        self.assertEqual(snapshot["forecast_ids"], [r["event_id"] for r in self.cohort["new_forecasts"]])
        self.assertEqual(self.manifest["snapshot_sha256"], snapshot["snapshot_sha256"])
        self.assertEqual(self.manifest["cohort_sha256"], sha256_bytes(canonical_json(self.cohort)))
        self.assertEqual(self.manifest["monitoring_sha256"], sha256_bytes(canonical_json(self.monitor)))
        self.assertEqual(self.manifest["original_activation_sha256"], hash_file(ROOT / "data/forecast_engine/activated_forecasts.json"))
        self.assertEqual(self.manifest["original_monitoring_sha256"], hash_file(ROOT / "data/forecast_engine/activated_forecast_monitoring.json"))

    def test_monitoring_is_prepared_but_inactive(self):
        self.assertEqual(self.monitor["status"], "PREPARED_INACTIVE")
        self.assertEqual(self.monitor["active_monitoring_count"], 0)
        self.assertEqual(self.monitor["scheduled_jobs"], [])
        self.assertFalse(self.monitor["workers_started"])
        self.assertEqual(self.monitor["original_specifications_copied_unchanged"], self.original_monitor["specifications"])
        self.assertTrue(all(not row["active"] for row in self.monitor["new_specifications"]))

    def test_families_and_targets_remain_explicitly_separate(self):
        assignments = self.cohort["research_family_assignments"]
        self.assertEqual(set(assignments), {r["event_id"] for r in self.activation["forecasts"] + self.cohort["new_forecasts"]})
        dynamic = [r for r in self.cohort["new_forecasts"] if r["event_id"].startswith(("DYNAMIC-MATCHING", "ORS-"))]
        self.assertEqual(len(dynamic), 2)
        self.assertEqual(len({r["research_family_id"] for r in dynamic}), 1)
        self.assertFalse(self.manifest["outcomes_frozen"])
        self.assertFalse(self.manifest["predictive_accuracy_evaluated"])

    def test_screening_counts_and_subfield_labels_are_consistent(self):
        screen = self.report["candidate_discovery"]
        rejected = screen["rejected_or_excluded"]
        self.assertEqual(screen["new_candidate_questions_screened"], 14)
        self.assertEqual(screen["fully_operationalized"] + len(rejected), 14)
        self.assertEqual(len(self.cohort["subfield_assignments"]), 10)
        self.assertEqual(sum(self.cohort["subfield_counts_total"].values()), 10)
        for item in rejected:
            for url in item.get("sources", []):
                self.assertTrue(url.startswith(("https://arxiv.org/", "https://doi.org/", "https://drops.dagstuhl.de/")))


if __name__ == "__main__":
    unittest.main()
