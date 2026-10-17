# CS breakthrough outcome adjudication and prospective validation protocol

Version: `CS-GROUND-TRUTH-ADJUDICATION-V1`

Prepared: `2026-10-17T00:02:01Z`

Status: **protocol proposal; not a completed independent adjudication study**

This protocol supplements, and does not replace, the frozen Paper 3 protocols. It does not alter the original 20-paper cohort, the separate 16-paper evidence-trajectory cohort, Round 6, the 2026-10-16 radar, or any historical labels. The endpoint operationalizations were authored after the radar cutoff and cannot be represented as predictions made on 2026-10-16.

## Evidence levels and unit of adjudication

Every record must carry one of these distinctions:

| Level | Meaning | May enter Paper 3 ground truth? |
|---|---|---|
| `VERIFIED_SOURCE_FACT` | A primary-source passage, date, version, theorem, artifact, or reported measurement has been checked and cited. | No, not by itself. |
| `PROPOSED_ENDPOINT` | A candidate event definition written for future prospective use. | No. |
| `CANDIDATE_OUTCOME_EVIDENCE` | A potentially relevant dated source has been found but exact matching and independent review are incomplete. | No. |
| `INDEPENDENTLY_ADJUDICATED_OUTCOME` | Two independent human reviewers agree under a frozen endpoint; disagreements have been resolved by a third reviewer or left explicitly unresolved. | Yes, subject to the target-specific frozen gate. |
| `UNRESOLVED` | Available sources do not decide the frozen proposition, or reviewers cannot resolve a substantive disagreement. | Not a negative label. |
| `MISSING_EVIDENCE` | Retrieval, version, date, full text, denominator, or provenance is inadequate. | No. |
| `NOT_YET_DUE` | The frozen follow-up horizon has not ended. | No. |

The unit is a frozen source question grouped with its verified research family. A paper, result, or related topic is not automatically a separate independent unit. Retain source-paper IDs, family membership, question wording, cutoff, version hash, horizon, and later evidence as separate fields. Before splitting, group all versions, replications, and near-duplicate formulations from one research family together.

## Question and endpoint matching rubric

For every candidate follow-up, reviewers independently answer `MATCH`, `MISMATCH`, or `UNCLEAR` for each field and cite the source location supporting that decision:

1. **Question/object:** Is it the same object or formal proposition, not only the same topic?
2. **Assumptions:** Are all material assumptions, input regimes, and scope restrictions compatible?
3. **Computational model:** For algorithmic claims, do input model, resource model, adversary, oracle, and cost accounting match?
4. **Baseline/comparator:** Is the source-frozen comparator used, or is a proved equivalence available?
5. **Metric and endpoint:** Are the same outcome, denominator, units, and direction measured?
6. **Threshold/falsifier:** Does the evidence meet or violate the frozen success/falsification condition? A post hoc threshold cannot be used.
7. **Version and timing:** Is the exact source version and first-public date authenticated? Is the result strictly after the question cutoff and no later than the frozen observation end?
8. **Independence:** Are authors, data, code, or proof checking sufficiently independent for the claimed category? “Different paper” alone is not independence.
9. **Evidence completeness:** Are the primary full text, proof, raw measurements, benchmark versions, and denominators available at the level required by the endpoint?

Any `MISMATCH` on a necessary condition prevents a direct-resolution label. `UNCLEAR` leads to `UNRESOLVED` or `MISSING_EVIDENCE`, not a guessed binary outcome. A shortest-path, metric, systems, or empirical result on a different task may count as partial progress only if the frozen trajectory rubric permits it and the relation is explicit.

## Separate outcome axes

Do not collapse these dimensions into one success variable:

- **Attention:** engagement by dated work under the source-native Paper 3 definition. Do not substitute current citation count or topic volume. The exact source-native class strings and annotation rules have not been recovered in this task; until the pinned Paper 3 files are directly authenticated, this axis remains unmapped and unscored.
- **Direct resolution:** exact result for the frozen question, assumptions, model, endpoint, and falsifier.
- **Premise refutation/revision:** evidence invalidates or narrows a necessary premise. Keep this distinct from a solution to the original question.
- **Substantive evidence progress (Target B):** one of the frozen categories: verified theorem/bound directly narrowing the gap; matched-baseline algorithmic improvement; independent empirical replication; independent counterexample; premise refutation/revision; or substantive scope narrowing that changes a boundary. Publication, citation, proposal score, implementation announcement, and topical similarity do not qualify.
- **Computational impact:** separate deployment or operational outcome with a defined population, exposure, baseline, cost, and impact measure. An algorithmic benchmark win alone does not establish impact.

The existing `research/paper3_target_b_protocol_v1.json` controls Target B categories and thresholds. The existing Target A three-year protocol and Round 6 five-year rule remain as each cohort froze them; do not harmonize or extend their horizons after seeing evidence.

## Adjudication sequence

1. **Freeze first.** Record exact source question text, source URL/version/hash, cutoff, object, assumptions, computational model, baseline, endpoint, denominator, success threshold, falsifier, observation end, family group, and allowed source types. Timestamp and hash the record before follow-up retrieval. A missing essential field means `NEEDS_ENDPOINT_DESIGN`, not permission for a reviewer to invent it.
2. **Search and capture.** Log queries, databases, dates, result IDs, full-text access, failed retrievals, and exclusions. Search non-detection is coverage metadata only. Never code it as `VERIFIED_UNRESOLVED_AT_HORIZON`.
3. **Candidate evidence.** One researcher may identify a candidate source and prepare a provenance packet. This is `CANDIDATE_OUTCOME_EVIDENCE`, not a ground-truth label. The packet contains canonical URL/DOI/arXiv ID, version, first-public date, source hash when locally available, exact pages/sections/theorem/table, and a neutral summary.
4. **Blind independent review.** Two reviewers independently see the frozen endpoint and source packet, but not each other's decisions or any model-generated conclusion. Each fills a separate worksheet and records field-by-field matches, decision, rationale, and citations. Reviewers disclose relevant authorship/collaboration and prior involvement.
5. **Resolve or preserve disagreement.** Exact agreement is required for a final binary/positive label. Any difference on outcome class, endpoint relation, assumption/model/comparator/metric match, date, or independence goes to a third reviewer who receives both reasoned worksheets after submitting an initial independent view. If disagreement remains, record both views and set `DISAGREEMENT_UNRESOLVED`; do not majority-vote away a definitional problem.
6. **Finalize append-only.** Create a new adjudication version with reviewers, timestamps, evidence IDs, decision, uncertainty, and links to prior versions. Appeals/corrections append a superseding record with reason and reviewer provenance; never edit or delete the prior adjudication or event log.
7. **Audit agreement.** Report raw agreement and a chance-corrected statistic only when sample size and class distribution make it meaningful. No inter-rater reliability is claimed until cases are independently double-coded. Adjudication consensus is not a substitute for reliability measurement.

### When one reviewer is insufficient

One reviewer can only triage a source into a candidate-evidence queue. Two independent reviewers are required for every claimed positive, direct negative/refutation, verified no-progress outcome, premise revision, contradiction, independent-strengthening event, or final `UNRESOLVED` label. Three reviewers are required when the first two disagree on any necessary matching field or evidence level. A negative/no-progress label additionally requires a completed, documented retrieval protocol with independently checked coverage; it can never be assigned from search absence.

An LLM can help locate or summarize source passages, but cannot become one of the independent human reviewers, cannot silently set a final outcome, and must not see future evidence while generating historical source-only features.

## Paper 3 readiness and evidence-acquisition plan

The frozen gates remain unchanged:

- **Target A:** at least 20 labeled questions, at least 5 positive and 5 negative, at least three question-family groups in every chronological evaluation split, and independent adjudication.
- **Target B:** at least 30 questions, at least 10 independently adjudicated positives and 10 verified no-progress/negative outcomes, at least three grouped chronological holdout blocks, and a frozen feature table.

Current status is `NOT_EVALUABLE`; exact counts are in `reports/CS_BREAKTHROUGH_GROUND_TRUTH_READINESS_20261016.json`. All 13 original blind-cohort eligible questions, all 6 Round 6 eligible questions, and all 12 trajectory-cohort eligible questions remain without independently adjudicated direct outcomes. The 5 partial-progress, 1 independent-strengthening, and 3 scope-narrowing observations in the trajectory artifact remain candidate evidence records, not final human labels. All fixed historical windows in those cohorts have elapsed; none is `NOT_YET_DUE`, but elapsed time does not turn missing evidence into a negative.

Evidence-based next steps, without relaxing gates:

1. Recover the exact pinned Paper 3 source files to authenticate source-native label strings and rules; if unavailable, keep that mapping missing and use only the separate explicitly named CS rubrics.
2. Conduct a bounded, provenance-complete, two-reviewer re-adjudication only for the already frozen eligible questions with extant candidate primary sources or traceable citation chains. Stop when the frozen search protocol is exhausted; do not expand by keyword variations or replace missing rows with known winners.
3. If valid labels remain sparse, propose a separately versioned source-only cohort with publication-year cutoffs, endpoint observability rules, family grouping, and follow-up protocol frozen before outcome search. Selection must not use later outcomes. It is a proposal, not an added observation.
4. Wait for future prospective windows to mature where appropriate. Do not claim the required class counts will be reached; feasibility is empirical.
5. Freeze source-only features before labels are revealed, group by family, retain an untouched final chronological period, and compute metrics only after the existing gates pass. Until then report label counts and `NOT_EVALUABLE` only.

## Twelve radar items: prospective operationalization

The machine-readable item-by-item records are in `data/forecast_engine/radar_endpoint_operationalization_20261016.json`. All twelve have candidate event statements but **zero are freeze-ready**. Eleven require endpoint/threshold/unit decisions; the broad adaptive-IVM formulation additionally requires reframing because the existing source audit found the broad skew-adaptation claim already covered by amortized rebalancing. Each record distinguishes evidence that could support the event from counterevidence and lists unresolved definitions and independent reviewer decisions.

The 2026-10-16 snapshot is historical qualitative editorial evidence only. Operationalizations were created at the timestamp in the machine-readable artifact. No forecast was made on the new definitions, no outcome is present, and the candidate 2031 date is conditional on freezing the endpoint at the stated creation time.

## Paper 4 prospective action validation

Use the existing `schemas/forecast_engine/paper4_action_plan.schema.json` and `paper4_action_outcome.schema.json`; do not create a parallel planner or infer numeric utility from outcomes. Before any future authorized action:

1. Freeze the original scientific question, competing hypotheses, evidence graph/gaps, all eligible candidate actions, provenance roots, cost assumptions, feasibility assumptions, and the Paper 4 ranking. Save a content hash and timestamp before selection or execution.
2. Record all options considered. Evaluate each option under fixed, disclosed assumptions. Keep Paper 4 utility separate from three fixed simple baselines: lowest estimated cost; highest prespecified uncertainty reduction; and evidence momentum computed only from pre-action evidence. A random eligible-action baseline is allowed only in a future authorized prospective comparison with a frozen candidate set and randomization seed.
3. Record selection rationale, actual execution or blocker, actual cost, raw evidence IDs, and result. A feasibility blocker is not scientific hypothesis evidence. No execution is not a null efficacy outcome.
4. Two reviewers independently assess whether new evidence was genuinely informative: does it distinguish the frozen competing hypotheses, satisfy the source question's endpoint, and reduce a declared uncertainty rather than merely add a paper? Record their reasons and dissent; do not backfill a missing pre-action plan.
5. Keep ranking quality, feasibility prediction, actual scientific utility, and causal action benefit separate. No superiority claim before multiple matched, prospectively frozen action sets and independently reviewed outcomes support a valid comparison. No action was executed under this assignment.

## Reviewer worksheet

The ready-to-copy blank record is `data/forecast_engine/adjudication_worksheet_template.json`; its schema is `schemas/forecast_engine/adjudication_worksheet.schema.json`. It requires source/version/date, frozen endpoint, assumption/model/baseline/metric/threshold matches, evidence level, explicit decision rationale, reviewer independence declaration, and dissent. Blank fields mean pending, never a negative outcome. Final records must additionally satisfy the existing `outcome_adjudication.schema.json` and the cohort-specific frozen protocol.
