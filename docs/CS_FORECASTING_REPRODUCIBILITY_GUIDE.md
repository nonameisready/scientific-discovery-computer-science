# CS forecasting pilot: reproducibility and integrity guide

## Scope

This guide validates existing software artifacts and explains the boundary between artifact integrity, source verification, human adjudication, and predictive evaluation. It does not initiate monitoring, make forecasts, fetch outcomes, or authorize model/worker execution.

## Frozen artifact rules

Do not edit `data/forecast_engine/activated_forecasts.json`, `activated_forecast_monitoring.json`, `prospective_cohort_v2.json`, `prospective_cohort_v2_monitoring.json`, `prospective_cohort_v2_manifest.json`, historical radar files, or `followup_snapshots.jsonl` to repair audit findings. A defect or correction is a new append-only record referencing the original event ID and hash. A citation metadata hash must never be described as a source-paper hash.

## Reproduction commands

From the repository root:

```sh
python3 scripts/research_check.py
python3 scripts/research_status.py
PYTHONPATH=src /opt/homebrew/bin/python3.12 -m unittest discover -s tests -v
python3 -m json.tool data/forecast_engine/prospective_cohort_v2.json >/dev/null
python3 -m json.tool data/forecast_engine/prospective_cohort_v2_manifest.json >/dev/null
shasum -a 256 data/forecast_engine/activated_forecasts.json data/forecast_engine/prospective_cohort_v2.json data/forecast_engine/prospective_cohort_v2_manifest.json data/forecast_engine/followup_snapshots.jsonl
git diff --check
```

The full unit suite verifies the repository's schema, immutable snapshots, hash relationships, date/cutoff gates, append-only behavior, and refusal to produce unsupported numeric forecast outputs. It does not establish that cited sources were correctly interpreted, that an event is adjudicable, that reviewers agree, or that any model predicts outcomes.

## Source-level reproducibility

For each event, a future reviewer must capture the exact primary-source version and first-public date, source-content checksum where permitted, theorem/algorithm locator, full scope and quantifiers, computational model, and a source packet. Current registry fields do not include authenticated content hashes for all cited papers. The audit's web retrieval is a source-level check, not an archived preservation layer; source version/hash completeness remains a readiness gap.

## Human adjudication

Use two independent human reviewers, blinded to one another's decisions and to any model conclusion. Review the exact event against each candidate result's object, assumptions, model, baseline, metric, threshold, date, independence, and evidence completeness. A third reviewer handles disagreements; unresolved ambiguity remains unresolved. Search failure is not a negative. Use the separate Target B rubric and keep Target A, Target B, attention, and research-planning outcomes distinct.

## Evaluation

No metric is valid for the current ten qualitative forecasts: they are not probabilities and have no mature labels. Any future scoring must be target-specific, family-grouped, chronological, include an untouched final test interval, compare predeclared simple baselines, and report class counts, censoring, uncertainty, power, and selection limits. Do not infer performance from a completed software test or a registry hash.
