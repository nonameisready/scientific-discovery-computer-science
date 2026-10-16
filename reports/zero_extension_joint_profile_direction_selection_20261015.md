# Zero Extension joint-profile review and theory-direction selection

Review date: 2026-10-15 (bounded mathematical cycle; no experiment)

## Decision

The attempted Priority-A route does not produce a defensible simultaneous
representative-family theorem in this cycle.  It is closed as a candidate
route, not disproved as a mathematical possibility.  The exact property that
would be needed is recorded below, together with the obstruction that prevents
the tempting "correlate the gammoid layers and delete the uniform layer"
argument.

Exactly one successor is admitted to the theory queue:
`THEORY-PARALLEL-TOKEN-SWAPPING-TREE-APPROX-001`.

## O13 correction and provenance boundary

The earlier all-terminal `K3` proposal was invalid.  Every edge of that graph
belongs to the terminal boundary `E_S`, while the source collection
`Y(e)=(e'_1,...,e'_s,e_0)` is indexed only by `E\\E_S`.

The corrected raw source-level witness is the two-terminal parallel bundle

```
a --(3 parallel edges)-- u --(e1,e2 parallel)-- v --(3 parallel edges)-- b,
S={a,b}, k=3, q=2, mu(A,B)=1.
```

The four possible `a`-side sets have cut sizes `3,2,8,3`.  Thus the unique
cost-2, at-most-3-crossing extension crosses `e1,e2`, and both are outside
the *raw* terminal boundary of six edges.  For either target, the gammoid
coordinates are the same; `M_0=U_{8,3}` with the other central edge in
`X_0` supplies the unique-extension discriminator.  This is the corrected
finite witness requested for the historical O13 failure record.

There is an important source-provenance qualification.  Reidl--Wahlström
apply Corollary 4.2 before constructing the gammoids.  In this two-terminal
graph the furthest minimum `a`--`b` cut is the two-edge middle cut, so the
preprocessing contracts `u` into `a` (and symmetrically on the other side);
the middle edges then become terminal-incident.  Consequently the bundle is
a valid witness for the raw certificate-layer audit, but not a claim that the
two edges remain non-boundary after that preprocessing.  The ledger now says
this explicitly and retains the historical K3 rejection.

For an actually preprocessed adversarial check, take four terminals `a,b,c,d`,
nonterminals `u,v`, two parallel `u-v` edges `e1,e2`, and `L>=3` parallel
edges on each of `a-u`, `b-u`, `c-v`, and `d-v`.  For each terminal, its
singleton cut has size `L`; adding its adjacent nonterminal exposes at least
`L+2` edges, so the furthest isolating cut is the singleton and the central
edges survive Corollary 4.2.  With the discrete metric on `A,B,C,D`, terminal
labels in that order, and `k=q=2L+2`, every extension of cost at most `q`
must give `u` one of `A,B`, `v` one of `C,D`; it then crosses exactly the two
central edges and one `L`-bundle on each side.  Any equal-label or same-side
choice costs at least `3L>2L+2` for `L>=3`.  Hence both central edges are
essential in a graph that survives the source preprocessing.  This check does
not prove a lower bound on representative-family size.

## Exact joint-extension property

Let `U=E\\E_S`.  For a tuple of independent gammoid-layer sets
`X=(X_1,...,X_s)`, define

```
Gamma(X) = { e in U : {e'_i} extends X_i in gammoid M_i for every i in [s] }.
```

For a uniform-layer exclusion set `B subseteq U` with `|B|<=k-1`, the full
direct-sum query has extension set

```
Q(X,B) = Gamma(X) \\ B.
```

A retained edge set `R subseteq U` is a joint representative for the source
query family exactly when, for every admissible `X` and `B`,

```
Q(X,B) is nonempty  <=>  R intersection Q(X,B) is nonempty.
```

This is stronger than preserving each gammoid layer separately.  It also
separates an abstract representative family from the later sequential
contraction algorithm and from an arbitrary terminal-preserving sparsifier.

The uniform coordinate cannot simply be dropped.  Whenever an admissible
profile has `|Gamma(X)|<=k`, choosing `B=Gamma(X)\\{e}` makes `e` the only
surviving answer.  Therefore every edge in such a profile must belong to any
representative satisfying the displayed property.  In the corrected bundle
audit, `Gamma(X)` contains both central edges and each is forced by the
corresponding singleton exclusion.  In the four-terminal post-preprocessing
check, the same argument applies to `e1,e2`.

This does not establish that the union of all such profiles is large.  It does
establish the first proof obligation for any claimed correlation theorem: it
must either bound that union, or replace the source query with a different
reconstruction argument.  A common gammoid-only hitting set is insufficient.

## Candidate lemma and adversarial review

The narrow candidate was the following stable-profile lemma.

> For fixed `s`, let `P(G,S,k)` be the profiles induced by pushed,
> minimum-crossing optimal witnesses in the source proof.  The union of all
> `Gamma(X)` with `|Gamma(X)|<=k` has size at most `f(s) k^c`, for a universal
> constant `c`, and a retained set of that size preserves every essential-edge
> query.

The hoped-for target was `c=1` or `c=2` with `f(s)=2^{O(s)}`.  The first
implication is valid only for the stated profile family: the uniform exclusion
argument then forces retaining the union.  The second implication is not a
proof.  The union can be as large as the set of essential edges, and the
source proof gives no bound on that union before representative compression.

The corrected bundle witness tests the exact failure mode but does not refute
the lemma: its union has size two.  The four-terminal construction also gives
only two forced edges.  Conversely, replacing the direct sum by an intersection
of layer-wise extension systems is not justified: intersections of matroids
need not be matroids, and no representative-set theorem applies without an
exchange axiom or a new exchange surrogate.  The source's componentwise
independence gives no cross-layer exchange for free.

Thus the candidate has a precise target and proof obligations, but no proved
size bound and no valid route from correlations to a representative theorem.
The cycle is closed at this boundary.

## Claim classification

| Claim | Status |
|---|---|
| Source definition, `s+1` certificate layers, ranks, and `O_s(k^(s+1))` bound | Known prior art; source reconstructed |
| All-terminal `K3` is an eligible O13 witness | Disproved; all edges are in `E_S` |
| Two-terminal parallel bundle is a raw source-level witness for the M0 deletion audit | Finite counterexample; independently checked |
| The same bundle remains an internal-edge witness after Corollary 4.2 | False; preprocessing qualification above |
| Four-terminal two-edge bundle survives preprocessing and retains two essential internal edges | Finite construction, hand-verified; not an asymptotic lower bound |
| The exact joint query is `Gamma(X)\\B` for `|B|<=k-1` | Fully proved from direct-sum extension |
| A smaller simultaneous gammoid representative family exists | Plausible but unproved |
| A universal-exponent sparsifier improvement follows | Not established |

## Independent source check and alternative direction

Reidl--Wahlström define the exact metric sparsifier and state the
`O(k^(s+1))` construction in Section 4.3 of the primary paper
([arXiv:1802.06026v1](https://arxiv.org/html/1802.06026v1), Definition 4.5,
Theorem 4.6, Lemma 4.7 and the proof at lines 303--331).  The later
token-swapping sources are a separate problem, not evidence for Zero
Extension.  Aichholzer et al. prove NP-completeness of parallel token swapping
on trees but leave approximation substantially open in their source discussion
([ESA 2022](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2022.3)).
Bansal--Günlük--Shapley give constant-factor algorithms for cycles, subdivided
stars and grid topologies, not arbitrary trees
([arXiv:2411.18581](https://arxiv.org/abs/2411.18581); published version,
2025).  A targeted search through this checkpoint found no primary-source
result settling a constant-factor approximation for arbitrary trees; this is
a bounded eligibility statement, not a global absence proof.

The admitted task asks first for a theorem-level test of the concrete
congestion-plus-dilation conjecture

```
rounds(T,pi) <= C(T,pi) + D(T,pi) + O(1),
```

where `D` is the maximum token path length and `C` the maximum number of token
paths crossing one tree edge.  Since every schedule needs at least
`max(C,D)` rounds, a proof would immediately give a constant-factor
approximation.  A proof or a hand-checkable counterexample is a sharper first
obligation than another literature audit.  No computational experiment is
authorized or implied.

## Paper 3 and execution boundary

Paper 3 Target A (direct resolution/refutation) and Target B (evidence growth)
remain separate, frozen, and unscored.  No historical label was added.  The
worker-execution validation record remains distinct from independent scientific
reconciliation; no supervisor-owned state was attributed to a worker.  No
experiment budget was renewed.
