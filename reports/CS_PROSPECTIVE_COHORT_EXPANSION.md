# CS prospective cohort v2 — build and integrity report

**Frozen at:** 2026-10-17 03:15:09 UTC
**Decision:** a small, qualitative prospective benchmark cohort was expanded; no predictive performance is evaluated or claimed.

## What was created

The immutable v2 cohort has 10 forecast records: the 3 October 17 source records carried forward unchanged as values, plus 7 newly frozen qualitative questions. The new questions span 7 subfields. Dynamic matching and the ordered Ruzsa–Szemerédi parameter (ORS) are deliberately one research family, not independent evaluation units. The 3 legacy rows did not have a family identifier; the new cohort-level mapping assigns each a unique `LEGACY-<event_id>` label without rewriting the records.

New questions: unrestricted MAX BISECTION at the Goemans–Williamson ratio; explicit fully dynamic near-maximum matching with a fixed polynomial update-time saving; polynomial lower growth of the linear-density ORS parameter; a fixed exponential-base improvement for worst-case exact Subset Sum; optimization for two-stage block-structured integer programs with unbounded global coefficients; a multiplicative PTAS for 1D constant-depth shallow-circuit diamond-norm identity checking; and a valid fully adaptive approximate-GDP filter over an intermediate subsampling-rate range.

All 7 records have exact events, explicit scope and exclusions, primary-source baselines, qualitative directional judgments only, future deadlines, censoring rules, and independent-review requirements. No probabilities, scores, human labels, or outcomes were inserted. The two dynamic-matching/ORS records share the declared family ID `DYNAMIC-MATCHING-AND-ORS-EXTREMAL-STRUCTURE`; analyses must cluster them and must not count them as independent cases.

## Time and historical-record handling

The process clock at build time was 2026-10-17 03:15:09 UTC. The original 3 forecasts were issued at 02:47:37 UTC on that date, with a snapshot field `forecast_horizon.start = 2027-01-01`; their exact event definitions, however, say “by deadline.” Those records and the original snapshot are not edited. For any later evaluation, retain the original exact event as the primary endpoint and report post-issuance evidence before 2027-01-01 separately as an early-resolution interval. Do not silently shift their frozen dates. The seven new records explicitly set their observation start equal to issue timestamp.

The original activation, monitoring specification, and source radar remain unchanged. V2 monitoring is `PREPARED_INACTIVE`: no crawler, scheduled job, worker, or automated adjudication was started. A separate authorization and an actual monitoring implementation audit are required before activation.

## Candidate screening

14 additional literature leads were screened; 7 became operationalized questions and 7 were rejected or excluded from this issuance:

* 4-block integer programming FPT and the QMC linear-sample question had already received relevant 2026 primary results before issuance ([4-block IP](https://arxiv.org/abs/2609.23711), [4-block IP](https://arxiv.org/abs/2609.26746), [QMC](https://arxiv.org/abs/2609.10921)).
* A broad sublinear approximation target for minimum-dilation spanning trees, a truly subquadratic unit-disk graph diameter result, polynomial-time orthogonal-polygon square covering, and a point-algebra MinCSP parameterized classification were already resolved at the proposed broad endpoint ([minimum dilation tree](https://arxiv.org/abs/2609.08990), [unit-disk diameter](https://arxiv.org/abs/2510.16346), [orthogonal polygon covering](https://arxiv.org/abs/2407.02658), [point-algebra MinCSP](https://arxiv.org/abs/2310.05839)).
* Stateless asynchronous amnesiac flooding was not frozen because the scheduler, fairness, and termination semantics were not stable enough for a defensible event.

These rejections are screening decisions, not negative scientific outcomes. In particular, a literature search miss was never converted into a label.

## Reproducibility and interpretation

`prospective_cohort_v2_manifest.json` binds the cohort and monitoring documents to canonical content hashes and records source-file hashes. The appended snapshot is hash-verified and links to the original activation snapshot. Original rows are equality-checked against the source activation. A focused regression test validates IDs, hashes, inactive monitoring, and family clustering.

This is an initial benchmark substrate, not a validated forecasting benchmark: 10 questions are too few for reliable model comparison, outcomes are not due, event difficulty and field selection are heterogeneous, and qualitative expectations are not calibrated. The appropriate current scientific paper is a benchmark/methodology paper, not “Predicting Computer Science Breakthroughs with AI.” Paper 3 Target A (direct resolution/refutation) and Target B (substantial evidence growth) remain separate and have no new labels or scores. Paper 4 action-planning recommendations remain assumptions, not demonstrated planner utility.

## Artifact index

* `data/forecast_engine/prospective_cohort_v2.json`
* `data/forecast_engine/prospective_cohort_v2_monitoring.json`
* `data/forecast_engine/prospective_cohort_v2_manifest.json`
* `data/forecast_engine/followup_snapshots.jsonl` (one append-only new snapshot)
* `reports/CS_PROSPECTIVE_COHORT_EXPANSION.json`
* `tests/test_prospective_cohort_v2.py`
