# Proof mechanism discovery: transferable invariants, failed bridges, and no-go

**Bounded-cycle decision: NO-GO.** Three successful mechanisms were reconstructed from primary papers. They clarify how to preserve extension behavior, compress profile counts, or exploit planar order, but no candidate theorem crossed the Category-C admission gate: each was known, equivalent to an existing open problem, or lacked a valid invariant transfer. No new theorem is claimed.

## 1. What the earlier campaigns did—and did not—establish

The history contains correct results, but most stopped at the boundary between a sound restricted argument and a new general principle.

| Campaign result | Correct classification | Actual limitation |
|---|---|---|
| Double-star two-phase routing | Proved restricted-class schedule; priority/publication value uncertain | A double star has one central cut. First sorting tokens by side and then sorting each star works with two centers; on a longer backbone, local preparations at one hub can move identities across or disturb already processed cuts. The proof has no invariant that makes cut phases commute or bounds repeated repair. |
| Monotone crossing-event DAG | Correct characterization of distance-optimal/all-happy schedules | The DAG includes only one traversal per token per edge of its original source-destination path. It is acyclic exactly when a zero-detour schedule exists. Valid solutions may require shoves or temporary displacement; (N_t(e)=1[e\in P_t]+2b_t(e)). Those extra traversal pairs and occupancy dependencies are absent from the DAG. This refutes the proof route, not the existence of a constant-factor algorithm. |
| Bounded-(h) endpoint transpositions | Fully proved elementary parameterized approximation | The diameter bound is (h+1), while up to (hLB_{hub}+h) positions can be wrong. Path endpoint transpositions yield factor (4h^2-1) (or the earlier coarser (2h(2h+1))). The factor depends quadratically on (h), so it gives no uniform bound for arbitrary trees. |
| CS3 corridor signatures | A reformulation equivalent up to constants to the simple-tw3 profile conjecture | A signature to an LCA guard of size at most eight is itself a profile on at most eight landmarks. Conversely (O(k)) guards plus signature-to-profile determination implies the target. CS3 does not reduce the central difficulty. |
| Maximal simple-3-tree clique-distance bound | Correct restricted host result | Distances within a host (K_4) bag differ by at most one, but deleting host edges can make distances in (G) differ arbitrarily. For example, (P_4\subset K_4) has distances (0,1,2,3) from one endpoint in (P_4), unlike the host clique pattern. Host distances cannot replace the partial-graph metric. |

None of these failed bridges disproves its overarching conjecture. The double-star and maximal-host statements are elementary restricted theorems; CS3 is equivalent to its target; and the DAG failure concerns a representation that excludes necessary detours. The history is useful mainly as a warning: identify exactly what an invariant preserves before promoting it to a theorem.

## 2. Three primary-source proof mechanisms

### Mechanism I — LCA-closure guards: local separators, global profile counting

**Source theorem.** Beaudou et al., Lemma 15: if (G) has treewidth at most (t), then for every landmark set (A\subseteq V(G)) and radius (r), there is an ((r,2(t+1)))-guarding family of at most (4|A|) sets. Each guard intersects every (G)-path of length at most (r) from its assigned vertex (x) to any landmark in (A).

**Reconstruction.** Take a width-(t) tree decomposition ((T,(B_z))), root (T), and mark the topmost bag-node (s_a) containing each (a\in A). Let (M) be the marked nodes and (M^*\) their LCA closure. The tree fact (|M^*|\leq2|M|) holds, and every component of (T-M^*) has at most two closure-node neighbors. For (b\in M^*), let (p^*(b)) be its nearest strict ancestor in (M^*) (or (b) at the root). Include (B_b) and (B_b\cup B_{p^*(b)}). There are at most (2|M^*|\leq4|A|) guards, each of size at most (2(t+1)).

For a vertex whose model contains a closure node, that node's bag hits all paths out of the vertex's bag model. Otherwise its model lies in a component (C\subseteq T-M^*). The one or two boundary bags of (C) separate it from landmarks whose models do not enter (C); if a landmark model enters (C), connectedness of that model makes it meet a boundary bag. Thus the appropriate one-bag/two-bag guard hits every graph path, not just paths staying inside the decomposition region.

**Invariant and hypotheses.** The invariant is separator coverage: all short paths from a vertex to the landmark set pass through a bounded bag union. It requires a valid tree decomposition of the measured graph, connected vertex models, and LCA closure. It says nothing about the number of distance vectors to a guard. Applying a separate profile bound to each guard is an additional step; in the general treewidth proof that step costs (r^{t+1}).

**Minimal obstruction to dropping a hypothesis.** If one marks three incomparable leaves of a rooted decomposition tree but omits their LCA from the marked closure, the intervening component can have three boundary attachments. The “at most two boundary bags” argument then no longer supplies the claimed guard. This is a failure of that proof construction, not a counterexample to every possible guard family.

**Known extensions and limit.** The same source combines LCA guards with minor-free profile bounds and colouring-number arguments. The method is established. For simple treewidth three it yields the general (O(r^4|A|)) route unless the per-guard profile count is improved. As shown in the prior CS3 audit, asserting (O(r^3)) for every size-eight guard is equivalent to the full (O(r^3k)) conjecture, not a new bridge.

### Mechanism II — Outerplanar BFS layers: monotone distance partitions

**Source theorem.** Beaudou et al., Theorem 7: for every outerplanar (G), landmark set (A), and (r\geq0),
\[
\mathrm{pc}_r(G,A)\leq1+(2r+2)^2|A|.
\]

**Reconstruction.** In a plane outerplanar embedding all vertices lie on the outer boundary. Start the circular vertex order at a landmark (a_1), and partition vertices into BFS layers (L_i=\{v:d(a_1,v)=i\}). For a fixed landmark (a\neq a_1) and layer (L_i), choose (y\in L_i) minimizing (d(a,y)). The cited boundary-order lemma says distance to (a) is nondecreasing along either circular arc from (y) through (L_i). Hence the truncated (a)-distance partitions that layer into at most (2r+2) consecutive pieces. Overlaying interval partitions adds, rather than multiplies, the number of pieces.

Let (A_i\) be the landmarks other than (a_1) whose radius-(r) balls meet (L_i). Each such landmark is within (r) of at most (2r+1) root-distance layers, so \(\sum_i |A_i|\leq(2r+1)|A|\). Counting the pieces over layers gives
\[
1+\sum_i(2r+2)|A_i|\leq1+(2r+2)^2|A|.
\]

**Invariant and hypotheses.** The invariant is a one-dimensional order on each BFS layer in which each landmark's distance is monotone away from a minimum. The common outer boundary and noncrossing planar structure provide that order. Removing the outerplanar hypothesis removes the proof's global circular order; for example, (K_4) has no embedding with every vertex on the outer face. This is a failure of the mechanism's premise, not by itself a counterexample to any profile bound.

**Known extensions and limit.** The result is tight up to constants even for trees; outerplanar graphs are exactly simple-treewidth at most two. The source explicitly conjectures the (O(r^t|A|)) analogue for bounded simple treewidth. A proposed “corridor order” for treewidth three would need to define an order on partial-graph BFS layers and prove monotonicity under edge deletion. The clique tree's branching and the loss of host edges defeat the immediate boundary-order transfer. No such order or monotonicity lemma was established in this cycle.

### Mechanism III — Matroid representative families: preserve every feasible extension

**Source theorem.** Fomin, Lokshtanov, Panolan, and Saurabh, Theorem 1 / Theorem 3: for a linear matroid (M) of rank (p+q), a family \(\mathcal F\) of independent (p)-sets has a (q)-representative subfamily of size at most \(\binom{p+q}{p}\). Weighted versions preserve a minimum- or maximum-weight feasible representative, and the paper gives a deterministic construction with the stated matrix-operation complexity.

**Reconstruction of the invariant.** Represent elements by columns (x_e\in\mathbb F^{p+q}). Encode each independent (p)-set (S) as its exterior product (w_S=\bigwedge_{e\in S}x_e), represented by all (p\times p) minors, a vector in a space of dimension \(\binom{p+q}{p}\). For a (q)-set (Y), the determinant of the concatenated columns (S\cup Y)—nonzero exactly when (S\cup Y) is a basis—is a bilinear pairing of (w_S) with the complementary (q)-minor vector (w_Y), by generalized Laplace expansion.

Keep a minimum-weight basis of the vectors (w_S). Any discarded (w_X) is a linear combination of retained basis vectors. If some (Y) extends (X), its pairing with (w_Y) is nonzero; by linearity, at least one retained vector also has nonzero pairing, hence its set is disjoint from (Y) and extends with (Y). The minimum-weight basis exchange argument ensures the retained set has weight no larger than (X). For (|Y|<q), extend (X\cup Y) to a basis and apply the size-(q) case. The dimensional bound gives at most \(\binom{p+q}{p}\) representatives.

**Invariant and hypotheses.** It preserves the predicate “there exists a feasible extension of this partial solution by every allowed context (Y),” and optionally its optimum weight. It depends on one fixed linear matroid, independent fixed-cardinality states, and an extension test encoded by the determinant pairing. If a matroid has no supplied linear representation (for example, a nonrepresentable matroid), this exterior-algebra algorithm cannot be invoked; that identifies the limit of this mechanism, not a claim that representative sets cannot exist combinatorially. If (p+q) is not bounded, the dimension bound itself grows.

**Known extensions and limit.** Product-family algorithms compose representative families and are used in connectivity dynamic programs on bounded-treewidth graphs. The mechanism is not new here. Metric corridor states instead combine by min-plus: a state vector (d) and an external offset vector (c) are observed through values such as \(\min_i(d_i+c_i)\), not through a linear-independence predicate. To transfer the method one would first need a representation of *all relevant min-plus completion behavior* by a bounded-dimensional linear pairing. Neither the cited theorem nor the existing CS3 hypotheses provide one.

## 3. Candidate theorem generation and bridge tests

| Candidate | Baseline and proposed change | Bridge test / strongest prior art | Disposition |
|---|---|---|---|
| **C1: compress every two-sided CS3 guard's joint distances to (O(r^3))** | General treewidth gives (O(r^4)) per constant-size guard; target one fewer radius power. | The LCA family has (O(k)) guards and guard vectors determine (A)-profiles. Conversely a guard has at most eight vertices, so the simple-tw3 conjecture itself implies its signature bound. The prior audit proves the two-way equivalence. | **Reject, Category B:** equivalent to the full open conjecture. |
| **C2: import matroid representatives for corridor states** | Replace a large set of partial corridor solutions by a small family preserving every completion. | Matroid theorem requires fixed-cardinality independent sets and linear extension tests. Distance profiles are min-plus and may have unrelated Pareto-optimal states; no linear representation or extension-equivalence proof is known. A universal claim over all guard contexts would again preserve all constant-landmark profiles and risk restating C1. | **Reject, Category A as currently stated / no bridge:** known theorem in new notation without a valid encoding. |
| **C3: extend outerplanar layer monotonicity to two-sided simple-tw3 corridors** | Use decomposition order plus two boundary adhesions to retain an interval-like partition of each BFS layer after edge deletions. | Must first define a canonical order on vertices in a branching decomposition component and prove distances in (G), not (H), are monotone or have bounded alternations. The simple-treewidth hypothesis supplies a planar host, but deleted edges alter geodesics and the host's layer order need not be a metric order in (G). No precise order-statistic survives the test. | **Reject for this cycle:** proof obligation not yet a lemma; no admissible counterexample to all such orders, but no invariant to prove. |
| **C4: turn detour accounting into a universal caterpillar schedule** | Use (N_t(e)=1[e\in P_t]+2b_t(e)) to charge temporary traversals to hub loads and obtain (O(D+W_{max})) rounds. | The identity is exact but aggregate. It neither attributes a detour to a specific exchange nor orders occupancy dependencies. A round bound also needs matching feasibility and precedence depth. Existing DAG only characterizes distance-tight schedules. | **Reject, Category C not met:** no schedule-construction lemma or charging invariant survived. |

The smallest tests were: (K_4) to check the missing common-boundary-order hypothesis; (P_4\subset K_4) to check host-distance transfer; a two-boundary min-plus state to check representative-set transfer; and the known double-star/caterpillar results to check whether distance accounting controls schedule order. Each test exposes a missing premise; none is an asymptotic refutation of the target conjecture.

## 4. Selection, attempted proof, and independent review

No candidate passed the required Category-C gate, so **none was admitted for a full proof attempt**. C3 looked most structurally aligned with the simple-treewidth gap, but after formalizing it the required “corridor order” is not specified by the decomposition: a two-attachment component can branch, and its partial-graph distance layers can differ from host layers. Making the lemma say “the guard signatures have (O(r^3)) possibilities” would simply restore C1, which is equivalent to the original conjecture. This is the exact reason for stopping rather than inventing a new name for CS3.

Independent review:

1. **LCA guards:** the count is (2|M^*|\leq4|A|), guard size is (2(t+1)), and separator coverage concerns paths in the measured graph. No distance bound follows without a separate profile-count theorem.
2. **Outerplanar layers:** each landmark contributes at most (2r+1) layers, and at most (2r+2) intervals per relevant layer; overlaying interval partitions gives additive counts. The proof relies on the common outer-face order.
3. **Matroid representatives:** the wedge/minor vector dimension is exactly \(\binom{p+q}{p}\); nonzero complementary pairing is precisely basis extension; linear dependence guarantees a retained extension. The conclusion preserves extension feasibility, not arbitrary numerical distance vectors.

No proof here depends on host distances equaling subgraph distances. No finite construction is used as an asymptotic lower bound. No theorem beyond the published results is claimed.

## 5. Final classification and research decision

**Classification: F — no substantive new mathematical result.** The work establishes an evidence-based methodology result: all shortlisted bridges were filtered by their preservation invariant before proof expansion. No bound improves the literature, no full open problem was solved, and no candidate theorem was sufficiently precise and independent to admit. Publication potential as a standalone mathematical contribution is low; this is a research-process audit, not a new proof technique.

Remaining mathematical barriers:

* For simple treewidth three, find a genuinely narrower corridor statement than arbitrary constant-landmark profile complexity, with a canonical structural restriction that survives edge deletion and does not merely imply the full conjecture; or attack the conjecture directly with a new invariant.
* For arbitrary-tree/caterpillar token swapping, construct an identity-preserving detour/precedence schedule or a schedule-independent asymptotic obstruction. The parity accounting and distance-tight DAG are insufficient.
* For any future representative-family transfer to distances, define a linear/gammoid object whose extension predicate exactly reproduces min-plus completion behavior, then prove the representation and size bound. This prerequisite is currently absent.

**Stop:** no successor task is created and no new proof cycle is started.

## Primary sources

* Beaudou et al., [*Profile and neighbourhood complexity of graphs excluding a minor and tree-structured graphs*](https://arxiv.org/abs/2501.08895v3), Lemma 15, Theorems 6–7, Conjecture 33.
* Joret and Rambaud, [*Neighborhood complexity of planar graphs*](https://doi.org/10.1007/s00493-024-00110-6), outerplanar/planar profile arguments and Theorem 36.
* Fomin, Lokshtanov, Panolan, and Saurabh, [*Efficient Computation of Representative Sets with Applications in Parameterized and Exact Algorithms*](https://arxiv.org/abs/1304.4626), Theorems 1 and 3.
* Fomin, Lokshtanov, Panolan, and Saurabh, [*Representative Sets of Product Families*](https://arxiv.org/abs/1402.3909), composition algorithms and bounded-treewidth connectivity applications.
* Prior repository records: [token-swapping detour accounting](parallel_token_swapping_caterpillar_distance_accounting_20261016.md), [bounded-(h) tree argument](parallel_token_swapping_bounded_h_caterpillar_20261016.md), [simple-treewidth-3 reconstruction](simple_treewidth3_profile_reconstruction_20261016.md), and [CS3 stress test](simple_treewidth3_CS3_stress_test_20261016.md).
