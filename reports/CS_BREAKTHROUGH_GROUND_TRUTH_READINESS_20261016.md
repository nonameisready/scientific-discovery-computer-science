# CS Breakthrough Ground Truth & Historical Forecast Readiness

Audit timestamp: 2026-10-17 00:02 UTC. The required filename preserves the 2026-10-16 campaign label; this work was created after the radar snapshot. Structured counts and row-level limits are in [the JSON result](CS_BREAKTHROUGH_GROUND_TRUTH_READINESS_20261016.json).

## Decision

**Paper 3 Target A: `NOT_EVALUABLE`. Paper 3 Target B: `NOT_EVALUABLE`. Paper 4 action-ranking validation: `NOT_EVALUABLE`.** No forecast metrics, probabilities, training, inference, experiments, or human outcome adjudications were produced. This is a readiness audit, not a new cohort or a claim that the underlying questions were unresolved.

The main blocker is not simply sample size. The frozen CS source questions have no independently adjudicated exact outcomes. Missing or near-match literature is not a negative label. Target B's recorded trajectory observations are useful candidate evidence but have not passed independent two-reviewer adjudication.

## Frozen Paper 3 source taxonomy

The local provenance audit identifies Paper 3 repository `nonameisready/scientific-question-outcome-prediction-indicators` at commit `9b842fb0105c58819c4a5e6401ce984bd5b28b90`, with `paper/paper3.md`, `pipeline/models.py`, `docs/design_mapping.md`, and `results/baselines.json` as relevant files. It verifies that the method distinguishes future attention, scientific resolution, and premise revision, and describes a five-way outcome classifier. It does **not** preserve the exact five class strings or their annotation rules.

I tried the pinned raw and GitHub blob URLs for the three source files, but retrieval failed with a cache-miss response; no pinned checkout was found in the inspected local tree. Therefore the exact source-native taxonomy is `MISSING_EVIDENCE`: I have not inferred class names from the classifier shape, reported counts, or the project's separate CS labels. The linked repository/commit provenance is auditable, but the exact taxonomy remains unauthenticated. Paper 4's pinned source revision is also recorded from the local audit; its offline-planner boundary is explicit, while its publication URL remains unresolved in that audit.

## Historical cohort audit

The frozen records are unchanged. Their counts do not form one exchangeable benchmark because they came from different selection and labeling protocols.

| Evaluation target / cohort | Selected | Eligible source questions | Direct positives | Direct refutations/revisions | Verified no-progress/unresolved | Current disposition |
|---|---:|---:|---:|---:|---:|---|
| Target A: original blind cohort (2018–2021 cutoffs) | 20 | 13 | 0 | 0 | 0 | 13 eligible outcomes remain unadjudicated |
| Target A: Round 6 (2017–2020 cutoffs) | 16 | 6 | 0 | 0 | 0 | 6/6 unadjudicated; 5/6 had authenticated follow-up coverage, but all five records failed exact tuple matching |
| Target B: separate trajectory cohort (2017–2020 cutoffs) | 16 | 12 | 0 direct resolutions | 0 premise refutations/revisions | 0 independently verified no-progress | 12/12 lack independent final outcome adjudication |

The two Target A cohorts together contain 19 eligible source-paper questions, but **zero positive and zero negative labels**. The 20-paper cohort has 13 eligible and 7 ineligible rows; Round 6 has 6 eligible and 10 ineligible rows. All their fixed 3- or 5-year windows have elapsed by the audit date. That makes the records due for adjudication, not automatically negative.

In the separate Target B cohort, the existing trajectory artifact records 5 partial-progress, 1 independent-evidence-strengthening, and 3 scope-narrowing observations. These categories can overlap; they sum to neither a unique count nor final ground truth. They are `CANDIDATE_OUTCOME_EVIDENCE`, not `INDEPENDENTLY_ADJUDICATED_OUTCOME`. Direct resolution, premise revision, contradiction, explicit unresolved outcomes, and verified no-progress labels remain zero. Family clustering has not been verified; source-paper IDs are not assumed to be distinct question families. The union spans cutoff years 2017–2021, but the mixed cohorts cannot be combined to manufacture temporal sample size.

The frozen gates remain unchanged:

- **Target A:** at least 20 labeled questions; at least 5 positives and 5 negatives; at least 3 family groups in each chronological evaluation split; independent adjudication.
- **Target B:** at least 30 questions; at least 10 independently adjudicated positive progress and 10 verified no-progress/negative outcomes; at least 3 grouped chronological holdout blocks; frozen feature table.

Neither target has a valid labeled temporal holdout. Metrics prohibited by the gates include AUROC/AUPRC, F1, Brier score, calibration, ranking performance, and forecast probabilities. AUC or a “breakthrough probability” would be fabricated from the present data.

## Radar operationalization

All twelve 2026-10-16 radar items now have a post-baseline candidate event, possible supporting/refuting evidence, uncertainty sources, and reviewer questions in [`radar_endpoint_operationalization_20261016.json`](../data/forecast_engine/radar_endpoint_operationalization_20261016.json). **Zero are freeze-ready.** Eleven still need essential endpoint, threshold, comparator, population, or independent-oracle decisions. The adaptive-IVM item additionally needs reframing because the broad changing-skew claim was already covered by the audited heavy/light rebalancing result.

The radar itself remains an editorial snapshot, not a forecast table. The operationalizations were written on 2026-10-17, after its 2026-10-16 baseline. Their proposed five-year due dates are conditional on a future endpoint freeze; no forecast, outcome, or hindsight-correct label was created. Attention, direct resolution, premise revision, substantive evidence progress, and computational impact are represented as separate axes. Publication/citation counts, topical similarity, proposal ratings, and search non-detection are excluded as outcome substitutes.

## Independent adjudication readiness

The new [adjudication protocol](../docs/CS_BREAKTHROUGH_OUTCOME_ADJUDICATION_PROTOCOL.md) defines exact question/assumption/computational-model/baseline/metric/date/independence checks, source priority, theorem verification, replication, benchmark comparability, partial progress, premise revision, contradiction, missingness, disagreement, appeals, and reviewer independence. One reviewer may only triage candidate evidence. Two independent human reviewers are required for any final outcome; a third reviews disagreements. No inter-rater reliability is claimed because this cycle did not double-code cases.

The [worksheet schema](../schemas/forecast_engine/adjudication_worksheet.schema.json) and [blank template](../data/forecast_engine/adjudication_worksheet_template.json) are ready for future human review. Existing source and evidence records were not relabeled.

## Paper 4 prospective validation

The existing audit found five heterogeneous non-QAOA feasibility decisions, only one complete pre/post plan correspondence, and zero independently verified efficacy outcomes. This is not evidence that the planner succeeded or failed scientifically. The Paper 4 protocol in the adjudication document requires timestamped, hashed pre-action rankings over the complete candidate set; explicit competing hypotheses and provenance-linked gaps; cost/feasibility/utility assumptions; retention of all alternatives; post-action actual costs and new evidence; independent information-gain review; and comparison with lowest-cost, highest-assumed-uncertainty-reduction, evidence-momentum, and—only in an authorized future study—random eligible-action baselines. No research action was executed for this assignment.

## Evidence-based next path (no gate lowering)

1. Recover the exact pinned Paper 3 repository files to close the source-taxonomy gap. If not accessible, keep the mapping missing.
2. Only re-adjudicate the existing frozen eligible cases for which candidate primary sources or forward citation chains already exist; use two independent reviewers, stop at the frozen retrieval boundary, and do not substitute easier known outcomes.
3. If direct outcomes remain sparse, propose a separately versioned cohort with source-only selection, family grouping, endpoint and horizon frozen before follow-up retrieval. Do not add it to existing cohorts silently and do not promise it will meet the label gates.
4. Keep all historical forecasts unscored until the original target-specific class, grouping, temporal, and adjudication gates pass. For prospective radar items, complete endpoint design first, then freeze with a true new timestamp and observation window.
5. For Paper 4, collect only future authorized actions under a common pre-action record and retain feasibility failures separately from scientific outcomes. Do not claim ranking superiority from the current heterogeneous records.

## Integrity and validation

No historical cohort, source screen, label, Paper 3/Paper 4 methodology code, supervisor state, queue, worker record, or experiment artifact was edited. No experiment, simulation, model fitting/inference, worker, service, new cohort, or successor task was started. The existing user-dirty state/queue/supervisor/Paper 3 HTML files were preserved. See final repository checks in the task handoff; no commit should stage those unrelated paths.
