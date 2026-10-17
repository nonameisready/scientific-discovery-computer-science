# CS Target B: evidence-growth adjudication rubric

**Status:** proposed protocol addendum; no labels created by this document. It does not amend Paper 3's frozen protocol, historical cohorts, or existing Target B protocol version.

## Unit and frozen endpoint

The unit is one source-grounded research question at its frozen cutoff, grouped with its research family. A follow-up paper is evidence, not a label. Before searching later work, record the exact question, source version and date, assumptions, formal object, claimed baseline, measurement, time window, and family dependencies. Preserve the source question and cutoff verbatim.

## Evidence dimensions (multi-label; do not collapse)

For each candidate follow-up, independently record each dimension as `YES`, `NO_AFTER_COVERAGE`, `UNCLEAR`, or `NOT_APPLICABLE`; separately record evidence status. `NO_AFTER_COVERAGE` requires a defined search-coverage protocol and is not inferred from a missing search result.

1. **Verified theorem or bound:** a primary proof establishes a new theorem, bound, or impossibility statement that directly narrows the frozen question.
2. **Matched-baseline algorithmic improvement:** same input class, model, and comparator; improvement threshold fixed before review; theorem and complexity proof checked.
3. **Independent empirical replication:** an independent team reproduces a relevant empirical result with frozen protocol/data/code provenance and uncertainty; replication is not inferred from a second publication alone.
4. **Independent counterexample:** a valid counterexample to a frozen premise or conjecture, checked against every quantifier and independently verified.
5. **Premise refutation or revision:** evidence invalidates or materially revises a necessary premise. Record the changed premise and do not automatically call this direct resolution.
6. **Substantive scope narrowing:** a result changes the viable parameter, graph, model, or assumption boundary in a way that excludes a nontrivial part of the original uncertainty. Mere special-case progress does not qualify without a stated boundary change.
7. **Contradictory evidence:** independently sourced evidence conflicts on a material claim or outcome. Keep both sources and do not choose one by publication count.
8. **Continued explicit uncertainty:** a primary source explicitly states an unresolved gap at a dated time. This is not proof of no progress or a negative forecast outcome.
9. **Unadjudicated / missing:** candidate sources, incomplete text, uncertain dates, or unresolved reviewer disagreement. This is never a negative.

Evidence dimensions 1–6 can coexist. Dimension 7 is a relation among records. Dimensions 8–9 are status descriptors, not progress categories. Publication count, citations, venue prestige, topical similarity, benchmark leaderboard rank without endpoint matching, and search non-detection are excluded as sufficient evidence.

## Decision workflow

1. One researcher prepares a neutral packet: canonical source/version, first-public date, archived source hash when legally possible, theorem/section/page/table locator, relation to the frozen question, and explicit near-miss checks.
2. Two independent human reviewers separately score object, assumptions, model, baseline, endpoint, threshold, date, independence, and evidence completeness as `MATCH`, `MISMATCH`, or `UNCLEAR`. They then code the dimensions above and explain each `YES`.
3. Any material disagreement receives a third independent review; unresolved disagreement remains `UNADJUDICATED`.
4. A final adjudication appends a new immutable record with reviewer IDs, timestamps, evidence IDs, coverage record, and rationale. Corrections supersede; they do not overwrite.
5. Report raw agreement and class counts before any chance-corrected statistic. Agreement is not truth, and no reliability claim is possible until independent double-coding is actually performed.

## Separation from Target A and attention

Target A is direct resolution/refutation of the frozen question under its exact quantifiers. Target B records progress that can occur while Target A remains open. Attention is the source-native Paper 3 target and is not replaced by publication/citation counts here. Do not infer any one axis from another. Do not combine dimensions into a binary score unless a future, separately frozen analysis justifies and validates that mapping.

## Current state

No Target B outcome is adjudicated for the ten-item prospective cohort. This rubric is a proposed human-review aid, not a retrospective relabeling. The cohort's frozen event records and the historical Paper 3 artifacts remain unchanged.
