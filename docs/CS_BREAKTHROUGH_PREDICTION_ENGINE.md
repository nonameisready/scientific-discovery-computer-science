# CS breakthrough-prediction engine (implementation 0.1)

## Purpose and scientific boundary

This is an append-only, point-in-time record and evaluation-gating layer for
the existing Paper 3/Paper 4 research program. It is not a learned predictor,
an evidence harvester, or a research worker. The current implementation
imports the frozen 12-item qualitative radar as an editorial baseline and
preserves its original text and source links. That import creates **no numeric
probabilities**. Paper 3 Target A (direct resolution/refutation) and Target B
(independently verifiable evidence growth) remain separate endpoints.

The engine fails closed: statistical and calibrated requests return
`NOT_READY` until endpoint-specific labels, grouped chronological validation,
calibration evidence, and explicit evaluation authorization all exist. The
currently audited CS data do not meet those gates; no AUC, calibrated
probability, or Paper 3 transfer score is produced. Publication/citation
volume and topical resemblance are not outcome labels. Missing evidence is
never silently assigned a negative outcome.

Paper 4 action rankings are recommendations under declared assumptions. A
frozen ranking is not evidence of realized utility or planner superiority.
Feasibility/execution is stored separately from scientific utility; utility
requires an executed action, evidence, actual cost, and independent review.
Candidate ranking reuses the repository's `planner.rank_actions` implementation
through `rank_and_freeze_paper4_plan`. The input must declare hypothesis
priors, outcome likelihoods under each hypothesis, planner weights, cost,
tractability, expected observations, falsification value, and provenance.
Likelihoods are validated rather than guessed. The resulting score is
conditional on those assumptions and is frozen before any action outcome is
observed; it is not an evaluation of Paper 4's realized utility.

## Data flow and immutable artifacts

1. `freeze-baseline` hashes and imports
   `reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json` into
   `data/forecast_engine/qualitative_editorial_baseline_20261016.json`.
   The file is created with exclusive-create semantics and is never overwritten.
2. `add-evidence` appends one provenance-bearing event to
   `data/forecast_engine/evidence_events.jsonl`. Exact re-import is
   idempotent; an event ID with different content is rejected. Corrections
   require a new ID linked by `supersedes_event_id`.
3. `new-snapshot` makes a later qualitative snapshot and appends it to
   `data/forecast_engine/followup_snapshots.jsonl`. Availability is evaluated
   against the requested snapshot time; uncertain availability is quarantined.
   A later snapshot does not rewrite the frozen baseline or claim that later
   evidence existed at the earlier cutoff.
4. Human outcome adjudications and Paper 4 action outcomes use append-only
   JSONL stores at caller-provided paths. The JSON Schemas in
   `schemas/forecast_engine/` define the interchange records.
5. `readiness` reports endpoint gates from the frozen protocol and existing
   audits. `forecast` can return only an explicitly requested qualitative
   editor's note today; numeric modes stay `NOT_READY`.

All content hashes declare their scope. A URL hash is a citation-record hash,
not a full-text hash. The imported baseline registry labels its links
`CITATION_RECORD_ONLY`; it does not claim primary-text retrieval or
claim-level validation.

## Commands

Run from the repository root:

```sh
PYTHONPATH=src python3.12 scripts/cs_forecast_engine.py freeze-baseline
PYTHONPATH=src python3.12 scripts/cs_forecast_engine.py radar
PYTHONPATH=src python3.12 scripts/cs_forecast_engine.py show <question-id>
PYTHONPATH=src python3.12 scripts/cs_forecast_engine.py readiness
PYTHONPATH=src python3.12 scripts/cs_forecast_engine.py forecast <question-id> --mode QUALITATIVE_EDITORIAL --qualitative
PYTHONPATH=src python3.12 scripts/cs_forecast_engine.py forecast <question-id> --mode CALIBRATED_BREAKTHROUGH_FORECAST --endpoint resolution
PYTHONPATH=src python3.12 scripts/cs_forecast_engine.py demo
```

The demo uses only a synthetic post-cutoff fixture in a temporary directory.
It demonstrates cutoff quarantine, a later immutable snapshot, an unchanged
baseline hash, a structured diff, the Paper 4 recommendation disclaimer, a
numeric no-score response, and a reproducibility manifest. It emits no
scientific result and changes no persistent event store.

Additional commands are shown by `--help`: `add-evidence`, `new-snapshot`,
`history`, `freeze-action-plan`, `plan-compare`, `record-action-outcome`, and
`adjudicate`. Never supply fabricated or fixture records to persistent stores.

## Evaluation gates

The current frozen gates are read from
`research/paper3_target_b_protocol_v1.json`. Target A requires at least 20
adjudicated question endpoints and at least five examples in each outcome
class, with grouped chronological evaluation blocks and an untouched final
test. Target B requires at least 30 endpoint observations, at least ten
independently adjudicated progress outcomes and ten verified no-progress
outcomes, grouped chronological holdouts, and a frozen feature table.
Target A resolution and premise revision remain distinct endpoint records;
Target B is not substituted for exact resolution.

The engine's numeric evaluation utility uses the existing AUROC, AUPRC, and
Brier implementations, and supports deterministic group bootstrap intervals.
Neither utility runs by default: the endpoint gate and explicit authorization
must both pass. No model fitting, inference, forecasting benchmark, or external
data collection is part of this software-only implementation.

## Validation and limitations

The unit tests exercise immutable snapshots, append-only event behavior,
cutoff enforcement, separate endpoints, missingness handling, plan hashes,
readiness gates, grouped splits, and the fixture demo. They validate software
behavior only. The baseline contains 12 editorial candidates, not 12 frozen
and operationally adjudicable forecast targets. Their success criteria remain
milestone-level and require future human operationalization before a forecast
dataset can be frozen. No retrospective performance claim is made.
