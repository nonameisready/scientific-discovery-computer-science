# Contraction-only Zero Extension: a proved obstruction and the remaining gap

**Task:** THEORY-ZEROEXT-CONTRACTION-LOWER-BOUND-001
**Candidate:** ZERO-EXTENSION-EXACT-SPARSIFIER-005
**Scope:** mathematical proof audit only; no experiment, network search, or budget renewal.

## 1. Exact model and objective

Let \(G=(V,E)\) be a finite undirected multigraph, \(S\subseteq V\) its terminal
set, \(s\ge |S|\), and \(k\in\mathbb N\). Parallel edges count separately.
For a finite metric \((D,\mu)\), an injective terminal labeling
\(\tau:S\to D\), and an extension \(\phi:V\to D\), define

\[
  \operatorname{cr}_G(\phi)=|\{uv\in E:\phi(u)\ne\phi(v)\}|,
  \qquad
  \operatorname{cost}_G(\phi)=\sum_{uv\in E}\mu(\phi(u),\phi(v)).
\]

The exact crossing-bounded objective is

\[
  \operatorname{OPT}_{G,k}(\mu,\tau)=
  \min_{\substack{\phi|_S=\tau\\\operatorname{cr}_G(\phi)\le k}}
  \operatorname{cost}_G(\phi),
\]

with value \(+\infty\) when the feasible set is empty. Exact preservation
means equality of this value for every finite metric with
\(|D|\le s\), every injective \(\tau:S\to D\), and the fixed \(k\).

### Contraction-only quotient

Choose \(F\subseteq E\) such that every connected component of \((V,F)\)
contains at most one terminal. Let \(\Pi_F\) be those connected components.
The quotient \(G/F\) has one vertex for each bag \(B\in\Pi_F\). Every original
edge whose endpoints lie in distinct bags becomes one quotient edge between
the corresponding bags; loops are deleted and parallel edges are retained
with their multiplicity. The terminal in a bag is the same terminal in the
quotient. No new vertices, edges, or edge deletions other than loops are
allowed.

This is deliberately narrower than the source's full sparsifier model. The
source construction uses a retained certificate and a contraction step after
source-specific preprocessing; it is not a theorem that every instance can
be replaced by a small quotient of the original graph. In particular, an
early no-instance replacement, if used, is outside this total quotient model.
It is also different from an arbitrary terminal-preserving graph \(G'\), which
may add fresh vertices or edges.

## 2. The pair-bundle family

For integers \(r\ge2\) and \(t\ge1\), define \(B_{r,t}\) as follows. The
terminals are \(S=\{1,\ldots,r\}\). For every unordered pair
\(\{i,j\}\subseteq S\), create \(t\) fresh vertices
\(u_{ij,1},\ldots,u_{ij,t}\), with edges

\[
  i-u_{ij,\ell}-j \qquad (1\le \ell\le t).
\]

There are \(L=t\binom r2\) internally vertex-disjoint terminal-to-terminal
paths of length two.

### Lemma 1: exact value and crossing threshold

For every finite metric \((D,\mu)\) and every injective
\(\tau:S\to D\),

\[
  \operatorname{OPT}_{B_{r,t},k}(\mu,\tau)=
  \begin{cases}
    t\displaystyle\sum_{i<j}\mu(\tau(i),\tau(j)), & k\ge L,\\
    +\infty, & k<L.
  \end{cases}
\]

**Proof.** On every length-two path \(i-u-j\), its endpoint labels are
distinct. Any intermediate label \(d\) satisfies

\[
  \mu(\tau(i),d)+\mu(d,\tau(j))\ge\mu(\tau(i),\tau(j))
\]

by the triangle inequality, and at least one of its two edges crosses. Giving
\(u\) the label \(\tau(i)\) attains exactly one crossing and exactly the
endpoint distance. The paths have disjoint interiors, so the lower bounds add.
Thus the total minimum crossing count is \(L\), and the displayed cost is
attained exactly when \(L\le k\). \(\square\)

### Lemma 2: every terminal-preserving quotient has at least \(L\) edges

For every allowed contraction set \(F\),

\[
  |E(B_{r,t}/F)|\ge L.
\]

Moreover the bound is tight: contract one of the two edges on every path,
producing \(L\) parallel terminal-terminal edges.

**Proof.** A path \(i-u_{ij,\ell}-j\) cannot have both edges in \(F\), because
that would put the two distinct terminals \(i,j\) in one contraction bag. If
neither edge is contracted, the path contributes two non-loop quotient edges.
If exactly one is contracted, it contributes one edge between the terminal bags.
No internal vertex of one path is adjacent to an internal vertex of another
path, so contractions cannot merge two paths except through a terminal, and
terminal bags cannot merge. Hence every one of the \(L\) paths contributes at
least one quotient edge. Contracting exactly one edge per path gives equality.
\(\square\)

### Lemma 3: the quotient family is exact, but gives only a linear budget bound

Every terminal-preserving quotient of \(B_{r,t}\) has the same exact
\(k\)-bounded objective as \(B_{r,t}\) for all admissible metrics and
labelings. Consequently, when \(L\le k\), every contraction-only exact
sparsifier of this family has minimum size exactly \(L\le k\).

**Proof.** Each quotient image of an original path is either a direct edge or a
length-two path with the same distinct terminal endpoints. The same triangle
inequality and one-crossing construction used in Lemma 1 applies to each
image, and the path interiors remain disjoint. Therefore the value and
feasibility threshold remain \(L\) and the displayed metric sum. \(\square\)

## 3. What this does and does not prove

### Feasible lower bound

Taking \(r=2\) and \(t=k\) gives a feasible family with

\[
  \min_F |E(B_{2,k}/F)|=k.
\]

This is a fully proved \(\Omega(k)\) lower bound for the strict contraction-only
model, already with two terminals and with all finite metrics allowed up to
any label budget \(s\ge2\).

Taking \(r=s\) and \(t=1\), \(k=\binom{s}{2}\), gives a lower bound
\(\binom{s}{2}=\Theta(s^2)=\Theta(k)\). It still has no exponent growing with
\(s\): the apparent \(s\)-dependence is absorbed by the chosen value of \(k\).

More generally, feasibility forces

\[
  t\binom r2\le k,
\]

so the path-bundle edge count is at most \(k\) on every feasible instance.
This is the exact reason that pairwise-distinguishable path signatures do not
yield a \(k^{\Omega(s)}\) lower bound here.

### Infeasible-instance model pathology

If \(t\binom r2>k\), Lemma 1 says the objective is \(+\infty\) for every
admissible metric and labeling, while Lemma 2 says every quotient still has
at least \(t\binom r2\) edges. Letting \(t\to\infty\) gives no finite size
bound as a function of \(k,s\) for a **total** contraction-only model, even
with fixed \(r=2\) and \(k=1\).

This is not evidence for a superconstant-in-\(s\) representative-set lower
bound. It is a representation obstruction: a source algorithm can recognize
the no-instance and return a different small graph only if its model permits
that operation. A pure quotient of the input cannot do so.

### Why the stronger signature argument fails

The following implication is false:

> If many original edges have pairwise distinct metric signatures, then every
> exact quotient must retain one edge per signature and the signatures force
> \(k^{\Omega(s)}\) edges.

Lemma 3 is an explicit counterexample to that inference. The signatures are
fully distinguishable, but one retained quotient edge per path simultaneously
preserves every metric and every terminal labeling. Pairwise distinguishability
does not establish a hitting-set lower bound against **joint** contractions.

The unproved broad statement remains:

> There may exist feasible connected families whose joint contraction choices
> require a retained set larger than \(O(k^c)\) for every universal \(c\), with
> the growth depending on \(s\).

This note neither proves nor disproves that statement. It closes the proposed
pair-bundle construction as an \(s\)-exponent witness and records the exact
obstruction to upgrading it.

## 4. Adversarial review of all contraction cases

* **Single-edge contractions:** one edge of a path is safe and produces one
  terminal edge; contracting both is forbidden by terminal preservation.
* **Joint contractions:** joining several internal vertices to the same
  terminal only turns their paths into separate parallel terminal edges; it
  does not save an edge per path.
* **Cross-path contractions:** impossible because distinct internal vertices
  have no connecting original edge. The quotient model contracts edge sets,
  not arbitrary vertex identifications.
* **Parallel-edge simplification:** forbidden in this model; multiplicity is
  part of the objective. Merging parallel edges would change both cost and
  crossing count and is a different representation rule.
* **New gadgets:** unavailable in a quotient. Allowing fresh vertices or
  edges moves to the arbitrary terminal-preserving model and invalidates this
  lower-bound argument.
* **Metric degeneracy:** positivity and injectivity ensure every terminal pair
  has positive distance and different labels. The proof uses only symmetry,
  positivity, and triangle inequality; no special metric is selected.
* **Crossing budget:** the proof uses the exact minimum crossing count \(L\),
  including the \(+\infty\) case. It does not silently replace a budgeted
  optimum by an unconstrained cut value.

## 5. Independent cactus counting audit

The earlier cactus reduction remains correct, but its size paragraph is made
explicit here. Let \(t=|S|\). Form the block-cut tree and attach one marker
leaf for each terminal: a terminal that is a cut vertex marks that cut node;
a non-cut terminal marks its block node. Let \(T^*\) be the minimal subtree
connecting the \(t\) marker leaves. For \(t\ge2\), after suppressing maximal
unmarked degree-two corridors, the number of unmarked branching nodes is at
most \(t-2\), by the standard degree-sum identity for a tree. The marked
nodes and marker leaves contribute \(O(t)\), so \(T^*\) has \(O(t)\) retained
nodes and edges. The \(t=0,1\) cases reduce to the already proved pendant
deletion cases.

For every retained cycle block \(C\), let \(b(C)\) be the number of its
boundary vertices: terminal vertices in \(C\), plus cut vertices through which
retained block-cut branches attach. Each terminal contributes at most once to
\(\sum_C b(C)\). Each nonterminal attachment is witnessed by an incidence edge
of \(T^*\), so it contributes at most once per relevant block-cut incidence.
Therefore

\[
  \sum_C b(C)\le t+|E(T^*)|=O(t).
\]

A cycle with \(b(C)\le1\) is deleted; a cycle with \(b(C)\ge2\) contributes
exactly \(b(C)\) boundary arcs. Bridge blocks and compressed corridors
contribute \(O(|E(T^*)|)\). Thus the multigraph core has \(O(t)\) edges. The
simple fresh-vertex realization replaces each two-parallel-edge bundle by two
length-two paths, a constant-factor increase. No hidden \(s\)-dependent factor
or exponent appears. This is a counting audit, not a reopening of the cactus
preservation proof.

## 6. Claim classification and next obligation

| Claim | Classification |
|---|---|
| Pair-bundle exact-value formula | Fully proved |
| Every quotient of \(B_{r,t}\) has at least \(t\binom r2\) edges | Fully proved |
| Feasible contraction-only \(\Omega(k)\) lower bound | Fully proved |
| Unbounded total quotient size on infeasible instances | Fully proved model obstruction |
| Pairwise signatures imply an \(s\)-dependent exponent | Disproved by the pair-bundle quotient |
| \(k^{\Omega(s)}\) lower bound for feasible contraction-only instances | Plausible but unproved; this construction does not establish it |
| Transfer to arbitrary terminal-preserving sparsifiers | Not established and explicitly excluded |
| Cactus \(O(|S|)k^0\) size count | Independently rechecked; prior restricted result unchanged |

The narrowest next mathematical question is now:

> **Feasible contraction hitting-set problem:** for fixed \(s\ge3\), can a
> family with finite optimum for every admissible labeling force every
> terminal-preserving quotient to retain \(\omega(k)\) edges through joint,
> rather than pairwise, contraction constraints? If yes, quantify the
> dependence on \(s\); if no, prove a universal feasible-instance quotient
> bound.

This is narrower and more informative than repeating pairwise signature
searches. It remains pure mathematics. The arbitrary-sparsifier transfer
obligation O8 remains separate and is not implied by any result here.

## 7. Final novelty assessment

The \(\Omega(k)\) pair-bundle lemma is a new, self-contained diagnostic for the
explicit quotient model, but it is elementary and does not resolve the
source's \(s\)-dependent exponent question. The infeasible-instance obstruction
shows that the quotient model is too strict to stand in for the source's full
sparsifier model without a no-instance convention. No publication-level
breakthrough, unrestricted lower bound, or lower bound for arbitrary
terminal-preserving sparsifiers is claimed.

No experiment was run, no authorization was consumed, and Paper 3 was not
modified.
