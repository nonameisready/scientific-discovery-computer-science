# Technical source audit of the ten frozen prospective events

**Audit date:** 2026-10-17. **Disposition:** source-level screening only; not independent event approval or future-outcome adjudication. The original 10 event records are unchanged.

## Summary

All ten events are tied to identifiable primary sources. The reviewed baselines generally match the cited source's stated problem neighborhood, and several records rely on an explicit author-stated open question. This does not establish that every event is fully adjudicable: the frozen ORS date conflict is definite; the original-three horizon boundary is ambiguous; and model/encoding/comparator details for several events need domain-expert approval before outcome coding. Every reviewer status remains pending. No future outcome evidence was collected or classified.

## Frozen event/date index

The exact event text, complete assumptions, directional forecast, and frozen citations remain in `data/forecast_engine/prospective_cohort_v2.json`; the concise endpoint descriptions below are not replacements for those bytes.

| Event | Issue / evidence cutoff (UTC) | Frozen deadline field | Frozen target summary | Family |
|---|---|---|---|---|
| `PLANAR-THREE-SETS-CUT-UNCUT-112` | 2026-10-17 02:47:37 | 2030-12-31 | Exact polynomial algorithm for unweighted planar (1,1,2) Three-Sets Cut-Uncut, preserving the size-two set connectivity | Legacy singleton mapping |
| `DISCRETE-FRECHET-TRANSLATION-PLANAR-N4` | 2026-10-17 02:47:37 | 2031-10-16 | Exact planar discrete translation Fréchet in (O(n^4\log^C n)), model comparable | Legacy singleton mapping |
| `K-HOP-DOMINATION-LOW-EXPANSION-NO-GIRTH` | 2026-10-17 02:47:37 | 2031-10-16 | Same local-round/approximation regime without girth restriction | Legacy singleton mapping |
| `MAXBISECTION-GW-APPROX-001` | 2026-10-17 03:15:09 | 2031-12-31 | General unweighted MAX BISECTION expected ratio ≥ αGW | MAX-BISECTION-APPROXIMATION-THRESHOLD |
| `DYNAMIC-MATCHING-POLY-EXPONENT-001` | 2026-10-17 03:15:09 | 2031-12-31 | Explicit ((1-\epsilon))-matching with (O(n^{1-\delta})) amortized updates | DYNAMIC-MATCHING-AND-ORS-EXTREMAL-STRUCTURE |
| `ORS-POLYNOMIAL-GROWTH-001` | 2026-10-17 03:15:09 | 2030-12-31; exact-event text says 2031-12-31 | Polynomial ORS growth at fixed linear matching density | DYNAMIC-MATCHING-AND-ORS-EXTREMAL-STRUCTURE |
| `SUBSET-SUM-EXPONENT-IMPROVEMENT-001` | 2026-10-17 03:15:09 | 2031-12-31 | Exact worst-case Subset Sum with fixed exponent improvement below (2^{n/2}) | WORST-CASE-EXACT-SUBSET-SUM-RUNTIME |
| `TWO-STAGE-IP-OPT-UNBOUNDED-GLOBAL-COEFF-001` | 2026-10-17 03:15:09 | 2030-12-31 | Exact optimization FPT in local coefficient/dimension, with unbounded global coefficients | BLOCK-STRUCTURED-INTEGER-PROGRAMMING-LARGE-GLOBAL-COEFFICIENTS |
| `SHALLOW-QC-IDENTITY-PTAS-001` | 2026-10-17 03:15:09 | 2031-12-31 | Multiplicative PTAS for 1D constant-depth channel diamond-distance-to-identity | SHALLOW-QUANTUM-CIRCUIT-IDENTITY-CHECK |
| `ADAPTIVE-FDP-GDP-FILTER-MID-Q-001` | 2026-10-17 03:15:09 | 2030-12-31 | Fully adaptive approximate GDP filter for subsampled Gaussian (q\in[0.2,0.8]) with strict RDP-baseline improvement | FULLY-ADAPTIVE-PRIVACY-FILTERS-SUBSAMPLED-GAUSSIAN |

For every row, the frozen record's assumptions specify the model and scope; the per-event sections below give the primary-source comparison and unresolved adjudication flags.

## Record-by-record audit

### 1. `PLANAR-THREE-SETS-CUT-UNCUT-112`

**Frozen target:** exact polynomial-time solution to unweighted planar Three-Sets Cut-Uncut with terminal set sizes (1,1,2), preserving connectivity within the two-vertex set. **Primary source:** Bentert et al., [ICALP 2024 DOI](https://doi.org/10.4230/LIPIcs.ICALP.2024.22), [arXiv:2305.01314](https://arxiv.org/abs/2305.01314). The paper proves randomized FPT for planar Two-Sets Cut-Uncut in terminal count and poses the specified three-set case as an open question. Ordinary Multiway Cut does not enforce the `a,b` uncut condition. **Assessment:** source-anchored, theorem-level and reasonably adjudicable after checking the formal open-problem wording and graph conventions. Check whether the event's requirement to output a realizing cut and report infeasibility is exactly compatible with the source's problem definition. **Status:** baseline supported; future outcome none; independent event review pending.

### 2. `DISCRETE-FRECHET-TRANSLATION-PLANAR-N4`

**Frozen target:** exact discrete Fréchet distance for two unrestricted planar n-vertex curves under arbitrary translation in (O(n^4\log^C n)); exact-value computation. **Primary source:** Bringmann, Künnemann, and Nusser, [arXiv:1810.10982](https://arxiv.org/abs/1810.10982), SODA 2019/TALG. It gives ~O(n^{14/3}) and a conditional (n^{4-o(1)}) lower bound under SETH for the discrete planar translation problem. The two cited 2025 sources concern 1D or continuous/other transformations, not this endpoint. **Assessment:** source and endpoint distinction is strong. **Adjudication risk:** computation model, real/algebraic operations, bit complexity and “exact value” conversion from any decision routine must be compared theorem-by-theorem; the frozen event correctly treats unclear comparability as unresolved. **Status:** baseline supported; human model review pending.

### 3. `K-HOP-DOMINATION-LOW-EXPANSION-NO-GIRTH`

**Frozen target:** remove the high-girth condition while retaining deterministic constant-round (O(k+f(k)^{k/(k+1)})) approximation for k-hop domination on bounded k-hop-expansion families. **Primary source:** Lenzen and Wenning, [arXiv:2408.12998](https://arxiv.org/abs/2408.12998), SSS 2024. The source abstract states the 3k-round upper bound in high girth, model distinctions for upper/lower bounds, and asks whether the restriction is an artifact. **Assessment:** source-explicit extension target. **Adjudication risks:** inspect the theorem's precise port-numbering/message assumptions, whether constants depend on k or f, and the source's exact open-question wording; the event's deterministic requirement should be verified against the actual algorithm, not only the abstract summary. **Status:** baseline supported; model audit pending.

### 4. `MAXBISECTION-GW-APPROX-001`

**Frozen target:** polynomial-time approximation for general unweighted MAX BISECTION with expected value at least the Goemans–Williamson MAX CUT constant αGW. **Primary source:** Brakensiek, Huang, Potechin, and Zwick, [SODA 2026 DOI](https://doi.org/10.1137/1.9781611978971.197), [arXiv:2512.04951](https://arxiv.org/abs/2512.04951). It gives an explicit Basic-SDP integrality-gap obstruction to the αGW guarantee when the first stage supplies only ε-uncorrelatedness; its instance ratio is below 0.87853, while αGW is about 0.878567. That rules out the specified proof paradigm, not every possible algorithm. **Assessment:** the event does not confuse the obstruction with a general impossibility. **Adjudication risk:** spell out bisection cardinalities for odd n and the expected-value convention; verify whether “unweighted general graph” means the same finite simple graph model. **Status:** baseline supported; convention review pending.

### 5. `DYNAMIC-MATCHING-POLY-EXPONENT-001`

**Frozen target:** explicit ((1-\epsilon))-approximate matching under fully dynamic insertions/deletions in general graphs with (O(n^{1-\delta})) amortized update time for fixed positive constants and stated adversary guarantee. **Primary sources:** Behnezhad and Ghafari, [FOCS 2024 DOI](https://doi.org/10.1109/FOCS61266.2024.00027), [arXiv:2404.06069](https://arxiv.org/abs/2404.06069); Assadi, Khanna, and Kiss, [SODA 2025 DOI](https://doi.org/10.1137/1.9781611978322.96), [arXiv:2406.13573](https://arxiv.org/abs/2406.13573). The former gives an update-time bound parameterized by ORS density and states the fixed-exponent improvement as open; the latter further reduces complexity to an ORS quantity but leaves its density gap. **Assessment:** outcome predicate correctly excludes size estimators, bipartite-only results, and subpolynomial savings. **Adjudication risks:** adversary, high-probability quantifier over sequence length, explicit matching representation, amortized versus worst-case bounds, and preprocessing/space conventions. **Dependence:** same research family as ORS event 6; do not count independently.

### 6. `ORS-POLYNOMIAL-GROWTH-001` — frozen endpoint defect

**Frozen target:** polynomial lower bound for the ordered RS parameter at fixed linear matching density for infinitely many n, with exact ordered induced-matching semantics. **Primary source:** Assadi, Khanna, and Kiss, [SODA 2025 DOI](https://doi.org/10.1137/1.9781611978322.96), [arXiv:2406.13573](https://arxiv.org/abs/2406.13573). The paper defines ORS through ordered edge-disjoint linear-size matchings, gives a subpolynomial lower/near-linear upper gap, and describes closing it as challenging. Prefix-versus-suffix conventions can be reconciled by reversing the sequence, if the exact definition is checked. **Defect:** structured `deadline` = `2030-12-31`; frozen `exact_event` says `By 2031-12-31`. This changes the observation window and is not safely resolvable by inference. Append defect ID `AUDIT-ORS-DEADLINE-MISMATCH-20261017`; preserve both strings and mark event not adjudicable unless the original preregistration artifact resolves which field is controlling. **Status:** baseline supported; frozen endpoint ambiguous. Same research family as event 5.

### 7. `SUBSET-SUM-EXPONENT-IMPROVEMENT-001`

**Frozen target:** exact worst-case positive-integer Subset Sum with a fixed exponential-base improvement over (2^{n/2}), not merely a polynomial factor. **Primary sources:** Chen, Jin, Randolph, and Servedio, [arXiv:2301.07134](https://arxiv.org/abs/2301.07134), which gives randomized (O(2^{n/2}n^{-0.5023})) in the stated RAM models; their ESA 2025 paper, [DOI](https://doi.org/10.4230/LIPIcs.ESA.2025.86), distinguishes pigeonhole equal Subset Sum from the core worst-case problem and states the fixed-exponent question. **Assessment:** the event properly excludes average-case, promise, and Merlin–Arthur-only results. **Adjudication risks:** exact positive-input convention, input-bit-length factors, randomization error, and theorem model; check any later source for direct scope match. **Status:** baseline supported; human review pending.

### 8. `TWO-STAGE-IP-OPT-UNBOUNDED-GLOBAL-COEFF-001`

**Frozen target:** exact FPT linear optimization for two-stage stochastic IP with fixed block dimension and local coefficient bound while global matrices (A_i) are unbounded, with infeasible/unbounded cases handled. **Primary source:** Cslovjecsek et al., SODA 2024 version, [DOI](https://doi.org/10.1137/1.9781611977912.29); later full journal/preprint [TheoretiCS DOI](https://doi.org/10.46298/theoretics.25.15), [arXiv:2311.01890](https://arxiv.org/abs/2311.01890). The source proves FPT feasibility for two-stage programs with unbounded global blocks, but its optimization result is for uniform n-fold programs, not this two-stage case. **Assessment:** the event's separation from the 2026 general 4-block FPT result is correct in principle, because that result's coefficient parameterization is not the same as allowing (A_i) to be arbitrarily large outside the parameter. **Adjudication risks:** verify exact variable sign constraints, matrix dimensions, objective encoding, parameter ΔD, weakly-polynomial bit-size model, and whether source describes optimization specifically as open. **Status:** baseline supported; formulation review pending.

### 9. `SHALLOW-QC-IDENTITY-PTAS-001`

**Frozen target:** a ((1+\epsilon))-multiplicative approximation for diamond-norm distance from every constant-depth 1D nearest-neighbor circuit channel to identity. **Primary source:** Bravyi, Parham, and Tran, [arXiv:2401.16525](https://arxiv.org/abs/2401.16525). It gives constant-factor algorithms under stated conditions and identifies PTAS-level approximation as open; additive inverse-polynomial hardness does not by itself rule out a fixed-ε multiplicative PTAS. **Assessment:** direct motivation exists. **Adjudication risks:** gate-description encoding/precision, whether depth is fixed as a parameter, channel versus unitary representation, and zero distance. For a multiplicative guarantee (d\le\hat d\le(1+\epsilon)d), (d=0) forces \hat d=0; the frozen event appropriately flags exact-zero semantics but does not specify a finite gate encoding sufficiently to adjudicate all inputs. Do not infer that inverse-polynomial additive hardness settles this event. **Status:** source motivation supported; endpoint encoding review needed.

### 10. `ADAPTIVE-FDP-GDP-FILTER-MID-Q-001`

**Frozen target:** valid fully adaptive approximate GDP privacy filters for Poisson-subsampled Gaussian mechanisms throughout (q\in[0.2,0.8]), with a finite approximation guarantee and strict improvement over a frozen RDP-conversion baseline on some open region. **Primary source:** Tran, Koskela, Räisä, and Honkela, [arXiv:2602.06756](https://arxiv.org/abs/2602.06756), v2 dated 2026-05-12. It proves the naïve natural f-DP filter can fail under full adaptivity, gives necessary/sufficient validity conditions, and constructs an approximate GDP filter in asymptotic small/large-q regimes; the paper flags realistic intermediate-rate limitations. **Assessment:** the event is a specific extension, not a claim that no filter works in the middle. **Adjudication risks:** exact mechanism/adaptive parameter assumptions; what counts as “finite approximation/error guarantee”; and the frozen RDP comparator/metric are not fully pinned in the event text. “Strict improvement on an open region” needs a declared privacy utility measure and admissible parameter domain before it is reliably binary. **Status:** source gap is plausible; endpoint comparability needs design-level review, not post-hoc repair.

## Cross-cutting frozen-record defects and risks

1. **Definite ORS deadline conflict:** event text versus structured deadline (described above). This is an append-only defect, not a corrected forecast.
2. **Original three date-window ambiguity:** issue/evidence cutoff 2026-10-17 but nominal snapshot start 2027-01-01. Preserve both; classify qualifying results in the intervening interval separately. Do not alter the original events.
3. **Source hash scope:** v2 manifest hashes the cohort/monitoring/snapshot objects. The source rows declare `CITATION_METADATA_RECORD_ONLY`; no cited-source full text has an authenticated content hash in this cohort. Citation metadata integrity is not source-paper provenance.
4. **Adjudication:** all reviewer lists empty/pending; no event has independent approval. This is not evidence any baseline is wrong, merely that final source-level approval remains open.

## Engine, schema, provenance, and hash-scope audit

The source-code audit of `src/research_platform/forecast_engine/core.py` and its tests finds several different hash scopes that must not be conflated:

- `freeze_prospective_forecast` hashes canonical JSON of the frozen forecast material (before adding its hash/snapshot identifiers), then hashes the completed snapshot record. These provide record integrity, not source-paper integrity.
- `build_prospective_snapshot` hashes each cited `source` object as `citation_record_sha256` with scope `CITATION_METADATA_RECORD_ONLY`. The imported legacy baseline may hash the URL string only. Neither represents the PDF/arXiv HTML bytes.
- The manifest separately hashes full local bytes of activation/monitoring source artifacts and canonical JSON of the new cohort and monitoring object. Those checks are useful and the current tests pass; they prove artifact consistency against those expected bytes, not claim correctness.
- Outcome/evidence records may carry a real source-content `content_sha256`; if absent, some compatibility paths fall back to hashing the canonical URL and mark scope accordingly. Reviewers must inspect the scope field before treating a digest as a source hash.

No hash-scope bug is claimed in this cycle: the implementation exposes distinct scope strings and the cohort marks citation-record-only scope. The practical limitation is incomplete full-text/version checksums in the frozen ten-event data. No schema or engine code was changed.

## Audit classification

`PRIMARY_BASELINE_SUPPORTED` is a bounded literature verification judgment; `ADJUDICABILITY_PENDING` means the event may be usable after specified review; `FROZEN_AMBIGUOUS` applies to ORS. No event is labeled resolved, unresolved-at-horizon, or negative. This audit is not a future-evidence search, does not amend Paper 3, and does not create outcomes.
