# Prospective Forecasting of Computer Science Research Breakthroughs: An Evidence-Grounded Benchmark and Evaluation Framework

**Manuscript status:** research draft; not submission-ready.
**Version:** 0.1, 2026-10-17.
**Evidence status:** prospective qualitative cohort pilot; zero matured outcomes; no AI forecast-performance claim.

## Abstract

Claims that artificial intelligence can predict scientific breakthroughs are difficult to test: “breakthrough” is often retrospective and underspecified, source information may leak across time, related questions are treated as independent, and absence of a discovered paper is mislabeled as failure. We present an evidence-grounded protocol for prospective evaluation of computer-science research forecasts. The protocol freezes a research question, point-in-time source baseline, exact event and deadline, admissible evidence, exclusions, censoring policy, research-family dependence, and independent-review requirements before the outcome window. It separates two targets: (A) direct resolution or refutation of a frozen question, and (B) substantial independently verifiable scientific progress that need not resolve it. We report an initial, manually screened cohort of ten qualitative prospective questions: three previously frozen records preserved unchanged and seven newly operationalized questions across seven subfields. The cohort includes explicit exclusions for candidate problems already resolved before issuance and groups dynamic matching with its ordered Ruzsa–Szemerédi structural parameter as one dependent family. All records remain unscored, outcomes are not yet due, and monitoring is inactive. The contribution is therefore a benchmark design and pilot registry—not evidence that AI predicts breakthroughs. We specify a second-stage temporal evaluation that will compare models with simple baselines only after sufficient independently adjudicated outcomes mature.

**Keywords:** scientific forecasting; computer science; benchmark design; temporal validation; research evaluation; evidence adjudication; censoring.

## 1. Introduction

Research forecasting is attractive but unusually vulnerable to hindsight. A topic may appear prescient only because its endpoint is redefined after publication; publication volume can be mistaken for scientific progress; and a failure to retrieve a result can be confused with evidence that no result exists. Machine-learning accuracy claims face an additional leakage risk: features computed after a forecast date can encode the outcome.

We propose a prospective benchmark protocol for computer-science research questions. We use “breakthrough” operationally, not rhetorically: an event must specify a mathematical or empirical claim, scope, comparison, deadline, and evidence standard. Forecasts are frozen with their source cutoff and content hash. Future evidence is separately collected and adjudicated. The framework is intentionally compatible with a later test of whether AI has predictive skill, but it does not assume such skill.

The program has two stages. Stage 1 builds the event registry and reproducible evaluation protocol. Stage 2 tests predictive validity after outcomes mature, using temporal holdouts and independent research-family units. The proposed title reflects this boundary. “Predicting Computer Science Breakthroughs with AI” would imply a validated ability not established here.

## 2. Evaluation targets

Let each unit be a frozen research question (q_i), issued at time (t_i), with a deadline (d_i), point-in-time evidence set (E_i(t_i)), and a declared research-family identifier (g_i).

### Target A: direct resolution or refutation

Target A asks whether, by (d_i), a primary-source result directly proves the frozen target, supplies a qualifying counterexample/refutation, or revises a premise in a way that settles the stated question. The full theorem must match the graph class, assumptions, model, approximation ratio, parameter regime, and quantifiers frozen in the event. Nearby results are partial progress, not success.

### Target B: substantial evidence growth

Target B asks whether substantial, independently verifiable progress occurs, even if the original question remains open. Candidate categories include a new verified theorem or bound, a matched-baseline algorithmic improvement, a replicated empirical improvement, an independent counterexample, premise revision, or substantive narrowing. These categories are not collapsed into a binary Target A label. Publication or citation counts, topical similarity, and search-result counts are not progress labels. A separate frozen rubric and adjudication study are required before Target B evaluation.

For both targets, statuses include `NOT_YET_DUE`, `EVIDENCE_FOUND_UNADJUDICATED`, a qualifying event label, `PARTIAL_PROGRESS`, `INSUFFICIENT_EVIDENCE`, and `VERIFIED_UNRESOLVED_AT_HORIZON` only after documented source coverage and independent review. Missing evidence remains missing; it is never imputed as a negative.

## 3. Prospective protocol

Before issuance, each event record freezes:

1. A precise question and source-as-of cutoff.
2. The strongest audited baseline and primary citations, with version dates and scope.
3. An exact outcome predicate, deadline, assumptions, and improvement threshold.
4. Explicit nonqualifying near misses and ambiguity rules.
5. Evidence provenance, source-coverage plan, censoring policy, and two-reviewer adjudication requirements.
6. Research-family/dependency metadata, so linked questions do not masquerade as independent samples.
7. A qualitative judgment only in this pilot. No numeric probability is added without a validated forecasting procedure.

The frozen record is content-addressed. Follow-up evidence is appended as a new record; it does not rewrite the forecast. Original cohorts remain immutable. Primary-source retrieval is a discovery mechanism, not an outcome label. At a deadline, a source-coverage audit and independent adjudication distinguish unresolved-at-horizon from insufficient evidence.

## 4. Initial cohort

The v2 registry contains ten question records. Three original forecasts are copied unchanged from the prior activation. Seven additional questions were frozen at 2026-10-17 03:15:09 UTC, after a source screen and before any post-issuance outcome search. They cover: (i) the unrestricted MAX BISECTION Goemans–Williamson ratio; (ii) fixed-exponent sublinear update time for explicit fully dynamic maximum matching; (iii) polynomial growth of a linear-density ordered Ruzsa–Szemerédi parameter; (iv) a fixed exponential-base improvement for worst-case exact Subset Sum; (v) optimization for two-stage block-structured integer programs with unbounded global coefficients; (vi) a multiplicative PTAS for diamond-norm identity checking of constant-depth 1D circuits; and (vii) valid approximate-GDP privacy filters over an intermediate subsampling-rate interval.

The dynamic-matching and ORS questions share one family identifier. They are analytically related and are not independent forecast examples. The other five new questions have distinct families. Three legacy rows predate family metadata; the cohort-level manifest maps each to its own legacy family without adding fields to the frozen rows.

Candidate selection is not a representative sample of computer science. Fourteen additional leads were screened; seven were operationalized and seven were excluded because a related endpoint had already been solved or the problem semantics were insufficiently fixed. Examples include 4-block integer programming and a linear-sample QMC result, both resolved in primary work before issuance. The exclusion log is preserved. This screening reduces obvious hindsight contamination but does not remove researcher-selection bias.

All seven new forecasts are qualitative, pending two human reviewers, and marked `NOT_YET_DUE`. No outcomes, forecast scores, or Paper 3 labels are present. The monitoring file is prepared but inactive: no crawler, worker, or scheduled job runs.

## 5. Stage 2: predictive evaluation design

When enough events mature, evaluate Target A and Target B separately. Use chronological splits defined before model fitting; group related questions by research family; compute all features only from sources available by each issue time; retain an untouched final period. Compare at least: (a) publication-volume baseline, (b) historical field-momentum baseline, and (c) source-only textual features. Any model trained on labels must be fit without future information. A “Paper 3 transfer” model is not assumed valid merely because a method worked in another corpus.

Report event and family counts, positive/negative/censored counts, reviewer agreement and adjudication protocol, calibration and proper scoring metrics only when probability forecasts exist, ranking metrics where appropriate, cluster-aware uncertainty, and power limitations. Do not publish AUROC or forecast probabilities when labels or class counts do not support them. A separate source-coverage report is required before unresolved-at-horizon is assigned. Target B requires dimension-specific reporting and must not be substituted for direct resolution.

Simple baselines are necessary: publication volume and field momentum may capture attention without predicting resolution, while textual similarity may retrieve related work without forecasting it. These are comparators, not ground truth. Forecast skill is established only by prospective labels and a fair temporal evaluation.

## 6. Relationship to planning (Paper 4)

Paper 4 is a planning methodology for competing hypotheses, evidence graphs, missing decisive evidence, candidate actions, costs, feasibility, and assumed information gain. It can structure how a research question is investigated. This registry does not validate Paper 4's action ranking, realized information gain, or superiority over simple selection baselines. Planning utility requires separate prospective action records and observed outcomes. Forecasting and action selection therefore remain distinct evaluation claims.

## 7. Limitations and governance

The pilot has only ten questions, no mature outcomes, qualitative editorial judgments, uneven subfield coverage, selected rather than sampled questions, and dependent events. Its family map is coarse. The original three records also have a temporal nuance: they were issued 2026-10-17 02:47:37 UTC, while their snapshot metadata says the nominal horizon begins 2027-01-01 and the exact event is “by deadline.” We preserve both. Evidence between issue time and 2027-01-01 will be reported as an early-resolution interval, not silently excluded or used to rewrite the original record.

The current artifact is a pilot registry, not a validated public benchmark or evidence of AI skill. External submission should wait for a systematic prior-art review, domain-expert event review, a formal Target B rubric, a blinded evidence-adjudication pilot, a transparent inclusion flow, license/provenance audit, and a larger cohort. Outcome monitoring, external publication, and OpenFindings posting are not authorized by this manuscript.

## 8. Conclusion

Prospective evaluation of scientific forecasting is possible only when the future event, information boundary, dependency structure, and evidence rules are fixed before outcomes. We provide a small auditable cohort and a protocol that keeps direct resolution, broader scientific progress, forecasting, and research planning separate. The present evidence supports a benchmark/methodology research program; it does not support the claim that AI can predict computer-science breakthroughs. Whether models outperform simple baselines remains a future empirical question.

## Data and reproducibility statement

The repository contains the cohort, inactive monitoring specification, manifest, append-only snapshot, candidate-screen report, and validation test. The manifest records content hashes. The original activation is preserved. No licensed full-text corpus is included. Reproduction command: `python3 -m unittest tests.test_prospective_cohort_v2` (or the repository's discovery command). The builder is create-only and refuses to overwrite artifacts.

## References

See `paper/CS_BREAKTHROUGH_FORECASTING_REFERENCES.bib` for primary sources. Core baselines include Bentert et al. on planar Two-Sets Cut-Uncut; Bringmann et al. on discrete Fréchet distance under translation; Brakensiek et al. on MAX BISECTION; Behnezhad and Ghafari on fully dynamic matching; Assadi, Khanna, and Kiss on ORS; ESA 2025 on Subset Sum; Cslovjecsek et al. on block-structured integer programming; Bravyi, Parham, and Tran on shallow-circuit identity checking; and Tran et al. on f-DP filters.
