# CS Breakthrough Prediction Engine — implementation checkpoint

**Disposition:** software-only implementation validated; predictive validity
not established; no scientific experiment or inference was run.

## What changed

The new `src/research_platform/forecast_engine/` package and static CLI provide
an append-only, point-in-time record layer around the existing Paper 3 and
Paper 4 workflows. The original 12-candidate qualitative radar was imported
into a one-time immutable baseline at
`data/forecast_engine/qualitative_editorial_baseline_20261016.json`. Candidate
IDs, rank order, prose, horizon labels, and citation links are copied from the
frozen radar JSON. The baseline hashes that source and identifies its citation
entries as citation records only; it does not imply full-text validation.

The engine has machine-readable schemas for research questions, evidence,
forecast snapshots, outcome adjudications, Paper 4 action plans and outcomes,
and reproducibility manifests. It keeps exact resolution, premise revision,
and evidence growth separate. Later evidence is checked by earliest verified
availability, and source uncertainty is quarantined. Snapshot differences
distinguish evidence already present in the baseline from genuinely added
events. Existing snapshots and plans are hash-checked and cannot be silently
rewritten.

Paper 4 candidate ranking can be frozen and displayed alongside simple
assumption-based selection views (least assumed cost, highest assumed
uncertainty reduction, and historical momentum). These are decision baselines,
not realized utility comparisons. Action execution feasibility and scientific
utility are separate fields; verified utility requires independent validation,
evidence, and actual cost.

The implementation reuses `research_platform.opportunity`'s AUROC/AUPRC/Brier
functions and the existing `research_platform.planner.rank_actions` plus its
declared expected-information-gain calculation. The adapter requires explicit
hypothesis priors, per-outcome likelihoods, weights, costs and provenance,
then freezes the resulting ranking. No likelihoods or weights are inferred
from the current research data. The existing Paper 3 Target A/B protocol and
frozen historical audits provide the readiness gates; their records were not
edited.

## End-to-end software demonstration

The deterministic CLI demo starts from the immutable baseline, presents a
synthetic future-dated evidence fixture, verifies that the original cutoff
rejects it, constructs a later snapshot that records the fixture, keeps the
original baseline hash unchanged, emits an exact diff and Paper 4
recommendation disclaimer, returns `NOT_READY` for a numerical forecast, and
outputs a fixture-only reproducibility manifest. The demo operates in a
temporary directory. Its status explicitly says
`FIXTURE_DEMONSTRATION_ONLY_NO_SCIENTIFIC_RESULT`.

The new focused suite has 20 tests covering this path and its fail-closed
conditions. Full repository tests and research checks are reported separately
in the final validation record.

## Current scientific gates

* **Paper 3 Target A:** unchanged and unscored. Direct resolution/refutation
  still lacks authenticated CS labels; no probability or score is created.
* **Paper 3 Target B:** separately represented as evidence-growth outcomes.
  Existing trajectory records are not converted into forecast labels; the
  current question set and classes do not satisfy the frozen score gate.
* **Paper 4:** recommendations remain assumption-dependent. Prior audited
  actions do not establish planner utility, and this software work adds no
  action outcome.
* **Retrospective prediction:** not run. There is no frozen, sufficiently
  powered, point-in-time CS outcome dataset ready for honest metric estimates.
* **Experiments or model execution:** none. No data harvesting, model fitting,
  inference, or background worker was started.

The baseline's milestone language is not yet a complete falsifiable endpoint:
numeric acceptance thresholds, population/workload or theorem scope, and
complete falsification criteria are explicitly marked missing. Human
operationalization is required before creating new frozen forecast labels.

## Limitations and decision

This checkpoint delivers usable software and a reproducible fixture workflow,
not a predictor or a computer-science discovery. The historical editorial
radar is preserved as descriptive content only. The exact Paper 3 source-native
five-class label mapping remains outside this implementation; operational CS
categories are not claimed to be Paper 3-native labels. No publication,
causal, forecast, or Paper 4 superiority claim follows.

**Decision:** accept the engineering artifact; keep Paper 3 and Paper 4
scientific claims gated. The next valid step is operationalizing the questions
and acquiring independently adjudicated outcomes under the frozen endpoint
protocol, not running a model on the current sparse records.
