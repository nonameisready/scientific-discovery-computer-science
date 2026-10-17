from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import freeze_activated_cs_forecasts as builder  # noqa: E402
from research_platform.forecast_engine.core import (  # noqa: E402
    ForecastEngineError,
    append_snapshot,
    build_prospective_snapshot,
    freeze_prospective_forecast,
    hash_file,
    load_json,
    validate_prospective_forecast,
    verify_snapshot_hash,
    canonical_json,
    sha256_bytes,
)


ISSUED = "2026-10-17T03:00:00Z"


class ProspectiveForecastActivationTests(unittest.TestCase):
    def setUp(self):
        self.drafts = builder.drafts()
        self.forecast = freeze_prospective_forecast(deepcopy(self.drafts[0]), ISSUED)

    def test_freeze_is_directional_point_in_time_and_hash_checked(self):
        self.assertEqual(self.forecast["issued_at"], ISSUED)
        self.assertEqual(self.forecast["evidence_cutoff"], ISSUED)
        self.assertEqual(self.forecast["issue_date"], "2026-10-17")
        self.assertTrue(self.forecast["qualitative_only"])
        self.assertEqual(self.forecast["review_status"], "PENDING_TWO_INDEPENDENT_HUMAN_REVIEWERS")
        self.assertEqual(self.forecast["reviewer_ids"], [])
        self.assertEqual(self.forecast["outcome_status"], "NOT_YET_DUE")
        self.assertEqual(self.forecast["outcome_evidence_ids"], [])
        validate_prospective_forecast(self.forecast)
        tampered = deepcopy(self.forecast)
        tampered["exact_event"] += " Tampered."
        with self.assertRaises(ForecastEngineError):
            validate_prospective_forecast(tampered)

    def test_future_cutoff_source_and_deadline_are_rejected(self):
        future_cutoff = deepcopy(self.drafts[0]) | {"evidence_cutoff": "2026-10-17T03:00:01Z"}
        with self.assertRaises(ForecastEngineError):
            freeze_prospective_forecast(future_cutoff, ISSUED)
        future_source = deepcopy(self.drafts[0])
        future_source["sources"][0]["source_date"] = "2026-10-18"
        with self.assertRaises(ForecastEngineError):
            freeze_prospective_forecast(future_source, ISSUED)
        expired = deepcopy(self.drafts[0]) | {"deadline": "2026-10-16"}
        with self.assertRaises(ForecastEngineError):
            freeze_prospective_forecast(expired, ISSUED)

    def test_empty_nondirectional_and_numeric_forecasts_are_rejected(self):
        empty = deepcopy(self.drafts[0]) | {"forecast_statement": ""}
        with self.assertRaises(ForecastEngineError):
            freeze_prospective_forecast(empty, ISSUED)
        nondirectional = deepcopy(self.drafts[0]) | {"expectation": "NEUTRAL"}
        with self.assertRaises(ForecastEngineError):
            freeze_prospective_forecast(nondirectional, ISSUED)
        numeric = deepcopy(self.drafts[0]) | {"probability_estimate": 0.5}
        with self.assertRaises(ForecastEngineError):
            freeze_prospective_forecast(numeric, ISSUED)

    def test_theorem_forecasts_require_no_empirical_hardware_or_sample_fields(self):
        self.assertEqual(len(self.drafts), 3)
        for draft in self.drafts:
            self.assertTrue(any(term in draft["event_type"] for term in ("THEORETICAL", "ALGORITHM", "THEOREM")))
            frozen = freeze_prospective_forecast(deepcopy(draft), ISSUED)
            self.assertNotIn("hardware", frozen)
            self.assertNotIn("sample_size", frozen)
            self.assertNotIn("benchmark", frozen)
            validate_prospective_forecast(frozen)

    def test_snapshot_and_append_only_history_keep_radar_baseline_immutable(self):
        radar = ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json"
        before_hash = hash_file(radar)
        baseline = load_json(ROOT / "data/forecast_engine/qualitative_editorial_baseline_20261016.json")
        rows = [freeze_prospective_forecast(deepcopy(draft), ISSUED) for draft in self.drafts]
        snapshot = build_prospective_snapshot(
            rows, ISSUED, baseline["snapshot_id"], before_hash,
            [{"path": radar.name, "sha256": before_hash, "scope": "FULL_RADAR_JSON_BYTES_UNMODIFIED"}],
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "snapshots.jsonl"
            append_snapshot(path, snapshot)
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 1)
            with self.assertRaises(ForecastEngineError):
                append_snapshot(path, snapshot)
        self.assertEqual(before_hash, hash_file(radar))
        self.assertEqual(rows[0]["parent_radar_id"], None)

    def test_inactive_monitoring_milestones_use_each_frozen_deadline(self):
        activation, monitoring, _, _ = builder.build(ISSUED)
        self.assertEqual(monitoring["active_monitoring_count"], 0)
        self.assertEqual(monitoring["scheduled_jobs"], [])
        deadlines = {row["event_id"]: row["deadline"] for row in activation["forecasts"]}
        for spec in monitoring["specifications"]:
            self.assertFalse(spec["active"])
            self.assertEqual(spec["milestones"], ["2027-01-01", "2028-12-31", deadlines[spec["event_id"]]])
            self.assertTrue(spec["technical_milestones"])
            self.assertIn("PREMISE_REVISION_NOT_SUCCESS", spec["adjudication"]["outcome_categories"])
            self.assertIn("INSUFFICIENT_EVIDENCE", spec["adjudication"]["outcome_categories"])

    def test_frozen_repository_bundle_is_internally_consistent(self):
        activation = load_json(ROOT / "data/forecast_engine/activated_forecasts.json")
        monitoring = load_json(ROOT / "data/forecast_engine/activated_forecast_monitoring.json")
        report = load_json(ROOT / "reports/CS_BREAKTHROUGH_FORECAST_DISCOVERY_AND_ACTIVATION.json")
        bundle_material = {key: value for key, value in activation.items() if key != "activation_sha256"}
        self.assertEqual(activation["activation_sha256"], sha256_bytes(canonical_json(bundle_material)))
        self.assertEqual(activation["forecast_count"], 3)
        for row in activation["forecasts"]:
            validate_prospective_forecast(row)
        snapshot = activation["prospective_snapshot"]
        self.assertTrue(verify_snapshot_hash(snapshot))
        self.assertEqual(snapshot["snapshot_id"], report["activation_snapshot_id"])
        self.assertEqual(snapshot["snapshot_sha256"], report["activation_snapshot_sha256"])
        self.assertEqual(hash_file(ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json"),
                         activation["baseline"]["sha256"])
        self.assertEqual(monitoring["active_monitoring_count"], 0)
        self.assertEqual(monitoring["scheduled_jobs"], [])
        self.assertIn("Pre-commit audit correction", monitoring["correction_notice"])
        self.assertEqual({row["event_id"] for row in monitoring["specifications"]},
                         {row["event_id"] for row in activation["forecasts"]})


if __name__ == "__main__":
    unittest.main()
