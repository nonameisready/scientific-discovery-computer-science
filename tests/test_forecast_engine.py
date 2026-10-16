from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

from research_platform.forecast_engine.core import (
    ForecastEngineError, action_comparison_views, append_action_outcome,
    append_adjudication, append_evidence_event, baseline_evidence_refs, classify_evidence_timing,
    build_baseline_snapshot, canonical_json, create_qualitative_snapshot,
    diff_snapshots, eligible_evidence, evaluate_predictions, evaluate_readiness,
    evaluate_prediction_baselines,
    forecast_request, freeze_action_plan, grouped_chronological_split,
    grouped_bootstrap_intervals, rank_and_freeze_paper4_plan, score_declared_paper4_plan,
    hash_file, load_json, sha256_bytes, verify_snapshot_hash,
    write_immutable_json,
)
from research_platform.forecast_engine.cli import _current_readiness

ROOT = Path(__file__).resolve().parents[1]


def assert_schema_conforms(test: unittest.TestCase, value, schema_path: Path):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if "$ref" in schema:
        schema = json.loads((schema_path.parent / schema["$ref"]).read_text(encoding="utf-8"))

    def check(instance, rule, location="$"):
        if "type" in rule:
            expected = rule["type"] if isinstance(rule["type"], list) else [rule["type"]]
            types = {"object": dict, "array": list, "string": str, "boolean": bool,
                     "integer": int, "number": (int, float), "null": type(None)}
            test.assertTrue(any((isinstance(instance, types[t]) and
                                 not (t in {"integer", "number"} and isinstance(instance, bool)))
                                for t in expected), f"{location}: wrong type, expected {expected}")
        if "const" in rule:
            test.assertEqual(instance, rule["const"], location)
        if "enum" in rule:
            test.assertIn(instance, rule["enum"], location)
        if isinstance(instance, dict):
            for key in rule.get("required", []):
                test.assertIn(key, instance, f"{location}.{key}")
            for key, child_rule in rule.get("properties", {}).items():
                if key in instance:
                    check(instance[key], child_rule, f"{location}.{key}")
        if isinstance(instance, list) and "items" in rule:
            for i, item in enumerate(instance):
                check(item, rule["items"], f"{location}[{i}]")
        if isinstance(instance, str):
            if "minLength" in rule:
                test.assertGreaterEqual(len(instance), rule["minLength"], location)
            if "pattern" in rule:
                test.assertRegex(instance, re.compile(rule["pattern"]), location)
            if rule.get("format") == "date":
                test.assertEqual(date.fromisoformat(instance).isoformat(), instance, location)
            if rule.get("format") == "date-time":
                datetime.fromisoformat(instance.replace("Z", "+00:00"))
        if isinstance(instance, list) and "minItems" in rule:
            test.assertGreaterEqual(len(instance), rule["minItems"], location)
        if isinstance(instance, (int, float)) and not isinstance(instance, bool) and "minimum" in rule:
            test.assertGreaterEqual(instance, rule["minimum"], location)

    check(value, schema)


def evidence(**overrides):
    record = {
        "evidence_id": "EV-1", "question_id": "Q-1", "source_identifier": "source-1",
        "canonical_url": "https://example.org/paper", "evidence_type": "PRIMARY_RESULT",
        "claim": "fixture claim", "availability_status": "VERIFIED",
        "earliest_verified_availability_date": "2026-10-20",
        "availability_basis": "fixture timestamp", "retrieval_date": "2026-10-21",
        "content_hash_scope": "NO_SOURCE_CONTENT", "content_sha256": None,
        "supersedes_event_id": None,
    }
    return record | overrides


def action_plan():
    return freeze_action_plan({
        "plan_id": "PLAN-1", "question_id": "Q-1", "decision_timestamp": "2026-10-16T10:00:00Z",
        "hypotheses": [{"id": "H1", "statement": "claim true", "prior": 0.5},
                       {"id": "H2", "statement": "claim false", "prior": 0.5}],
        "evidence_gaps": ["gap"], "planner_weights": {"information_gain": 10, "novelty": 1, "tractability": 1, "cost": 1},
        "observed_provenance_roots": [],
        "candidate_actions": [
            {"action_id": "A", "estimated_cost": 2, "uncertainty_reduction_assumption": 0.3,
             "feasibility_assumption": "fixture", "expected_observations": ["x"],
             "falsification_value_assumption": "fixture", "provenance": {"source": "fixture", "roots": ["root-A"]},
             "tractability_assumption": 0.8,
             "expected_outcomes": {"x": {"H1": 1.0, "H2": 0.0}, "y": {"H1": 0.0, "H2": 1.0}},
             "research_momentum_at_cutoff": 0.1},
            {"action_id": "B", "estimated_cost": 1, "uncertainty_reduction_assumption": 0.2,
             "feasibility_assumption": "fixture", "expected_observations": ["y"],
             "falsification_value_assumption": "fixture", "provenance": {"source": "fixture", "roots": ["root-B"]},
             "tractability_assumption": 0.8,
             "expected_outcomes": {"x": {"H1": 0.5, "H2": 0.5}, "y": {"H1": 0.5, "H2": 0.5}},
             "research_momentum_at_cutoff": 0.5},
        ],
        "ranking": [{"action_id": "A", "rank": 1}, {"action_id": "B", "rank": 2}],
        "selection_rationale": "assumptions only", "assumptions": {"utility_scale": "declared"},
    })


class ForecastEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = build_baseline_snapshot()

    def test_imports_all_twelve_frozen_editorial_candidates_and_citations(self):
        baseline = self.baseline
        source = json.loads((ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json").read_text())
        self.assertEqual(baseline["candidates"], source["candidates"])
        self.assertEqual([q["question_id"] for q in baseline["questions"]], [c["id"] for c in source["candidates"]])
        self.assertEqual(len(baseline["questions"]), 12)
        self.assertEqual(baseline["forecast_type"], "QUALITATIVE_EDITORIAL_BASELINE")
        self.assertFalse(baseline["numerical_predictions_allowed"])
        self.assertIsNone(baseline["paper3_probabilities"])
        self.assertTrue(baseline["evidence_registry"])
        self.assertTrue(all(e["evidence_type"] == "CITATION_RECORD_ONLY" for e in baseline["evidence_registry"]))
        self.assertEqual(baseline["questions"][0]["forecast_horizon"]["start"], "2027-01-01")
        late_horizon = next(q for q in baseline["questions"] if q["forecast_horizon"]["radar_label"] == "2029-2031")
        self.assertEqual(late_horizon["forecast_horizon"]["start"], "2029-01-01")
        self.assertEqual(set(baseline["questions"][0]["outcome_endpoints"]),
                         {"attention", "resolution", "premise_revision", "evidence_growth", "impact"})
        self.assertTrue(verify_snapshot_hash(baseline))
        disk_snapshot = load_json(ROOT / "data/forecast_engine/qualitative_editorial_baseline_20261016.json")
        self.assertEqual(disk_snapshot, baseline)
        self.assertEqual(baseline["source_hashes"][0]["sha256"], hash_file(ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json"))

    def test_immutable_json_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "frozen.json"
            write_immutable_json(path, {"x": 1})
            with self.assertRaises(ForecastEngineError):
                write_immutable_json(path, {"x": 2})
            self.assertEqual(json.loads(path.read_text()), {"x": 1})

    def test_cutoff_is_inclusive_and_post_cutoff_or_unknown_availability_is_quarantined(self):
        self.assertEqual(eligible_evidence(evidence(earliest_verified_availability_date="2026-10-16"), "2026-10-16"),
                         (True, "ELIGIBLE_POINT_IN_TIME_EVIDENCE"))
        self.assertEqual(eligible_evidence(evidence(earliest_verified_availability_date="2026-10-17"), "2026-10-16"),
                         (False, "POST_CUTOFF_EVIDENCE"))
        self.assertEqual(eligible_evidence(evidence(availability_status="UNKNOWN", earliest_verified_availability_date=None), "2026-10-16"),
                         (False, "QUARANTINED_AVAILABILITY_UNVERIFIED"))
        self.assertEqual(classify_evidence_timing(evidence(earliest_verified_availability_date="2026-10-16",
                                                           retrieval_date="2026-10-20"), "2026-10-16"),
                         "LATE_DISCOVERED_BUT_VERIFIED_AVAILABLE_AT_CUTOFF")
        self.assertEqual(classify_evidence_timing(evidence(earliest_verified_availability_date="2026-10-17"), "2026-10-16"),
                         "POST_CUTOFF_EVIDENCE")
        with self.assertRaises(ForecastEngineError):
            eligible_evidence(evidence(earliest_verified_availability_date="2026-10-16garbage"), "2026-10-16")
        with self.assertRaises(ForecastEngineError):
            eligible_evidence(evidence(earliest_verified_availability_date="2026-10-20", retrieval_date="2026-10-19"), "2026-10-21")

    def test_evidence_events_are_append_only_idempotent_and_supersession_linked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            row = evidence()
            append_evidence_event(path, row)
            append_evidence_event(path, row)
            self.assertEqual(len(path.read_text().splitlines()), 1)
            with self.assertRaises(ForecastEngineError):
                append_evidence_event(path, row | {"claim": "changed"})
            with self.assertRaises(ForecastEngineError):
                append_evidence_event(path, evidence(evidence_id="EV-2", supersedes_event_id="missing"))
            append_evidence_event(path, evidence(evidence_id="EV-2", supersedes_event_id="EV-1"))
            self.assertEqual(len(path.read_text().splitlines()), 2)

    def test_new_snapshot_rejects_post_cutoff_from_original_but_records_later_fixture_and_exact_diff(self):
        baseline = self.baseline
        qid = baseline["candidates"][0]["id"]
        late = evidence(question_id=qid)
        new = create_qualitative_snapshot(baseline, qid, "2026-10-21T12:00:00Z",
                                          baseline_evidence_refs(baseline, qid) + [late], "fixture follow-up")
        diff = diff_snapshots(baseline, new)
        self.assertTrue(verify_snapshot_hash(baseline))
        self.assertEqual(baseline["snapshot_sha256"], self.baseline["snapshot_sha256"])
        self.assertIn("EV-1", [row["evidence_id"] for row in new["included_evidence"]])
        self.assertEqual(eligible_evidence(late, baseline["evidence_cutoff"])[1], "POST_CUTOFF_EVIDENCE")
        self.assertEqual(diff["added_evidence_ids"], ["EV-1"])
        self.assertFalse(diff["outlook_changed"])
        self.assertEqual(new["paper4_action_status"], "RECOMMENDATION_ONLY_NO_VALIDATED_SUPERIORITY")
        self.assertTrue(verify_snapshot_hash(new))
        self.assertEqual(new["included_evidence"][-1]["hash_scope"], "CANONICAL_URL_STRING_ONLY")
        future_retrieval = late | {"evidence_id": "EV-FUTURE-RETRIEVAL", "retrieval_date": "2026-10-22"}
        quarantined = create_qualitative_snapshot(baseline, qid, "2026-10-21T12:00:00Z", [future_retrieval], "future retrieval")
        self.assertEqual(quarantined["quarantined_evidence"][0]["status"], "RETRIEVED_AFTER_SNAPSHOT_AS_OF")

    def test_unknown_question_and_prebaseline_snapshot_are_rejected(self):
        with self.assertRaises(ForecastEngineError):
            create_qualitative_snapshot(self.baseline, "NO-SUCH-Q", "2026-10-21T00:00:00Z", [], "x")
        with self.assertRaises(ForecastEngineError):
            create_qualitative_snapshot(self.baseline, self.baseline["candidates"][0]["id"],
                                        "2026-10-15T00:00:00Z", [], "x")

    def test_qualitative_output_requires_opt_in_and_numeric_modes_fail_closed(self):
        qid = self.baseline["candidates"][0]["id"]
        self.assertEqual(forecast_request("QUALITATIVE_EDITORIAL", qid)["status"], "NOT_READY")
        result = forecast_request("QUALITATIVE_EDITORIAL", qid, qualitative_allowed=True, snapshot=self.baseline)
        self.assertEqual(result["status"], "QUALITATIVE_ONLY")
        self.assertIsNone(result["probabilities"])
        for mode in ("BASELINE_STATISTICAL", "PAPER3_TRANSFER", "CALIBRATED_BREAKTHROUGH_FORECAST"):
            output = forecast_request(mode, qid, endpoint="resolution", authorized=True,
                                      readiness={"status": "NOT_EVALUABLE", "blockers": ["no labels"]})
            self.assertEqual(output["status"], "NOT_READY")
            self.assertIsNone(output["prediction"])

    def test_outcome_missing_is_not_negative_and_endpoint_semantics_are_separate(self):
        base = {"adjudication_id": "J1", "question_id": "Q1", "endpoint": "resolution",
                "forecast_cutoff": "2020-01-01", "due_date": "2025-01-01", "observation_end": "2024-01-01",
                "status": "NOT_YET_DUE", "evidence_ids": [], "assumptions_match": False,
                "comparator_match": False, "metric_match": False, "reviewer_ids": [],
                "independent_review_status": "PENDING", "relation_to_frozen_question": "not yet adjudicated",
                "missingness_status": "INCOMPLETE", "criterion_version": "v1"}
        from research_platform.forecast_engine.core import validate_adjudication
        validate_adjudication(base)
        with self.assertRaises(ForecastEngineError):
            validate_adjudication(base | {"status": "AUTHENTICATED_SUBSTANTIVE_PROGRESS"})
        with self.assertRaises(ForecastEngineError):
            validate_adjudication(base | {"status": "INSUFFICIENT_EVIDENCE", "missingness_status": "NEGATIVE_OUTCOME"})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "adjudications.jsonl"
            append_adjudication(path, base)
            append_adjudication(path, base)
            self.assertEqual(len(path.read_text().splitlines()), 1)

    def test_not_yet_due_and_unresolved_horizon_gates(self):
        from research_platform.forecast_engine.core import validate_adjudication
        base = {"adjudication_id": "J", "question_id": "Q", "endpoint": "resolution",
                "forecast_cutoff": "2020-01-01", "due_date": "2025-01-01", "observation_end": "2025-01-01",
                "status": "NOT_YET_DUE", "evidence_ids": [], "assumptions_match": False,
                "comparator_match": False, "metric_match": False, "reviewer_ids": [],
                "independent_review_status": "PENDING", "relation_to_frozen_question": "not yet adjudicated",
                "missingness_status": "INCOMPLETE", "criterion_version": "v1"}
        with self.assertRaises(ForecastEngineError):
            validate_adjudication(base)
        with self.assertRaises(ForecastEngineError):
            validate_adjudication(base | {"status": "VERIFIED_UNRESOLVED_AT_HORIZON", "missingness_status": "INCOMPLETE"})

    def test_action_plan_hash_comparators_and_feasibility_are_not_utility(self):
        plan = action_plan()
        scored = score_declared_paper4_plan(plan)
        self.assertEqual(scored["status"], "ASSUMPTION_BASED_PAPER4_PLAN_ONLY")
        self.assertEqual(scored["ranking"][0]["action_id"], "A")
        self.assertIn("not observed action utility", scored["note"])
        draft = dict(plan)
        draft.pop("frozen_sha256")
        ranked_frozen = rank_and_freeze_paper4_plan(draft)
        self.assertEqual(ranked_frozen["ranking"][0]["action_id"], "A")
        self.assertTrue(ranked_frozen["frozen_sha256"])
        views = action_comparison_views(plan)
        self.assertEqual(views["paper4_rank_frozen"], ["A", "B"])
        self.assertEqual(views["lowest_assumed_cost"], ["B", "A"])
        self.assertTrue(any("None measures realized" in s for s in views["interpretation"]))
        with self.assertRaises(ForecastEngineError):
            append_action_outcome(Path(tempfile.gettempdir()) / "unused-action-test.jsonl", {
                "outcome_id": "O", "plan_id": "PLAN-1", "action_id": "A", "performed_at": "2026-01-01T00:00:00Z",
                "feasibility_status": "BLOCKED", "actual_resource_cost": None, "observed_evidence_ids": [],
                "independent_verification_status": "NOT_APPLICABLE", "uncertainty_resolved": None,
                "scientific_utility": "VERIFIED_NOT_USEFUL",
            }, plan)
        corrupted = dict(plan) | {"ranking": [{"action_id": "B", "rank": 1}, {"action_id": "A", "rank": 2}]}
        with self.assertRaises(ForecastEngineError):
            action_comparison_views(corrupted)
        duplicate_rank = dict(plan) | {"ranking": [{"action_id": "A", "rank": 1}, {"action_id": "B", "rank": 1}]}
        with self.assertRaises(ForecastEngineError):
            action_comparison_views(duplicate_rank)

    def test_action_outcome_valid_utility_requires_evidence_and_external_review(self):
        plan = action_plan()
        base = {"outcome_id": "O1", "plan_id": plan["plan_id"], "action_id": "A",
                "performed_at": "2026-10-20T00:00:00Z", "feasibility_status": "EXECUTED",
                "actual_resource_cost": 1.5, "observed_evidence_ids": ["E1"],
                "independent_verification_status": "VERIFIED", "uncertainty_resolved": True,
                "scientific_utility": "VERIFIED_USEFUL"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "outcomes.jsonl"
            append_action_outcome(path, base, plan)
            self.assertEqual(len(path.read_text().splitlines()), 1)
            with self.assertRaises(ForecastEngineError):
                append_action_outcome(path, base, plan)
            with self.assertRaises(ForecastEngineError):
                append_action_outcome(Path(tmp) / "bad.jsonl", base | {"actual_resource_cost": -1}, plan)

    def test_readiness_remains_no_score_for_real_current_data(self):
        current = _current_readiness()
        self.assertEqual(current["target_a"]["eligible_round6"], 6)
        self.assertEqual(current["target_a"]["unadjudicated"], 6)
        self.assertEqual(current["target_b"]["eligible_questions"], 12)
        readiness = evaluate_readiness([], "resolution", authorized=True)
        self.assertEqual(readiness["status"], "NOT_EVALUABLE")
        self.assertIsNone(readiness["metrics"])
        self.assertTrue(any("at least" in reason for reason in readiness["blockers"]))
        output = evaluate_predictions([0, 1], [0.2, 0.8], readiness, authorized=True)
        self.assertEqual(output["status"], "NOT_EVALUABLE")
        self.assertIsNone(output["metrics"])
        comparison = evaluate_prediction_baselines([0, 1], {"prevalence": [0.5, 0.5]}, readiness, authorized=True)
        self.assertEqual(comparison["status"], "NOT_EVALUABLE")
        self.assertIsNone(comparison["methods"]["prevalence"]["metrics"])

    def test_gated_metric_pipeline_reports_class_imbalance_and_calibration_when_ready(self):
        readiness = {"status": "READY", "blockers": []}
        result = evaluate_predictions([0, 1, 0, 1], [0.1, 0.8, 0.4, 0.9], readiness, authorized=True)
        self.assertEqual(result["status"], "EVALUATED")
        self.assertEqual(result["metrics"]["positive_count"], 2)
        self.assertEqual(result["metrics"]["negative_count"], 2)
        self.assertIn("log_loss", result["metrics"])
        self.assertIn("expected_calibration_error_10_bins", result["metrics"])
        comparison = evaluate_prediction_baselines(
            [0, 1, 0, 1], {"text": [0.2, 0.7, 0.3, 0.8], "momentum": [0.4, 0.6, 0.5, 0.7]},
            readiness, authorized=True)
        self.assertEqual(comparison["status"], "EVALUATED")
        self.assertEqual(set(comparison["methods"]), {"momentum", "text"})

    def test_ready_requires_complete_sample_class_group_and_untouched_final_test(self):
        rows = []
        for split in ("train", "validation", "final_test"):
            for i in range(10):
                positive = i < 5
                rows.append({"endpoint": "evidence_growth", "status": "AUTHENTICATED_SUBSTANTIVE_PROGRESS" if positive else "VERIFIED_UNRESOLVED_AT_HORIZON",
                             "reviewer_ids": ["r1", "r2"], "question_family_id": f"{split}-family-{i}",
                             "split_name": split, "untouched_final_test": split == "final_test"})
        result = evaluate_readiness(rows, "evidence_growth", authorized=True)
        self.assertEqual(result["status"], "READY")
        moved = [row | {"question_family_id": "shared"} if row["split_name"] == "train" else row for row in rows]
        moved = [row | {"question_family_id": "shared"} if row["split_name"] == "validation" else row for row in moved]
        blocked = evaluate_readiness(moved, "evidence_growth", authorized=True)
        self.assertEqual(blocked["status"], "NOT_EVALUABLE")
        self.assertTrue(any("crosses chronological splits" in msg for msg in blocked["blockers"]))

    def test_chronological_split_excludes_family_crossing_cutoff(self):
        records = [
            {"cutoff_date": "2020-01-01", "question_family_id": "A"},
            {"cutoff_date": "2021-01-01", "question_family_id": "A"},
            {"cutoff_date": "2019-01-01", "question_family_id": "B"},
            {"cutoff_date": "2022-01-01", "question_family_id": "C"},
        ]
        train, test = grouped_chronological_split(records, "2020-12-31")
        self.assertEqual([row["question_family_id"] for row in train], ["B"])
        self.assertEqual([row["question_family_id"] for row in test], ["C"])

    def test_cluster_bootstrap_is_deterministic_and_not_a_current_forecast(self):
        args = ([0, 1, 0, 1], [0.1, 0.9, 0.2, 0.8], ["g1", "g1", "g2", "g2"])
        a = grouped_bootstrap_intervals(*args, repetitions=100, seed=4)
        b = grouped_bootstrap_intervals(*args, repetitions=100, seed=4)
        self.assertEqual(a, b)
        self.assertEqual(a["status"], "FIXTURE_OR_AUTHORIZED_ANALYSIS_ONLY")

    def test_demo_cli_executes_fixture_only_complete_path_and_emits_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseline_path = Path(tmp) / "baseline.json"
            write_immutable_json(baseline_path, self.baseline)
            proc = subprocess.run([sys.executable, str(ROOT / "scripts/cs_forecast_engine.py"), "demo",
                                   "--baseline", str(baseline_path)], cwd=ROOT, capture_output=True, text=True,
                                   env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")}, check=True)
            result = json.loads(proc.stdout)
            self.assertEqual(result["status"], "FIXTURE_DEMONSTRATION_ONLY_NO_SCIENTIFIC_RESULT")
            self.assertEqual(result["original_hash_before"], result["original_hash_after"])
            self.assertEqual(result["late_fixture_rejected_from_original_cutoff"], "POST_CUTOFF_EVIDENCE")
            self.assertEqual(result["numeric_mode"]["status"], "NOT_READY")
            self.assertTrue(result["manifest"]["fixture_only"])
            self.assertFalse(result["manifest"]["scientific_claim"])
            self.assertFalse(result["exact_diff"]["outlook_changed"])

    def test_append_snapshot_checks_integrity_and_immutability(self):
        qid = self.baseline["candidates"][0]["id"]
        update = create_qualitative_snapshot(self.baseline, qid, "2026-10-21T00:00:00Z", [], "no change")
        from research_platform.forecast_engine.core import append_snapshot
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "snapshots.jsonl"
            append_snapshot(path, update)
            with self.assertRaises(ForecastEngineError):
                append_snapshot(path, update)
            corrupted = update | {"qualitative_outlook": {"attention": "altered"}}
            with self.assertRaises(ForecastEngineError):
                append_snapshot(Path(tmp) / "corrupt.jsonl", corrupted)

    def test_json_schemas_are_valid_json_and_explicitly_machine_readable(self):
        paths = sorted((ROOT / "schemas/forecast_engine").glob("*.schema.json"))
        self.assertGreaterEqual(len(paths), 7)
        for path in paths:
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(schema["type"], "object")
            self.assertTrue(schema["required"])
        schemas = ROOT / "schemas/forecast_engine"
        assert_schema_conforms(self, self.baseline, schemas / "forecast_snapshot.schema.json")
        for question in self.baseline["questions"]:
            assert_schema_conforms(self, question, schemas / "research_question.schema.json")
        for item in self.baseline["evidence_registry"]:
            assert_schema_conforms(self, item, schemas / "evidence_item.schema.json")
        assert_schema_conforms(self, action_plan(), schemas / "paper4_action_plan.schema.json")
        assert_schema_conforms(self, {"manifest_version": "1.0", "generated_at": "2026-10-16T00:00:00Z",
                                      "command": ["demo"], "inputs": [{"path": "fixture", "sha256": None}],
                                      "fixture_only": True, "scientific_claim": False},
                              schemas / "reproducibility_manifest.schema.json")
        assert_schema_conforms(self, {
            "adjudication_id": "fixture", "question_id": "Q", "endpoint": "resolution",
            "forecast_cutoff": "2020-01-01", "due_date": "2025-01-01", "observation_end": "2024-01-01",
            "status": "NOT_YET_DUE", "evidence_ids": [], "assumptions_match": False,
            "comparator_match": False, "metric_match": False, "reviewer_ids": [],
            "independent_review_status": "PENDING", "relation_to_frozen_question": "not yet adjudicated",
            "missingness_status": "INCOMPLETE", "criterion_version": "v1",
        }, schemas / "outcome_adjudication.schema.json")
        assert_schema_conforms(self, {
            "outcome_id": "fixture", "plan_id": "P", "action_id": "A", "performed_at": "2026-10-16T00:00:00Z",
            "feasibility_status": "BLOCKED", "actual_resource_cost": None, "observed_evidence_ids": [],
            "uncertainty_resolved": None, "scientific_utility": "NOT_ADJUDICATED",
            "independent_verification_status": "NOT_APPLICABLE",
        }, schemas / "paper4_action_outcome.schema.json")

    def test_engine_import_does_not_mutate_frozen_paper3_paper4_artifacts(self):
        frozen = [ROOT / "docs/paper3_methodology.md", ROOT / "docs/paper4_methodology.md",
                  ROOT / "research/paper3_target_b_protocol_v1.json",
                  ROOT / "research/historical_outcome_label_protocol_v1.json",
                  ROOT / "data/historical_cs_blind_cohort_20.jsonl"]
        before = {str(path): hash_file(path) for path in frozen}
        build_baseline_snapshot()
        after = {str(path): hash_file(path) for path in frozen}
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
