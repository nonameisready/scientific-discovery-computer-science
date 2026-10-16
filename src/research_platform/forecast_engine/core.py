"""Small append-only forecasting core. No model inference or experiment execution."""
from __future__ import annotations

from datetime import date, datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[3]
RADAR_PATH = ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json"
PAPER3_TARGETS_PATH = ROOT / "research/paper3_target_b_protocol_v1.json"
MODES = {
    "QUALITATIVE_EDITORIAL",
    "BASELINE_STATISTICAL",
    "PAPER3_TRANSFER",
    "CALIBRATED_BREAKTHROUGH_FORECAST",
}
OPERATIONAL_OUTCOMES = {
    "AUTHENTICATED_RESOLUTION",
    "AUTHENTICATED_REFUTATION_OR_PREMISE_REVISION",
    "AUTHENTICATED_SUBSTANTIVE_PROGRESS",
    "VERIFIED_UNRESOLVED_AT_HORIZON",
    "INSUFFICIENT_EVIDENCE",
    "NOT_YET_DUE",
}


class ForecastEngineError(ValueError):
    """Invalid, inconsistent, or non-point-in-time forecast-engine record."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_file(path: str | Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_date(value: str | None, field: str) -> date:
    if not value:
        raise ForecastEngineError(f"{field} is required")
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value:
            raise ValueError(value)
        return parsed
    except (TypeError, ValueError) as exc:
        raise ForecastEngineError(f"{field} must be an ISO date") from exc


def canonical_question(candidate: dict[str, Any], cutoff: str = "2026-10-16") -> dict[str, Any]:
    """Adapt a radar entry without inventing assumptions or frozen endpoints."""
    question_id = candidate.get("id")
    if not question_id or not candidate.get("precise_question"):
        raise ForecastEngineError("radar entry needs stable id and precise_question")
    starts = {"2027-2028": "2027-01-01", "2029-2031": "2029-01-01"}
    ends = {"2027-2028": "2028-12-31", "2029-2031": "2031-12-31"}
    if candidate["horizon"] not in starts:
        raise ForecastEngineError(f"unsupported frozen horizon: {candidate['horizon']}")
    end = ends[candidate["horizon"]]
    return {
        "question_id": question_id,
        "subfield": candidate["subfield"],
        "problem_statement": candidate["precise_question"],
        "operational_assumptions": {"status": "NOT_FULLY_SPECIFIED", "items": []},
        "existing_strongest_baseline": candidate["strongest_baseline"],
        "desired_improvement": candidate["objective_milestone"],
        "evidence_cutoff": cutoff,
        "forecast_horizon": {"start": starts[candidate["horizon"]], "due_date": end, "radar_label": candidate["horizon"]},
        "outcome_endpoints": {
            "attention": {"status": "EDITORIAL_ONLY_NOT_OPERATIONALIZED", "source_text": candidate["paper3_outlook"]["attention"], "criterion": None},
            "resolution": {"status": "MILESTONE_ONLY_NOT_FULLY_OPERATIONALIZED", "criterion": candidate["objective_milestone"]},
            "premise_revision": {"status": "EDITORIAL_ONLY_NOT_OPERATIONALIZED", "source_text": candidate["paper3_outlook"]["premise_revision"], "criterion": None},
            "evidence_growth": {"status": "OPERATIONAL_CATEGORIES_FROZEN_BY_PAPER3_TARGET_B_PROTOCOL", "protocol": "PAPER3-TARGET-B-EVIDENCE-GROWTH-V1"},
            "impact": {"status": "DESCRIPTIVE_NOT_A_FORECAST_EVENT", "description": candidate["potential_impact"], "criterion": None},
        },
        "resolution_criteria": {
            "status": "MILESTONE_ONLY_NOT_FULLY_OPERATIONALIZED",
            "candidate_criterion": candidate["objective_milestone"],
            "missing": ["numeric acceptance threshold", "frozen population/workload or theorem scope", "complete falsification threshold"],
        },
        "required_evidence_standard": "Dated primary-source evidence matching the frozen object, assumptions, comparator and endpoint; independent adjudication required.",
        "outcome_adjudication_policy": "Use the CS operational outcome schema; missing evidence is not a negative outcome; do not map to source-native Paper 3 classes without the pinned taxonomy.",
        "source_provenance": [{
            "url": url,
            "citation_record_sha256": sha256_bytes(url.encode("utf-8")),
            "hash_scope": "URL_STRING_ONLY_FULL_SOURCE_NOT_HASHED",
        } for url in candidate.get("primary_sources", [])],
        "question_version": 1,
        "origin": "QUALITATIVE_EDITORIAL_BASELINE",
        "maturity": candidate["maturity"],
        "impact_assessment": {
            "description": candidate["potential_impact"],
            "event_forecast": False,
            "status": "DESCRIPTIVE_NOT_OPERATIONALIZED",
        },
    }


def build_baseline_snapshot(radar_path: str | Path = RADAR_PATH,
                            baseline_timestamp: str = "2026-10-16T19:19:48-04:00") -> dict[str, Any]:
    """Import the radar exactly as a qualitative snapshot; never infer probabilities."""
    path = Path(radar_path)
    radar = load_json(path)
    if radar.get("report_id") != "FUTURE-CS-BREAKTHROUGH-RADAR-20261016" or len(radar.get("candidates", [])) != 12:
        raise ForecastEngineError("unexpected radar source; expected frozen 12-question 2026-10-16 report")
    candidates = sorted(radar["candidates"], key=lambda row: row["rank"])
    ids = [item.get("id") for item in candidates]
    if len(ids) != len(set(ids)) or ids != [item["id"] for item in candidates]:
        raise ForecastEngineError("baseline candidates must have unique stable IDs in preserved rank order")
    cutoff = radar["as_of"]
    source_hash = hash_file(path)
    snapshot = {
        "schema_version": "1.0",
        "snapshot_id": f"SNAP-QUAL-EDITORIAL-20261016-{source_hash[:12]}",
        "as_of": baseline_timestamp,
        "evidence_cutoff": cutoff,
        "method_version": "forecast-engine-0.1.0",
        "candidate_set_version": radar["report_id"],
        "source_hashes": [{"path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name,
                           "sha256": source_hash, "scope": "FULL_RADAR_JSON_BYTES"}],
        "forecast_type": "QUALITATIVE_EDITORIAL_BASELINE",
        "numerical_predictions_allowed": False,
        "missingness_status": "PAPER3_CS_DIRECT_OUTCOMES_UNADJUDICATED; PAPER4_ACTION_UTILITY_UNVALIDATED",
        "calibration_status": "NOT_AVAILABLE",
        "paper3_probabilities": None,
        "paper4_superiority_claim": False,
        "questions": [],
        "candidates": candidates,
        "provenance_note": "Each citation is preserved as included in the frozen radar. URL hashes are citation-record hashes, not full-text content hashes. No additional publication dates or full-text hashes are inferred.",
    }
    snapshot["questions"] = [canonical_question(item, cutoff) for item in candidates]
    snapshot["evidence_registry"] = [
        reference
        for candidate in candidates
        for reference in baseline_evidence_refs(snapshot, candidate["id"])
    ]
    snapshot["snapshot_sha256"] = sha256_bytes(canonical_json(snapshot))
    return snapshot


def write_immutable_json(path: str | Path, value: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    except FileExistsError as exc:
        raise ForecastEngineError(f"immutable artifact already exists: {target}") from exc


def append_snapshot(path: str | Path, snapshot: dict[str, Any]) -> None:
    if not verify_snapshot_hash(snapshot):
        raise ForecastEngineError("snapshot content hash mismatch")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines() if line.strip()] if target.exists() else []
    if snapshot.get("snapshot_id") in {row.get("snapshot_id") for row in existing}:
        raise ForecastEngineError("snapshot IDs are immutable and append-only")
    with target.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(snapshot, ensure_ascii=False, sort_keys=True) + "\n")


def validate_evidence(item: dict[str, Any]) -> None:
    required = ("evidence_id", "question_id", "source_identifier", "canonical_url", "evidence_type",
                "claim", "availability_status", "retrieval_date", "content_hash_scope")
    missing = [key for key in required if key not in item]
    if missing:
        raise ForecastEngineError(f"evidence missing fields: {', '.join(missing)}")
    if item["availability_status"] == "VERIFIED":
        parse_date(item.get("earliest_verified_availability_date"), "earliest_verified_availability_date")
        if not item.get("availability_basis"):
            raise ForecastEngineError("verified availability requires an independent basis")
    elif item.get("earliest_verified_availability_date") is not None:
        parse_date(item["earliest_verified_availability_date"], "earliest_verified_availability_date")
    if item.get("supersedes_event_id") and item["supersedes_event_id"] == item["evidence_id"]:
        raise ForecastEngineError("an evidence event cannot supersede itself")
    for key in ("publication_date", "version_date", "retrieval_date"):
        if item.get(key) is not None:
            parse_date(item[key], key)
    if item.get("retrieval_date") and item.get("earliest_verified_availability_date"):
        if parse_date(item["retrieval_date"], "retrieval_date") < parse_date(
                item["earliest_verified_availability_date"], "earliest_verified_availability_date"):
            raise ForecastEngineError("retrieval cannot predate earliest verified public availability")
    if item.get("content_sha256") is not None and (len(item["content_sha256"]) != 64
            or any(char not in "0123456789abcdef" for char in item["content_sha256"])):
        raise ForecastEngineError("content_sha256 must be a 64-character SHA-256")


def eligible_evidence(item: dict[str, Any], cutoff: str) -> tuple[bool, str]:
    """Only verified availability at/before cutoff can enter a forecast snapshot."""
    validate_evidence(item)
    cutoff_date = parse_date(cutoff, "cutoff")
    if item["availability_status"] != "VERIFIED":
        return False, "QUARANTINED_AVAILABILITY_UNVERIFIED"
    available = parse_date(item["earliest_verified_availability_date"], "earliest_verified_availability_date")
    if available > cutoff_date:
        return False, "POST_CUTOFF_EVIDENCE"
    return True, "ELIGIBLE_POINT_IN_TIME_EVIDENCE"


def classify_evidence_timing(item: dict[str, Any], cutoff: str) -> str:
    """Distinguish source availability from when this project retrieved it."""
    ok, status = eligible_evidence(item, cutoff)
    if not ok:
        return status
    retrieval = item.get("retrieval_date")
    if retrieval is not None and parse_date(retrieval, "retrieval_date") > parse_date(cutoff, "cutoff"):
        return "LATE_DISCOVERED_BUT_VERIFIED_AVAILABLE_AT_CUTOFF"
    return "VERIFIED_AVAILABLE_BY_CUTOFF"


def append_evidence_event(path: str | Path, item: dict[str, Any]) -> None:
    """Append a new immutable evidence event; corrections use a new ID and supersedes link."""
    validate_evidence(item)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if target.exists():
        existing = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines() if line.strip()]
    previous = next((row for row in existing if row["evidence_id"] == item["evidence_id"]), None)
    if previous is not None:
        if previous == item:
            return  # exact repeat is an idempotent import
        raise ForecastEngineError("evidence event ID already exists with different content")
    supersedes = item.get("supersedes_event_id")
    if supersedes and not any(row["evidence_id"] == supersedes for row in existing):
        raise ForecastEngineError("superseded event must already exist in the append-only store")
    with target.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def create_qualitative_snapshot(baseline: dict[str, Any], question_id: str, as_of: str,
                                evidence_items: Iterable[dict[str, Any]], reason: str,
                                outlook: dict[str, Any] | None = None) -> dict[str, Any]:
    if not reason.strip():
        raise ForecastEngineError("qualitative updates require an explicit rationale")
    q = next((row for row in baseline["questions"] if row["question_id"] == question_id), None)
    if q is None:
        raise ForecastEngineError("unknown stable question_id")
    try:
        as_of_datetime = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ForecastEngineError("as_of must be an ISO timestamp") from exc
    if as_of_datetime.tzinfo is None:
        raise ForecastEngineError("as_of must include a timezone")
    as_of_date = as_of_datetime.date()
    if as_of_date < parse_date(baseline["evidence_cutoff"], "baseline evidence cutoff"):
        raise ForecastEngineError("follow-up snapshots cannot predate the baseline cutoff")
    eligible, quarantined = [], []
    for item in evidence_items:
        if item["question_id"] != question_id:
            continue
        ok, status = eligible_evidence(item, as_of_date.isoformat())
        if ok and item.get("retrieval_date") is not None and parse_date(item["retrieval_date"], "retrieval_date") > as_of_date:
            ok, status = False, "RETRIEVED_AFTER_SNAPSHOT_AS_OF"
        record = {"evidence_id": item["evidence_id"], "status": status}
        if ok:
            record["source_sha256"] = item.get("content_sha256") or sha256_bytes(item["canonical_url"].encode("utf-8"))
            record["hash_scope"] = (item["content_hash_scope"] if item.get("content_sha256")
                                     else "CANONICAL_URL_STRING_ONLY")
            record["timing_classification"] = classify_evidence_timing(item, as_of_date.isoformat())
        (eligible if ok else quarantined).append(record)
    previous = next(row for row in baseline["candidates"] if row["id"] == question_id)
    baseline_evidence_ids = {
        row["evidence_id"] for row in baseline.get("evidence_registry", [])
        if row.get("question_id") == question_id
    }
    added_evidence_ids = [row["evidence_id"] for row in eligible
                          if row["evidence_id"] not in baseline_evidence_ids]
    updated_outlook = outlook if outlook is not None else previous["paper3_outlook"]
    if not isinstance(updated_outlook, dict) or set(updated_outlook) != {"attention", "direct_resolution", "premise_revision"}:
        raise ForecastEngineError("qualitative outlook must keep attention, resolution, and revision separate")
    updated = {
        "schema_version": "1.0",
        "snapshot_id": f"SNAP-QUAL-{question_id}-{as_of_date.isoformat()}-{sha256_bytes(canonical_json([eligible, reason]))[:10]}",
        "previous_snapshot_id": baseline["snapshot_id"],
        "as_of": as_of,
        "evidence_cutoff": as_of_date.isoformat(),
        "method_version": baseline["method_version"],
        "candidate_set_version": baseline["candidate_set_version"],
        "source_hashes": list(baseline["source_hashes"]) + [
            {"path": row["evidence_id"], "sha256": row["source_sha256"], "scope": row["hash_scope"]}
            for row in eligible
        ],
        "forecast_type": "QUALITATIVE_EDITORIAL",
        "numerical_predictions_allowed": False,
        "question_id": question_id,
        "qualitative_outlook": updated_outlook,
        "included_evidence": eligible,
        "quarantined_evidence": quarantined,
        "paper4_action_recommendation": previous["paper4_recommended_action"],
        "paper4_action_status": "RECOMMENDATION_ONLY_NO_VALIDATED_SUPERIORITY",
        "change_summary": {
            "reason": reason,
            "added_evidence_ids": added_evidence_ids,
            "changed_fields": ["as_of", "evidence_cutoff", "included_evidence", "change_summary"],
            "qualitative_outlook_changed": updated_outlook != previous["paper3_outlook"],
        },
        "paper3_probabilities": None,
        "calibration_status": "NOT_AVAILABLE",
    }
    updated["snapshot_sha256"] = sha256_bytes(canonical_json(updated))
    return updated


def diff_snapshots(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    old_outlook = old.get("qualitative_outlook")
    if old_outlook is None:
        candidate = next(row for row in old["candidates"] if row["id"] == new["question_id"])
        old_outlook = candidate["paper3_outlook"]
    return {
        "question_id": new["question_id"],
        "previous_snapshot_id": old["snapshot_id"],
        "new_snapshot_id": new["snapshot_id"],
        "added_evidence_ids": new["change_summary"]["added_evidence_ids"],
        "quarantined_evidence": new["quarantined_evidence"],
        "outlook_before": old_outlook,
        "outlook_after": new["qualitative_outlook"],
        "outlook_changed": old_outlook != new["qualitative_outlook"],
        "change_reason": new["change_summary"]["reason"],
    }


def validate_adjudication(record: dict[str, Any]) -> None:
    required = ("adjudication_id", "question_id", "endpoint", "forecast_cutoff", "due_date",
                "observation_end", "status", "evidence_ids", "assumptions_match", "comparator_match",
                "metric_match", "reviewer_ids", "independent_review_status",
                "relation_to_frozen_question", "missingness_status", "criterion_version")
    missing = [key for key in required if key not in record]
    if missing:
        raise ForecastEngineError(f"adjudication missing fields: {', '.join(missing)}")
    if record["status"] not in OPERATIONAL_OUTCOMES:
        raise ForecastEngineError("unknown CS operational outcome state")
    if not isinstance(record["evidence_ids"], list) or not isinstance(record["reviewer_ids"], list):
        raise ForecastEngineError("evidence_ids and reviewer_ids must be arrays")
    if not isinstance(record["relation_to_frozen_question"], str) or not record["relation_to_frozen_question"].strip():
        raise ForecastEngineError("relation_to_frozen_question must be explicit")
    if record["endpoint"] not in {"attention", "resolution", "premise_revision", "evidence_growth", "impact"}:
        raise ForecastEngineError("endpoints must remain distinct")
    cutoff = parse_date(record["forecast_cutoff"], "forecast_cutoff")
    due = parse_date(record["due_date"], "due_date")
    observation_end = parse_date(record["observation_end"], "observation_end")
    if due < cutoff:
        raise ForecastEngineError("due date cannot precede forecast cutoff")
    if record["status"] == "NOT_YET_DUE" and observation_end >= due:
        raise ForecastEngineError("a horizon that has elapsed cannot remain NOT_YET_DUE")
    if record["status"] == "VERIFIED_UNRESOLVED_AT_HORIZON":
        if observation_end < due or record["missingness_status"] != "COMPLETE_COVERAGE":
            raise ForecastEngineError("verified unresolved requires elapsed horizon and complete coverage")
    adjudicated = record["status"] not in {"INSUFFICIENT_EVIDENCE", "NOT_YET_DUE"}
    if adjudicated and (len(set(record["reviewer_ids"])) < 2 or not record["evidence_ids"]):
        raise ForecastEngineError("outcome decisions require evidence and two distinct reviewers")
    if record["independent_review_status"] not in {"AGREED", "DISAGREEMENT", "PENDING", "NOT_APPLICABLE"}:
        raise ForecastEngineError("unknown independent review status")
    if adjudicated and record["independent_review_status"] != "AGREED":
        raise ForecastEngineError("adjudicated outcomes require agreement from independent reviewers")
    if record["status"] in {"AUTHENTICATED_RESOLUTION", "AUTHENTICATED_REFUTATION_OR_PREMISE_REVISION"}:
        if not record["assumptions_match"] or not record["comparator_match"] or not record["metric_match"]:
            raise ForecastEngineError("direct outcomes require matching assumptions, comparator, and metric")
    if record["status"] == "AUTHENTICATED_RESOLUTION" and record["endpoint"] != "resolution":
        raise ForecastEngineError("resolution status can only adjudicate the resolution endpoint")
    if record["status"] == "AUTHENTICATED_REFUTATION_OR_PREMISE_REVISION" and record["endpoint"] != "premise_revision":
        raise ForecastEngineError("premise revision/refutation is a separate endpoint")
    if record["status"] == "AUTHENTICATED_SUBSTANTIVE_PROGRESS" and record["endpoint"] != "evidence_growth":
        raise ForecastEngineError("substantive progress belongs to the separate evidence_growth endpoint")
    if record["status"] == "INSUFFICIENT_EVIDENCE" and record["missingness_status"] == "NEGATIVE_OUTCOME":
        raise ForecastEngineError("insufficient evidence cannot be represented as a negative outcome")


def validate_action_plan(plan: dict[str, Any]) -> None:
    required = ("plan_id", "question_id", "decision_timestamp", "hypotheses", "evidence_gaps",
                "candidate_actions", "ranking", "selection_rationale", "assumptions", "frozen_sha256")
    if any(key not in plan for key in required):
        raise ForecastEngineError("Paper 4 action plan is incomplete")
    if not isinstance(plan["candidate_actions"], list) or not isinstance(plan["ranking"], list):
        raise ForecastEngineError("candidate_actions and ranking must be arrays")
    if not plan["candidate_actions"] or len(plan["candidate_actions"]) != len(plan["ranking"]):
        raise ForecastEngineError("freeze the full candidate-action list and its ranking")
    try:
        timestamp = datetime.fromisoformat(plan["decision_timestamp"].replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ForecastEngineError("decision_timestamp must be an ISO timestamp") from exc
    if timestamp.tzinfo is None:
        raise ForecastEngineError("decision_timestamp must include a timezone")
    if not isinstance(plan["hypotheses"], list) or not plan["hypotheses"]:
        raise ForecastEngineError("candidate actions must be tied to explicit competing hypotheses")
    hypothesis_ids = [row.get("id") for row in plan["hypotheses"] if isinstance(row, dict)]
    if len(hypothesis_ids) != len(plan["hypotheses"]) or not all(isinstance(i, str) and i for i in hypothesis_ids):
        raise ForecastEngineError("each hypothesis needs a stable id and statement")
    if len(hypothesis_ids) != len(set(hypothesis_ids)) or any(not row.get("statement") for row in plan["hypotheses"]):
        raise ForecastEngineError("hypothesis IDs must be unique and statements explicit")
    priors = [row.get("prior") for row in plan["hypotheses"]]
    if any(isinstance(p, bool) or not isinstance(p, (int, float)) or p < 0 for p in priors) or abs(sum(priors) - 1.0) > 1e-9:
        raise ForecastEngineError("hypothesis priors must be nonnegative and sum to one")
    if not isinstance(plan.get("planner_weights"), dict) or not isinstance(plan.get("observed_provenance_roots"), list):
        raise ForecastEngineError("Paper 4 weights and observed-source roots must be declared")
    weight_names = {"information_gain", "novelty", "tractability", "cost"}
    if set(plan["planner_weights"]) != weight_names or any(
            isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)
            for value in plan["planner_weights"].values()):
        raise ForecastEngineError("all four finite Paper 4 planner weights must be explicitly declared")
    if any(not isinstance(item, dict) or not isinstance(item.get("action_id"), str)
           for item in plan["candidate_actions"]):
        raise ForecastEngineError("every candidate action needs a string action_id")
    if any(not isinstance(row, dict) or not isinstance(row.get("action_id"), str)
           for row in plan["ranking"]):
        raise ForecastEngineError("every ranking row needs a string action_id")
    ids = [item["action_id"] for item in plan["candidate_actions"]]
    required_action = ("estimated_cost", "uncertainty_reduction_assumption", "feasibility_assumption",
                       "expected_observations", "falsification_value_assumption", "provenance",
                       "tractability_assumption", "expected_outcomes")
    for action in plan["candidate_actions"]:
        missing = [key for key in required_action if key not in action]
        if missing:
            raise ForecastEngineError(f"candidate action {action.get('action_id')} lacks declared fields: {', '.join(missing)}")
        if any(isinstance(action[key], bool) or not isinstance(action[key], (int, float)) or action[key] < 0
               for key in ("estimated_cost", "uncertainty_reduction_assumption")):
            raise ForecastEngineError("action cost and uncertainty-reduction assumptions must be nonnegative numbers")
        if not isinstance(action["expected_observations"], list) or not isinstance(action["provenance"], dict):
            raise ForecastEngineError("expected observations and provenance must be structured records")
        if not isinstance(action["expected_outcomes"], dict) or not action["expected_outcomes"]:
            raise ForecastEngineError("action likelihoods must be explicitly declared; never infer them")
        if not isinstance(action["tractability_assumption"], (int, float)) or not 0 <= action["tractability_assumption"] <= 1:
            raise ForecastEngineError("tractability assumption must be in [0,1]")
        if not all(isinstance(action[key], str) and action[key].strip()
                   for key in ("action_id", "feasibility_assumption", "falsification_value_assumption")):
            raise ForecastEngineError("action identity and qualitative assumptions must be explicit")
        probability_mass = {hypothesis_id: 0.0 for hypothesis_id in hypothesis_ids}
        for outcome, likelihoods in action["expected_outcomes"].items():
            if not isinstance(likelihoods, dict) or set(likelihoods) != set(hypothesis_ids):
                raise ForecastEngineError(f"action {action['action_id']} outcome {outcome} must specify every hypothesis")
            for hypothesis_id, likelihood in likelihoods.items():
                if isinstance(likelihood, bool) or not isinstance(likelihood, (int, float)) or not 0 <= likelihood <= 1:
                    raise ForecastEngineError("declared likelihoods must be in [0,1]")
                probability_mass[hypothesis_id] += likelihood
        if any(abs(total - 1.0) > 1e-9 for total in probability_mass.values()):
            raise ForecastEngineError("declared outcome likelihoods must sum to one under each hypothesis")
    if len(ids) != len(set(ids)) or set(ids) != {row["action_id"] for row in plan["ranking"]}:
        raise ForecastEngineError("ranking must cover every unique candidate action exactly once")
    ranks = [row.get("rank") for row in plan["ranking"]]
    if any(isinstance(rank, bool) or not isinstance(rank, int) for rank in ranks) or sorted(ranks) != list(range(1, len(ids) + 1)):
        raise ForecastEngineError("ranking must have each integer rank from 1 through the full candidate count")
    material = {key: value for key, value in plan.items() if key != "frozen_sha256"}
    if sha256_bytes(canonical_json(material)) != plan["frozen_sha256"]:
        raise ForecastEngineError("pre-action plan hash mismatch; ranking is immutable")


def freeze_action_plan(plan: dict[str, Any]) -> dict[str, Any]:
    frozen = dict(plan)
    frozen.pop("frozen_sha256", None)
    frozen["frozen_sha256"] = sha256_bytes(canonical_json(frozen))
    validate_action_plan(frozen)
    return frozen


def score_declared_paper4_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Apply the repository's Paper 4 EIG/novelty/tractability/cost utility to explicit assumptions."""
    validate_action_plan(plan)
    from research_platform.models import Action
    from research_platform.planner import PlannerWeights, rank_actions
    hypotheses = plan.get("hypotheses", [])
    beliefs = {row["id"]: row["prior"] for row in hypotheses}
    weights_data = plan.get("planner_weights", {})
    weights = PlannerWeights(
        information_gain=weights_data.get("information_gain", 10.0),
        novelty=weights_data.get("novelty", 1.0),
        tractability=weights_data.get("tractability", 1.0),
        cost=weights_data.get("cost", 1.0),
    )
    actions = []
    for row in plan.get("candidate_actions", []):
        actions.append(Action(
            id=row["action_id"], description=row["feasibility_assumption"],
            tests=tuple(row["expected_observations"]), cost=row["estimated_cost"],
            tractability=row["tractability_assumption"], expected_outcomes=row["expected_outcomes"],
            provenance_roots=tuple(row["provenance"].get("roots", [])),
        ))
    ranked = rank_actions(actions, beliefs, weights, set(plan.get("observed_provenance_roots", [])))
    return {"status": "ASSUMPTION_BASED_PAPER4_PLAN_ONLY",
            "ranking": [{"action_id": action.id, "rank": index, "utility": utility}
                        for index, (action, utility) in enumerate(ranked, 1)],
            "note": "Scores are conditional on frozen priors, likelihoods, weights and costs; they are not observed action utility."}


def rank_and_freeze_paper4_plan(draft: dict[str, Any]) -> dict[str, Any]:
    """Compute the repository's declared-utility ranking, then freeze it before outcomes."""
    candidate = dict(draft)
    candidate.pop("frozen_sha256", None)
    candidate["ranking"] = [{"action_id": row["action_id"], "rank": index}
                            for index, row in enumerate(candidate.get("candidate_actions", []), 1)]
    validated_draft = freeze_action_plan(candidate)
    computed = score_declared_paper4_plan(validated_draft)
    validated_draft.pop("frozen_sha256")
    validated_draft["ranking"] = computed["ranking"]
    return freeze_action_plan(validated_draft)


def append_action_outcome(path: str | Path, outcome: dict[str, Any], frozen_plan: dict[str, Any]) -> None:
    validate_action_plan(frozen_plan)
    if outcome.get("plan_id") != frozen_plan["plan_id"]:
        raise ForecastEngineError("action outcome must link to its frozen pre-action plan")
    if outcome.get("action_id") not in {row["action_id"] for row in frozen_plan["candidate_actions"]}:
        raise ForecastEngineError("outcome action must exist in frozen candidate set")
    required = ("outcome_id", "performed_at", "actual_resource_cost", "observed_evidence_ids",
                "independent_verification_status", "uncertainty_resolved")
    if any(key not in outcome for key in required):
        raise ForecastEngineError("action outcome must include execution time, cost, evidence and independent-verification fields")
    try:
        datetime.fromisoformat(outcome["performed_at"].replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ForecastEngineError("performed_at must be an ISO timestamp") from exc
    cost = outcome["actual_resource_cost"]
    if cost is not None and (isinstance(cost, bool) or not isinstance(cost, (int, float)) or cost < 0):
        raise ForecastEngineError("actual_resource_cost must be a nonnegative number or null")
    if not isinstance(outcome["observed_evidence_ids"], list):
        raise ForecastEngineError("observed_evidence_ids must be a list")
    if outcome.get("feasibility_status") not in {"EXECUTED", "NOT_EXECUTED", "BLOCKED"}:
        raise ForecastEngineError("feasibility/execution status is required")
    if outcome.get("scientific_utility") not in {"VERIFIED_USEFUL", "VERIFIED_NOT_USEFUL", "NOT_ADJUDICATED"}:
        raise ForecastEngineError("scientific utility must be separately adjudicated")
    if outcome["feasibility_status"] != "EXECUTED" and outcome["scientific_utility"] != "NOT_ADJUDICATED":
        raise ForecastEngineError("feasibility or setup failure cannot be coded as scientific utility")
    if outcome["scientific_utility"] != "NOT_ADJUDICATED":
        if (outcome["independent_verification_status"] != "VERIFIED" or not outcome["observed_evidence_ids"]
                or outcome["actual_resource_cost"] is None or outcome["uncertainty_resolved"] is None):
            raise ForecastEngineError("verified utility needs executed action, evidence, actual cost, uncertainty outcome and independent review")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines() if line.strip()] if target.exists() else []
    if outcome.get("outcome_id") in {row.get("outcome_id") for row in existing}:
        raise ForecastEngineError("action outcomes are append-only and IDs must be unique")
    with target.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(outcome, ensure_ascii=False, sort_keys=True) + "\n")


def append_adjudication(path: str | Path, record: dict[str, Any]) -> None:
    validate_adjudication(record)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines() if line.strip()] if target.exists() else []
    previous = next((row for row in existing if row["adjudication_id"] == record["adjudication_id"]), None)
    if previous is not None:
        if previous == record:
            return
        raise ForecastEngineError("adjudication ID already exists with different content")
    with target.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def evaluate_readiness(outcomes: list[dict[str, Any]], endpoint: str,
                       protocol: dict[str, Any] | None = None, authorized: bool = False) -> dict[str, Any]:
    """Return NOT_EVALUABLE unless frozen Paper 3 endpoint-specific sample gates pass."""
    if endpoint not in {"resolution", "premise_revision", "evidence_growth"}:
        raise ForecastEngineError("readiness scoring is defined only for distinct Target A/B outcome endpoints")
    protocol = protocol or load_json(PAPER3_TARGETS_PATH)
    target_key = "A_direct_resolution" if endpoint in {"resolution", "premise_revision"} else "B_substantial_progress"
    spec = protocol["targets"][target_key]
    relevant = [row for row in outcomes if row.get("endpoint") == endpoint
                and row.get("status") not in {"INSUFFICIENT_EVIDENCE", "NOT_YET_DUE"}
                and len(set(row.get("reviewer_ids", []))) >= 2]
    statuses = [row.get("status") for row in relevant]
    positive_states = ({"AUTHENTICATED_RESOLUTION", "AUTHENTICATED_REFUTATION_OR_PREMISE_REVISION"}
                       if target_key == "A_direct_resolution" else {"AUTHENTICATED_SUBSTANTIVE_PROGRESS"})
    positive = sum(status in positive_states for status in statuses)
    negative = sum(status == "VERIFIED_UNRESOLVED_AT_HORIZON" for status in statuses)
    blockers = []
    gate = spec["paper3_score_gate"]
    minimum_n = 20 if target_key == "A_direct_resolution" else 30
    minimum_class = 5 if target_key == "A_direct_resolution" else 10
    if len(statuses) < minimum_n:
        blockers.append(f"requires at least {minimum_n} adjudicated endpoint records; observed {len(statuses)}")
    if positive < minimum_class:
        blockers.append(f"requires at least {minimum_class} positive endpoint records; observed {positive}")
    if negative < minimum_class:
        blockers.append(f"requires at least {minimum_class} verified no-progress/negative records; observed {negative}")
    if not authorized:
        blockers.append("evaluation authorization is absent")
    groups_by_split: dict[str, set[str]] = {}
    family_split: dict[str, str] = {}
    for row in relevant:
        split = row.get("split_name")
        family = row.get("question_family_id")
        if split and family:
            groups_by_split.setdefault(split, set()).add(family)
            if family in family_split and family_split[family] != split:
                blockers.append(f"question family {family} crosses chronological splits")
            family_split[family] = split
    if len(groups_by_split) < 3 or any(len(groups) < 3 for groups in groups_by_split.values()):
        blockers.append("requires at least 3 question-family groups in each of 3 chronological splits")
    if not any(row.get("split_name") == "final_test" and row.get("untouched_final_test") is True for row in relevant):
        blockers.append("an untouched chronological final-test period is not recorded")
    return {
        "status": "READY" if not blockers else "NOT_EVALUABLE",
        "endpoint": endpoint,
        "paper3_target": target_key,
        "records": len(statuses),
        "positive": positive,
        "verified_negative_or_unresolved": negative,
        "gate_reference": gate,
        "metrics": None,
        "blockers": blockers,
    }


def grouped_chronological_split(records: list[dict[str, Any]], train_cutoff: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Chronological holdout that excludes a question family from both sides if it straddles cutoff."""
    cutoff = parse_date(train_cutoff, "train_cutoff")
    early_families, late_families = set(), set()
    for row in records:
        parse_date(row.get("cutoff_date"), "cutoff_date")
        family = row.get("question_family_id")
        if not family:
            raise ForecastEngineError("every evaluation row needs question_family_id")
        if parse_date(row["cutoff_date"], "cutoff_date") <= cutoff:
            early_families.add(family)
        else:
            late_families.add(family)
    crossing_families = early_families & late_families
    train = [row for row in records if parse_date(row["cutoff_date"], "cutoff_date") <= cutoff
             and row["question_family_id"] not in crossing_families]
    test = [row for row in records if parse_date(row["cutoff_date"], "cutoff_date") > cutoff
            and row["question_family_id"] not in early_families]
    return train, test


def evaluate_predictions(labels: list[int], probabilities: list[float],
                         readiness: dict[str, Any], authorized: bool = False) -> dict[str, Any]:
    if not authorized:
        return {"status": "NOT_EVALUABLE", "metrics": None, "blockers": ["explicit evaluation authorization is absent"]}
    if readiness.get("status") != "READY":
        return {"status": "NOT_EVALUABLE", "metrics": None,
                "blockers": readiness.get("blockers", ["endpoint sample gate has not passed"])}
    if len(labels) != len(probabilities) or not labels or any(label not in (0, 1) for label in labels):
        raise ForecastEngineError("binary labels and probabilities must be non-empty, aligned and valid")
    if any(not 0 <= probability <= 1 for probability in probabilities):
        raise ForecastEngineError("probabilities must be in [0,1]")
    from research_platform.opportunity import auprc, auroc, brier_score
    epsilon = 1e-15
    log_loss = -sum(label * math.log(max(probability, epsilon))
                    + (1 - label) * math.log(max(1 - probability, epsilon))
                    for label, probability in zip(labels, probabilities)) / len(labels)
    bins = []
    ece = 0.0
    for index in range(10):
        low, high = index / 10, (index + 1) / 10
        members = [i for i, p in enumerate(probabilities)
                   if low <= p < high or (index == 9 and p == 1.0)]
        if not members:
            continue
        mean_probability = sum(probabilities[i] for i in members) / len(members)
        observed_rate = sum(labels[i] for i in members) / len(members)
        ece += len(members) / len(labels) * abs(mean_probability - observed_rate)
        bins.append({"lower": low, "upper": high, "n": len(members),
                     "mean_probability": mean_probability, "observed_rate": observed_rate})
    return {"status": "EVALUATED", "metrics": {
        "n": len(labels), "positive_count": sum(labels), "negative_count": len(labels) - sum(labels),
        "auroc": auroc(labels, probabilities), "auprc": auprc(labels, probabilities),
        "brier": brier_score(labels, probabilities), "log_loss": log_loss,
        "expected_calibration_error_10_bins": ece, "calibration_bins": bins,
    }, "blockers": []}


def evaluate_prediction_baselines(labels: list[int], predictions_by_method: dict[str, list[float]],
                                  readiness: dict[str, Any], authorized: bool = False) -> dict[str, Any]:
    """Compare eligible methods under the same frozen labels and gate."""
    if not predictions_by_method:
        raise ForecastEngineError("at least one named baseline prediction vector is required")
    methods = {}
    for name, probabilities in sorted(predictions_by_method.items()):
        if not name.strip():
            raise ForecastEngineError("baseline method names must be nonempty")
        methods[name] = evaluate_predictions(labels, probabilities, readiness, authorized)
    return {"status": "EVALUATED" if all(row["status"] == "EVALUATED" for row in methods.values())
            else "NOT_EVALUABLE", "methods": methods,
            "comparison_claim": "Common endpoint data and gate only; no causal or superiority claim."}


def forecast_request(mode: str, question_id: str, qualitative_allowed: bool = False,
                     snapshot: dict[str, Any] | None = None, authorized: bool = False,
                     readiness: dict[str, Any] | None = None, endpoint: str | None = None) -> dict[str, Any]:
    mode = mode.upper()
    if mode not in MODES:
        raise ForecastEngineError(f"unsupported forecast mode: {mode}")
    if mode == "QUALITATIVE_EDITORIAL":
        if not qualitative_allowed:
            return {"status": "NOT_READY", "mode": mode, "question_id": question_id,
                    "blockers": ["qualitative output must be explicitly requested"], "prediction": None}
        if snapshot is None:
            snapshot = build_baseline_snapshot()
        candidate = next((row for row in snapshot["candidates"] if row["id"] == question_id), None)
        if candidate is None:
            raise ForecastEngineError("unknown question_id")
        return {"status": "QUALITATIVE_ONLY", "mode": mode, "question_id": question_id,
                "outlook": candidate["paper3_outlook"], "probabilities": None,
                "disclaimer": "Editorial assessment; not calibrated, not model output."}
    blockers = []
    if endpoint not in {"attention", "resolution", "premise_revision", "evidence_growth", "impact"}:
        blockers.append("a distinct, predeclared outcome endpoint is required")
    readiness = readiness or {"status": "NOT_EVALUABLE", "blockers": ["eligible historical outcomes are insufficient"]}
    if readiness["status"] != "READY":
        blockers.extend(readiness.get("blockers", ["historical evaluation gate is not satisfied"]))
    blockers.append("no authenticated, temporally validated model artifact is registered")
    blockers.append("input schema compatibility has not been established for a trained predictor")
    blockers.append("calibration protocol has not passed for this CS endpoint")
    if not authorized:
        blockers.append("explicit inference/evaluation authorization is absent")
    return {"status": "NOT_READY", "mode": mode, "question_id": question_id,
            "prediction": None, "blockers": list(dict.fromkeys(blockers))}


def make_manifest(paths: Iterable[str | Path], command: list[str], fixture_only: bool = False) -> dict[str, Any]:
    entries = []
    for raw in paths:
        path = Path(raw)
        entries.append({"path": str(path), "sha256": hash_file(path) if path.is_file() else None})
    return {
        "manifest_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "command": command,
        "python_runtime": "stdlib-only forecast engine",
        "inputs": entries,
        "fixture_only": fixture_only,
        "scientific_claim": False,
    }


def verify_snapshot_hash(snapshot: dict[str, Any]) -> bool:
    material = {key: value for key, value in snapshot.items() if key != "snapshot_sha256"}
    return snapshot.get("snapshot_sha256") == sha256_bytes(canonical_json(material))


def grouped_bootstrap_intervals(labels: list[int], probabilities: list[float], groups: list[str],
                                repetitions: int = 1000, seed: int = 17) -> dict[str, Any]:
    """Deterministic cluster bootstrap; intended for authorized future evaluation only."""
    if not (len(labels) == len(probabilities) == len(groups)) or not labels:
        raise ForecastEngineError("bootstrap inputs must be non-empty and aligned")
    if repetitions < 100:
        raise ForecastEngineError("use at least 100 bootstrap draws")
    import random
    from research_platform.opportunity import auprc, auroc, brier_score
    by_group: dict[str, list[int]] = {}
    for index, group in enumerate(groups):
        by_group.setdefault(group, []).append(index)
    names = sorted(by_group)
    if len(names) < 2:
        raise ForecastEngineError("cluster bootstrap requires at least two independent groups")
    rng = random.Random(seed)
    samples = {"auroc": [], "auprc": [], "brier": []}
    for _ in range(repetitions):
        chosen = [rng.choice(names) for _ in names]
        indices = [idx for group in chosen for idx in by_group[group]]
        y = [labels[i] for i in indices]
        p = [probabilities[i] for i in indices]
        if len(set(y)) < 2:
            continue
        samples["auroc"].append(auroc(y, p))
        samples["auprc"].append(auprc(y, p))
        samples["brier"].append(brier_score(y, p))
    intervals = {}
    for metric, values in samples.items():
        values = sorted(v for v in values if v is not None)
        if not values:
            intervals[metric] = None
        else:
            intervals[metric] = {"lower_95": values[int(.025 * (len(values) - 1))],
                                 "upper_95": values[int(.975 * (len(values) - 1))],
                                 "valid_draws": len(values)}
    return {"status": "FIXTURE_OR_AUTHORIZED_ANALYSIS_ONLY", "independent_groups": len(names),
            "repetitions": repetitions, "seed": seed, "intervals": intervals}


def action_comparison_views(plan: dict[str, Any]) -> dict[str, list[str]]:
    """Expose simple baselines without scoring Paper 4's realized utility."""
    validate_action_plan(plan)
    actions = plan["candidate_actions"]
    paper4 = [row["action_id"] for row in sorted(plan["ranking"], key=lambda row: row["rank"])]
    def ordered(key: str, reverse: bool = False) -> list[str]:
        return [row["action_id"] for row in sorted(actions, key=lambda row: (row.get(key) is None,
                            row.get(key, 0) if not reverse else -row.get(key, 0), row["action_id"]))]
    return {
        "paper4_rank_frozen": paper4,
        "lowest_assumed_cost": ordered("estimated_cost"),
        "highest_assumed_uncertainty_reduction": ordered("uncertainty_reduction_assumption", reverse=True),
        "simple_momentum": ordered("research_momentum_at_cutoff", reverse=True),
        "interpretation": ["All views are pre-action selections only.",
                           "None measures realized scientific utility or establishes Paper 4 superiority."],
    }


def baseline_evidence_refs(snapshot: dict[str, Any], question_id: str) -> list[dict[str, Any]]:
    candidate = next((row for row in snapshot["candidates"] if row["id"] == question_id), None)
    if candidate is None:
        raise ForecastEngineError("unknown question_id")
    return [{
        "evidence_id": f"CIT-{sha256_bytes(url.encode('utf-8'))[:16]}",
        "question_id": question_id,
        "source_identifier": url.rsplit("/", 1)[-1],
        "canonical_url": url,
        "doi": None,
        "arxiv_id": url.rsplit("/", 1)[-1].replace("abs/", "") if "arxiv.org/abs/" in url else None,
        "publication_date": None,
        "version_date": None,
        "retrieval_date": None,
        "earliest_verified_availability_date": snapshot["evidence_cutoff"],
        "availability_status": "VERIFIED",
        "availability_basis": "URL is included as a citation in the frozen baseline input; this verifies use by that snapshot, not the source's earliest publication date.",
        "evidence_type": "CITATION_RECORD_ONLY",
        "claim": "Citation included by the qualitative editorial radar; claim-level full-text linkage has not been imported.",
        "assumptions": [],
        "contradicts_evidence_ids": [],
        "source_reliability": "PRIMARY_SOURCE_URL_UNVERIFIED_FULLTEXT",
        "independent_replication_status": "NOT_ASSESSED",
        "provenance": {"baseline_snapshot_id": snapshot["snapshot_id"]},
        "content_sha256": None,
        "content_hash_scope": "URL_STRING_ONLY",
    } for url in candidate["primary_sources"]]
