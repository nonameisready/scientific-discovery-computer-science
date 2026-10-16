# Paper 3 / Paper 4 Forecast Integration Audit — 2026-10-16

## Executive result

The current project can support a source-grounded, qualitative editorial radar and a structured evidence/action dossier. It cannot support a numeric CS breakthrough forecast, a CS Paper 3 score, or a claim that Paper 4 selects scientifically superior actions. No model inference, training, benchmark, experiment, worker, or new action-outcome evaluation was run for this audit.

The findings below are reconstructed from the repository's pinned-source audit and frozen protocols. The pinned upstream source revisions are Paper 3 `9b842fb0105c58819c4a5e6401ce984bd5b28b90` and Paper 4 `d3b61480a390a224bff9d688322f26270734c0a4`. Direct web retrieval of those exact GitHub source files was unavailable in this session; the locally committed source audit and methodology documents are the evidence used here. That source-access limitation is not filled by guessing.

## Paper 3 — what is supported

### Unit, cutoff, horizon, features

The audited Paper 3 baseline uses a question × historical cutoff as the observation unit. Its astronomy pilot contains 980 questions, five cutoffs (2012, 2014, 2016, 2018, 2020), eight subfields, four question-source types, eight years of pre-cutoff context, and a five-year future outcome window. Features are restricted to information available at the cutoff: question structure, prior evidence context, novelty, falsifiability, tractability and environmental controls. Repeated snapshots and related questions require temporal grouping; random splits are not a valid transfer evaluation.

### Outcomes and exact-label boundary

The locally audited scientific outcome roles are future substantive attention, direct scientific resolution/answer, and premise revision/refutation. The original work also explored a five-way outcome classifier; the local source audit records macro-F1 0.23 and only eight answered and four premise-refuted cases among 980. It does **not** establish a reliable separate resolution or premise-revision predictor. Attention is the only substantially supported outcome in the audited astronomy results (2020 temporal AUC 0.713; cross-subfield AUC 0.71; leave-one-subfield-out values 0.62–0.78).

The exact source-native string enumeration and decision rules for all five classes are not reproduced in the local audit document available in this worktree, and the pinned upstream manuscript could not be fetched by the web reader. Accordingly, this report does not invent those strings or map them onto the CS pilot. The current CS protocol has its own frozen categories: `direct_supported`, `direct_refuted_or_premise_revised`, `explicitly_unresolved`, and `unadjudicated`, with attention kept separate. Those are transfer-protocol categories, not claimed verbatim Paper 3 source labels.

“Neglect” / “not addressed” must be treated with special caution. Paper 4's local audit documents a blind citation-graph re-adjudication of 62 high-specificity questions: of 36 initially called `not_addressed`, 34 were engaged under a lenient rule and 25 under the strict rule. The original utility-attention association (reported p=.004) disappeared under re-adjudication (p=.70/.61). Thus low retrieval yield is not evidence of neglect, no follow-up, or a negative scientific outcome. The transfer pipeline does not assign an absence label from search failure.

### Existing performance and limits

- **Attention:** the astronomy temporal AUC 0.713 is a source-reported ranking result for that domain and evaluation, not a CS result. The audited source also reports cross-subfield AUC 0.71 and LOSO 0.62–0.78.
- **Resolution/premise revision:** five-way macro-F1 0.23 with only eight answered/four premise-refuted cases does not support reliable class-specific prediction.
- **Calibration:** no calibrated CS probabilities exist. The local audit does not establish that the cited astronomy AUC is calibrated; AUC alone does not establish calibration.
- **CS transfer:** original blind cohort: 13 eligible questions, all 13 without authenticated direct outcome labels; separately observable cohort: 12 eligible, all direct outcomes unadjudicated; Round 6: 6 eligible and zero exact direct matches. Partial progress, scope narrowing and other evidence-trajectory dimensions are separate and cannot become resolution labels.
- **Predictor artifact:** no validated CS model artifact with an input schema, frozen point-in-time features, and eligible inference protocol is available for this radar. No inference was authorized or performed.

Therefore Paper 3 cannot currently answer “which CS question has X% probability of resolution by 2030?” It also cannot rank the candidates by validated attention probability. This report offers only explicit qualitative editorial judgments.

## Paper 4 — what is supported

### Actual planning workflow

The source-audited offline planner represents a question, competing hypotheses, a typed evidence graph with provenance and independence, missing/weak/contradictory evidence gaps, candidate evidence actions, assumed action likelihoods and cost/tractability/novelty/information-value terms, then ranks an action and supports a Bayesian evidence update. It does not execute the action. Likelihoods and utility weights are declared assumptions; they are not observed frequencies merely because a score is calculated.

### Validation status

The repository's action-outcome audit covers five prior lead-level feasibility decisions and finds zero matched efficacy outcomes. Only one has an inspectable pre-action ranking record and outcome gate; other cases lack a unified immutable ranking. Thus rank correlation, calibration, top-K utility against realized scientific information, and superiority over simple baselines are not estimable. The audit explicitly gates Paper 4 planning utility as unvalidated.

The QAOA records supply negative historical evidence: a conditional state-quality effect replicated, but a fixed-shot complete procedure underperformed standard sampling, and a separate proposed action was infeasible. EDCS yielded a narrow counterexample to a frozen implementation variant, not a general algorithmic breakthrough. These observations show why feasibility and scientifically successful outcomes must remain distinct; they do not validate the planner.

The prior scaled-benchmark “neglect” claim was withdrawn after citation-graph adjudication. The correct Paper 4 role here is to make assumptions, gaps, actions, costs and falsification conditions explicit—not to pronounce a field neglected or an action optimal.

## Integration: what the two methods can and cannot do together

**Can do now:** use source-only evidence to define a candidate question; preserve competing explanations and provenance; distinguish attention, direct resolution and premise revision; propose a discriminating action with explicit assumptions and costs; record what observation would upgrade, downgrade or close the lead. That is a useful decision dossier.

**Cannot do now:** produce calibrated CS breakthrough probabilities; claim forecast accuracy; substitute partial progress or publication activity for direct resolution; estimate the causal benefit of a Paper 4-selected action; claim the joint system beats trend, volume, textual, cost-only or uncertainty-only baselines; or infer “neglect” from missed retrieval.

The radar's rankings are a human-readable synthesis, not predictions produced by the two systems. “Attention” is not “resolution”; resolution is not “impact”; a high-impact problem is not automatically near resolution.

## Future validation plan (no work executed here)

1. **Authenticate source semantics first.** Preserve the exact Paper 3 class enumeration and adjudication manual from its pinned source; retain the CS transfer mapping separately. Any ambiguous category must be resolved before labeling.
2. **Paper 3 Target A:** retain frozen historical cohorts unchanged. Only a separately versioned, source-cutoff-selected cohort can add rows. Target is exact independently authenticated resolution/refutation under the frozen object, assumptions, comparator, endpoint and falsification criterion in 3–5 years. Current gate remains ≥20 labeled units, ≥5 positive and ≥5 negative, grouped chronological splits and independent adjudication. Search misses remain missing.
3. **Paper 3 Target B:** separate target for substantial independently verified evidence growth (new theorem/bound, matched algorithmic improvement, replicated empirical gain, independent counterexample, premise revision, or substantive narrowing). Current frozen gate remains ≥30 questions, ≥10 positive and ≥10 verified no-progress/negative outcomes, ≥3 grouped chronological blocks, and outcome adjudication that excludes publication counts and topic similarity. Do not merge B into Target A.
4. **Freeze features and baselines:** only source-version text, explicit uncertainty, baseline gap, endpoint specificity, artifact availability at cutoff and point-in-time field momentum. Compare to simple baselines only after labels pass the relevant class gate; preserve an untouched final time period and question-family grouping.
5. **Paper 4 prospectively:** timestamp the full action ranking, priors/likelihoods, assumed costs, expected information gain and alternatives before action. Afterward independently record feasibility separately from scientific evidence yield. Compare against lowest-cost, highest-uncertainty, and simple field-momentum choices where comparable. Accumulate independent actions; do not score planner superiority from a single success or failure.
6. **Combined claim gate:** only after Paper 3 passes temporal outcome evaluation and Paper 4 has prospective action-outcome records can the combined system be tested against baselines. Measure resolution, evidence-growth, attention, impact, and action utility as distinct endpoints. Require calibration checks for probabilities, missingness analysis, adjudicator agreement and leakage audit. No experiment or inference is authorized by this plan.

## Final capability assessment

| Question | Current answer |
|---|---|
| Does Paper 3 beat documented baselines on CS outcomes? | Unknown; no eligible labeled temporal CS evaluation. |
| Has it demonstrated valid time-separated astronomy attention performance? | The pinned-source audit reports temporal AUC 0.713 for astronomy; it is not transferable evidence for CS. |
| Are CS probabilities calibrated? | No. None are produced. |
| Does Paper 4 select better actions than simple baselines? | Unknown; no adequate paired prospective action outcomes. |
| Are Paper 3 and 4 meaningfully integrated and validated as a joint predictor? | No. Their concepts are used together in a qualitative dossier only. |
| What is predictive in this report? | Nothing from a validated predictive model. All candidate rankings and outlooks are qualitative editorial synthesis. |
| What remains useful? | A provenance-linked, falsifiable map of bottlenecks, milestones and evidence that would change the ranking. |

**Audit status:** complete as a bounded method/capability review; source-native five-class spelling remains an explicit source-access limitation; no scientific outcome has been relabeled; no successor task, experiment, inference, training or worker was started.
