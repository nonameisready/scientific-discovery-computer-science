#!/usr/bin/env python3
"""Freeze an append-only, source-grounded qualitative CS forecast cohort v2.

This builder does not infer outcomes, run models, activate monitoring, or edit
the original October 17 forecasts.  It refuses to overwrite any deliverable.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from research_platform.forecast_engine.core import (  # noqa: E402
    ForecastEngineError,
    append_snapshot,
    build_prospective_snapshot,
    canonical_json,
    freeze_prospective_forecast,
    hash_file,
    load_json,
    sha256_bytes,
    verify_snapshot_hash,
    write_immutable_json,
)

DIR = ROOT / "data/forecast_engine"
ORIGINAL = DIR / "activated_forecasts.json"
ORIGINAL_MONITORING = DIR / "activated_forecast_monitoring.json"
SNAPSHOTS = DIR / "followup_snapshots.jsonl"
COHORT = DIR / "prospective_cohort_v2.json"
MONITORING = DIR / "prospective_cohort_v2_monitoring.json"
MANIFEST = DIR / "prospective_cohort_v2_manifest.json"
REPORT_JSON = ROOT / "reports/CS_PROSPECTIVE_COHORT_EXPANSION.json"


def source(title: str, url: str, source_date: str, role: str, scope: str) -> dict:
    return {
        "title": title,
        "url": url,
        "source_date": source_date,
        "role": role,
        "checked_scope": scope,
        "hash_scope": "CITATION_METADATA_RECORD_ONLY",
    }


def drafts() -> list[dict]:
    """Seven operationalized questions; related dynamic outcomes share a family."""
    return [
        {
            "event_id": "MAXBISECTION-GW-APPROX-001",
            "question_id": "MAXBISECTION-GW-APPROX-001",
            "research_family_id": "MAX-BISECTION-APPROXIMATION-THRESHOLD",
            "subfield": "approximation_algorithms",
            "event_type": "THEORETICAL_APPROXIMATION_GUARANTEE",
            "scientific_question": "Does general unweighted MAX BISECTION admit a polynomial-time approximation guarantee at the Goemans–Williamson MAX CUT ratio, under the same worst-case input scope?",
            "source_baseline": "Austrin–Benabbas–Georgiou establish the approximately 0.8776 line of algorithms; Brakensiek et al. (SODA 2026) retain the α_GW question as open and prove that the ε-uncorrelated Basic-SDP two-stage paradigm alone cannot reach α_GW (their gap is below 0.87853). That is a limitation of this paradigm, not an impossibility for all algorithms.",
            "baseline_version": "SODA 2026 proceedings paper, DOI 10.1137/1.9781611978971.197; accessed before issue cutoff",
            "exact_event": "By 2031-12-31, a public primary theorem gives a polynomial-time algorithm for MAX BISECTION on every finite unweighted general graph whose expected cut value is at least α_GW times optimum, where α_GW is the standard Goemans–Williamson MAX CUT constant. The theorem must specify the randomized or deterministic guarantee and polynomial running time. A result only for a restricted graph class, an SDP integrality-gap statement, or a ratio strictly below α_GW does not count.",
            "frozen_assumptions": [
                "Input is a finite unweighted undirected graph with even vertex count; a feasible bisection has equal-size sides.",
                "The guarantee is worst-case over all such input graphs and is an approximation guarantee for the produced bisection, not an SDP value bound.",
                "The approximation ratio is at least the conventional α_GW constant; no Unique Games assumption is allowed for the algorithmic upper bound.",
                "A randomized algorithm may state the ratio in expectation, but must define that convention explicitly."
            ],
            "improvement_criterion": "Reach the MAX CUT α_GW approximation ratio for unrestricted unweighted MAX BISECTION, with an exact theorem and polynomial-time algorithm.",
            "deadline": "2031-12-31",
            "resolution_policy": "Two independent reviewers compare the full theorem, graph scope, bisection constraint, approximation ratio, runtime, and randomness convention with this frozen event. The SODA 2026 Basic-SDP obstruction alone is not success or refutation of the all-algorithms question.",
            "evidence_standard": "Dated primary paper or proceedings article with a complete algorithm and proof; two independent human theorem checks are required.",
            "ambiguity_policy": "Restricted graph classes, an integrality gap, a method-specific limitation, or a ratio below α_GW is recorded as partial progress only. If approximation conventions or graph weights differ, outcome is unresolved.",
            "sources": [
                source("MAX BISECTION might be harder to approximate than MAX CUT", "https://doi.org/10.1137/1.9781611978971.197", "2026-01-07", "PRIMARY_CURRENT_GAP_AND_METHOD_LIMITATION", "SODA 2026 theorem and open-question context"),
                source("MAX BISECTION might be harder to approximate than MAX CUT (preprint)", "https://arxiv.org/abs/2512.04951", "2025-12-04", "PRIMARY_PREPRINT_VERSION", "Problem statement and ε-uncorrelated Basic-SDP obstruction")
            ],
            "forecast_statement": "I judge an unrestricted α_GW guarantee for MAX BISECTION by the deadline highly uncertain, with a directional lean that it will not be established by then: the latest primary result blocks an influential route, but leaves other algorithmic paradigms open.",
            "expectation": "HIGHLY_UNCERTAIN_WITH_DIRECTIONAL_LEAN",
            "directional_lean": "NO_UNRESTRICTED_ALPHA_GW_GUARANTEE_BY_2031",
            "supporting_evidence": "A 2026 SODA paper constructs ε-uncorrelated Basic-SDP solutions with integrality ratios below α_GW, directly invalidating the sufficiency of the prevailing two-stage proof template.",
            "counterevidence": "The paper does not rule out other hierarchies, strengthened relaxations, or non-SDP algorithms; MAX BISECTION remains a longstanding open approximation question.",
            "uncertainty": "The method-specific gap may redirect rather than halt progress; the horizon is five years and no defensible event base rate is available.",
            "primary_future_sources": ["SODA/FOCS/ICALP proceedings", "arXiv primary versions", "journal versions"],
            "search_strategy": "Search MAX BISECTION with α_GW and 0.878567, inspect theorem assumptions and approximation conventions, then trace citations and follow-up work from the frozen SODA 2026 paper. Search non-SDP as well as SDP approaches.",
            "censoring_policy": "Failure to locate a matching theorem is not a negative outcome. At deadline, require a documented venue/arXiv coverage log; otherwise classify as INSUFFICIENT_EVIDENCE.",
            "independent_review_requirement": "Two independent human reviewers; at least one checks the formal approximation guarantee and randomized expectation convention."
        },
        {
            "event_id": "DYNAMIC-MATCHING-POLY-EXPONENT-001",
            "question_id": "DYNAMIC-MATCHING-POLY-EXPONENT-001",
            "research_family_id": "DYNAMIC-MATCHING-AND-ORS-EXTREMAL-STRUCTURE",
            "subfield": "dynamic_graph_algorithms",
            "event_type": "THEORETICAL_DYNAMIC_ALGORITHM",
            "scientific_question": "Can one maintain an explicit (1−ε)-approximate maximum matching under arbitrary single-edge insertions and deletions in general graphs with a fixed polynomial saving over linear amortized update time?",
            "source_baseline": "Behnezhad–Ghafari (FOCS 2024) reduce the runtime to a bound parameterized by ORS graph density and state the n^{1−Ω(1)} update-time target as a major open problem. Assadi–Khanna–Kiss (SODA 2025) further make the algorithmic bound depend directly on ORS density, but do not establish a fixed polynomial exponent unconditionally.",
            "baseline_version": "FOCS 2024 and SODA 2025 proceedings versions; exact explicit-matching problem and amortized update model",
            "exact_event": "By 2031-12-31, a public randomized or deterministic algorithm maintains, after every update in a fully dynamic general undirected graph, an explicit matching of size at least (1−ε)·OPT for some fixed constants ε>0 and δ>0, with amortized update time O(n^{1−δ}) and polynomial preprocessing/space. The approximation must hold with high probability over every polynomial-length update sequence under a stated adversary model. A matching-size estimate alone, a bipartite-only result, or n/2^{Ω(√log n)} time without a fixed exponent δ does not count.",
            "frozen_assumptions": [
                "One edge insertion or deletion is one update; the graph is a general undirected n-vertex graph.",
                "The data structure outputs the matching edges, not only an estimate of matching size.",
                "ε and δ are positive constants independent of n; the update bound is amortized over every prefix or a clearly equivalent standard guarantee.",
                "The adversary model and probability of maintaining a valid (1−ε)-approximation are stated in the theorem."
            ],
            "improvement_criterion": "Achieve explicit near-optimal matching with a fixed n^{1−δ} amortized update-time exponent on unrestricted general graphs.",
            "deadline": "2031-12-31",
            "resolution_policy": "Reviewers verify that the algorithm maintains edges of a valid matching after every update, handles insertions and deletions, uses unrestricted general graphs, and has constants ε,δ independent of n. ORS-conditional bounds do not count unless they imply an unconditional fixed-exponent bound.",
            "evidence_standard": "Primary theorem and full proof in a dated proceedings article or public preprint; independently check the data-structure output and asymptotic bound.",
            "ambiguity_policy": "Size-only estimators, restricted bipartite graphs, conditional ORS assumptions, or subpolynomial improvements n^{1−o(1)} are not event achievement.",
            "sources": [
                source("Fully Dynamic Matching and Ordered Ruzsa-Szemerédi Graphs", "https://doi.org/10.1109/FOCS61266.2024.00027", "2024-10-27", "PRIMARY_DYNAMIC_MATCHING_BASELINE", "FOCS 2024 explicit matching algorithm and stated n^{1−Ω(1)} gap"),
                source("Improved Bounds for Fully Dynamic Matching via Ordered Ruzsa-Szemerédi Graphs", "https://doi.org/10.1137/1.9781611978322.96", "2025-01-07", "PRIMARY_FOLLOWUP_AND_MODEL_CHECK", "SODA 2025 algorithmic consequence of ORS density")
            ],
            "forecast_statement": "I judge an unconditional fixed-exponent update-time algorithm for explicit near-optimal dynamic matching unlikely by the deadline; recent work has sharpened the ORS reduction but still leaves the extremal density gap central.",
            "expectation": "UNLIKELY_BEFORE_DEADLINE",
            "directional_lean": "NO_UNCONDITIONAL_FIXED_POLYNOMIAL_SAVING_BY_2031",
            "supporting_evidence": "The strongest audited dynamic algorithms turn the question into an ORS-density bound and the published bounds remain between subpolynomial lower and near-linear upper exponents.",
            "counterevidence": "A combinatorial advance on ORS density could immediately imply the dynamic improvement; dynamic matching has seen rapid algorithmic progress.",
            "uncertainty": "The event is coupled to extremal combinatorics and could be resolved by a new structural construction or proof rather than a direct data-structure breakthrough.",
            "primary_future_sources": ["FOCS/SODA/STOC proceedings", "arXiv primary versions", "journal versions"],
            "search_strategy": "Track explicit output-matching results and check graph class, update type, adversary, probability, amortized versus worst-case complexity, and whether constants yield a fixed power saving.",
            "censoring_policy": "A search miss never yields a failure label. At the horizon, document source venues and exact query coverage; if coverage is inadequate, retain INSUFFICIENT_EVIDENCE.",
            "independent_review_requirement": "Two independent human reviewers; one verifies the data-structure theorem and one checks model/complexity comparability."
        },
        {
            "event_id": "ORS-POLYNOMIAL-GROWTH-001",
            "question_id": "ORS-POLYNOMIAL-GROWTH-001",
            "research_family_id": "DYNAMIC-MATCHING-AND-ORS-EXTREMAL-STRUCTURE",
            "subfield": "extremal_combinatorics",
            "event_type": "THEOREM_ON_EXTREMAL_GRAPH_PARAMETER",
            "scientific_question": "Does the ordered Ruzsa–Szemerédi parameter have polynomial growth for some fixed linear matching density?",
            "source_baseline": "The SODA 2025 primary paper defines ORS(n,δn) using ordered edge-disjoint linear-size matchings, gives lower bounds n^{Ω(1/log log n)} and upper bounds n^{1−o(1)}, and explicitly calls closing the gap challenging. This structural parameter controls the runtime of the FOCS 2024/SODA 2025 dynamic matching algorithms.",
            "baseline_version": "Assadi–Khanna–Kiss, SODA 2025 proceedings, full author-hosted PDF",
            "exact_event": "By 2031-12-31, a public theorem proves that there exist constants δ>0 and ε>0 and infinitely many n for which an n-vertex graph has an ordered sequence of at least n^ε edge-disjoint matchings, each of size at least δn, where each matching is induced in the union of itself and all later matchings (equivalently, reverse the ordering convention consistently). A mere n^{o(1)} lower bound, a bound for sublinear-size matchings, or a non-ordered RS construction that does not satisfy the frozen ordered condition does not count.",
            "frozen_assumptions": [
                "Use the SODA 2025 definition of ORS(n,r): edge-disjoint ordered matchings of size r, each induced in the suffix union.",
                "The constants δ and ε are fixed independently of n, and the lower bound holds for infinitely many n.",
                "Any reversal between prefix and suffix conventions must be explicitly proved by reversing the matching order."
            ],
            "improvement_criterion": "Establish a polynomial lower bound ORS(n,δn)≥n^ε for some fixed positive δ,ε, or a theorem that implies it with exact constants and quantifiers.",
            "deadline": "2030-12-31",
            "resolution_policy": "Two reviewers verify the ordered induced-matching condition, linear size, graph order, constants, and infinitely-many-n quantifier from the proof. The implication to dynamic matching is reported separately and not used as the ORS label.",
            "evidence_standard": "Primary mathematical proof in a dated paper or proceedings version with an explicit asymptotic family or theorem.",
            "ambiguity_policy": "A subpolynomial bound or an ordinary RS graph bound is partial progress unless the order condition and polynomial exponent are established.",
            "sources": [
                source("Improved Bounds for Fully Dynamic Matching via Ordered Ruzsa-Szemerédi Graphs", "https://doi.org/10.1137/1.9781611978322.96", "2025-01-07", "PRIMARY_DEFINITION_BOUNDS_AND_OPEN_GAP", "Definition 1.1 and introduction, ORS bounds and implications")
            ],
            "forecast_statement": "I judge a fixed polynomial lower bound for ORS(n,δn) unlikely by 2030; the known subpolynomial lower bound reflects a long-standing extremal obstruction, although an improved construction could change the dynamic-matching landscape.",
            "expectation": "UNLIKELY_BEFORE_DEADLINE",
            "directional_lean": "NO_POLYNOMIAL_ORS_LOWER_BOUND_BY_2030",
            "supporting_evidence": "The current gap is between n^{Ω(1/log log n)} and n^{1−o(1)}, and the latest algorithmic paper describes it as notoriously challenging.",
            "counterevidence": "The dynamic-matching papers have increased attention to this parameter, and progress can come from constructions not visible in the old RS literature.",
            "uncertainty": "This event is statistically and causally dependent on the dynamic matching event in the same research family; it is not an independent forecast unit.",
            "primary_future_sources": ["STOC/SODA/FOCS proceedings", "arXiv primary versions", "combinatorics journals"],
            "search_strategy": "Search ORS(n,δn), ordered induced matchings, suffix-induced matchings, and exact construction bounds; validate every claimed family against the SODA 2025 definition.",
            "censoring_policy": "No located construction is not proof of nonexistence. Without a documented search and independent coverage check, use INSUFFICIENT_EVIDENCE.",
            "independent_review_requirement": "Two independent reviewers check the combinatorial definition and asymptotic quantifiers; disclose shared dynamic-matching family with event DYNAMIC-MATCHING-POLY-EXPONENT-001."
        },
        {
            "event_id": "SUBSET-SUM-EXPONENT-IMPROVEMENT-001",
            "question_id": "SUBSET-SUM-EXPONENT-IMPROVEMENT-001",
            "research_family_id": "WORST-CASE-EXACT-SUBSET-SUM-RUNTIME",
            "subfield": "exact_exponential_algorithms",
            "event_type": "THEORETICAL_EXACT_ALGORITHM_RUNTIME",
            "scientific_question": "Can worst-case exact Subset Sum be solved with a fixed exponential-base improvement over meet-in-the-middle, rather than only a polynomial-factor saving?",
            "source_baseline": "Horowitz–Sahni meet-in-the-middle uses O*(2^{n/2}); Chen, Jin, Randolph, and Servedio improve this by a polynomial factor, while the ESA 2025 primary paper explicitly says it remains open whether worst-case Subset Sum admits O*(2^{(1/2−ε)n}) for a constant ε>0.",
            "baseline_version": "ESA 2025 article 86, DOI 10.4230/LIPIcs.ESA.2025.86; primary source lines state the exponent question remains open",
            "exact_event": "By 2031-12-31, a public theorem gives an exact randomized or deterministic algorithm for every worst-case instance of Subset Sum on n positive binary-encoded integers and a target, running in O(2^{(1/2−ε)n}·poly(n,L)) time for some fixed ε>0, where L is the maximum input bit length; randomized algorithms must have error at most 1/3 on every input. The algorithm must decide existence exactly up to its stated error. A 2^{n/2}/poly(n) improvement, average-case algorithm, promise-restricted algorithm, or Merlin–Arthur protocol alone does not count.",
            "frozen_assumptions": [
                "The problem is exact worst-case Subset Sum with positive integer weights in binary and a target integer.",
                "The running time is measured in a standard word-RAM or circuit-RAM model with polynomial factors in input bit length stated.",
                "ε is a positive constant independent of n; an O*(2^{n/2}/poly(n)) bound is not a fixed exponential-base improvement.",
                "Randomized decision algorithms have worst-case input error at most 1/3; deterministic algorithms qualify directly."
            ],
            "improvement_criterion": "Prove a fixed constant ε>0 exponential-base improvement for exact worst-case Subset Sum over O*(2^{n/2}).",
            "deadline": "2031-12-31",
            "resolution_policy": "Reviewers inspect the full algorithm, correctness, input quantifiers, computational model, exponent, and dependence on bit length. Average-case or Merlin–Arthur results are classified separately as partial progress.",
            "evidence_standard": "Dated primary paper/proceedings article and a complete mathematical runtime/correctness proof; independently check the exponent and model.",
            "ambiguity_policy": "Polynomial-factor savings do not count as 2^{(1/2−ε)n}; exactness cannot be inferred from a one-sided protocol without a valid conversion theorem.",
            "sources": [
                source("New Algorithms for Pigeonhole Equal Subset Sum", "https://doi.org/10.4230/LIPIcs.ESA.2025.86", "2025-09-08", "PRIMARY_2025_STATUS_AND_OPEN_EXPONENT_QUESTION", "Introduction distinguishes Subset Sum from Pigeonhole Equal Subset Sum and states the exact worst-case open problem"),
                source("Subset Sum in Time 2^{n/2}/poly(n)", "https://arxiv.org/abs/2301.07134", "2023-01-17", "PRIMARY_CURRENT_WORST_CASE_ALGORITHM", "Worst-case polynomial-factor improvement and standard RAM model")
            ],
            "forecast_statement": "I judge a fixed exponential-base improvement for worst-case exact Subset Sum unlikely by the deadline: the latest checked work still reports only polynomial-factor savings for the core problem after a half-century of meet-in-the-middle dominance.",
            "expectation": "UNLIKELY_BEFORE_DEADLINE",
            "directional_lean": "NO_FIXED_EXPONENT_IMPROVEMENT_BY_2031",
            "supporting_evidence": "The primary 2025 source explicitly distinguishes the still-open worst-case core from solved or faster variants, and the best audited core algorithm saves only a polynomial factor.",
            "counterevidence": "Several neighboring subset-balancing and equal-subset-sum problems have recently seen exponential improvements; new representation techniques may transfer.",
            "uncertainty": "The outcome is sensitive to rapid exact-algorithm breakthroughs; no strong conditional lower bound is known for this exact exponent target.",
            "primary_future_sources": ["STOC/FOCS/SODA/ESA proceedings", "arXiv primary versions", "journal versions"],
            "search_strategy": "Track exact worst-case Subset Sum theorem statements; separate positive weights, signed variants, equal-subset-sum, average-case, promise, quantum, and Merlin–Arthur results.",
            "censoring_policy": "Do not infer failure from a search miss. At deadline, use INSUFFICIENT_EVIDENCE unless a documented comprehensive source review supports a horizon-end unresolved category.",
            "independent_review_requirement": "Two independent reviewers; one verifies the asymptotic bound and one verifies that the problem variant is the frozen core problem."
        },
        {
            "event_id": "TWO-STAGE-IP-OPT-UNBOUNDED-GLOBAL-COEFF-001",
            "question_id": "TWO-STAGE-IP-OPT-UNBOUNDED-GLOBAL-COEFF-001",
            "research_family_id": "BLOCK-STRUCTURED-INTEGER-PROGRAMMING-LARGE-GLOBAL-COEFFICIENTS",
            "subfield": "parameterized_complexity_integer_programming",
            "event_type": "THEORETICAL_FIXED_PARAMETER_ALGORITHM",
            "scientific_question": "Does the FPT feasibility algorithm for two-stage stochastic integer programs with unbounded global-block coefficients extend to exact linear optimization under the same local-coefficient parameterization?",
            "source_baseline": "Cslovjecsek et al. (SODA 2024) prove FPT feasibility parameterized by block dimension k and maximum local-block coefficient Δ_D while allowing arbitrary entries in global blocks A_i; they explicitly call extension to optimization an outstanding open problem. The 2026 general 4-block FPT result bounds all input coefficients, so it does not directly settle this unbounded-A_i parameterization.",
            "baseline_version": "SODA 2024 DOI 10.1137/1.9781611977912.29; cross-checked against 2026 4-block FPT preprint arXiv:2609.26746",
            "exact_event": "By 2030-12-31, a public theorem gives an algorithm with running time f(k,Δ_D)·|P|^{O(1)} for exact linear optimization of every two-stage integer program with x,y_i∈Z_{≥0}^k, A_i x + D_i y_i = b_i for i=1,…,m, arbitrary integer global matrices A_i and objective coefficients, and Δ_D=max_i||D_i||∞; the algorithm returns an optimum, reports infeasibility, or correctly detects an unbounded objective. The parameter function may be any computable f, but no dependence on max_i||A_i||∞ may appear outside the input bit length.",
            "frozen_assumptions": [
                "Use the SODA 2024 two-stage integer-program form with nonnegative integral variables and block dimension k; rectangular blocks may be padded as in the source.",
                "Local matrices D_i have maximum absolute entry Δ_D; global matrices A_i and linear objective coefficients have arbitrary binary-encoded magnitudes.",
                "Running time is FPT in (k,Δ_D) and polynomial in total input bit length.",
                "Optimization returns an exact optimum, infeasibility, or unboundedness; a feasibility-only theorem does not count."
            ],
            "improvement_criterion": "Extend the source's FPT feasibility guarantee to exact linear optimization while retaining arbitrary large global coefficients and no new parameter dependence on them.",
            "deadline": "2030-12-31",
            "resolution_policy": "Two reviewers compare the algorithm parameterization and exact two-stage input class. Check separately whether a 4-block theorem assumes a bound on every matrix entry; such a theorem does not imply the frozen result when A_i are unbounded.",
            "evidence_standard": "Primary theorem and proof with explicit FPT runtime and optimization/unboundedness semantics; independent check of the reduction from the declared model.",
            "ambiguity_policy": "Feasibility only, bounds on A_i, dependence on Δ_A, approximation-only optimization, or a different stochastic/continuous model is not event achievement.",
            "sources": [
                source("Parameterized algorithms for block-structured integer programs with large entries", "https://doi.org/10.1137/1.9781611977912.29", "2024-01-11", "PRIMARY_FPT_FEASIBILITY_AND_EXPLICIT_OPTIMIZATION_GAP", "SODA 2024 Theorems 1.1–1.2 and explicit next-step paragraph"),
                source("4-Block Integer Programming is in FPT", "https://arxiv.org/abs/2609.26746", "2026-09-22", "PRIMARY_SCOPE_CROSS_CHECK", "General 4-block result parameterized by maximum coefficient; not a result for unbounded A_i under Δ_D-only parameterization")
            ],
            "forecast_statement": "I judge the optimization extension by 2030 highly uncertain, with a directional lean toward a theorem appearing: the 2024 paper identifies this as the next natural step, and 2026 structural progress on 4-block programs may provide relevant techniques, but the large-global-coefficient regime remains materially different.",
            "expectation": "HIGHLY_UNCERTAIN_WITH_DIRECTIONAL_LEAN",
            "directional_lean": "FPT_OPTIMIZATION_EXTENSION_BY_2030",
            "supporting_evidence": "The authors explicitly identify the feasibility-to-optimization extension as an outstanding open problem and motivate it as a route toward broader block-structured IP results.",
            "counterevidence": "Optimization adds a global coupling constraint and may be substantially harder; standard Graver-based arguments depend on bounded entries, and 4-block FPT with all entries bounded does not remove unbounded A_i.",
            "uncertainty": "The 2026 FPT 4-block result is adjacent but not equivalent; an unverified reduction could falsely make this event appear solved.",
            "primary_future_sources": ["SODA/ESA/ICALP proceedings", "arXiv primary versions", "integer-programming journals"],
            "search_strategy": "Search the exact source phrase, two-stage stochastic integer programming optimization, large global A_i, and k/Δ_D parameterization; audit 4-block and treedepth results for coefficient assumptions.",
            "censoring_policy": "A missing follow-up is not a negative. At deadline, require a logged source sweep across theory proceedings and integer-programming venues; otherwise retain INSUFFICIENT_EVIDENCE.",
            "independent_review_requirement": "Two independent reviewers; one specifically audits whether all large global coefficients remain outside the parameter function."
        },
        {
            "event_id": "SHALLOW-QC-IDENTITY-PTAS-001",
            "question_id": "SHALLOW-QC-IDENTITY-PTAS-001",
            "research_family_id": "SHALLOW-QUANTUM-CIRCUIT-IDENTITY-CHECK",
            "subfield": "quantum_algorithms_and_complexity",
            "event_type": "THEORETICAL_APPROXIMATION_SCHEME",
            "scientific_question": "Can the diamond-norm distance from a constant-depth 1D geometrically local quantum circuit to the identity channel be approximated within 1+ε in polynomial time for every fixed ε>0?",
            "source_baseline": "Bravyi, Parham, and Tran give constant-factor classical algorithms for shallow geometrically local circuits and identify a 1+ε approximation scheme for the identity-check problem as an open question. They show inverse-polynomial additive accuracy is QMA-hard in a constant-depth 1D setting; that does not itself rule out a fixed-ε multiplicative scheme.",
            "baseline_version": "arXiv:2401.16525, v1 dated 2024-01-29; full theorem and open-problem section",
            "exact_event": "By 2031-12-31, a public theorem gives a classical or quantum algorithm which, for every fixed ε>0 and every constant-depth nearest-neighbor circuit U on a 1D line of n qubits, outputs an estimate d_hat of the diamond-norm distance d(U) between the induced unitary channel and the identity channel satisfying d(U)≤d_hat≤(1+ε)d(U), in time polynomial in n and the encoded gate-description length (with degree allowed to depend on fixed depth and ε). The algorithm must handle d(U)=0 exactly or define a valid zero-distance convention. Results only for near-identity circuits, operator norm, a fixed constant factor, or inverse-polynomial additive precision do not count.",
            "frozen_assumptions": [
                "Circuit gates act on neighboring sites of a one-dimensional qubit line and depth is a fixed constant independent of n.",
                "The target is diamond-norm distance between quantum channels, not operator norm, and the approximation is multiplicative.",
                "For every fixed ε>0 the runtime is polynomial in input length; the polynomial degree may depend on ε and depth.",
                "The theorem states the gate precision / computation model and treats zero distance correctly."
            ],
            "improvement_criterion": "Establish a PTAS-style multiplicative approximation scheme for the 1D shallow-circuit diamond-norm identity-check problem.",
            "deadline": "2031-12-31",
            "resolution_policy": "Two independent reviewers verify norm, channel, circuit locality/depth, multiplicative guarantee, zero case, precision model, and runtime. An additive-hardness statement is not treated as refutation of fixed-ε multiplicative approximation.",
            "evidence_standard": "A complete primary proof or algorithm theorem; independent quantum-complexity reviewer checks the norm conversion and input model.",
            "ambiguity_policy": "Operator norm, near-identity-only promise, approximate channels, or additive error without the required multiplicative guarantee is partial progress, not success.",
            "sources": [
                source("Identity check problem for shallow quantum circuits", "https://arxiv.org/abs/2401.16525", "2024-01-29", "PRIMARY_BASELINE_AND_OPEN_PTAS_QUESTION", "Abstract, approximation guarantees, hardness discussion, and Open Problems")
            ],
            "forecast_statement": "I judge a multiplicative PTAS for this unrestricted constant-depth 1D identity-check target unlikely by 2031; the source already has constant-factor methods and strong precision barriers, but those barriers do not rule out the fixed-ε target.",
            "expectation": "UNLIKELY_BEFORE_DEADLINE",
            "directional_lean": "NO_MULTIPLICATIVE_PTAS_BY_2031",
            "supporting_evidence": "The source identifies the PTAS as open and explains that substantially finer additive approximation is QMA-hard even in a restricted 1D setting.",
            "counterevidence": "Fixed-ε multiplicative error is weaker than inverse-polynomial additive accuracy, and constant-depth 1D circuits have exploitable tensor-network structure.",
            "uncertainty": "The source's hardness statement does not imply hardness for this frozen event; algorithmic advances may exploit the fixed precision regime.",
            "primary_future_sources": ["FOCS/STOC/SODA/QIP proceedings", "arXiv primary versions", "quantum information journals"],
            "search_strategy": "Search identity check, diamond norm, channel distance, shallow geometrically local circuits, and PTAS; check whether statements concern operator norm or diamond norm and whether the circuit depth is fixed.",
            "censoring_policy": "Search absence cannot establish nonexistence; use a documented primary-source sweep and mark insufficient coverage as censored.",
            "independent_review_requirement": "Two independent human reviewers, including a reviewer competent in quantum information/complexity definitions."
        },
        {
            "event_id": "ADAPTIVE-FDP-GDP-FILTER-MID-Q-001",
            "question_id": "ADAPTIVE-FDP-GDP-FILTER-MID-Q-001",
            "research_family_id": "FULLY-ADAPTIVE-PRIVACY-FILTERS-SUBSAMPLED-GAUSSIAN",
            "subfield": "differential_privacy_and_theory",
            "event_type": "THEORETICAL_PRIVACY_ACCOUNTING_GUARANTEE",
            "scientific_question": "Can valid approximate Gaussian-DP privacy filters be proved for fully adaptive compositions of Poisson-subsampled Gaussian mechanisms throughout the intermediate sampling-rate interval not covered by the current approximate-filter construction?",
            "source_baseline": "Tran et al. (2026) show the naive natural f-DP filter can fail under full adaptivity, characterize validity conditions, and give an approximate GDP filter for subsampled Gaussian mechanisms at q<0.2 and q>0.8. This leaves the stated intermediate interval as a theorem-coverage gap in that construction; it is not evidence that all filters fail there.",
            "baseline_version": "arXiv:2602.06756, version available before 2026-10-17; theorem assumptions and q regimes",
            "exact_event": "By 2030-12-31, a public theorem constructs a privacy filter valid under fully adaptive composition for Poisson-subsampled Gaussian mechanisms for every sampling rate q in the closed interval [0.2,0.8], with a stated finite approximation/error guarantee and explicit dependence on the noise multiplier, number of steps, and target privacy parameter. To count, the paper must also prove strict improvement over the frozen RDP-conversion baseline on a nonempty open parameter region within the interval. Merely applying an RDP accountant and relabeling its bound as GDP, or proving validity only for nonadaptive composition, does not count.",
            "frozen_assumptions": [
                "Mechanism is the Poisson-subsampled Gaussian mechanism with the adjacency and sampling semantics specified in the theorem.",
                "The adaptive choice of future mechanisms/privacy parameters may depend on all prior outputs, as in the source's full-adaptivity model.",
                "The theorem covers every q∈[0.2,0.8] and states its approximation error explicitly; no claim is made about other mechanisms.",
                "Strict improvement is compared with the standard optimized RDP-to-(ε,δ) conversion for the same parameters on a nonempty open parameter region."
            ],
            "improvement_criterion": "Extend proof-valid approximate GDP filtering through the intermediate q range and exhibit a formally certified privacy bound strictly tighter than the specified RDP baseline on an open parameter region.",
            "deadline": "2030-12-31",
            "resolution_policy": "Two reviewers check the adaptive model, sampling semantics, complete closed q interval, approximation guarantee, and an explicit analytic comparison with the frozen RDP conversion. Numerical experiments alone are not sufficient.",
            "evidence_standard": "Primary theorem/proof in a dated paper; an independent privacy-theory reviewer verifies the filter validity and the strict comparator inequality.",
            "ambiguity_policy": "A filter that is valid only for fixed mechanism sequences, covers only a subinterval, has no error guarantee, or does not beat the specified RDP conversion is partial progress only.",
            "sources": [
                source("f-Differential Privacy Filters: Validity and Approximate Solutions", "https://arxiv.org/abs/2602.06756", "2026-02-06", "PRIMARY_VALIDITY_THEOREMS_AND_APPROXIMATE_FILTER_REGIMES", "Fully adaptive validity characterization and q<0.2/q>0.8 subsampled Gaussian approximate-filter results")
            ],
            "forecast_statement": "I judge substantial progress on a valid intermediate-rate adaptive GDP filter by 2030 plausible but highly uncertain: the 2026 paper supplies a rigorous framework and nontrivial endpoint regimes, while the omitted middle range may reflect a real technical obstacle.",
            "expectation": "HIGHLY_UNCERTAIN_WITH_DIRECTIONAL_LEAN",
            "directional_lean": "INTERMEDIATE_RATE_FILTER_PROGRESS_BY_2030",
            "supporting_evidence": "The 2026 source proves a fully adaptive central-limit theorem and valid approximate filters in two nontrivial sampling regimes, providing a concrete technical platform for extension.",
            "counterevidence": "The natural composition filter is fundamentally invalid in general; the excluded middle interval may be where the approximation error or adaptivity obstruction is worst.",
            "uncertainty": "The event's strict improvement requirement is stronger than mere validity and depends on a carefully matched RDP comparator; only a formal theorem can decide it.",
            "primary_future_sources": ["AISTATS/NeurIPS/ICML/ITC/FOCS proceedings", "arXiv primary versions", "privacy journals"],
            "search_strategy": "Search f-DP filters, privacy filters, approximate GDP, Poisson subsampling and adaptive composition. Verify exact q intervals, composition model, proof-level validity, and numerical-versus-analytic comparisons.",
            "censoring_policy": "No result found is not a failure label. A horizon-end nonoccurrence requires a logged source-coverage report and independent review; otherwise retain INSUFFICIENT_EVIDENCE.",
            "independent_review_requirement": "Two independent human reviewers, at least one specializing in differential privacy accounting; reviewers check the RDP conversion formula and same-parameter comparison."
        }
    ]


def monitoring_spec(row: dict) -> dict:
    return {
        "event_id": row["event_id"],
        "active": False,
        "status": "PREPARED_INACTIVE",
        "issue_timestamp": row["issued_at"],
        "observation_start": row["observation_start"],
        "deadline": row["deadline"],
        "primary_sources": row["primary_future_sources"],
        "search_strategy": row["search_strategy"],
        "milestones": ["2027-12-31", "2028-12-31", row["deadline"]],
        "partial_progress_is_not_success": True,
        "search_miss_is_not_negative": True,
        "outcome_categories": [
            "EVIDENCE_FOUND_UNADJUDICATED", "EVENT_ACHIEVED", "PARTIAL_PROGRESS_NOT_SUCCESS",
            "PREMISE_REVISION_NOT_SUCCESS", "EVENT_CONTRADICTED", "INSUFFICIENT_EVIDENCE", "NOT_YET_DUE"
        ],
        "adjudicators_required": 2,
        "llm_counts_as_independent_reviewer": False,
        "escalate_if_assumptions_or_model_ambiguous": True,
        "status_only": "NO_CRAWLER_NO_SCHEDULE_NO_WORKER"
    }


def _write_json(path: Path, value: dict) -> None:
    write_immutable_json(path, value)


def build() -> tuple[dict, dict, dict, dict, dict]:
    for path in (COHORT, MONITORING, MANIFEST, REPORT_JSON):
        if path.exists():
            raise ForecastEngineError(f"refusing to overwrite existing deliverable: {path.relative_to(ROOT)}")
    original = load_json(ORIGINAL)
    original_monitoring = load_json(ORIGINAL_MONITORING)
    if original.get("forecast_count") != 3 or len(original.get("forecasts", [])) != 3:
        raise ForecastEngineError("the original activation must still contain exactly three records")
    issue = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    frozen = []
    for draft in drafts():
        draft = deepcopy(draft)
        draft["evidence_cutoff"] = issue
        draft["observation_start"] = issue
        draft["forecast_issue_timestamp"] = issue
        draft["forecast_direction"] = draft["expectation"]
        draft["frozen_event_definition"] = draft["exact_event"]
        draft["acceptance_criterion"] = draft["improvement_criterion"]
        row = freeze_prospective_forecast(draft, issue)
        # The forecast engine's generic snapshot schema is retained; these extra
        # versioned fields are included in the canonical content hash.
        frozen.append(row)
    ids = [row["event_id"] for row in frozen]
    if len(ids) != len(set(ids)):
        raise ForecastEngineError("duplicate event IDs in new cohort")
    original_ids = {row["event_id"] for row in original["forecasts"]}
    if original_ids.intersection(ids):
        raise ForecastEngineError("new forecasts must not duplicate original event IDs")

    original_snapshot = original["prospective_snapshot"]
    # The original three rows predate the family field.  Keep those frozen rows
    # byte/value-identical and represent each legacy row as its own family only
    # in the new cohort-level metadata.
    family_assignments = {
        row["event_id"]: row.get("research_family_id", f"LEGACY-{row['event_id']}")
        for row in original["forecasts"] + frozen
    }
    legacy_subfields = {
        "PLANAR-THREE-SETS-CUT-UNCUT-112": "planar_graph_algorithms",
        "DISCRETE-FRECHET-TRANSLATION-PLANAR-N4": "computational_geometry",
        "K-HOP-DOMINATION-LOW-EXPANSION-NO-GIRTH": "distributed_algorithms",
    }
    subfield_assignments = {
        row["event_id"]: row.get("subfield", legacy_subfields.get(row["event_id"], "unclassified"))
        for row in original["forecasts"] + frozen
    }
    source_hashes = [
        {"path": "data/forecast_engine/activated_forecasts.json", "sha256": hash_file(ORIGINAL),
         "scope": "FULL_ORIGINAL_ACTIVATION_BYTES_UNMODIFIED"},
        {"path": "data/forecast_engine/activated_forecast_monitoring.json", "sha256": hash_file(ORIGINAL_MONITORING),
         "scope": "FULL_ORIGINAL_INACTIVE_MONITORING_BYTES_UNMODIFIED"},
    ]
    snapshot = build_prospective_snapshot(
        frozen, issue, original_snapshot["snapshot_id"], original_snapshot["snapshot_sha256"], source_hashes
    )
    snapshot["candidate_set_version"] = "CS-PROSPECTIVE-COHORT-V2-20261017"
    snapshot["snapshot_sha256"] = sha256_bytes(canonical_json({k: v for k, v in snapshot.items() if k != "snapshot_sha256"}))
    if not verify_snapshot_hash(snapshot):
        raise ForecastEngineError("new prospective snapshot failed hash validation")

    cohort = {
        "schema_version": "2.0",
        "cohort_id": "CS-PROSPECTIVE-COHORT-V2-20261017",
        "created_at": issue,
        "purpose": "Prospective qualitative benchmark substrate; no outcomes or predictive accuracy are claimed.",
        "original_cohort": {
            "activation_id": original["activation_id"],
            "created_at": original["created_at"],
            "source_file": "data/forecast_engine/activated_forecasts.json",
            "source_sha256": hash_file(ORIGINAL),
            "records": deepcopy(original["forecasts"]),
        },
        "new_forecasts": frozen,
        "new_forecast_count": len(frozen),
        "forecast_count_total": len(original["forecasts"]) + len(frozen),
        "research_family_count_total": len(set(family_assignments.values())),
        "research_family_assignments": family_assignments,
        "subfield_assignments": subfield_assignments,
        "subfield_counts_total": {},
        "prospective_snapshot": snapshot,
        "immutability": "Create-only cohort artifact; later evidence/adjudication must be appended as new records and must not alter forecast rows.",
    }
    # Preserve old records exactly as values and derive counts without editing them.
    for name in subfield_assignments.values():
        cohort["subfield_counts_total"][name] = cohort["subfield_counts_total"].get(name, 0) + 1

    monitoring = {
        "schema_version": "2.0",
        "created_at": issue,
        "active_monitoring_count": 0,
        "scheduled_jobs": [],
        "workers_started": False,
        "activation_requires_separate_authorization": True,
        "original_specifications_copied_unchanged": deepcopy(original_monitoring["specifications"]),
        "new_specifications": [monitoring_spec(row) for row in frozen],
        "specification_count_total": len(original_monitoring["specifications"]) + len(frozen),
        "status": "PREPARED_INACTIVE",
    }
    manifest = {
        "schema_version": "1.0",
        "cohort_id": cohort["cohort_id"],
        "created_at": issue,
        "original_activation_sha256": hash_file(ORIGINAL),
        "original_monitoring_sha256": hash_file(ORIGINAL_MONITORING),
        "original_radar_sha256": hash_file(ROOT / "reports/FUTURE_CS_BREAKTHROUGH_RADAR_20261016.json"),
        "original_forecast_ids": sorted(original_ids),
        "new_forecast_ids": ids,
        "forecast_count_total": cohort["forecast_count_total"],
        "new_forecast_count": len(frozen),
        "unique_research_families_total": cohort["research_family_count_total"],
        "subfield_counts_total": cohort["subfield_counts_total"],
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_sha256": snapshot["snapshot_sha256"],
        "source_hashes": source_hashes,
        "outcomes_frozen": False,
        "monitoring_active": False,
        "predictive_accuracy_evaluated": False,
        "cohort_sha256": sha256_bytes(canonical_json(cohort)),
        "monitoring_sha256": sha256_bytes(canonical_json(monitoring)),
    }
    report = {
        "schema_version": "1.0",
        "created_at": issue,
        "decision": "PROSPECTIVE_COHORT_EXPANDED_QUALITATIVELY; NO_FORECAST_ACCURACY_CLAIM",
        "original_forecast_count": len(original["forecasts"]),
        "new_forecast_count": len(frozen),
        "total_forecast_count": cohort["forecast_count_total"],
        "new_research_families": sorted({row["research_family_id"] for row in frozen}),
        "subfield_counts_total": cohort["subfield_counts_total"],
        "directions": {value: sum(row["expectation"] == value for row in frozen) for value in sorted({row["expectation"] for row in frozen})},
        "deadlines": {row["event_id"]: row["deadline"] for row in frozen},
        "new_snapshot_id": snapshot["snapshot_id"],
        "new_snapshot_sha256": snapshot["snapshot_sha256"],
        "original_forecasts_byte_preserved": True,
        "paper3_target_a": "SEPARATE; no direct outcome labels or scores added.",
        "paper3_target_b": "SEPARATE; no evidence-growth outcome labels or scores added.",
        "paper4": "Action recommendations remain unvalidated; no planner utility result is claimed.",
        "monitoring": "PREPARED_INACTIVE; no jobs, workers, or crawlers started.",
        "candidate_discovery": {
            "new_candidate_questions_screened": 14,
            "fully_operationalized": 7,
            "frozen": 7,
            "subfields_in_depth": 7,
            "rejected_or_excluded": [
                {"candidate": "4-block IP FPT parameterized by block dimension and maximum coefficient", "reason": "Resolved by two 2026 primary preprints before this issue; not prospectively forecastable.", "sources": ["https://arxiv.org/abs/2609.23711", "https://arxiv.org/abs/2609.26746"]},
                {"candidate": "QMC beyond-Hardy–Krause with O(n) samples", "reason": "Resolved in the 2026 primary follow-up before issue; not forecastable.", "sources": ["https://arxiv.org/abs/2609.10921"]},
                {"candidate": "Minimum dilation tree sublinear approximation", "reason": "A September 2026 primary preprint already gives a sublinear approximation; broad target was already achieved.", "sources": ["https://arxiv.org/abs/2609.08990"]},
                {"candidate": "Unit-disk graph diameter truly subquadratic algorithm", "reason": "A 2025 primary theorem already resolves this open question.", "sources": ["https://arxiv.org/abs/2510.16346"]},
                {"candidate": "Minimum cover of orthogonal polygons with squares in polynomial time", "reason": "The cited 2024 primary paper already gives an O(n^10) exact algorithm.", "sources": ["https://arxiv.org/abs/2407.02658"]},
                {"candidate": "MinCSP point-algebra parameterized classification", "reason": "The 2023 primary paper reports a complete classification; no fresh unresolved child endpoint was identified.", "sources": ["https://arxiv.org/abs/2310.05839"]},
                {"candidate": "Stateless asynchronous amnesiac flooding", "reason": "The source question lacks a sufficiently stable frozen scheduler/fairness/termination model for an honest prospective endpoint in this cycle.", "sources": []}
            ]
        }
    }
    return cohort, monitoring, manifest, report, snapshot


def main() -> None:
    cohort, monitoring, manifest, report, snapshot = build()
    # Validate all records before touching persistent stores.
    if len(cohort["new_forecasts"]) != 7 or cohort["forecast_count_total"] != 10:
        raise ForecastEngineError("cohort size invariant failed")
    if len({r["event_id"] for r in cohort["new_forecasts"]}) != 7:
        raise ForecastEngineError("new forecast IDs are not unique")
    if not verify_snapshot_hash(snapshot):
        raise ForecastEngineError("snapshot hash failed its final validation")
    _write_json(COHORT, cohort)
    _write_json(MONITORING, monitoring)
    _write_json(MANIFEST, manifest)
    _write_json(REPORT_JSON, report)
    append_snapshot(SNAPSHOTS, snapshot)
    print(json.dumps({
        "cohort": str(COHORT.relative_to(ROOT)),
        "new_forecasts": 7,
        "total_forecasts": 10,
        "issue_timestamp": cohort["created_at"],
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_sha256": snapshot["snapshot_sha256"],
        "monitoring_active": False,
        "outcomes_scored": False
    }, indent=2))


if __name__ == "__main__":
    main()
