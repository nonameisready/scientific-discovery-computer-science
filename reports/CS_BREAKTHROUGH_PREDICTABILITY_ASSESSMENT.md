# Predictability assessment: what this evidence can and cannot say

**Cutoff:** 2026-10-17 03:50:01 UTC.

## Scientific target

Primary target Q2 is whether a frozen CS question receives **substantial independently verifiable technical progress** during the stated period, whether or not the original question is fully answered. Operational categories follow the existing, separately versioned Target B rubric: verified theorem/bound; algorithmic improvement against a frozen matched baseline; independently replicated empirical improvement; independent counterexample; premise revision/refutation; or substantive narrowing. These remain dimensions rather than a single inferred “success” score. Target A is direct proof/refutation of the original proposition. Attention, direct resolution, evidence progress, and practical impact are not interchangeable.

## Candidate indicators and evidence labels

| Indicator | Point-in-time definition | Classification here | Provenance and limitation |
|---|---|---|---|
| Explicit formal bottleneck | A primary paper states the exact remaining question and assumptions. | `OBSERVED_SOURCE_FACT` for the cited papers. | Verifiable from the paper; does not establish that the problem is near solution. |
| Recent theorem/algorithm progression | Pre-cutoff sequence changes a bound, model, or applicable class. | `OBSERVED_SOURCE_FACT` descriptively; predictive relation is `SCIENTIFIC_HYPOTHESIS`. | Results may be related or dependent; rate-to-future extrapolation is untested. |
| Known gap width | Difference between strongest comparable upper/lower guarantees under same model. | `OBSERVED_SOURCE_FACT` only after model alignment; otherwise `UNVALIDATED_HEURISTIC`. | Exact comparability is especially difficult for model-sensitive complexity results. |
| Available proof/evaluation path | A verifier, code, public instance, or independent theorem-check procedure exists at cutoff. | `OBSERVED_SOURCE_FACT` where source artifact is public. | Accessibility increases verifiability, not likelihood of success. |
| Independent approach convergence | Distinct groups/methods attack the same proposition or parameter. | `UNVALIDATED_HEURISTIC` unless provenance independence is established. | Shared authors/data/benchmarks can create false convergence. |
| Field activity/popularity | Pre-cutoff papers/citations in a topic. | `OBSERVED_SOURCE_FACT` if measured; predictor is unvalidated. | Never used as a success label; can reward attention rather than progress. |
| Counterevidence/barriers | Conditional lower bounds, impossibility, failed replications, or explicit negative results. | `OBSERVED_SOURCE_FACT` within exact scope; forecasting effect unvalidated. | Must not transfer across models or assumptions. |
| Human endpoint agreement | Agreement on whether a result meets a frozen predicate. | Unavailable for this CS portfolio. | Astronomy backtesting reports κ=0.17 for two careful human raters on a distinct taxonomy; that is a warning, not a CS estimate. |

No indicator is an `EMPIRICALLY_SUPPORTED_PREDICTOR` for CS Target A or B in this project. The only Paper 3 quantitative evidence mentioned is source-reported astronomy attention performance; it is not a CS result, a Target B score, or calibrated probability. No candidate receives a numeric likelihood.

## Qualitative method and sensitivity

Candidates pass an inclusion gate only if a primary-source baseline, exact progress object, main obstacle, counterargument, and independent verification path can be stated. The eligible set is ordered using qualitative considerations: evidential clarity, plausible technical route, horizon tractability, significance, verifiability, and counterevidence. The ranking is not a weighted or calibrated model.

Three sensitivity readings were compared: (1) proof tractability emphasizes explicit theorem targets (DP, planar cut-uncut, two-stage IP); (2) capability impact emphasizes inference and verified software; (3) evidence maturity emphasizes public artifacts and independently checkable endpoints, demoting process verification and autonomous science. Leading-family membership is more robust than exact rank; medium-horizon ordering is especially sensitive. Full order variants are recorded separately.

## Predictive power verdict

Paper 3 currently has **no validated predictive power on CS outcomes**: frozen cohorts lack sufficient independently adjudicated Target A/B labels, no leakage-free CS feature table has passed the sample/class/group gates, no temporal holdout model was fitted, and no probability calibration exists. It is scientifically incorrect to infer a CS forecast from astronomy AUC. Paper 4 contributes a useful organization of competing explanations, evidence gaps, possible observations, and costed actions, but its efficacy is unvalidated and no information-gain value here is empirical.

Qualitative judgments still answer the portfolio question: they make explicit which issues appear more likely to yield visible technical progress and why. Their validity will be testable only after future outcomes mature and independent adjudication reliability is adequate. Prospective evaluation should compare source-only Paper 3 features and qualitative forecasts against publication-volume, field-momentum, and text-only baselines, with family-grouped chronology and an untouched future period; do not use those baselines as outcome labels.

## Uncertainty

The largest uncertainty is not only future technical difficulty. It includes event selection, source-version coverage, publication latency, adjudicator agreement, benchmark drift, and dependence among related candidates. The ten frozen forecasts are purposive commitments rather than a representative sample. The ORS deadline inconsistency remains. The final ranking is a one-researcher qualitative synthesis; it has not been elicited from an independent panel and does not claim inter-rater reliability.
