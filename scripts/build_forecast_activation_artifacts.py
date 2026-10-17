#!/usr/bin/env python3
"""Build evidence-only Forecast Activation records from frozen repository inputs.

This builder deliberately refuses to issue a forecast. The current twelve radar
endpoints have unresolved operational fields; this cycle records that gate and
prepares review packets from already frozen historical cohorts only.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RADAR = ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json"
OPERATIONAL = ROOT / "data/forecast_engine/radar_endpoint_operationalization_20261016.json"
TARGET_A_AUDIT = ROOT / "reports/paper3_direct_endpoint_cohort_round6.json"
TARGET_A_COHORT = ROOT / "data/historical_cs_observable_cohort_16.jsonl"
TARGET_B_AUDIT = ROOT / "reports/historical_evidence_trajectory_round2.json"
TARGET_B_COHORT = ROOT / "data/historical_cs_observable_cohort_16.jsonl"
TARGET_B_SCREEN_FILES = (
    ROOT / "reports/historical_observable_source_screen_round5.json",
    ROOT / "reports/historical_observable_source_screen_round6.json",
)

TARGET_A_IDS = ("1707.09038v3", "1806.03283v1", "1903.06407v2")
TARGET_B_IDS = ("1905.02597v1", "2005.00972v1", "1903.05387v1")


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")


def _candidate_category(dimensions: dict[str, str]) -> list[str]:
    mapping = {
        "partial_progress": "CANDIDATE_PARTIAL_PROGRESS",
        "independent_evidence_strengthening": "CANDIDATE_INDEPENDENT_EVIDENCE_STRENGTHENING",
        "scope_narrowing_or_reformulation": "CANDIDATE_SCOPE_NARROWING",
        "direct_scientific_resolution": "CANDIDATE_DIRECT_RESOLUTION",
        "premise_refutation_or_revision": "CANDIDATE_PREMISE_REVISION",
        "contradictory_evidence": "CANDIDATE_CONTRADICTORY_EVIDENCE",
    }
    return [label for key, label in mapping.items() if dimensions.get(key) == "supported"]


def build_historical_packets() -> list[dict[str, Any]]:
    a = _json(TARGET_A_AUDIT)
    a_rows = {row["versioned_id"]: row for row in a["source_screen"]["eligible"]}
    a_followups = {row["versioned_id"]: row for row in a["followup_audit"]["coverage_rows"]}
    a_source_hashes = a["original_version_audit"]["sha256"]
    a_cohort = {row["versioned_id"]: row for row in _jsonl(TARGET_A_COHORT)}

    b = _json(TARGET_B_AUDIT)
    b_rows = {row["versioned_id"]: row for row in b["rows"]}
    b_cohort = {row["versioned_id"]: row for row in _jsonl(TARGET_B_COHORT)}
    b_screen = {
        row["versioned_id"]: row
        for path in TARGET_B_SCREEN_FILES
        for row in _json(path)["rows"]
    }

    packets: list[dict[str, Any]] = []
    for versioned_id in TARGET_A_IDS:
        frozen = a_rows[versioned_id]
        cohort = a_cohort.get(versioned_id)
        if cohort is None:
            # Round 6 is a separately frozen direct-endpoint cohort; preserve
            # its task identity instead of silently assigning the older 16-row ID.
            cohort = {
                "cohort_id": a["task_id"],
                "title": frozen["title"],
                "versioned_id": versioned_id,
                "source_pdf_url": frozen["source_url"],
                "source_abstract_url": "https://arxiv.org/abs/" + versioned_id.removesuffix("v1"),
                "as_of": frozen["cutoff"],
            }
        followup = a_followups[versioned_id]
        url = cohort["source_pdf_url"]
        abstract_id = re.sub(r"v\d+$", "", versioned_id)
        evidence = [{
            "title_or_record": followup["primary_record"],
            "url": followup["url"],
            "date": followup.get("date") or (re.search(r"\b20\d{2}-\d{2}-\d{2}\b", followup["primary_record"]) or re.search(r"\b20\d{2}\b", followup["primary_record"])).group(0),
            "date_precision": "exact_day" if (followup.get("date") or re.search(r"\b20\d{2}-\d{2}-\d{2}\b", followup["primary_record"])) else "year_only",
            "date_scope": followup.get("date_scope", "date precision is limited to what the frozen round-6 record states"),
            "result_identifiers": [],
            "reported_relation": followup["classification"],
            "claim_summary": "No stronger claim is inferred here; see the cited primary record and the frozen match audit.",
            "match_or_mismatch": followup["classification"],
            "evidence_status": "CANDIDATE_OUTCOME_EVIDENCE",
            "content_hash_scope": "URL_OR_IDENTIFIER_ONLY; source bytes were not rehashed in this activation task",
            "citation_record_sha256": _sha(followup["url"]),
        }]
        packets.append({
            "packet_id": f"P3-A-{versioned_id}-ACTIVATION-01",
            "track": "PAPER3_TARGET_A_DIRECT_RESOLUTION",
            "source_question_id": versioned_id,
            "cohort_id": a["task_id"],
            "original_source": {
                "title": cohort["title"], "versioned_id": versioned_id,
                "citation_url": cohort.get("source_abstract_url", f"https://arxiv.org/abs/{abstract_id}"), "fulltext_url": url,
                "source_as_of": cohort["as_of"],
                "source_pdf_sha256": a_source_hashes[versioned_id],
                "hash_scope": "exact source PDF bytes retrieved for round-6 audit",
            },
            "historical_window": {"cutoff": frozen["cutoff"], "followup_end": frozen["followup_end"]},
            "original_source_question": {
                "question_statement": None,
                "representation_note": "Round 6 froze this source question as an object/comparator/endpoint/falsification tuple rather than a single quoted sentence; no new prose question is substituted.",
                "object": frozen["object"],
                "comparator": frozen["comparator"],
                "endpoint": frozen["endpoint"],
                "falsification_condition": frozen["falsification_condition"],
                "artifact_or_benchmark": frozen["artifact_or_benchmark"],
            },
            "model_and_assumptions": {
                "topic": frozen["topic"],
                "source_scope": "exactly the source-screen object and comparator above",
                "additional_assumptions": "No assumptions have been added; the endpoint tuple is copied from the frozen round-6 audit.",
            },
            "documented_later_evidence": evidence,
            "conflicting_or_excluded_evidence": [],
            "candidate_outcome_categories": [],
            "matching_analysis": {
                "direct_resolution": "NOT_ESTABLISHED",
                "reason": followup["classification"],
                "search_absence_is_not_negative": True,
            },
            "human_review": {
                "status": "PENDING_TWO_INDEPENDENT_HUMAN_REVIEWERS",
                "target_a_label": None, "target_b_label": None, "trajectory_label": None,
                "reviewer_decisions_required": [
                    "Does the later record match the full frozen object/comparator/endpoint/falsification tuple?",
                    "Are source version, date, and in-window availability authenticated?",
                    "Does the result directly resolve/refute the tuple, or only show adjacent progress?",
                    "Are the source authors independent from the later evidence authors?",
                ],
            },
            "unresolved_facts": ["No exact direct outcome is established by the recorded follow-up classification."],
            "provenance": {"preparation_source": "reports/paper3_direct_endpoint_cohort_round6.json", "future_information_used_for_question_selection": False},
        })

    for versioned_id in TARGET_B_IDS:
        frozen = b_rows[versioned_id]
        cohort = b_cohort[versioned_id]
        screen = b_screen[versioned_id]
        url = cohort["source_pdf_url"]
        evidence = []
        for item in frozen["evidence"]:
            public_url = item["first_public_url"]
            evidence.append({
                "title_or_record": item["title"],
                "url": public_url,
                "primary_fulltext_url": item.get("primary_fulltext_url"),
                "date": item.get("first_public_date"),
                "date_precision": "exact_day" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", item.get("first_public_date", "")) else "year_only",
                "date_scope": item.get("date_scope", "as recorded in the frozen trajectory audit"),
                "locator": item.get("locator"),
                "reported_claim": item.get("observed_claim"),
                "reported_relation": item.get("directness"),
                "independence_concern": item.get("independence"),
                "match_or_mismatch": item.get("directness"),
                "evidence_status": "CANDIDATE_OUTCOME_EVIDENCE",
                "content_hash_scope": "URL_OR_IDENTIFIER_ONLY; source bytes were not rehashed in this activation task",
                "citation_record_sha256": _sha(public_url),
                "result_identifiers": [],
            })
        packets.append({
            "packet_id": f"P3-B-{versioned_id}-ACTIVATION-01",
            "track": "PAPER3_TARGET_B_SUBSTANTIVE_EVIDENCE_GROWTH",
            "source_question_id": versioned_id,
            "cohort_id": cohort["cohort_id"],
            "original_source": {
                "title": cohort["title"], "versioned_id": versioned_id,
                "citation_url": "https://arxiv.org/abs/" + versioned_id.removesuffix("v1"),
                "fulltext_url": url, "source_as_of": frozen["cutoff"],
                "source_url_sha256": _sha(url),
                "hash_scope": "URL string only; no claim about full source bytes",
            },
            "historical_window": {"cutoff": frozen["cutoff"], "followup_end": frozen["followup_end"]},
            "original_source_question": {
                "question_statement": frozen["question"],
                "source_question_status": "FROZEN_IN_HISTORICAL_EVIDENCE_TRAJECTORY_ROUND2",
                "assumptions_and_comparator": screen.get("comparison_and_metric"),
                "original_falsification_or_match_rule": screen.get("falsification_gate"),
                "source_locator": screen.get("source_locator"),
            },
            "model_and_assumptions": {
                "topic": cohort["sampling_topic"],
                "frozen_comparison": screen.get("comparison_and_metric"),
                "frozen_falsification_gate": screen.get("falsification_gate"),
            },
            "documented_later_evidence": evidence,
            "conflicting_or_excluded_evidence": frozen.get("excluded_near_matches", []),
            "candidate_outcome_categories": _candidate_category(frozen["dimensions"]),
            "matching_analysis": {
                "dimension_record": frozen["dimensions"],
                "decision_from_frozen_audit": frozen["decision"],
                "direct_outcome": "UNADJUDICATED",
                "non_detection_is_not_negative": True,
            },
            "human_review": {
                "status": "PENDING_TWO_INDEPENDENT_HUMAN_REVIEWERS",
                "target_a_label": None, "target_b_label": None, "trajectory_label": None,
                "reviewer_decisions_required": [
                    "Does the cited primary result address the exact frozen question and its assumptions?",
                    "Does it meet a Paper 3 Target B progress category without substituting publication/citation counts?",
                    "Is the evidence date within the frozen window and independently verifiable?",
                    "Is the relation direct, partial, scope-narrowing, or merely adjacent?",
                ],
            },
            "unresolved_facts": [frozen["limitations"]],
            "provenance": {"preparation_source": "reports/historical_evidence_trajectory_round2.json", "future_information_used_for_question_selection": False},
        })

    return packets


def build_activation(created_at: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    radar = _json(RADAR)
    operational = _json(OPERATIONAL)
    if len(radar["candidates"]) != 12 or len(operational["items"]) != 12:
        raise ValueError("expected the frozen twelve-item radar and its twelve endpoint reviews")
    if operational.get("frozen_forecast_count") != 0 or any(item.get("operationalization_freeze_at") for item in operational["items"]):
        raise ValueError("refusing to reinterpret already frozen endpoint status")

    assessments = []
    for candidate in radar["candidates"]:
        endpoint = next(item for item in operational["items"] if item["item_id"] == candidate["id"])
        assessments.append({
            "parent_candidate_id": candidate["id"],
            "rank_in_original_radar": candidate["rank"],
            "candidate_event": endpoint["proposed_event"],
            "status": endpoint["readiness"],
            "missing_definition_fields": endpoint.get("missing_definition_fields", []),
            "independent_review_questions": endpoint.get("reviewer_decisions_required", []),
            "activation_decision": "NOT_FROZEN",
            "reason": "The previously recorded endpoint audit has unresolved operational fields; no acceptance threshold or comparator is supplied by inference in this activation cycle.",
        })

    prospective = {
        "schema_version": "1.0",
        "record_id": "CS-PROSPECTIVE-FORECAST-EVENTS-ACTIVATION-20261017-v1",
        "created_at": created_at,
        "baseline_id": radar["report_id"],
        "baseline_date": radar["as_of"],
        "baseline_sha256": _sha(RADAR.read_text(encoding="utf-8")),
        "purpose": "Append-only prospective forecast event registry; this activation audit freezes no events because none passed endpoint review.",
        "events": [],
        "candidate_assessments": assessments,
        "activation_result": {
            "radar_directions_reviewed": 12,
            "candidate_endpoints_assessed": 12,
            "prospective_forecasts_frozen": 0,
            "forecast_issue_timestamps": [],
            "numeric_forecasts_created": 0,
            "human_outcomes_created": 0,
            "no_forecast_reason": "Every candidate retains at least one critical endpoint-design gap in the frozen operationalization artifact; one broad adaptive-IVM formulation also requires reframing due to the recorded prior-art boundary. The activation gate disallows invented thresholds and incomplete comparator/workload definitions.",
        },
        "immutability": "This activation record is append-only. It does not modify the 2026-10-16 editorial radar or baseline snapshot.",
    }

    monitors = []
    for candidate in radar["candidates"]:
        endpoint = next(item for item in operational["items"] if item["item_id"] == candidate["id"])
        title_words = [word.strip(".,:;()[]") for word in candidate["title"].split() if len(word.strip(".,:;()[]")) > 2]
        monitors.append({
            "monitor_id": "MON-" + candidate["id"],
            "parent_candidate_id": candidate["id"],
            "status": "PREPARATORY_NOT_ACTIVE_FORECAST",
            "active_forecast_event_id": None,
            "exact_search_terms": list(dict.fromkeys([candidate["id"], *title_words, candidate["subfield"]]))[:12],
            "exact_search_phrases_from_frozen_radar": [
                candidate["title"], candidate["precise_question"], candidate["unresolved_bottleneck"]
            ],
            "canonical_source_identifiers": candidate["primary_sources"],
            "venue_monitoring": "No event-specific venues were frozen in the source audit; use primary-source indexes and verify venue/version dates rather than treating this list as exhaustive.",
            "recommended_manual_cadence": "Quarterly review, only after endpoint design is completed; no scheduled job, crawl, or worker is activated.",
            "evidence_types_that_matter": endpoint.get("success_evidence", []),
            "advancement_triggers": endpoint.get("success_evidence", []),
            "downgrade_or_counterevidence_triggers": endpoint.get("against_or_refutation", []),
            "reviewer_escalation_triggers": endpoint.get("reviewer_decisions_required", []),
            "attention_vs_outcome_rule": "New papers, citations, topical mentions, and benchmarks alone are attention only; count progress/resolution only if the future frozen endpoint is met and independently adjudicated.",
            "source_availability_checks": ["authenticate version and first public date", "preserve full-text locator and source hash scope", "quarantine post-horizon records from in-window outcome adjudication"],
            "operationalization_gaps": endpoint.get("missing_definition_fields", []),
        })
    monitoring = {
        "schema_version": "1.0",
        "record_id": "CS-FORECAST-MONITORING-PREPARATION-20261017-v1",
        "created_at": created_at,
        "active_monitor_count": 0,
        "active_forecast_event_ids": [],
        "monitoring_specs": monitors,
        "execution_status": "NOT_STARTED_BY_DESIGN",
        "policy": "Specifications are preparatory only. No background process, scheduled task, crawler, model, or worker was started.",
    }

    summary = {
        "report_id": "CS-BREAKTHROUGH-FORECAST-ACTIVATION-20261017-v1",
        "created_at": created_at,
        "scope": "One bounded activation review; no model inference, experiment, new cohort, source crawl, worker, or human adjudication.",
        "baseline": {"id": radar["report_id"], "as_of": radar["as_of"], "sha256": prospective["baseline_sha256"], "modified": False},
        "radar_directions_reviewed": 12,
        "candidate_endpoints_assessed": 12,
        "prospective_forecasts_frozen": 0,
        "candidate_assessments": assessments,
        "historical_packets_prepared": 6,
        "historical_packet_ids": [packet["packet_id"] for packet in build_historical_packets()],
        "paper3": {
            "target_a": "Direct resolution remains separate and unadjudicated; six packets cover three existing Target A cases.",
            "target_b": "Evidence-growth categories remain candidate-only; three packets cover existing Target B questions.",
            "score_status": "NO_SCORE; frozen sample-size and class/group/adjudication gates are not met.",
            "source_native_five_class_mapping": "UNAVAILABLE_IN_PINNED_LOCAL_AUDIT; no mapping inferred.",
        },
        "paper4": {
            "use": "recommendation framework only; no action executed and no utility outcome added",
            "superiority_claim": False,
        },
        "human_packets_pending": 6,
        "independent_human_reviews_required": 12,
        "limitations": [
            "No prospective event passed the predeclared objective-endpoint gate; zero forecasts is an intentional no-go, not an inferred negative scientific outcome.",
            "Historical evidence packets preserve stored candidate evidence and mismatch classifications; no independent human review occurred.",
            "The source-native Paper 3 five-way taxonomy is unavailable in pinned local source materials, so no taxonomy mapping is guessed.",
            "Monitoring specifications are inactive preparation and make no claim of ongoing surveillance.",
        ],
    }
    return prospective, monitoring, summary


def build(output_root: Path, created_at: str) -> dict[str, Any]:
    datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    prospective, monitoring, summary = build_activation(created_at)
    packets = build_historical_packets()
    for packet in packets:
        _write_new(output_root / "data/forecast_engine/historical_packets" / f"{packet['source_question_id']}.json", packet)
    _write_new(output_root / "data/forecast_engine/prospective_forecast_events.json", prospective)
    _write_new(output_root / "data/forecast_engine/forecast_monitoring_spec.json", monitoring)
    _write_new(output_root / "reports/CS_BREAKTHROUGH_FORECAST_ACTIVATION.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--created-at", required=True, help="authenticated UTC ISO timestamp for this preparation record")
    parser.add_argument("--output-root", type=Path, default=ROOT)
    args = parser.parse_args()
    summary = build(args.output_root, args.created_at)
    print(json.dumps({"status": "BUILT_EVIDENCE_ONLY_NO_FORECAST", "packet_count": summary["historical_packets_prepared"],
                      "candidate_endpoints_assessed": summary["candidate_endpoints_assessed"],
                      "forecasts_frozen": summary["prospective_forecasts_frozen"]}, sort_keys=True))


if __name__ == "__main__":
    main()
