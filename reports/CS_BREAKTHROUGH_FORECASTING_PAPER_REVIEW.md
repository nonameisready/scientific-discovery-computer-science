# Independent-style critical review: benchmark/methodology manuscript

**Review status:** internal adversarial review; not an external or independent human peer review.
**Recommendation:** major revision before submission; do not submit this version as a validated benchmark paper.

## Central claim and fit

The defensible contribution is a protocol for prospectively freezing research questions, point-in-time source baselines, exact theorem-level event definitions, censoring rules, dependent-family identifiers, and separate adjudication targets. The manuscript does **not** establish that AI predicts breakthroughs, that qualitative forecasts are calibrated, or that the Paper 4 planner selects better experiments. The proposed title correctly avoids those claims.

## Strengths

1. Events are theorem-level and rule out near misses (restricted graph classes, method-specific barriers, proxy metrics, and search absence).
2. Original records are preserved and content-addressed; new questions have independent family and scope metadata.
3. Outcomes, human labels, forecasts, and publication activity are not conflated. Missing evidence remains censored.
4. Target A (direct resolution/refutation) and Target B (substantial verified progress) remain separate. The latter needs its own frozen rubric and human-adjudication dataset before evaluation.
5. The candidate screen records already-resolved leads instead of treating them as future events.

## Major threats to validity

* **Cohort size and selection:** 10 records, hand-selected from a research radar, are not a representative sample of CS questions. Seven new records do not repair the selection bias. No population-level generalization or model comparison is supported.
* **Forecast reliability:** all forecasts are qualitative editorial judgments, pending two human reviewers. They are not probability forecasts and cannot support calibration, AUC, or accuracy claims.
* **Outcome latency and right censoring:** most deadlines are 2030–2031. This paper can publish a protocol and baseline registry, but cannot validate future forecasting skill now.
* **Family dependence:** the dynamic-matching and ORS events are causally linked. Other questions may also share authors, techniques, or venues. A family ID is a start, not a complete dependency graph.
* **Endpoint adjudication:** evidence standards are written, but a two-reviewer adjudication workflow, disagreement protocol, and evidence packet format still need implementation and pilot reliability measurement.
* **Time-window ambiguity in the original three:** the engine horizon begins 2027-01-01 but issue time is 2026-10-17. The original rows are preserved; the manuscript must report the post-issue/pre-2027 interval separately rather than retroactively altering the dates.
* **Source freshness:** source cutoffs are content-addressed citation metadata, not cryptographic hashes of paper contents. Full-paper version hashes and archival copies should be recorded where legally permitted.
* **Novelty:** prospective scientific forecasting and benchmark methodology have adjacent prior literature. A dedicated systematic prior-art comparison is needed before asserting a first benchmark or novel methodology.

## Required before external submission

1. Independent domain experts must review each event definition, feasibility, and literature cutoff.
2. Conduct a prior-art review of forecasting science, science-of-science prediction, benchmark governance, and prospective evaluation datasets.
3. Publish a transparent inclusion/exclusion flow and complete candidate-screening log.
4. Add a formal rubric for Target B and distinguish its categories from direct resolution.
5. Pilot blinded adjudication on evidence packets; report reviewer agreement and adjudication costs without treating agreement as truth.
6. Provide a data dictionary, machine-readable schema, validation command, source provenance, and license/redistribution audit.
7. Obtain a larger, balanced and explicitly nonrepresentative-or-representative cohort design; preregister how field and family clustering will be handled.
8. Do not report predictive scores until matured labels and a valid temporal holdout exist.

## Decision

The two-stage publication strategy is scientifically sound. Stage 1 can become a benchmark/methodology manuscript after the above design and reproducibility work. Stage 2—whether AI forecasts CS breakthroughs better than simple baselines—must wait for matured, independently adjudicated outcomes. The current draft is a research manuscript draft and cohort pilot, not submission-ready evidence of forecasting ability.
