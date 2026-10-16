"""Static CLI for inspecting and versioning qualitative CS forecast snapshots."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile

from .core import (
    ROOT, RADAR_PATH, ForecastEngineError, append_evidence_event, append_snapshot,
    append_adjudication, append_action_outcome,
    baseline_evidence_refs, build_baseline_snapshot, create_qualitative_snapshot,
    diff_snapshots, evaluate_readiness, forecast_request, load_json, make_manifest,
    write_immutable_json, rank_and_freeze_paper4_plan, validate_action_plan, validate_adjudication,
)

BASELINE = ROOT / "data/forecast_engine/qualitative_editorial_baseline_20261016.json"
EVIDENCE_STORE = ROOT / "data/forecast_engine/evidence_events.jsonl"
SNAPSHOT_STORE = ROOT / "data/forecast_engine/followup_snapshots.jsonl"


def _json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def _baseline(path: str | Path = BASELINE) -> dict:
    return load_json(path)


def _candidate(snapshot: dict, question_id: str) -> dict:
    for row in snapshot["candidates"]:
        if row["id"] == question_id:
            return row
    raise ForecastEngineError(f"unknown question ID: {question_id}")


def _read_events() -> list[dict]:
    if not EVIDENCE_STORE.exists():
        return []
    return [json.loads(line) for line in EVIDENCE_STORE.read_text(encoding="utf-8").splitlines() if line.strip()]


def _current_readiness() -> dict:
    direct = load_json(ROOT / "reports/paper3_direct_endpoint_cohort_round6.json")
    trajectory = load_json(ROOT / "reports/paper3_trajectory_readiness.json")
    protocol = load_json(ROOT / "research/paper3_target_b_protocol_v1.json")
    return {
        "status": "NOT_EVALUABLE",
        "target_a": {
            "selected_round6": direct.get("observed_result", {}).get("selected_rows"),
            "eligible_round6": direct.get("observed_result", {}).get("source_eligible_questions"),
            "direct_positive": direct.get("observed_result", {}).get("direct_resolution_positive"),
            "direct_negative": direct.get("observed_result", {}).get("direct_resolution_negative"),
            "unadjudicated": direct.get("followup_audit", {}).get("direct_tuple_adjudication", {}).get("direct_unadjudicated"),
            "gate": protocol["targets"]["A_direct_resolution"]["paper3_score_gate"],
        },
        "target_b": {
            "eligible_questions": len(load_json(ROOT / "reports/historical_evidence_trajectory_round2.json").get("rows", [])),
            "partial_progress_supported": trajectory.get("outcome_counts", {}).get("partial_progress", {}).get("supported"),
            "scope_narrowing_supported": trajectory.get("outcome_counts", {}).get("scope_narrowing_or_reformulation", {}).get("supported"),
            "direct_resolution_class_gate_passed": trajectory.get("class_power_gate", {}).get("passed"),
            "gate": protocol["targets"]["B_substantial_progress"]["paper3_score_gate"],
        },
        "paper4_action_utility": "GATED_UNVALIDATED; five feasibility/gate actions, zero efficacy outcomes; no common complete pre-action ranking.",
        "blockers": ["CS direct labels fail Paper 3 Target A gates.",
                     "Target B cohort does not meet sample/class/group gates; missing is not negative.",
                     "No authenticated temporally validated predictor or calibration artifact.",
                     "No prospective Paper 4 action-utility validation."],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cs-forecast-engine")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("freeze-baseline", help="import the radar as a one-time immutable qualitative snapshot")
    p.add_argument("--source", default=str(RADAR_PATH))
    p.add_argument("--output", default=str(BASELINE))
    p = sub.add_parser("radar", help="list the frozen qualitative editorial candidates")
    p.add_argument("--baseline", default=str(BASELINE))
    p = sub.add_parser("show", help="show a question, original outlook, citations and Paper 4 action proposal")
    p.add_argument("question_id")
    p.add_argument("--baseline", default=str(BASELINE))
    p = sub.add_parser("forecast", help="request a gated forecast")
    p.add_argument("question_id")
    p.add_argument("--mode", required=True, choices=["QUALITATIVE_EDITORIAL", "BASELINE_STATISTICAL", "PAPER3_TRANSFER", "CALIBRATED_BREAKTHROUGH_FORECAST"])
    p.add_argument("--qualitative", action="store_true", help="explicitly permit qualitative-only output")
    p.add_argument("--endpoint", choices=["attention", "resolution", "premise_revision", "evidence_growth", "impact"],
                   help="required distinct target for numeric-mode readiness checks")
    p.add_argument("--baseline", default=str(BASELINE))
    sub.add_parser("readiness", help="show current Paper 3/4 readiness without fitting or scoring")
    p = sub.add_parser("add-evidence", help="append one validated evidence event from a JSON file")
    p.add_argument("record")
    p = sub.add_parser("new-snapshot", help="append a qualitative update; does not perform Bayesian updating")
    p.add_argument("question_id")
    p.add_argument("--as-of", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--baseline", default=str(BASELINE))
    p = sub.add_parser("plan-compare", help="show frozen Paper 4 order beside simple pre-action baselines")
    p.add_argument("plan")
    p = sub.add_parser("freeze-action-plan", help="freeze a complete Paper 4 candidate list and rank before action")
    p.add_argument("input")
    p.add_argument("output")
    p = sub.add_parser("record-action-outcome", help="append an independently coded outcome linked to frozen plan")
    p.add_argument("plan")
    p.add_argument("outcome")
    p.add_argument("store")
    p = sub.add_parser("adjudicate", help="validate and append a human-reviewed outcome record")
    p.add_argument("record")
    p.add_argument("store")
    p = sub.add_parser("history", help="list immutable baseline and follow-up snapshots for one question")
    p.add_argument("question_id")
    p.add_argument("--baseline", default=str(BASELINE))
    p = sub.add_parser("demo", help="run fixture-only acceptance demonstration in a temporary directory")
    p.add_argument("--baseline", default=str(BASELINE))
    return parser


def run(args: argparse.Namespace) -> int:
    if args.command == "freeze-baseline":
        snapshot = build_baseline_snapshot(args.source)
        write_immutable_json(args.output, snapshot)
        _json({"status": "IMPORTED_IMMUTABLE_QUALITATIVE_BASELINE", "path": args.output,
               "snapshot_id": snapshot["snapshot_id"], "question_count": len(snapshot["questions"]),
               "snapshot_sha256": snapshot["snapshot_sha256"]})
    elif args.command == "radar":
        baseline = _baseline(args.baseline)
        _json({"snapshot_id": baseline["snapshot_id"], "forecast_type": baseline["forecast_type"],
               "numerical_predictions_allowed": baseline["numerical_predictions_allowed"],
               "questions": [{"rank": row["rank"], "question_id": row["id"], "title": row["title"],
                              "horizon": row["horizon"], "maturity": row["maturity"]}
                             for row in baseline["candidates"]]})
    elif args.command == "show":
        baseline = _baseline(args.baseline)
        candidate = _candidate(baseline, args.question_id)
        question = next(row for row in baseline["questions"] if row["question_id"] == args.question_id)
        _json({"question": question, "original_qualitative_outlook": candidate["paper3_outlook"],
               "evidence_available_in_original_snapshot": baseline_evidence_refs(baseline, args.question_id),
               "paper4_action_recommendation": candidate["paper4_recommended_action"],
               "paper4_status": "RECOMMENDATION_ONLY_NO_VALIDATED_SUPERIORITY"})
    elif args.command == "forecast":
        result = forecast_request(args.mode, args.question_id, qualitative_allowed=args.qualitative,
                                  snapshot=_baseline(args.baseline), endpoint=args.endpoint,
                                  readiness={"status": "NOT_EVALUABLE", "blockers": _current_readiness()["blockers"]})
        _json(result)
    elif args.command == "readiness":
        _json(_current_readiness())
    elif args.command == "add-evidence":
        record = load_json(args.record)
        append_evidence_event(EVIDENCE_STORE, record)
        _json({"status": "APPENDED_IMMUTABLE_EVIDENCE_EVENT", "evidence_id": record["evidence_id"]})
    elif args.command == "new-snapshot":
        baseline = _baseline(args.baseline)
        events = baseline_evidence_refs(baseline, args.question_id) + _read_events()
        updated = create_qualitative_snapshot(baseline, args.question_id, args.as_of, events, args.reason)
        append_snapshot(SNAPSHOT_STORE, updated)
        _json({"status": "APPENDED_QUALITATIVE_SNAPSHOT", "snapshot": updated,
               "diff": diff_snapshots(baseline, updated)})
    elif args.command == "plan-compare":
        from .core import action_comparison_views, load_json as read_json
        _json(action_comparison_views(read_json(args.plan)))
    elif args.command == "freeze-action-plan":
        frozen = rank_and_freeze_paper4_plan(load_json(args.input))
        write_immutable_json(args.output, frozen)
        _json({"status": "FROZEN_PRE_ACTION_PLAN", "plan_id": frozen["plan_id"],
               "candidate_actions": len(frozen["candidate_actions"]), "frozen_sha256": frozen["frozen_sha256"]})
    elif args.command == "record-action-outcome":
        plan, outcome = load_json(args.plan), load_json(args.outcome)
        append_action_outcome(args.store, outcome, plan)
        _json({"status": "APPENDED_ACTION_OUTCOME", "outcome_id": outcome["outcome_id"],
               "utility_status": outcome["scientific_utility"]})
    elif args.command == "adjudicate":
        record = load_json(args.record)
        append_adjudication(args.store, record)
        _json({"status": "APPENDED_HUMAN_ADJUDICATION", "adjudication_id": record["adjudication_id"],
               "outcome_status": record["status"]})
    elif args.command == "history":
        baseline = _baseline(args.baseline)
        rows = [{"snapshot_id": baseline["snapshot_id"], "as_of": baseline["as_of"],
                 "forecast_type": baseline["forecast_type"]}]
        if SNAPSHOT_STORE.exists():
            for line in SNAPSHOT_STORE.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    if row.get("question_id") == args.question_id:
                        rows.append({"snapshot_id": row["snapshot_id"], "as_of": row["as_of"],
                                     "forecast_type": row["forecast_type"], "change_summary": row["change_summary"]})
        _json({"question_id": args.question_id, "history": rows})
    elif args.command == "demo":
        baseline = _baseline(args.baseline)
        question_id = baseline["candidates"][0]["id"]
        before_hash = baseline["snapshot_sha256"]
        base_refs = baseline_evidence_refs(baseline, question_id)
        late = {
            "evidence_id": "FIXTURE-ONLY-POST-CUTOFF-001", "question_id": question_id,
            "source_identifier": "fixture-source-001", "doi": None, "arxiv_id": None,
            "canonical_url": "https://example.invalid/fixture-only", "publication_date": "2026-10-20",
            "version_date": "2026-10-20", "retrieval_date": "2026-10-21",
            "earliest_verified_availability_date": "2026-10-20", "availability_status": "VERIFIED",
            "availability_basis": "Synthetic software-test fixture; not an actual paper or observation.",
            "evidence_type": "SYNTHETIC_FIXTURE_ONLY", "claim": "Synthetic post-cutoff evidence for cutoff-enforcement tests.",
            "assumptions": [], "contradicts_evidence_ids": [], "source_reliability": "FIXTURE_ONLY",
            "independent_replication_status": "NOT_APPLICABLE", "provenance": {"fixture_only": True},
            "content_sha256": None, "content_hash_scope": "NO_SOURCE_CONTENT",
        }
        from .core import eligible_evidence
        _, cutoff_rejection = eligible_evidence(late, baseline["evidence_cutoff"])
        with tempfile.TemporaryDirectory(prefix="cs-forecast-demo-") as temp:
            updated = create_qualitative_snapshot(baseline, question_id, "2026-10-21T12:00:00Z",
                                                   base_refs + [late],
                                                   "Fixture-only demonstration: a later evidence event is recorded; qualitative outlook intentionally unchanged.")
            append_snapshot(Path(temp) / "snapshots.jsonl", updated)
            diff = diff_snapshots(baseline, updated)
            manifest = make_manifest([args.baseline], ["cs-forecast-engine", "demo"], fixture_only=True)
        not_ready = forecast_request("CALIBRATED_BREAKTHROUGH_FORECAST", question_id,
                                     readiness={"status": "NOT_EVALUABLE", "blockers": _current_readiness()["blockers"]})
        _json({"status": "FIXTURE_DEMONSTRATION_ONLY_NO_SCIENTIFIC_RESULT",
               "question_id": question_id,
               "original_snapshot_id": baseline["snapshot_id"], "original_hash_before": before_hash,
               "original_hash_after": baseline["snapshot_sha256"], "original_sources": base_refs,
               "original_qualitative_outlook": baseline["candidates"][0]["paper3_outlook"],
               "late_fixture_rejected_from_original_cutoff": cutoff_rejection,
               "later_snapshot_id": updated["snapshot_id"], "later_snapshot_included_evidence": updated["included_evidence"],
               "exact_diff": diff, "paper4_action_recommendation": updated["paper4_action_recommendation"],
               "paper4_claim": updated["paper4_action_status"], "numeric_mode": not_ready,
               "current_readiness": _current_readiness(), "manifest": manifest})
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except (ForecastEngineError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
