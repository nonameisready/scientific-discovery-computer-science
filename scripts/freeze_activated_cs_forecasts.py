#!/usr/bin/env python3
"""Freeze the bounded 2026-10-17 prospective CS forecast batch, without inference."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from research_platform.forecast_engine.core import (  # noqa: E402
    ForecastEngineError, append_snapshot, build_prospective_snapshot,
    canonical_json, freeze_prospective_forecast, hash_file, load_json,
    sha256_bytes, write_immutable_json,
)

RADAR = ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json"
BASELINE = ROOT / "data/forecast_engine/qualitative_editorial_baseline_20261016.json"
ACTIVATED = ROOT / "data/forecast_engine/activated_forecasts.json"
MONITORING = ROOT / "data/forecast_engine/activated_forecast_monitoring.json"
SNAPSHOTS = ROOT / "data/forecast_engine/followup_snapshots.jsonl"
REPORT_JSON = ROOT / "reports/CS_BREAKTHROUGH_FORECAST_DISCOVERY_AND_ACTIVATION.json"


def _source(title: str, url: str, source_date: str, role: str, checked_scope: str) -> dict:
    return {"title": title, "url": url, "source_date": source_date, "role": role,
            "checked_scope": checked_scope, "hash_scope": "CITATION_METADATA_RECORD_ONLY"}


def drafts() -> list[dict]:
    return [
        {
            "event_id": "PLANAR-THREE-SETS-CUT-UNCUT-112",
            "scientific_question": "For an unweighted planar graph G and pairwise disjoint terminal sets S1={s}, S2={t}, S3={a,b}, can the minimum number of edges whose deletion separates every pair of distinct terminal sets while keeping the two terminals in S3 connected be computed in polynomial time?",
            "event_type": "THEORETICAL_ALGORITHM_COMPLEXITY",
            "source_baseline": "Bentert et al. (ICALP 2024), Theorem 1: planar Two-Sets Cut-Uncut is solvable by a one-sided-error randomized algorithm in 2^(|S|+|T|) n^O(1) time, but the paper explicitly leaves the three-set planar case with two singleton sets and one two-vertex set open. Fixed-k planar Multiway Cut is polynomial, but it does not impose this uncut connectivity constraint.",
            "exact_event": "By 2030-12-31, a publicly accessible primary theorem gives an exact polynomial-time algorithm for the specified planar unweighted Three-Sets Cut-Uncut problem, with runtime polynomial in |V(G)|+|E(G)| and success probability at least 2/3 on every input if randomized. The algorithm must either return the optimum cut size and a realizing edge set or correctly report infeasibility. A special case, approximation, or algorithm that drops the requirement that a and b remain connected does not count.",
            "frozen_assumptions": [
                "G is a finite simple undirected planar graph, given without requiring a fixed embedding.",
                "S1={s}, S2={t}, and S3={a,b} are pairwise disjoint; all edge deletion costs are one.",
                "A feasible edge set F leaves s, t, and the connected component containing a and b in three pairwise distinct connected components of G-F; a and b must remain connected.",
                "The objective is to minimize |F|; infeasible instances must be detected.",
                "The event concerns an exact algorithm, not a heuristic, approximation, empirical implementation, or the general nonplanar problem."
            ],
            "improvement_criterion": "Resolve the explicitly stated planar (1,1,2)-terminal case with an exact polynomial-time algorithm; randomized polynomial time with a standard per-instance success probability of at least 2/3 qualifies.",
            "deadline": "2030-12-31",
            "resolution_policy": "Two independent reviewers inspect the dated primary source and full proof/algorithm against every frozen assumption. A mismatched graph class, terminal pattern, weighted variant only, or relaxation is not a match. A proof of infeasibility handling and exactness is required. A search miss is not a negative; if no matching source is found by deadline, record INSUFFICIENT_EVIDENCE unless the separately documented source-coverage review supports an explicit unresolved-at-horizon record.",
            "evidence_standard": "A dated peer-reviewed article or public preprint containing a complete mathematical algorithm and correctness proof; two independent human reviewers must agree after checking the formal problem statement and proof. LLM review is not an independent reviewer.",
            "ambiguity_policy": "If edge/vertex deletion, weighted/unweighted costs, the S3 connectivity condition, exactness, or polynomial runtime is unclear, mark UNRESOLVED rather than count the event as achieved.",
            "sources": [
                _source("Two-Sets Cut-Uncut on Planar Graphs", "https://doi.org/10.4230/LIPIcs.ICALP.2024.22", "2024-07-02", "PRIMARY_BASELINE_AND_EXPLICIT_OPEN_QUESTION", "ICALP 2024 proceedings, Theorem 1 and conclusion open question 2"),
                _source("Two-Sets Cut-Uncut on Planar Graphs (full preprint)", "https://arxiv.org/abs/2305.01314", "2023-05-02", "PRIMARY_PREPRINT_VERSION", "Problem definition, theorem scope, and open-problem statement")
            ],
            "forecast_statement": "I expect this exact planar three-set case to receive a correct polynomial-time algorithm by the deadline, but regard that outlook as highly uncertain.",
            "expectation": "HIGHLY_UNCERTAIN_WITH_DIRECTIONAL_LEAN",
            "directional_lean": "EXPECTED_ALGORITHM_BEFORE_DEADLINE",
            "supporting_evidence": [
                "The exact (1,1,2) terminal-size case is explicitly posed as an open question in the ICALP 2024 primary paper, so the endpoint is not invented post hoc.",
                "The immediately related planar Two-Sets Cut-Uncut problem has an exact one-sided-error randomized FPT algorithm in total terminal count; fixed-terminal planar multiway-cut algorithms offer adjacent structural tools."
            ],
            "counterevidence": [
                "The connectivity-preserving uncut condition is the central added difficulty and is not supplied by ordinary planar Multiway Cut algorithms.",
                "The same ICALP paper proves strong hardness for related unrestricted-graph variants; a small terminal count does not guarantee a tractable planar extension."
            ],
            "uncertainty": "One additional connected terminal set may create a fundamentally different dual-cycle interaction; the source authors singled it out as open. The four-year horizon is a judgment, not a measured historical base rate.",
            "primary_future_sources": ["ICALP/LIPIcs proceedings", "arXiv primary preprints", "SODA/ESA/ICALP/STACS proceedings", "journal versions indexed by DOI"],
            "search_strategy": "Search exact strings for Three-Sets Cut-Uncut, planar cut-uncut with terminal cardinalities (1,1,2), and equivalent formulations preserving one pair's connectivity; inspect theorem statements and proof sections, then trace citations from the 2024 ICALP paper."
        },
        {
            "event_id": "DISCRETE-FRECHET-TRANSLATION-PLANAR-N4",
            "scientific_question": "Can the exact discrete Frechet distance under translation between two n-vertex polygonal curves in the Euclidean plane be computed in O(n^4 polylog n) worst-case time under computation-model and arithmetic assumptions explicitly shown to be comparable to the published bounds?",
            "event_type": "THEORETICAL_ALGORITHM_UPPER_BOUND",
            "source_baseline": "Bringmann, Künnemann, and Nusser give a tilde-O(n^(14/3)) algorithm and a conditional n^(4-o(1)) lower bound under SETH. The exact 2D discrete problem remains between these exponents in the audited sources. The 2025 SoCG result improves one-dimensional translation/scaling variants and uses the known offline grid-reachability routine; it does not establish the 2D discrete event.",
            "exact_event": "By 2031-10-16, a public primary source proves an exact worst-case O(n^4 log^C n) algorithm for computing discrete Frechet distance under translation for two planar polygonal curves of n vertices each, for some fixed constant C. The theorem must state its computation model and arithmetic assumptions, and an independent reviewer must verify that they are no stronger in a material way than those underlying the cited baseline bounds; if comparability is unclear, the event is unresolved. A decision algorithm qualifies only if a stated reduction yields the same bound for exact value computation. Approximation, one-dimensional curves, continuous Frechet distance, or a restricted input family does not count.",
            "frozen_assumptions": [
                "Both input curves have n vertices in R^2; the translation is unrestricted in R^2.",
                "The endpoint is the exact discrete Frechet distance value, not only a fixed-threshold decision problem unless the source proves the stated value bound.",
                "The result must state its computational and arithmetic model; independent adjudication checks material comparability with the exact models used by the baseline papers rather than assuming all real-RAM/algebraic conventions are interchangeable.",
                "No input restrictions beyond those in the cited baseline are allowed."
            ],
            "improvement_criterion": "Improve the current tilde-O(n^(14/3)) exponent to an exact O(n^4 polylog n) algorithm, matching the exponent of the conditional n^(4-o(1)) lower bound up to polylogarithmic factors.",
            "deadline": "2031-10-16",
            "resolution_policy": "Two independent reviewers verify the source's problem variant, dimension, exactness, model, and full runtime derivation. The event is achieved only if the theorem yields O(n^4 log^C n) for a fixed C. A later conditional lower bound alone does not achieve the event. No matching result by the deadline is not a verified negative without the coverage protocol; otherwise retain INSUFFICIENT_EVIDENCE.",
            "evidence_standard": "Public peer-reviewed or preprint theorem with complete algorithm and asymptotic proof, independently checked by two human reviewers. Benchmark speed is irrelevant to this theorem event.",
            "ambiguity_policy": "Do not transfer results across 1D/2D, discrete/continuous, translation/other transformations, decision/value, or restricted/unrestricted curves. If the computation model differs materially, mark UNRESOLVED pending comparability review.",
            "sources": [
                _source("Frechet Distance Under Translation: Conditional Hardness and an Algorithm via Offline Dynamic Grid Reachability", "https://arxiv.org/abs/1810.10982", "2021-10-12", "PRIMARY_UPPER_AND_CONDITIONAL_LOWER_BOUND", "SODA 2019/TALG version; exact discrete 2D problem and exponent gap"),
                _source("Transforming Dogs on the Line: On the Fréchet Distance Under Translation or Scaling in 1D", "https://arxiv.org/abs/2501.12821", "2025-01-22", "PRIMARY_NEARBY_VARIANT_CROSS_CHECK", "SoCG 2025; 1D discrete/continuous variants, not the frozen 2D discrete event"),
                _source("Faster Fréchet Distance under Transformations", "https://arxiv.org/abs/2501.12814", "2025-01-22", "PRIMARY_NEARBY_VARIANT_CROSS_CHECK", "ICALP 2025 continuous transformation results using known offline dynamic grid reachability")
            ],
            "forecast_statement": "I judge an O(n^4 polylog n) exact algorithm for the unrestricted 2D discrete translation problem unlikely by the deadline.",
            "expectation": "UNLIKELY_BEFORE_DEADLINE",
            "directional_lean": "NO_N4_POLYLOG_ALGORITHM_BY_DEADLINE",
            "supporting_evidence": [
                "The 2019 result improved the prior exponent to 14/3 and established a conditional lower bound at exponent 4; the exponent gap has persisted in the primary-source line checked here.",
                "The 2025 papers advance adjacent one-dimensional and continuous transformation variants but continue to use the existing offline dynamic grid reachability bound for the relevant subroutine."
            ],
            "counterevidence": [
                "The remaining exponent gap is mathematically meaningful and the underlying offline dynamic reachability subproblem may admit a new algorithm.",
                "A conditional lower bound close to n^4 can focus algorithmic effort on exactly the remaining gap; no theorem rules out the forecast event."
            ],
            "uncertainty": "The event is one new asymptotic algorithm away from a long-standing gap, and there is no reliable base rate for such fine-grained improvements. This is a directional judgment, not a probability.",
            "primary_future_sources": ["SoCG proceedings", "SODA proceedings", "ESA/ICALP proceedings", "ACM Transactions on Algorithms", "arXiv primary preprints"],
            "search_strategy": "Search the exact problem name and equivalent geometric-alignment formulations; trace citations from the 2019 SODA/TALG paper and 2025 SoCG/ICALP papers; inspect whether algorithms preserve exact discrete 2D translation semantics and derive the O(n^4 polylog n) bound."
        },
        {
            "event_id": "K-HOP-DOMINATION-LOW-EXPANSION-NO-GIRTH",
            "scientific_question": "Can the constant-round k-hop dominating-set approximation bound proved for high-girth graphs of bounded k-hop expansion be achieved on all graphs of the same bounded k-hop expansion, without a girth assumption?",
            "event_type": "DISTRIBUTED_ALGORITHM_THEOREM",
            "source_baseline": "Lenzen and Wenning (SSS 2024; arXiv 2024) prove a 3k-round O(k+f(k)^(k/(k+1))) approximation for k-hop dominating set under girth at least 4k+3 and k-hop expansion at most f(k), with upper bounds in the port-numbering model with small messages. They explicitly ask whether the high-girth restriction is an artefact or the bound extends to all graphs of bounded k-hop expansion.",
            "exact_event": "By 2031-10-16, a public primary theorem gives a deterministic LOCAL/port-numbering algorithm using at most 3k+O(1) rounds and small messages which, for every fixed integer k>=1 and every graph family whose k-hop expansion is bounded by f(k), computes a k-hop dominating set of size at most C*(k+f(k)^(k/(k+1)))*OPT on every graph in the family, for a universal constant C, with no girth assumption. A restricted girth class, randomized-only theorem, or asymptotically worse ratio does not count.",
            "frozen_assumptions": [
                "k-hop domination means every vertex is at graph distance at most k from a selected vertex; objective is minimum cardinality.",
                "The graph family has the cited k-hop expansion bound f(k), interpreted using the shallow-minor/contraction density definition in the primary source.",
                "The algorithm operates in the source's deterministic port-numbering model with small messages; for each fixed k the 3k+O(1) round limit is constant in n.",
                "No minimum-girth condition or other omitted structural restriction is allowed.",
                "The approximation factor must be O(k+f(k)^(k/(k+1))) with a universal hidden constant; it cannot hide dependence on n or girth."
            ],
            "improvement_criterion": "Remove the high-girth hypothesis from the cited 3k-round upper bound without worsening its asymptotic approximation ratio or model.",
            "deadline": "2031-10-16",
            "resolution_policy": "Two independent reviewers check the algorithm model, round count, approximation factor, expansion definition, and absence of any girth condition in the theorem hypotheses. A theorem for a narrower class or with weaker ratio is partial progress only. A search miss is not a negative; absent complete source coverage use INSUFFICIENT_EVIDENCE.",
            "evidence_standard": "Dated public primary theorem and full proof, independently checked by two human reviewers; simulations and benchmark evidence do not qualify.",
            "ambiguity_policy": "If the algorithm uses unique identifiers or message size assumptions inconsistent with the frozen port-numbering model, or if constants depend on n/family beyond the stated universal C, record UNRESOLVED rather than a match.",
            "sources": [
                _source("Tight Bounds for Constant-Round Domination on Graphs of High Girth and Low Expansion", "https://arxiv.org/abs/2408.12998", "2024-08-23", "PRIMARY_BASELINE_AND_EXPLICIT_EXTENSION_QUESTION", "Abstract, upper/lower bounds, and final open question")
            ],
            "forecast_statement": "I consider removal of the high-girth restriction at the same bound unlikely by the deadline, while recognizing that the question is explicit and technically active.",
            "expectation": "UNLIKELY_BEFORE_DEADLINE",
            "directional_lean": "HIGH_GIRTH_RESTRICTION_LIKELY_REMAINS",
            "supporting_evidence": [
                "The source obtains its tight ratio under an explicit high-girth assumption and identifies extension to all bounded-expansion graphs as an open question.",
                "Its deterministic local lower bound is close to the stated upper ratio, so a theorem without girth must manage both short-cycle structure and locality limitations."
            ],
            "counterevidence": [
                "The question is stated directly by the authors, and progress on decomposing bounded-expansion graphs may provide a route within five years.",
                "The high-girth hypothesis may only simplify the proof; the source itself does not show it necessary for the upper bound."
            ],
            "uncertainty": "The target is a source-explicit structural extension, but there is no measured publication base rate and the lower bound in the paper applies to a different, high-girth regime.",
            "primary_future_sources": ["SSS proceedings", "DISC proceedings", "PODC proceedings", "arXiv primary preprints", "ACM/Elsevier theory journals"],
            "search_strategy": "Track exact phrases for k-hop domination, k-hop expansion, and constant-round LOCAL approximation; follow citations from the 2024 SSS paper and check theorem hypotheses for girth, message size, identifiers, round complexity, and the exact O(k+f(k)^(k/(k+1))) ratio."
        }
    ]


def rejected_candidates() -> list[dict]:
    return [
        {"candidate_id": "ADAPTIVE-FDP-INTERMEDIATE-Q", "field": "differential privacy", "disposition": "NOT_FROZEN", "reason": "The 2026 primary paper's valid asymptotic approximate-GDP filters are proved for q near 0 and q near 1; it warns that CLT approximations are optimistic at realistic rates. Selecting q=0.5 and a finite-sample improvement threshold would be an investigator-imposed target without a source-native canonical regime or margin."},
        {"candidate_id": "OFFLINE-DYNAMIC-GRID-REACHABILITY-POLYLOG", "field": "dynamic algorithms", "disposition": "NOT_FROZEN", "reason": "The 2019 source identifies faster dynamic directed-grid reachability as open, but the later offline variant already has a precise N^(1/3)-per-update bound and now underlies multiple geometric results. A polylogarithmic update target is not source-grounded as the next likely event and substantially overlaps the selected Frechet question."},
        {"candidate_id": "TWO-STAGE-STOCHASTIC-ILP-OPTIMIZATION", "field": "parameterized integer programming", "disposition": "REJECTED_RESOLVED_BEFORE_CUTOFF", "reason": "The explicit optimization gap from the 2025 block-structured IP paper was closed by a June 2026 primary preprint proving FPT optimization of two-stage stochastic IPs with large global coefficients (arXiv:2606.30330)."},
        {"candidate_id": "FOUR-BLOCK-ILP-FPT", "field": "parameterized integer programming", "disposition": "REJECTED_RESOLVED_BEFORE_CUTOFF", "reason": "A September 20, 2026 primary preprint gives an FPT algorithm for 4-block integer programming (arXiv:2609.23711); freezing that event now would be backdated/false."},
        {"candidate_id": "PLANAR-NETWORK-DIVERSION", "field": "planar graph algorithms", "disposition": "REJECTED_RESOLVED_BEFORE_CUTOFF", "reason": "Bentert et al.'s ICALP 2024 planar Two-Sets Cut-Uncut theorem already implies a polynomial-time randomized algorithm for planar Network Diversion; a 2025 SEA paper gives a deterministic practical algorithm."},
        {"candidate_id": "TWO-SETS-CUT-UNCUT-INTERVAL-GRAPHS", "field": "parameterized graph algorithms", "disposition": "SCREENED_NOT_OPERATIONALIZED", "reason": "An IPEC 2024 source states that complexity on interval graphs remains open, but this bounded cycle prioritized the more specific source-posed planar three-set theorem and did not authenticate a later structural algorithm or a strong directional basis for a second event in the same problem family."},
        {"candidate_id": "NETWORK-DIVERSION-GENERAL-GRAPHS", "field": "graph algorithms", "disposition": "SCREENED_NOT_OPERATIONALIZED", "reason": "The general-graph problem remains a long-standing open question, but the source gives no close upper/lower-bound gap or tractable restriction for a directional 2027–2031 forecast. The planar event is sharper and source-explicit."}
    ]


def build(issued_at: str | None = None) -> tuple[dict, dict, dict, dict]:
    issued_at = issued_at or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    radar = load_json(RADAR)
    baseline = load_json(BASELINE)
    radar_hash = hash_file(RADAR)
    if baseline.get("source_hashes", [{}])[0].get("sha256") != radar_hash:
        raise ForecastEngineError("frozen original radar baseline does not match current radar bytes")
    forecasts = [freeze_prospective_forecast(draft, issued_at) for draft in drafts()]
    if len({row["event_id"] for row in forecasts}) != len(forecasts):
        raise ForecastEngineError("forecast event IDs must be unique")
    source_hashes = [{"path": "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json",
                      "sha256": radar_hash, "scope": "FULL_RADAR_JSON_BYTES_UNMODIFIED"}]
    for forecast in forecasts:
        for source in forecast["sources"]:
            source_hashes.append({"path": source["url"],
                                  "sha256": sha256_bytes(canonical_json(source)),
                                  "scope": "CITATION_METADATA_RECORD_ONLY"})
    snapshot = build_prospective_snapshot(forecasts, issued_at, baseline["snapshot_id"], radar_hash, source_hashes)
    activation = {
        "schema_version": "1.0",
        "activation_id": "ACT-CS-PROSPECTIVE-" + snapshot["snapshot_id"].rsplit("-", 1)[-1],
        "created_at": snapshot["as_of"], "evidence_cutoff": snapshot["as_of"],
        "baseline": {"snapshot_id": baseline["snapshot_id"], "sha256": radar_hash,
                     "scope": "FULL_RADAR_JSON_BYTES; ORIGINAL_2026_10_16_RADAR_UNCHANGED"},
        "forecast_count": len(forecasts), "forecasts": forecasts,
        "prospective_snapshot": snapshot,
        "immutability": "CREATE_ONLY_JSON_BUNDLE_PLUS_APPEND_ONLY_ENGINE_SNAPSHOT; CORRECTIONS_REQUIRE_NEW_VERSION",
        "immutable": True,
    }
    activation["activation_sha256"] = sha256_bytes(canonical_json(activation))
    monitoring = {
        "schema_version": "1.0", "created_at": snapshot["as_of"], "active_monitoring_count": 0,
        "scheduled_jobs": [], "workers_started": False,
        "specifications": [{
            "event_id": row["event_id"], "active": False,
            "primary_sources": row["primary_future_sources"],
            "search_strategy": row["search_strategy"],
            "milestones": ["2027-01-01", "2028-12-31", row["deadline"]],
            "technical_milestones": {
                "PLANAR-THREE-SETS-CUT-UNCUT-112": [
                    "Check whether a theorem handles unweighted planar (1,1,2) Three-Sets Cut-Uncut exactly, including the preserved pair connectivity and infeasibility."
                ],
                "DISCRETE-FRECHET-TRANSLATION-PLANAR-N4": [
                    "Check for exact 2D discrete unrestricted-translation value computation at O(n^4 polylog n), and audit the stated computational model."
                ],
                "K-HOP-DOMINATION-LOW-EXPANSION-NO-GIRTH": [
                    "Check whether a theorem removes the girth restriction while preserving the port-numbering model, 3k+O(1) rounds, and the frozen approximation order."
                ],
            }[row["event_id"]],
            "adjudication": {"reviewers_required": 2, "llm_counts_as_reviewer": False,
                             "partial_progress_is_not_success": True,
                             "no_search_hit_means_negative": False,
                             "outcome_categories": ["EVIDENCE_FOUND_UNADJUDICATED", "EVENT_ACHIEVED",
                                                    "PARTIAL_PROGRESS_NOT_SUCCESS", "PREMISE_REVISION_NOT_SUCCESS",
                                                    "EVENT_CONTRADICTED", "INSUFFICIENT_EVIDENCE", "NOT_YET_DUE"],
                             "not_yet_due_state": "NOT_YET_DUE",
                             "insufficient_coverage_state": "INSUFFICIENT_EVIDENCE"},
            "status": "PREPARED_INACTIVE",
        } for row in forecasts],
        "activation_requires_separate_authorization": True,
    }
    rejected = rejected_candidates()
    report = {
        "record_id": "CS-BREAKTHROUGH-FORECAST-DISCOVERY-ACTIVATION-20261017",
        "created_at": snapshot["as_of"], "evidence_cutoff": snapshot["as_of"],
        "search_budget": {"original_radar_directions_reviewed": 12, "additional_candidate_questions_examined": 10,
                          "total_candidates_examined": 22, "distinct_subfields_in_depth": 6,
                          "events_operationalized": 3, "scientific_gate_passes": 3,
                          "forecasts_frozen": len(forecasts), "limits_respected": True},
        "discovery_decision": "ACTIVATE_THREE_QUALITATIVE_PROSPECTIVE_THEOREM_FORECASTS",
        "baseline": activation["baseline"], "activation_snapshot_id": snapshot["snapshot_id"],
        "activation_snapshot_sha256": snapshot["snapshot_sha256"],
        "forecast_snapshot_hashes": [{"event_id": row["event_id"], "snapshot_id": row["snapshot_id"],
                                       "content_sha256": row["content_sha256"],
                                       "snapshot_sha256": row["snapshot_sha256"]} for row in forecasts],
        "forecasts": forecasts,
        "rejected_or_not_frozen_candidates": rejected,
        "original_radar_disposition": [{"candidate_id": row["id"], "disposition": "NOT_REUSED_AS_FROZEN_FORECAST",
                                        "reason": "Prior activation found the broad event operationalization incomplete; no parent radar wording or historical cutoff was edited."}
                                       for row in radar["candidates"]],
        "integrity": {"paper3_modified": False, "paper4_modified": False,
                      "original_radar_modified": False, "historical_labels_created": False,
                      "outcome_labels_created": False, "numeric_probabilities_created": False,
                      "experiments_or_workers_started": False, "monitoring_active": False,
                      "reviewer_status": "PENDING_TWO_INDEPENDENT_HUMANS",
                      "source_hash_scope": "SOURCE_HASHES_COVER_CITATION_METADATA_ONLY_EXCEPT_FROZEN_RADAR_BYTES"},
        "prospective_snapshot": snapshot,
    }
    return activation, monitoring, report, snapshot


def main() -> int:
    try:
        activation, monitoring, report, snapshot = build()
        targets = (ACTIVATED, MONITORING, REPORT_JSON)
        existing = [str(path.relative_to(ROOT)) for path in targets if path.exists()]
        if existing:
            raise ForecastEngineError("create-only output already exists: " + ", ".join(existing))
        if SNAPSHOTS.exists():
            previous = [json.loads(line) for line in SNAPSHOTS.read_text(encoding="utf-8").splitlines() if line.strip()]
            if snapshot["snapshot_id"] in {row.get("snapshot_id") for row in previous}:
                raise ForecastEngineError("prospective snapshot is already present in append-only engine history")
        append_snapshot(SNAPSHOTS, snapshot)
        write_immutable_json(ACTIVATED, activation)
        write_immutable_json(MONITORING, monitoring)
        write_immutable_json(REPORT_JSON, report)
        print(json.dumps({"status": "FROZEN_QUALITATIVE_PROSPECTIVE_FORECASTS",
                          "created_at": activation["created_at"], "forecast_count": activation["forecast_count"],
                          "event_ids": [row["event_id"] for row in activation["forecasts"]],
                          "snapshot_id": snapshot["snapshot_id"], "snapshot_sha256": snapshot["snapshot_sha256"],
                          "activation_sha256": activation["activation_sha256"]}, ensure_ascii=False, indent=2))
        return 0
    except (ForecastEngineError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
