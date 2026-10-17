# CS prospective forecasting data dictionary

This describes the existing v2 cohort and its append-only companion records. It is not a replacement schema and does not authorize edits to frozen records.

| Field / artifact | Meaning | Integrity and interpretation |
|---|---|---|
| `cohort_id` | Versioned registry identifier | Identifies this pilot cohort; not an independent study or benchmark validation. |
| `original_cohort.records[]` | Three records copied from the earlier activation | Preserve byte/value identity with the activation source. Their original family IDs are absent; cohort-level family mapping must not be written back into these records. |
| `new_forecasts[]` | Seven later qualitative forecasts | Each has its own event ID, research family, source cutoff, issue time, endpoint and deadline. Forecast direction is editorial, not a probability. |
| `event_id` / `question_id` | Event identity | Unique within the cohort; some legacy events predate `question_id`. |
| `scientific_question` | Short natural-language problem statement | Not the adjudication predicate; use the frozen exact event and assumptions. |
| `source_baseline` / `baseline_version` | Known results and source version used to formulate event | Must be checked against primary-source full text and date; citation alone does not establish source-content review. |
| `exact_event` / `frozen_event_definition` | Outcome predicate and deadline language | Both should be checked for consistency. ORS currently has a date conflict; record it in the separate defect ledger. |
| `frozen_assumptions` | Scope/model/quantifier constraints | A candidate result must match all material constraints. |
| `deadline` | Structured follow-up end date | For ORS it differs from the exact-event text. Never silently normalize. |
| `issued_at`, `issue_date`, `evidence_cutoff` | Point-in-time boundary | The three original rows also carry a 2027-01-01 nominal horizon start in their snapshot metadata; preserve and report this difference. |
| `research_family_id` | Dependency cluster | Dynamic matching and ORS share one family. It is the minimum grouping currently declared, not proof other questions are independent. |
| `subfield` | Topic classification | Descriptive only; not a sampling stratum or outcome class. |
| `expectation`, `forecast_direction`, `qualitative_only` | Directional editorial view | Not calibrated probabilities; do not compute Brier score, log loss, calibration, or accuracy from these fields. |
| `supporting_evidence`, `counterevidence` | Rationale at issue time | Preserve as text; not separately adjudicated evidence outcomes. |
| `review_status`, `reviewer_ids` | Human event-review status | Pending status and empty reviewer list mean no independent event review is complete. |
| `outcome_status`, `outcome_evidence_ids` | Outcome state and links | `NOT_YET_DUE` is a workflow state, not a label. No outcome IDs currently exist. |
| `content_sha256` | Hash of frozen event/citation record according to builder | Not a checksum of cited paper content. Verify scope before describing it as provenance. |
| `snapshot_sha256`, manifest hashes | Hashes of registry/snapshot/manifest objects | Integrity checks show artifacts have not changed relative to the manifest; they do not prove scientific correctness or source authenticity. |
| `source.hash_scope` | Scope of the source hash | `CITATION_METADATA_RECORD_ONLY` means metadata hash only, not full-text checksum. |
| `followup_snapshots.jsonl` | Later immutable snapshots | Append-only. Search findings remain candidate evidence until human adjudication. |
| monitoring JSON | Prepared monitoring specification | `PREPARED_INACTIVE`; no automated monitoring is running. |

## Event targets

Target A is exact direct resolution/refutation of the frozen question. Target B is a separate, dimension-specific evidence-trajectory rubric. Attention and planner/action utility are separate axes. Missing sources, reviewer disagreement, and search non-detection are not negative labels.

## Current counts

10 forecast records; 9 declared research-family units (the seven added events include two in one shared family and five separate families; the three legacy records are separately mapped in the manifest); 10 subfield/event categories per stored mapping; 0 human event reviews completed; 0 matured outcome labels; 0 predictive metrics; 0 active monitors. Counts describe the stored pilot, not the population of CS research.
