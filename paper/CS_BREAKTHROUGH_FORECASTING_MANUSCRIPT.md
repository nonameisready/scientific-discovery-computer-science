# Prospective Forecasting of Computer Science Research Breakthroughs: Protocol Design and a Pilot Event Registry

**Manuscript status:** internal research draft; not submission-ready.
**Version:** 0.2, 2026-10-17.
**Evidence ceiling:** ten frozen qualitative event records; no matured labels, forecast scores, model comparison, or demonstrated forecasting skill.

## Abstract

Claims that AI can forecast scientific breakthroughs require more than plausible ideas or hindsight-selected success stories. The target event, information boundary, evidence standard, censoring rule, and dependence among research questions must be specified before outcomes are observed. We describe a protocol for freezing theorem- and algorithm-level computer-science events and report a ten-record pilot registry assembled from a qualitative research radar. The registry contains three earlier records and seven additional events; it is selected, heterogeneous, and not an exchangeable or representative sample. Two records share a research family, one frozen record has a deadline/event-date inconsistency, and the three earlier records have a pre-2027 observation-window ambiguity. No outcomes have matured, no human event review is complete, and no monitoring is active. We separate direct resolution/refutation (Target A) from independently verifiable evidence growth (Target B), and both from attention, publication activity, and research-action utility. A prior-art audit finds substantial overlap with scientific forecasting benchmarks and, more directly, with a same-project astronomy historical-backtesting protocol that includes a 200-question prospective instance. The present artifact therefore does not establish a novel benchmark or validated evaluation framework. Its defensible status is a protocol proposal and pilot registry whose scientific contribution remains to be demonstrated through independent event review, repaired prospective governance for future cohorts, and adjudication reliability work. Predictive-validity claims are deferred until outcomes mature.

## 1. Research question and claim boundary

The methodological question is whether specific CS research claims can be frozen in a way that permits later, independent, point-in-time adjudication without redefining success after the fact. This is distinct from asking whether an AI system forecasts those claims accurately.

For event (i), let (q_i) be the frozen scientific question, (t_i) its issue/cutoff time, (d_i) its deadline, (E_i(t_i)) the admissible source record at issue, and (g_i) its research-family identifier. A result is not a match merely because it concerns a similar topic: reviewers must compare the object, assumptions, model, baseline, metric, threshold, quantifiers, version date, and evidence completeness.

The current evidence supports none of the following claims: (i) AI can predict CS breakthroughs; (ii) the ten items represent CS research; (iii) the records form a validated benchmark; (iv) qualitative directional judgments are calibrated; (v) Paper 3 transfers to CS; or (vi) Paper 4 ranks actions better than simple baselines. The cohort is a small, selected pilot registry, with unresolved technical defects.

## 2. Related work and originality

Scientific forecasting and prediction of research impact predate this registry. Science-of-science work has predicted citations, field trends, researcher impact, and proxies for breakthrough papers. Min, Bu, and Sun, for example, study early citation-network structure as a predictor of papers designated as breakthroughs; such retrospective bibliometric prediction is not the same target as theorem-level resolution of a frozen open CS question.

More directly, **PreScience** (Ajith et al., 2026) is a scientific forecasting dataset and benchmark built from 98,000 AI papers and a 502,000-paper scholarly graph. It includes temporally snapshotted metadata, seven paper-level or topic-level forecasting tasks, baselines from heuristics to language models, and released data/code. Its outcomes (e.g. future contribution similarity, citations, collaborators, topic trends) differ from the question-level exact theorem endpoint here, but its prior existence rules out broad novelty claims such as “the first scientific forecasting benchmark.”

The closest conceptual priors are the same project's **Evidence-Based Scientific Question Discovery** and **Historical Backtesting for Scientific Question Discovery: A Protocol and Astronomy Pilot** (Mao, 2026), which freeze source corpora and questions, adjudicate later answers/partial progress/independent posing/ignored status and premise support/refutation, evaluate historical cutoffs, study reviewer agreement, and release a 200-question prospective instance. These are same-project prior work, not independent corroboration. The current CS registry could eventually be a domain-specific extension, but the ten-item pilot has not established a distinct methodology contribution, reliability, or predictive validity. Scientific-discovery benchmarks such as ResearchBench assess inspiration retrieval and hypothesis composition/ranking; PaperBench assesses research replication. These are adjacent but not direct substitutes for prospective resolution forecasting.

Accordingly, the novelty verdict is **not established**. The protocol has sensible components, but freezing events, separating missing evidence from a negative, temporal cutoffs, and family grouping are established methodological practices. A defensible contribution would need to show a precise new operationalization problem solved beyond the same-project astronomy protocol and PreScience, with independent users, transparent curation, reliable adjudication, and a usable released dataset. This pilot does not yet do that.

## 3. Targets and adjudication units

### Target A: direct resolution or refutation

Target A asks whether a primary source published after (t_i) proves or refutes the exact frozen proposition by (d_i), including its graph class, parameter regime, assumptions, computational model, approximation factor, and quantifiers. Premise revision is recorded as its own dimension; it counts as direct resolution only when it settles the frozen proposition under a predeclared rule. A nearby theorem is partial progress, not a positive label.

### Target B: evidence trajectory / substantial progress

Target B is a separately specified evidence-growth endpoint, not a synonym for direct resolution and not a claim inherited automatically from Paper 3. Candidate dimensions are: (1) verified theorem or bound; (2) algorithmic improvement against a frozen matched baseline; (3) independent empirical replication; (4) independent counterexample; (5) premise refutation/revision; (6) substantive scope narrowing. Contradictory evidence, continued uncertainty, and unadjudicated evidence are retained as distinct states. Categories may coexist and should not be collapsed without an explicit analysis plan.

Attention, citations, publications, topical similarity, and search-result volume are not Target A or B labels. “No source found” is missing evidence. A horizon-end “verified unresolved” status requires a documented coverage protocol plus independent review; otherwise use `INSUFFICIENT_EVIDENCE`.

Paper 3's source-native attention, answer, and premise-revision taxonomy is not silently rewritten here. The separate CS Target B rubric in this project is an extension and requires its own protocol governance and human-labeling validation. The existing frozen Paper 3 cohorts and labels are unchanged.

## 4. Registry and source-only event protocol

The v2 registry contains ten qualitative records: three initially issued at 2026-10-17 02:47:37 UTC and seven added at 03:15:09 UTC. The latter cover planar cut-uncut, exact discrete Fréchet under translation, high-girth-free local domination, MAX BISECTION, dynamic matching, ordered Ruzsa–Szemerédi growth, exact Subset Sum, block-structured integer programming, shallow-circuit identity checking, and adaptive privacy filters. The seven new records represent seven stated subfields; all ten span ten event types/subfields as encoded in the registry. Dynamic matching and ORS are linked in one research family and must not be treated as independent evaluation units.

The source set includes primary conference papers/preprints and explicit source dates. This cycle checked theorem scopes against original primary sources where accessible, but did not archive full texts or compute content checksums of source papers. In the frozen cohort, `CITATION_METADATA_RECORD_ONLY` means exactly that: a hash of a citation metadata object is not a paper-content checksum and does not establish which full text was read. Independent reviewers have not yet certified any event definition.

The selection report states that 14 additional leads were screened, seven operationalized and seven excluded. It names the exclusions and their reasons. It does not supply a complete row-level log for all 14, search timestamps/queries/results for each, or a balanced inclusion rationale for each selected record. The original three came from a radar and the seven later records were selected by the project author. The resulting cohort is therefore a convenience/purposeful sample, not representative, probability-sampled, or sufficiently large for outcome modeling.

## 5. Event-level technical limitations

The separate technical audit covers all ten frozen event IDs and preserves their original bytes. It finds a definite contradiction in `ORS-POLYNOMIAL-GROWTH-001`: its structured `deadline` is 2030-12-31 while its `exact_event` says “By 2031-12-31.” The event cannot be adjudicated as written; it must remain frozen and be marked ambiguous in an append-only defect record, not silently corrected.

For the original three, `issued_at`/`evidence_cutoff` is 2026-10-17, while the snapshot's nominal horizon starts 2027-01-01 and the event predicate says “by deadline.” The original bytes remain authoritative. A result first public in the intervening period is post-issue evidence for the literal event but precedes the nominal horizon; both timestamps must be shown and the pre-2027 interval reported separately. No researcher should shift the dates or omit an early qualifying result.

Other issues are not necessarily theorem errors, but require reviewer attention: model comparability in the Fréchet event; precise outcome and adversary conventions for dynamic matching; equivalence of ordered matching prefix/suffix conventions; bit-length and unboundedness semantics in the IP optimization event; the exact zero-distance meaning of a multiplicative quantum-circuit PTAS; and the scope of a strict improvement over RDP accounting in the privacy-filter event. These are recorded as adjudication risks, not retroactive forecast changes.

## 6. Cohort selection, dependence, and temporal validity

The denominator “14 additional leads” is reported by the creation artifact, but the evidence packet does not permit independent reconstruction of the complete search-to-selection flow. The ten records are heterogeneous milestones across complexity theory, algorithms, privacy, quantum information, and distributed computing. Outcomes have different base rates and proof-cost profiles. The cohort has no observed labels, no outcome class balance, and no matured event. Qualitative predictions are not probabilities, so calibration, accuracy, AUC, ranking skill, and superiority cannot be computed.

Family grouping is minimal: the dynamic matching and ORS events share one family; other records are assigned separate families even though dependence through shared techniques/authors may exist. The unit of inference must be the research family, and the entire dependency graph should be reviewed before any split. The cohort does not support temporal train/test evaluation.

## 7. Prospective evaluation and quality gates

Three questions must be evaluated separately:

1. **Software validity:** are schemas, hashes, append-only behavior, date checks, and cutoff enforcement correct? Unit tests can answer only this engineering question.
2. **Adjudication validity/reliability:** can independent domain experts apply the frozen rubric to full evidence packets consistently? Require blinded dual review, field-by-field endpoint matching, a third-review path for disagreement, and report raw agreement and an appropriate reliability measure with uncertainty. Model-model agreement is not human reliability.
3. **Predictive superiority:** do pre-registered forecasts beat baselines on independent matured outcomes? This requires calibrated probabilities, target-specific labels, family-grouped chronological splits, untouched final test data, proper scoring rules, baseline comparisons, cluster-aware uncertainty, and adequate class counts. None is available now.

The existing repository gates remain unchanged. Target A requires at least 20 independently adjudicated outcomes with class and family counts specified in the frozen protocol. Target B requires its own larger cohort and its separate class/group gates. Do not lower them to fit ten prospective items. Publication volume, field momentum, and source-only textual features are legitimate simple comparators only after the outcome/forecast unit is well-defined and label support is adequate. For qualitative-only legacy judgments, no proper scoring rule can be retrofitted.

## 8. Paper 4 boundary

Paper 4 is described locally as an offline action planner combining expected information gain, provenance/independence, tractability, and cost. Expected-utility experimental design is established well before this project; for example, Chaloner and Verdinelli review Bayesian experimental-design criteria in a unified decision-theoretic framework ([1995 DOI](https://doi.org/10.1214/ss/1177009939)). The Paper 4 paper URL/version itself is not yet pinned in the local methods record, so its exact contribution cannot be independently novelty-audited here. This registry did not freeze competing-action sets, execute a ranked action, measure realized information gain, or compare against simple action-selection baselines. It provides no evidence of planner utility or superiority. Future evaluation must record feasibility separately from scientific information gain and compare the same candidate set prospectively.

## 9. Limitations, governance, and readiness

The pilot is selected, ten-item, qualitative, unadjudicated, not source-content-archived, and not yet externally reviewed. Monitoring is `PREPARED_INACTIVE`; no crawler, scheduled job, worker, or automatic adjudication ran in this audit. The original cohort, snapshots, Paper 3 cohorts, Paper 4 records, queues, supervisor files, budgets, and user-dirty files are not to be modified. No manuscript submission or OpenFindings publication is authorized.

**Readiness: internal research draft / not submission-ready.** A first-stage methodology paper is reasonable as a future objective, but the current pilot alone does not yet support a strong standalone benchmark/methodology contribution. The manuscript needs substantial redesign around the prior-art gap, complete transparent curation, event-level external review, source provenance and licenses, an adjudication reliability study, and a clear incremental contribution over the same-project astronomy protocol. Predictive-validity claims belong to a later paper after outcomes mature.

## 10. Conclusion

The two-stage idea is scientifically sound: first establish a carefully designed, usable event registry and adjudication method; later test prediction skill after the events mature. But “benchmark first, predictive paper later” is not automatically a publishable two-paper plan. PreScience already occupies broad scientific forecasting benchmark territory, and the same project already has a close historical/ prospective scientific-question evaluation protocol. The present ten-record CS registry is a useful pilot and source of future audit work, not proof of novelty, reliability, benchmark readiness, or AI forecasting ability. Preserve its records, append the ORS date defect, seek independent event/rubric review, and refrain from scoring until labels and valid evaluation design exist.

## References

See [`CS_BREAKTHROUGH_FORECASTING_REFERENCES.bib`](CS_BREAKTHROUGH_FORECASTING_REFERENCES.bib). Key sources include PreScience ([arXiv:2602.20459](https://arxiv.org/abs/2602.20459)); Mao's question-discovery and historical-backtesting papers ([arXiv:2608.09968](https://arxiv.org/abs/2608.09968), [arXiv:2608.16795](https://arxiv.org/abs/2608.16795)); ResearchBench ([ACL 2026](https://aclanthology.org/2026.findings-acl.644/)); PaperBench ([arXiv:2504.01848](https://arxiv.org/abs/2504.01848)); and the event-specific primary literature cited in the registry.

## Data and reproducibility statement

The frozen cohort is `data/forecast_engine/prospective_cohort_v2.json`; this paper does not alter it. The protocol/rubric, data dictionary, and reproduction commands are provided separately in `docs/CS_FORECASTING_TARGET_B_ADJUDICATION_RUBRIC.md`, `docs/CS_FORECASTING_DATA_DICTIONARY.md`, and `docs/CS_FORECASTING_REPRODUCIBILITY_GUIDE.md`. Cohort integrity checks validate record-level and snapshot hashes; source citation hashes are metadata hashes, not source-paper hashes. No full-text corpus or new human labels are released by this audit.
