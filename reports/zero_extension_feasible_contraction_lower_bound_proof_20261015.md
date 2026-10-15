# Feasible contraction-only lower bounds: the Multiway-Cut gate

**Task:** THEORY-ZEROEXT-FEASIBLE-CONTRACTION-LOWER-BOUND-002

## 1. Feasibility characterization

Let \(G=(V,E)\) be a finite undirected multigraph with terminals
\(S\subseteq V\), let \((D,\mu)\) be any finite metric, and let
\(\tau:S\to D\) be injective. Define

\[
  \operatorname{OPT}_{G,k}(\mu,\tau)
  =
  \min_{\substack{\phi:V\to D,\ \phi|_S=\tau\\
                  |\{uv\in E:\phi(u)\ne\phi(v)\}|\le k}}
       \sum_{uv\in E}\mu(\phi(u),\phi(v)),
\]

with \(+\infty\) for an empty feasible set. A terminal Multiway Cut is an
edge set \(C\subseteq E\) such that every connected component of \(G-C\)
contains at most one terminal; parallel edges are counted separately.

### Theorem (exact feasibility equivalence)

\[
  \operatorname{OPT}_{G,k}(\mu,\tau)<+\infty
  \quad\Longleftrightarrow\quad
  \lambda_{\mathrm{MWC}}(G,S)\le k.
\]

The right-hand side depends only on \((G,S,k)\), not on the metric or the
particular injective terminal labeling.

### Proof: finite optimum implies a Multiway Cut

Suppose \(\phi\) is feasible and let
\[
  C_\phi=\{uv\in E:\phi(u)\ne\phi(v)\}.
\]
Then \(|C_\phi|\le k\). Every component of \(G-C_\phi\) is monochromatic,
because each remaining edge has equal endpoint labels. If such a component
contained two terminals \(s\ne t\), their labels would be equal, contradicting
injectivity of \(\tau\). Thus \(C_\phi\) is a terminal Multiway Cut.

### Proof: a Multiway Cut implies a finite optimum

Let \(C\) be a terminal Multiway Cut with \(|C|\le k\). Every component of
\(G-C\) contains at most one terminal. Assign its unique terminal label when
it has one, and assign any fixed element of \(D\) to a terminal-free
component. This gives an extension \(\phi\) whose crossing set is contained
in \(C\), hence has at most \(k\) crossings. The graph, metric, and label set
are finite, so its cost is finite. Therefore the optimum is finite.
\(\square\)

The proof also covers disconnected graphs, loops, and parallel edges. A loop
cannot be a crossing edge and contributes zero metric cost. A terminal-free
component only needs one arbitrary label; injectivity is required only on
terminals.

## 2. Consequences for the lower-bound target

The equivalence removes the O7 infeasible-instance shortcut completely. A
candidate family for a feasible contraction-only lower bound must satisfy
\(\lambda_{\mathrm{MWC}}(G,S)\le k\). It is not enough to exhibit a metric
whose optimum is \(+\infty\), and it is not legitimate to use an arbitrarily
large quotient forced by a no-instance.

The equivalence also separates two claims:

1. **Feasibility preservation:** a quotient must retain the existence of a
   terminal Multiway Cut of size at most \(k\).
2. **Exact metric preservation:** the quotient must preserve the minimum cost
   among all extensions with at most \(k\) crossings, for every metric and
   injective terminal labeling.

The first is necessary but not sufficient for the exact sparsifier objective.
A quotient can preserve the minimum Multiway-Cut cardinality while destroying
which low-crossing decompositions are available to a metric labeling.

## 3. Adversarial review of feasible superlinear routes

The pair-bundle construction from O7 is preserved but not repeated. Its
proved inequality is \(L\le k\) on every feasible instance, so it cannot
produce a superlinear-in-\(k\) result. The following stronger route was tested
mathematically rather than by enumeration:

> Construct many edge signatures, each witnessed by a different
> terminal Multiway Cut of size at most \(k\), and prove that every quotient
> omitting enough signatures changes an exact metric optimum.

The missing step is a joint contraction hitting-set theorem. Pairwise
witnesses do not supply it: a single quotient edge can preserve many
signatures simultaneously, and contracting one edge can reroute all of the
witness cuts through another edge. The Multiway-Cut gate makes this
obstruction sharper: every witness must be a low-order terminal separation,
not merely a pairwise metric distinction.

No explicit feasible family survived all of the following proof obligations:

* all admissible injective labelings have finite optimum;
* every permitted joint contraction is covered, not just one edge at a time;
* the metric witnesses satisfy positivity, symmetry, and triangle inequality;
* an omitted edge or bag provably changes the exact \(k\)-bounded optimum;
* the number of forced retained edges is superlinear in \(k\);
* the argument does not silently become a lower bound for arbitrary
  terminal-preserving sparsifiers.

This is an evidence-based failure of the current construction route, not a
proof that no feasible superlinear family exists.

### Exact obstruction to the forbidden shortcut

Any proposed witness with \(\operatorname{OPT}_{G,k}=+\infty\) is invalid for
the present objective: by the theorem, it has
\(\lambda_{\mathrm{MWC}}(G,S)>k\). Such a witness can only diagnose a
representation restriction of a total quotient model. It cannot establish a
feasible lower bound and cannot be used to infer anything about the
source's full sparsifier construction.

## 4. Claim classification

| Claim | Classification |
|---|---|
| Finite exact objective iff terminal Multiway Cut size is at most \(k\) | Fully proved |
| The criterion is independent of the finite metric and injective labeling | Fully proved |
| Feasible pairwise path bundles give only \(\Omega(k)\) | Previously proved and preserved |
| Pairwise witnesses force a superlinear joint-contraction lower bound | Disproved as an inference |
| A feasible \(k^{\Omega(s)}\) contraction-only family exists | Plausible but unproved |
| A feasible superlinear family has been established in this cycle | Disproved for the attempted route; no family survived |
| Any contraction-only lower bound transfers to arbitrary sparsifiers | Not established |

## 5. Concrete alternative beyond the blocked route

The next mathematically narrower direction is a two-terminal
series-parallel interface theorem:

> For a two-terminal series-parallel graph with
> \(\lambda_{\mathrm{MWC}}\le k\), characterize the smallest
> terminal-preserving contraction quotient that preserves every metric
> \(k\)-bounded optimum. Either prove a universal polynomial bound using a
> finite dynamic-programming interface of cut states, or exhibit a feasible
> series-parallel counterexample whose joint states force a superlinear
> quotient.

This is beyond cactus, excludes the no-instance pathology by construction,
and directly tests whether the representative-set exponent is caused by
general graph topology or by label-state interaction. The first proof
obligation is an exact composition lemma for series and parallel nodes; it
must preserve both cost and the number of crossings, not only minimum cut
cardinality. No experiment is authorized or needed for this formulation.

Paper 3 Target A/B and all prior negative results remain unchanged.
