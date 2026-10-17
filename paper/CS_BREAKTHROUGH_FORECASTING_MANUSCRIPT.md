# Forecasting Future Computer Science Breakthroughs from Scientific Evidence: A Prospective Research Portfolio and Methodological Study

**Status:** internal research manuscript; not submission-ready.
**Version:** 0.3, 2026-10-17.
**Evidence cutoff:** 2026-10-17 03:50:01 UTC.
**Forecast type:** qualitative and uncalibrated; no Paper 3 CS predictions or predictive-skill claim.

## Abstract

We ask which specific computer-science questions are strongest candidates for substantive technical progress in 2027–2028 and 2029–2031. We define progress as a verified theorem or bound, matched-baseline algorithmic improvement, independent replication, independently checked counterexample, justified premise revision, or material narrowing of a frozen question—not attention or publication counts. We audit ten frozen prospective events without altering them, reassess a twelve-item CS radar, and screen new primary-source leads in formal verification, AI inference, agent verification, databases, graph algorithms, and cryptography. The resulting two-horizon portfolio is a qualitative research judgment, not a calibrated probability model. Near-term leaders are repository-scale code-and-proof synthesis, constrained LLM inference scheduling, intermediate-regime adaptive privacy filters, dynamic approximate matching, and artifact-level agent verification. Medium-horizon candidates include the dynamic matching–ordered-Ruzsa–Szemerédi bottleneck, planar Three-Sets Cut-Uncut, planar discrete Fréchet under translation, two-stage integer programming with unrestricted global coefficients, and reproducible scientific agents. Recent primary sources show concrete progress—for example, repository proof agents and speculative inference scheduling—but those results are author-reported and not independently reproduced here. Paper 3 has no validated predictive performance on CS Target A or B; Paper 4 provides a transparent action-structuring vocabulary but no demonstrated planner superiority. The manuscript therefore reports a falsifiable qualitative portfolio and an explicit future evaluation protocol, not evidence that AI can predict breakthroughs.

## 1. Introduction

Forecasting research progress is vulnerable to hindsight, vague outcomes, and popularity substitution. A forecast can appear prescient if “success” is redefined after the event; a citation surge is not a theorem; and a search miss is not a negative outcome. This study answers a narrower question: which technically precise CS problem families deserve the strongest qualitative expectation of independently verifiable progress over the next five years, and what evidence would change that ordering?

The time boundary is the public evidence available by 2026-10-17 03:50:01 UTC. The ten prospective event records remain immutable commitments, not validated model scores. Their selected and heterogeneous design does not represent all CS research. This portfolio is not a population-level estimate.

## 2. Related work and originality

Science-of-science work predicts citations, impact, or bibliometric “breakthrough” proxies; for example, [Min et al.](https://doi.org/10.1016/j.techfore.2020.120502) use knowledge-structure variation to predict breakthrough designations. [PreScience](https://arxiv.org/abs/2602.20459) supplies a large, time-snapshotted scientific forecasting benchmark over AI papers and future paper/topic outcomes. [ResearchBench](https://aclanthology.org/2026.findings-acl.644/) scores inspiration retrieval, hypothesis composition, and ranking; [PaperBench](https://arxiv.org/abs/2504.01848) evaluates replication of published AI research. The same project has already published an astronomy historical-backtesting protocol and a 200-question prospective instance, including a study of outcome-label agreement ([question discovery](https://arxiv.org/abs/2608.09968), [historical backtesting](https://arxiv.org/abs/2608.16795)).

These works rule out a broad “first scientific forecasting benchmark” claim. Our present contribution is narrower: an evidence-linked, two-horizon qualitative portfolio with explicit outcome separation and counterevidence. Whether that is independently novel or publishable is not established. A future paper would need a demonstrated methodological increment beyond PreScience and the same-project astronomy protocol, external users, transparent selection, reliable human adjudication, and matured outcomes.

## 3. Research question and forecast targets

The primary target is Q2: substantial independently verifiable technical progress in a specified period. The outcome dimensions remain separate:

* **Target A:** exact proof or refutation of the frozen proposition under its assumptions and quantifiers.
* **Target B:** substantial progress short of full resolution: verified theorem/bound, matched-baseline algorithmic improvement, independently replicated empirical improvement, independent counterexample, premise revision, or substantive narrowing.
* **Attention:** research activity or citation/publication visibility; never used as a success label.
* **Impact:** practical consequence if an advance works; not its probability.

The existing Target B rubric remains a separately versioned extension to Paper 3. This study does not rewrite Paper 3’s source-native taxonomy or historical labels. Contradictory evidence, continued uncertainty, and unadjudicated status remain distinct. Search non-detection is missing evidence, not a negative.

## 4. Evidence and candidate selection

We inspected ten frozen events, twelve prior radar candidates, and seven additional primary-source leads. We merged related questions into families and did not treat dynamic matching and ordered Ruzsa–Szemerédi (ORS) structure as independent. New leads included Vero and CoCo-Prover for repository-scale formal software, Spexis for inference scheduling, MAS-ProVe for process verification, semiring incremental view maintenance, and a dynamic maximal-matching result. Leads already resolved in their stated form or lacking a stable objective endpoint were not promoted. No new prospective event was frozen: new leads either overlap existing families or lack a non-arbitrary, independently adjudicable success threshold. The original ten were not modified.

Primary sources were checked for exact object, assumptions, model, baseline, outcome and stated limitation. The selection is purposive, not representative; the full selection and evidence records are in the companion reports and machine-readable portfolio.

## 5. Forecasting method

An opportunity first passes a source gate: an identifiable baseline, a falsifiable progress event, a technical obstacle, contrary evidence, and an independent verification route must be describable. Eligible questions are ordered qualitatively by (i) a credible technical path, (ii) horizon tractability, (iii) significance, (iv) evidence and endpoint clarity, and (v) strength of counterevidence. We use no numerical weights or probability estimates. The ranking is an editorial decision priority, not an empirically supported predictor.

Evidence labels are: `OBSERVED_SOURCE_FACT` for dated primary-source statements; `SCIENTIFIC_HYPOTHESIS` for untested predictive relationships; `UNVALIDATED_HEURISTIC` for the qualitative ordering; and `EMPIRICALLY_SUPPORTED_PREDICTOR` only after independent outcomes and temporal evaluation. No CS indicator in this study qualifies for the last category. A recent theorem is evidence that progress happened, not a validated predictor that further progress will happen.

## 6. Prospective portfolio and results

The 2027–2028 ordering is: (1) repository-scale code-and-proof synthesis; (2) inference scheduling jointly handling KV state and speculation; (3) fully adaptive privacy filters in intermediate sampling regimes; (4) fixed-exponent sublinear update time for approximate dynamic maximum matching; and (5) artifact-level multi-agent process verification.

For 2029–2031, the ordering is: (1) the dynamic matching–ORS extremal chain; (2) planar (1,1,2)-terminal Three-Sets Cut-Uncut; (3) exact planar discrete Fréchet under translation near the conditional exponent boundary; (4) two-stage IP optimization with unrestricted global matrices under the frozen parameterization; and (5) research agents that execute and independently reproduce evidence.

The most robust qualitative signal is that constrained software and inference systems have visible short feedback loops and objective artifacts; they are plausible near-term progress areas, but their reported gains remain implementation- and workload-sensitive. Theorem-facing candidates have clearer endpoints but less predictable time-to-proof. These orders do not mean that each item is more likely than not to succeed.

## 7. Technical case studies

### 7.1 Repository-level verified software

Vero contains 43 multi-module instances; its authors report 27 full code-and-proof solves for the strongest evaluated configuration and ten instances resistant to all tested configurations ([Vero](https://arxiv.org/abs/2608.13522)). [VeriSoftBench](https://arxiv.org/abs/2602.18307) reports difficulty on deep repository dependencies. [CoCo-Prover](https://arxiv.org/abs/2610.09681) reports improved success-cost results, including up to 26/43 Vero solves, in its own evaluation. This supports a concrete expectation of benchmark progress, not general correctness. A proof validates the encoded specification; an independent specification audit remains necessary.

### 7.2 Inference serving

KV-constrained scheduling results differ by stochastic and adversarial arrival models; the fully adversarial model admits no constant competitive ratio ([Jaillet et al.](https://arxiv.org/abs/2502.07115)). [Spexis](https://arxiv.org/abs/2609.34370) introduces speculative-parallel scheduling and reports up to 34% request-rate increase on its evaluated GPU/workload configurations. The next meaningful progress test holds memory, quality, arrival trace, hardware, and tail SLO fixed. A maximum configuration-specific speedup is not a universal forecast.

### 7.3 Adaptive privacy

[Tran et al.](https://arxiv.org/abs/2602.06756) show that a natural fully adaptive f-DP filter is invalid and derive approximate filters for low and high sampling-rate regimes. Intermediate regimes are a precise remaining opportunity, but no broad impossibility or solution is assumed. The exact frozen event’s comparator and improvement region remain under-specified in the prior technical audit.

### 7.4 Dynamic matching and ORS

The approximate dynamic maximum-matching bound is linked to an ordered-RS extremal parameter ([Assadi et al.](https://arxiv.org/abs/2406.13573)). [Bernstein et al.](https://arxiv.org/abs/2504.20780) achieve sublinear update time for dynamic **maximal** matching; this is important adjacent progress but does not solve approximate **maximum** matching. The frozen ORS deadline conflict is preserved. The two questions share a family and cannot be counted as independent successes.

### 7.5 Agent verification and scientific discovery

[MAS-ProVe](https://arxiv.org/abs/2602.03053) reports that process verification does not consistently improve multi-agent outcomes and can have high variance. EIG and ResearchBench evaluate ideation or benchmark-native quality; PaperBench evaluates replication. The astronomy backtesting study finds low agreement between two careful human annotators under its outcome taxonomy ([historical backtesting](https://arxiv.org/abs/2608.16795)). These facts support prioritizing outcome reliability and artifact reproduction, not a claim that autonomous scientists already deliver verified discoveries.

## 8. Sensitivity and uncertainty

Under proof-tractability emphasis, adaptive privacy, planar cut-uncut, and two-stage IP rise. Under capability-impact emphasis, inference serving and repository code/proof rise. Under evidence-maturity emphasis, exact theorem endpoints rise and process verification/autonomous science fall. Leading family membership is more stable than ordering; medium-horizon ranks are particularly sensitive. These are ordinal robustness checks, not statistical uncertainty intervals.

Major uncertainty includes selection bias, publication delay, source-version provenance, benchmark drift, family dependence, and label reliability. Source hashes in the registry cover citation metadata, not full paper contents. Author-reported results are not independent replications. The ORS event’s date conflict and the original-three observation-window issue remain as recorded.

## 9. Paper 3 and Paper 4 integration

Paper 3’s astronomy attention AUC is not a CS Target A/B result, and the historical CS outcomes do not meet the frozen sample, class, group, and adjudication gates. No CS model was fitted or scored; no AUC, calibration, or probability is reported. The project cannot claim validated CS predictive skill.

Paper 4 structures competing explanations, provenance-linked evidence gaps, and candidate evidence actions. Here its role is to identify discriminating source checks and future verification designs. Expected information gain is not assigned numerically because action likelihoods are not calibrated; no action-efficacy dataset demonstrates planner superiority.

## 10. Future evaluation and adjudication

For Target A and Target B separately, future evaluators should preserve question-family groups, source cutoffs, immutable event text, and chronological splits. Human reviewers should assess primary-source scope and evidence independently; disagreement should be retained and reliability reported. Missing evidence is not a failure label. A temporal model comparison requires eligible outcomes, a preregistered final period, simple volume/momentum/text baselines, and calibration checks. Paper 4 requires prospective action ranking before execution, followed by independent feasibility and evidence-yield coding. No such future validation is claimed here.

## 11. Limitations and threats to validity

The portfolio is one researcher’s purposive, heterogeneous shortlist. No independent panel reviewed the final ordering. There is no calibrated base rate for the selected event classes. Some source artifacts do not have archived full-text hashes. Events have differing horizons and outcome types. Author evaluations, preprints, and theorem statements have different evidence strength. Forecast ordering may be wrong even when source extraction is correct. The manuscript does not establish benchmark novelty, forecasting accuracy, planner efficacy, or a new CS theorem.

## 12. Conclusion

The strongest qualitative 2027–2031 opportunities are repository-scale verified code/proof synthesis and constrained inference scheduling in the near term, and dynamic matching/ORS plus specific planar and fine-grained algorithmic questions over the medium term. Adaptive privacy filters are a sharply specified theory opportunity; process verification and scientific agents remain highly uncertain because artifact-level outcome reliability is unresolved. These are uncalibrated research judgments with explicit failure conditions. Paper 3 currently has no validated CS predictive power; Paper 4 contributes structure but not proven action superiority. This manuscript is an internal research result, not submission-ready.

## 13. Reproducibility appendix

The canonical structured portfolio and its hash manifest are in `data/forecast_engine/final_breakthrough_portfolio.json` and `data/forecast_engine/final_breakthrough_portfolio_manifest.json`. The complete evidence per item is in `reports/FINAL_CS_BREAKTHROUGH_FORECAST_2027_2031.json`; the technical and predictability audits are separate reports. Original frozen forecast files are unchanged. Tests validate files and source mappings but do not validate the truth of forecasts. No experiments, model inference, labels, external publication, or worker execution occurred.

## References

See `CS_BREAKTHROUGH_FORECASTING_REFERENCES.bib` for source records. Primary URLs and exact claims are also embedded in the canonical portfolio and evidence analysis.
