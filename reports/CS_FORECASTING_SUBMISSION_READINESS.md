# Submission readiness and publication-path assessment

**Decision:** `NOT_SUBMISSION_READY`. **No submission, preprint deposit, or external publication was made.**

## Readiness by dimension

| Dimension | Current state | Gate |
|---|---|---|
| Frozen registry integrity | Cohort/snapshot metadata passes existing integrity tests; frozen source records remain unchanged | Sufficient for internal reproducibility only; not scientific validation |
| Event technical quality | Ten theorem-level questions with primary baselines; ORS deadline conflict; original-three window issue; other model/endpoint risks | Independent domain expert review required; ambiguous record must not be scored |
| Prior-art / novelty | PreScience is a prior scientific forecasting benchmark; same project has close historical backtesting plus a 200-question prospective instance | No novel benchmark claim supported; contribution delta not established |
| Cohort design | Ten selected qualitative records, incomplete candidate-level flow, heterogeneous events and coarse family mapping | Not representative and too small/unlabeled for model comparison |
| Outcomes/adjudication | 0 matured labels, 0 independent human event approvals, 0 adjudicated outcomes | No Target A/B evaluation or metrics |
| Target B | Separate proposed rubric provided; no reliability test | Requires independent rubric pilot; does not modify Paper 3's frozen protocol |
| Paper 4 | No prospective matched action outcome in this cohort | No planner utility claim |
| Source provenance | Registry artifact hashes verified; citation metadata hashes are not full-text hashes; source-version archives incomplete | Add legal source version/content hashes and theorem locators before release |
| Manuscript | Revised internal draft, bibliography expanded | Substantial contribution and independent scientific review still missing |
| Ethics and release | No license/redistribution audit for source-linked event metadata and no public deposit | Complete before any public benchmark release |

## Official venue fit checks (current public pages)

- **Quantitative Science Studies (QSS):** official scope includes theoretical and empirical work on science and the scientific workforce; it welcomes novel methodological approaches, but domain applications of existing methods need a novel contribution to understanding science. Its current author guidance calls for openly sharing essential data in a repository with a persistent identifier and a data-availability statement. That scope is plausible only if this project contributes something beyond a small CS-specific registry and can publish the required data. The current manuscript does not meet that bar. Sources: [QSS scope](https://direct.mit.edu/qss), [QSS submission guidelines](https://direct.mit.edu/qss/pages/submission-guidelines).
- **Research Evaluation:** official scope is evaluation of scientific research, technological development, innovation, and related policy/practice; the journal asks for a clear link to research evaluation theory/practice and states Articles are generally 8,000–10,000 words addressing an evaluation problem. Possible future fit if the method is validated and the implications for evaluation are substantive; not an endorsement or a present recommendation to submit. Source: [Author guidelines](https://academic.oup.com/rev/pages/author-guidelines).
- **NeurIPS 2026 Evaluations & Datasets:** the official call explicitly accepted datasets, protocols, tools, documentation, and audits, but requires a meaningful change/strengthening/enabling of AI evaluation and accessible, documented artifacts. The abstract deadline was 2026-05-04 and full-paper deadline 2026-05-06; both are past as of the audit. This edition is not a live route. Sources: [call](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets), [FAQ](https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ).

The QSS submission-guideline page is based on its current public content as retrieved for this audit; future requirements may change. No venue decision can substitute for editors' scope screening or peer review.

## Publication path recommendation

Keep a two-stage program as a research plan, not an assumed two-paper outcome:

1. **Stage 1 (future protocol/resource paper):** only proceed when a concrete methods delta beyond PreScience and the same-project astronomy work is specified; event definitions pass external domain review; inclusion/exclusion flow is fully reproducible; source dates/versions and licenses are auditable; Target B rubric is independently tested; and the released registry is judged useful by people beyond its author. The current ten-item pilot may be a development appendix or internal artifact, not the central validated benchmark claim.
2. **Stage 2 (future forecasting-skill paper):** wait for enough matured, independently adjudicated Target A and Target B outcomes, then run a preregistered family-grouped chronological comparison against simple baselines with untouched test period, proper scoring, cluster-aware uncertainty, and honest power/censoring. Do not claim model skill before this point.

The two-stage framing is conceptually sound, but it does not guarantee that Stage 1 merits publication before Stage 2. Current status: substantial revision and new validation evidence required. External peer review remains outstanding.
