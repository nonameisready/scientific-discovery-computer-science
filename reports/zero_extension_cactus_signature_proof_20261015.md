# Zero Extension on cactus graphs: exact reductions and the corrected cycle review

Task: `THEORY-ZEROEXT-CACTUS-CYCLE-001`
Candidate: `ZERO-EXTENSION-EXACT-SPARSIFIER-005`
Audit date: 2026-10-15

This note is a mathematical proof audit, not an experiment. It does not revisit
the completed tree proof, renew an experiment budget, or alter Paper 3.

## 1. Target and conventions

For a finite connected unweighted graph (G=(V,E)), terminals (S\subseteq V),
a finite metric ((D,\mu)), and an injective terminal labeling
(\tau:S\to D), define

\[
 C_G(\lambda)=\sum_{uv\in E}\mu(\lambda(u),\lambda(v)),
 \qquad
 X_G(\lambda)=|\{uv\in E:\lambda(u)\ne\lambda(v)\}|,
\]

and

\[
 \operatorname{OPT}_{G,k}(\mu,\tau)=
 \min\{C_G(\lambda):\lambda|_S=\tau,
                         X_G(\lambda)\le k\},
\]

with value (+\infty) when the feasible set is empty. The claim below is
quantified over every finite metric with (|D|\le s), every injective
\(\tau\), and every integer (k\ge0). The construction has no label-indexed
state; its only dependence on (s) is the number of retained terminals.

The proof is stated first for unweighted multigraphs, where parallel edges are
distinct objective terms. For a simple input cactus, the resulting two-edge
bundles have a simple realization described in Section 6. The inspected
Reidl--Wahlström source defines the objective on graph edges and obtains its
general sparsifier by contractions; it does not explicitly settle whether a
post-contraction output must be simple. The result below therefore records both
output conventions rather than silently choosing one.

## 2. General local path-suppression lemma

**Lemma (local path suppression).** Let (P=v_0v_1\ldots v_\ell) be a path in
an unweighted graph or multigraph, with distinct endpoints (x=v_0) and
(y=v_\ell). Assume every internal vertex of (P) is nonterminal, has degree
exactly two in the whole host graph, and is used by no other path being
suppressed. Replace (P) by one edge (xy), retaining it as a parallel edge
if (xy) already exists. Then for every fixed labeling of the vertices outside
the internal vertices of (P), the minimum pair ((C,X)) contribution of the
path is preserved exactly, and consequently

\[
 \operatorname{OPT}_{G,k}(\mu,\tau)=
 \operatorname{OPT}_{G/P,k}(\mu,\tau)
\]

for every admissible ((D,\mu,\tau,k)).

**Proof.** Given labels (z_i=\lambda(v_i)), the triangle inequality gives

\[
 \sum_{i=1}^{\ell}\mu(z_{i-1},z_i)\ge\mu(z_0,z_\ell).
\]

If (z_0=z_\ell), the replacement edge has zero cost and zero crossings. If
the endpoint labels differ, the path has at least one crossing and the
replacement edge has exactly one. Replacing all suppressed paths therefore
does not increase either cost or crossing count.

Conversely, for a labeling of the replacement graph, give every internal
vertex of (P) the label of (x). The path cost is exactly
(\mu(\lambda(x),\lambda(y))), and its crossing count is zero or one exactly
as for the replacement edge. Internal vertices are disjoint from the rest, so
these extensions agree at all boundary vertices. Both inequalities, including
the (+\infty) case, follow. The argument does not use acyclicity. In
particular, a cycle is not by itself an obstruction to local path compression.
\(\square\)

The endpoint-distinctness hypothesis matters: a closed terminal-free cycle is
not an (x)-to-(y) path. It is handled by the pendant-component lemma below.

## 3. Terminal-free pendant components

**Lemma (pendant deletion).** If a connected subgraph (R) meets the rest of
the host only at a vertex (v), and (R-v) contains no terminals, delete all
vertices of (R-v) and all incident edges. This preserves the exact restricted
optimum.

For the reverse map, label every deleted vertex by (\lambda(v)); all deleted
edges have zero cost and zero crossings. Restriction removes only nonnegative
terms. The lemma applies to pendant trees, pendant cycles, loops, and a cycle
attached at a terminal articulation. It is stronger than “delete only
terminal-free leaves.” It also handles a whole connected graph with no
terminals by reducing it to the empty graph (or to one isolated vertex when a
terminal remains).

## 4. Series-bundle lemma for cactus block-cut corridors

After pendant deletion and local path suppression, a terminal-free corridor in
the block-cut tree has the following form. Its boundary vertices are
(v_0,\ldots,v_r), and between (v_{i-1}) and (v_i) there are (q_i)
parallel unit edges, where a bridge gives (q_i=1) and a two-boundary cycle
gives (q_i=2). There are no terminal-bearing branches at an internal
(v_i).

**Lemma (series bundle compression).** Such a corridor can be replaced by
(q=\min_i q_i) parallel edges between (v_0) and (v_r), preserving exact
cost and crossing count for every pair of endpoint labels.

For an arbitrary corridor labeling with labels (a_i=\lambda(v_i)),

\[
 C=\sum_i q_i\mu(a_{i-1},a_i)
   \ge q\sum_i\mu(a_{i-1},a_i)
   \ge q\mu(a_0,a_r),
\]

and

\[
 X=\sum_i q_i\mathbf 1[a_{i-1}\ne a_i]
  \ge q\mathbf 1[a_0\ne a_r].
\]

For the reverse direction, use the constant label when (a_0=a_r). When
(a_0\ne a_r), choose an index (j) with (q_j=q), label
(v_0,\ldots,v_{j-1}) by (a_0), and label (v_j,\ldots,v_r) by (a_r).
The resulting cost and crossing count are exactly (q\mu(a_0,a_r)) and
(q). Thus the replacement is exact under any global upper crossing budget,
not merely for a fixed endpoint assignment.

For a standard cactus, (q\in\{1,2\}), so arbitrarily long chains of
terminal-free bridges and two-boundary cycles collapse to one or two edges.
This is the cactus-specific step missing from the earlier tree-only note.

## 5. Complete cactus reduction theorem

Use the block-cut tree (B(G)). Place a terminal marker at a cut-vertex node
when that vertex is terminal, and at a block node when a non-cut terminal lies
inside that block. Retain the minimal connected subtree carrying all markers.
Every component of (B(G)) outside it is a pendant component with no terminal
other than its attachment vertex and is deleted by Section 3. In the retained
subtree, maximal unmarked degree-two corridors are compressed by Sections 2
and 4.

For each remaining cycle block, let its boundary vertices be the terminals in
the block together with vertices where terminal-bearing components attach.
Apply the local path lemma to every open arc between consecutive boundary
vertices.

The resulting (H) has the same terminals and, for every admissible metric,
labeling, and (k),

\[
 \boxed{\operatorname{OPT}_{G,k}(\mu,\tau)=
        \operatorname{OPT}_{H,k}(\mu,\tau).}
\]

The proof is two-sided. In the forward direction, pendant deletion removes
zero-labelable components, and every suppressed arc/path is replaced using
triangle inequality and the endpoint-disagreement lower bound. In the reverse
direction, use constant-on-path extensions, the minimum-multiplicity switch in
each series corridor, and parent-label extensions in deleted components. All
pieces have disjoint interiors, so their cost and crossing counts add exactly.
This establishes preservation of the global crossing budget, including
infeasible (+\infty) cases.

### Cycle boundary cases

* **Zero boundary vertices:** the component is irrelevant unless it is the
  whole terminal-free instance; delete it.
* **One boundary vertex:** it is a pendant component, including a loop or a
  cycle attached only at a terminal articulation; delete it by constant
  labeling.
* **Two boundary vertices:** the two cycle arcs become two distinct parallel
  edges. They must remain distinct in the multigraph representation.
* **Three or more boundary vertices:** each arc is replaced by one edge; the
  cycle remains a simple cycle on its boundary vertices.
* **Loops:** a loop always has equal labels at its two incidences, hence zero
  cost and zero crossings; delete it.
* **Parallel edges:** retain multiplicity in the multigraph model. For a
  standard cactus, a cycle contributes at most two parallel edges after arc
  suppression. The series lemma also handles a two-edge cycle chain.
* **Terminal articulations:** a terminal articulation is a boundary vertex,
  but a cycle attached only there is still removable because all its other
  vertices can copy the fixed terminal label.

## 6. Simple-output realization

The previous Worker artifact incorrectly treated two parallel edges as an
unresolved simple-graph obstruction. They can be simulated exactly.

Replace two parallel edges (xy) by two internally vertex-disjoint paths
(x-u-y) and (x-v-y), with fresh nonterminals (u,v). The graph is simple.
Each path has endpoint cost at least \(\mu(a,b)\) and at least one crossing when
(a\ne b\), while assigning its internal vertex the label of (x) attains
exactly one crossing and cost \(\mu(a,b)\). The two paths therefore reproduce
exactly the cost (2\mu(a,b)) and crossing count
(2\mathbf1[a\ne b]) of the parallel pair. This remains true inside any
global graph because the two path interiors are disjoint.

Thus the cactus reduction is a simple-graph theorem if arbitrary fresh
nonterminal vertices are allowed in the output. If an external definition
requires a contraction-only output on the original vertex set and also forbids
parallel edges, that is a different representation restriction; this note does
not silently claim the 4-cycle gadget is a contraction of the original host.

## 7. Size bound and hidden label dependence

Let (t=|S|). The minimal marked subtree of the block-cut tree has at most
\(O(t)\) leaves and branching nodes: leaves are charged to distinct terminal
markers, and a tree with (L) leaves has at most (L-2) branching vertices.
Degree-two unmarked corridors are replaced by one bundle, and every retained
cycle block contributes one edge per boundary arc. The sum of all boundary
degrees over the reduced block-cut tree is \(O(t)\). A standard cactus cycle
has at most two edges per two-boundary bundle, and the simple realization in
Section 6 multiplies this by only a constant. Therefore

\[
 |E(H)|=O(t)=O(|S|)\le O(s),
 \qquad\text{with universal }k\text{-exponent }0.
\]

No label representative family is used, and no (s)-dependent exponent or
hidden label-indexed graph construction appears. This is a restricted host-class
theorem, not a solution of the unrestricted Zero Extension sparsifier problem.

## 8. Independent adversarial review

The fragile steps were checked separately:

1. The local path proof needs distinct endpoints and degree-two internal
   vertices; it is valid in cyclic host graphs because the proof is local.
2. Two parallel edges are not a counterexample to simple-output preservation:
   the two-path 4-cycle has the same endpoint cost/crossing signature.
3. A terminal-free cycle with one attachment is removable even when the
   attachment is terminal; the reverse constant labeling gives zero terms.
4. A chain of cycles cannot be compressed by blindly suppressing degree-four
   articulation vertices, but the weighted-series inequality proves the
   correct bundle compression.
5. A cycle with three or more boundary vertices is not collapsed to one edge;
   every boundary arc is retained separately, so independent crossing terms are
   not lost.
6. The size bound counts block-cut branching and boundary arcs, not merely
   terminals on the original graph; long terminal-free chains are explicitly
   removed by the series lemma.

No step proves a lower bound for arbitrary sparsifiers, and no finite example is
promoted to an asymptotic lower bound.

## 9. Prior-art and novelty assessment

The source-matched Reidl--Wahlström target is exact metric-labeling cost under a
crossing budget; its general fixed-(s) theorem remains (O(k^{s+1})). The
Goranci--Räcke *Vertex Sparsification in Trees* work concerns vertex flow/cut
sparsifiers and related exact restricted constructions, not this exact
metric-labeling objective. Its tree degree-two simplifications and the
block-cut/path reductions here are standard graph preprocessing ideas, not a
publication-level novelty claim. The cactus result is therefore classified as
an independently checked restricted corollary/engineering lemma. It does not
resolve the unrestricted label-independent exponent question.

## 10. Final classification and next obstacle

* **Fully proved:** local path suppression for arbitrary graph hosts under the
  stated degree-two/distinct-endpoint assumptions.
* **Fully proved, restricted:** exact (O(|S|)k^0) sparsification for standard
  connected cactus hosts, with a multigraph output and a simple fresh-vertex
  realization.
* **Known prior art / non-novel:** pendant deletion, degree-two suppression,
  block-cut pruning, and elementary series compression.
* **Not proved:** any universal exponent for unrestricted graphs; any lower
  bound for all terminal-preserving sparsifiers; any claim that (s+1) is
  necessary.

The cactus task is closed. The next genuinely nontrivial obligation is O7:
construct a contraction-only family with pairwise distinguishable exact
metric-cost signatures, then separately determine whether that obstruction can
be lifted to arbitrary terminal-preserving sparsifiers. No experiment is
authorized or needed for that mathematical task.

Paper 3 Target A and Target B remain unchanged.
