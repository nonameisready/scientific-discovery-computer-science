# Simple treewidth 3 and truncated distance-profile complexity

**Bounded-cycle outcome: NO-GO on the main conjecture; one proved host-only structural corollary.** This note reconstructs the primary sources, corrects the scope of the treewidth lower bound, and records why the proposed guard route remains unresolved for proper subgraphs of simple 3-trees. No experiment was run and no asymptotic counterexample to the simple-treewidth conjecture was found.

## 1. Definitions and exact target

All graphs in the two papers are finite, simple, undirected, and unweighted. For vertices `u,v`, `dist_G(u,v)` is shortest-path distance (infinity across components). For an integer `r>=0`, write
\[
\operatorname{cap}_r(d)=\begin{cases}d&d\leq r,\\+\infty&d>r.\end{cases}
\]
For `A subset V(G)`, the `r`-profile of `v` is the function `p_r(v,A)(a)=cap_r(dist_G(v,a))`. The quantity `pc_r(G,A)` counts distinct such profiles except the all-infinity profile, and `pc_r(G,k)=max_{|A|=k} pc_r(G,A)`. Thus `k` is the number of landmarks, while `r` is the truncation radius. A statement `O_t(...)` permits a multiplicative constant depending on fixed `t`, not on `r,k,G`.

A `t`-tree starts from `K_{t+1}` and repeatedly adds a vertex adjacent to all vertices of an existing `t`-clique. A *simple* `t`-tree additionally requires that no `t`-clique is used to attach two different added vertices. The simple treewidth `stw(G)` is the least `t` such that `G` is a **subgraph** of a simple `t`-tree. Ordinary treewidth is the least `t` such that `G` is a subgraph of a (not necessarily simple) `t`-tree, hence `tw(G)<=stw(G)`. At `t=1`, simple-treewidth graphs are disjoint unions of paths; at `t=2`, they are exactly outerplanar graphs. The current Beaudou et al. text states the conjecture
\[
\forall t\geq1\;\exists C_t<\infty\;\forall r,k\geq1\;\forall G\;(\operatorname{stw}(G)\leq t\Rightarrow \mathrm{pc}_r(G,k)\leq C_t r^t k).
\]
For `t=3`, the target is `O(r^3 k)`. It is a claim about **all subgraphs** of simple 3-trees, not only maximal simple 3-trees.

## 2. Primary-source reconstruction and exponent comparison

### Joret–Rambaud (Combinatorica 44, 2024)

The full paper [*Neighborhood complexity of planar graphs*](https://doi.org/10.1007/s00493-024-00110-6), also available as [arXiv:2302.12633v2](https://arxiv.org/abs/2302.12633v2), studies both neighbourhood and profile complexity. Its Theorem 5 gives, for treewidth at most (t),
\[
\mathrm{pc}_r(G,k)=O\!\left((t+1)\binom{r+t}{t}r^t k\right)=O_t(r^{2t}k),
\]
and gives (O(r^4k)) for planar profile complexity. The paper also gives a guarding-set/minor-free route: for a (K_h)-minor-free graph and a landmark set (B), profiles are bounded by ((r+1)^{h-1}|B|^{h-1}) (its Theorem 16 in the later Beaudou paper's citation of the result). Joret–Rambaud Theorem 36 constructs, for each fixed (t) and arbitrarily large admissible (r), a graph of treewidth at most (t) with Ω_t(r^{t+1}) profiles on (t+1) landmarks; disjoint copies give the corresponding linear dependence on (k). Their Corollary 37 converts this into a neighbourhood-complexity lower bound Ω_t(r^t k), not a profile lower bound of that exponent.

### Beaudou et al. (arXiv:2501.08895v3)

The full [v3 text](https://arxiv.org/html/2501.08895) defines the same truncated-distance profiles. Theorem 6 states
\[
\mathrm{pc}_r(G,k)=O(t^{O(t)}r^{t+1}k)\quad\text{when }\operatorname{tw}(G)\leq t.
\]
The proof supplies the explicit bound, for every landmark set (A),
\[
\mathrm{pc}_r(G,A)\leq 2^{t+3}(r+1)^{t+1}(t+1)^{t+1}|A|.
\]
This improves Joret–Rambaud's treewidth exponent from (2t) to (t+1), and matches their Ω_t(r^{t+1}k) lower exponent for general treewidth, up to constants depending on (t). At (t=3), the established general-treewidth bound is (O(r^4k)).

The source's Theorem 7 gives the stronger outerplanar bound
\[
\mathrm{pc}_r(G,A)\leq1+(2r+2)^2|A|,
\]
and says it is asymptotically tight even for trees. Its proof roots BFS layers at a landmark (a_1), orders each layer by the outer-face circular order, and uses a cited monotonicity lemma: relative to a closest point on a layer, distance to a fixed landmark is monotone along each of the two circular arcs. Each landmark is within radius (r) of at most (2r+1) layers, and its distance partitions a layer into at most (2r+2) intervals. Summing the layer/landmark incidences yields the (O(r^2k)) count. The source-specific ingredient is the outerplanar boundary order and its two-arc monotonicity; the paper does not provide an analogous ordering for simple 3-trees.

### Why the general proof has exponent four at (t=3)

The Beaudou–Bok–Foucaud–Quiroz–Raymond proof has two independent ingredients:

1. Its LCA-closure construction gives at most (4|A|) guards, each of size at most (2(t+1)). A tree minus the LCA closure has components with at most two attachment nodes; bags at a closure node and its nearest closure ancestor form the guards. This is a statement about *guard-family count* and *guard cardinality*.
2. The Joret–Rambaud minor-free profile estimate applied to a guard of size (p) gives at most ((r+1)^{t+1}p^{t+1}) profiles when (G) has treewidth (t) (it excludes (K_{t+2})). The guarding lemma multiplies this per-guard count by the number of guards.

Substituting (p=2(t+1)) and (4|A|) guards produces ((r+1)^{t+1}|A|) times a (t)-dependent factor. At (t=3), the lost power is precisely the (r^4) dependence of the general minor-free profile bound for a constant-size guard. It is not caused by having (O(k)) guards, nor by confusing guard cardinality with decomposition adhesion. The outerplanar proof avoids this per-guard enumeration by layer ordering and monotonicity. A simple-treewidth-3 proof would need some different control of the relevant profile/signature families.

## 3. Does the known treewidth lower construction already refute the stw-3 target?

No. The t=3 instance of Joret–Rambaud Theorem 36 has treewidth at most 3 and Ω(r^4) profiles for a constant-size landmark set, but it is not a simple-treewidth-3 graph.

Here is a direct obstruction, reconstructed from their construction. Put \(\ell=r/(2(t+1))\); for t=3, the theorem's divisibility condition makes \(\ell\geq4\) for its first positive admissible radius. The central tree has vertices \((x_0,x_1,x_2,x_3)\in[0,\ell-1]^4\), with parent obtained by decrementing the last nonzero coordinate. There are terminals \(a_0=(0,0,0,0),a_1,a_2,a_3\). For each \(i=1,2,3\), \(a_i\) is connected by internally disjoint paths of length \(r/2\) to its construction's attachment nodes: for i=1, \((\ell-1,0,0,0)\); for i=2, \((x_0,\ell-1,0,0)\) for each \(x_0\); and for i=3, \((x_0,x_1,\ell-1,0)\) for each \((x_0,x_1)\). (These attachment indices are also the ones yielding the paper's displayed distance coordinates.)

For j=0,1,2, let \(B_j\) be the tree-subtree rooted at \((j,1,0,0)\). These three branch sets are pairwise disjoint and avoid the spine \(P=\{(j,0,0,0):0\leq j<\ell\}\). Each \(B_j\) contains an attachment of \(a_2\), at \((j,\ell-1,0,0)\), and an attachment of \(a_3\), at \((j,\ell-1,\ell-1,0)\). The spine branch set contains \(a_0\) and has an edge into each \(B_j\). Expand the left branch set for each of \(a_2,a_3\) to include the interiors of its three selected attachment paths (one to each \(B_j\)); within each terminal these paths are internally disjoint, and the two terminals' path interiors are disjoint from each other, the spine, and all \(B_j\). The resulting six connected, pairwise disjoint branch sets have every cross-edge of \(K_{3,3}\), so the construction is nonplanar.

Every simple 3-tree is planar: start with the planar (K_4), and insert each new vertex into a facial triangle. Inductively, unused triangles are facial; a triangle ceases to be facial exactly when it is used, and the simple condition forbids using it again. Hence the construction cannot be a subgraph of a simple 3-tree, since subgraphs of planar graphs are planar. This is a specific structural reason the known Ω(r^4) lower bound does **not** disprove the simple-treewidth-3 conjecture. The argument does not furnish a new lower bound for simple treewidth.

## 4. Three-vertex guard proposal: implication is valid; existence remains open

For a vertex set S in G, suppose every path from v to a landmark in A of length at most r meets S. Then the full truncated profile of v on A is determined by its distances to S, *measured in the same graph G*. For each landmark a, if dist_G(v,a)<=r, a shortest path has length at most r and meets S at some s, so
\[
d_G(v,a)=\min_{s\in S}(d_G(v,s)+d_G(s,a)).
\]
The right side cannot be smaller than (d_G(v,a)), by the triangle inequality for shortest-path distance, and the hit geodesic supplies equality. If (d_G(v,a)>r), no (s\in S) can make the sum at most (r), since concatenating the two paths would give a (v\)-to-(a) walk of length at most (r). Thus the truncated coordinate is (+\infty). This handles multiple equal geodesics (the guard hits each by hypothesis), short paths versus longer unrestricted paths, and disconnected pairs.

Paths may leave and re-enter a decomposition region: that causes no issue for this implication, provided the proposed (S) really hits every short path in the **whole graph**. A separator argument confined to paths inside a region is insufficient unless it proves that global guard property.

If there were at most (Ck) such guards, each of size at most 3, then a guard-distance vector has at most ((r+2)^3) values, since each coordinate lies in \(\{0,1,\ldots,r,+\infty\}\). Assign each non-all-infinite vertex profile to one valid guard. This gives \(\mathrm{pc}_r(G,A)\leq Ck(r+2)^3=O(r^3k)\) for (r\geq1). So the proposed implication is sound. The existence claim—an (O(k)) family of size-three global guards for every simple-treewidth-3 subgraph, (A,r)—is **not proved or refuted** here.

The source's general LCA construction gives (O(k)) guards of size at most 8 for treewidth 3, not size 3. In a host simple 3-tree, maximal-clique bags are (K_4)'s, and a component of the LCA-closure complement can have two distinct attachment regions. Taking their union can require up to eight vertices. There is no source theorem making this union reducible to a 3-vertex separator. Equal shortest paths and two-sided routes must be handled in the full (G), not inferred from one chosen path or from a host completion.

### Completion does not preserve profiles

Simple treewidth is a subgraph-containment condition, but profiles use distances in G. Adding host edges can strictly shorten distances. For example, let G be P4 on v1,v2,v3,v4, and complete it to H=K4, a simple 3-tree. With landmarks A={v1,v4}, the radius-3 profile of v1 in G is (0,3), while in H it is (0,1). Thus an upper bound for the host's profiles cannot simply be transferred to its subgraph. A guard that hits every short H-path also hits every short G-path, since G is a subgraph of H; however, the profile-determination formula must use distances in G, so numerical distance signatures from H do not transfer.

## 5. One proved restricted signature lemma and the attempted extension

### Lemma (maximal simple 3-tree hosts only)

If (H) is a simple 3-tree, then for every (A\subseteq V(H)) and (r\geq0),
\[
\mathrm{pc}_r(H,A)\leq 4|A|\bigl(16(r+1)+1\bigr)^2.
\]

**Proof.** Use the maximal-clique tree of (H), whose bags are 4-cliques. Apply the cited LCA-closure guarding construction to obtain at most (4|A|) guard sets, each either one bag or the union of two bags. For a clique bag (Q) of size four, all distances from any fixed (v) to members of (Q) differ by at most one: if (q) minimizes distance, every (q'\in Q) is adjacent to (q), so (d(v,q)\leq d(v,q')\leq d(v,q)+1). For truncated distances, the minimum can be any of (0,ldots,r), with at most (2^4=16) coordinate patterns at that minimum, or the all-infinite pattern. Hence there are at most (16(r+1)+1) vectors on one bag. A guard uses at most two bags, so at most the square of this number of vectors. The guard property determines the profile on (A) from this vector, and multiplying by the number of guards proves the bound. \(\square\)

This is a host-only, elementary consequence of LCA guards plus clique distance geometry. It is not a theorem for (G\subseteq H). Deleting edges destroys the within-bag distance-difference bound: in the (P_4\subset K_4) example, distances from (v_1) across the host bag are (0,1,2,3), not two adjacent values. That example refutes only the attempted transfer step, not any (O(r^3k)) bound for the whole subgraph class.

### Candidate corridor-signature lemma (not proved)

The narrow structural target suggested by the exponent gap is the following. Let (H) be a simple 3-tree with clique tree (T), let (G\subseteq H), let (A\subseteq V(G)), and form the standard (O(|A|)) LCA guards from the topmost clique bags of (A). For each guard (S), let (X_S) be the vertices assigned to it by the guarding construction. Is there an absolute constant (C) such that, for every (r\geq1),
\[
\left|\left\{(\operatorname{cap}_r(d_G(x,s)))_{s\in S}:x\in X_S\right\}\right|\leq C(r+2)^3
\tag{CS3}
\]
for all such (H,G,A,S)? This is a local joint-signature statement, not an interface-table/output-graph equivalence. Since the guards are (O(k)) and their distance vectors determine profiles, CS3 would imply the conjectured (O(r^3k)) bound. It permits up to eight coordinates but asks for a genuine rank/correlation loss under the simple-host structure.

**Adversarial checks.** The general treewidth-(3) Ω(r^4) construction would refute CS3 if source-eligible; it is excluded by the explicit (K_{3,3}) minor above. The (P_4\subset K_4) example refutes the tempting proof that host-clique adjacency alone makes coordinates nearly equal, but its four vertices do not violate an (O(r^3)) counting statement. One-sided and two-sided regions, landmarks on both sides, equal geodesics, and paths that leave and re-enter the region must all be measured in (G); none can be dismissed using distances in (H). No asymptotic simple-treewidth-3 counterexample to CS3 was found.

**Exact blocker.** The LCA construction controls how many guards are needed but gives no bound on the number of (G)-distance vectors from vertices in a two-sided region to the union of its adhesion bags. The host cliques correlate coordinates in (H); omitted edges may make the corresponding distances in (G) independent. The needed new fact is a uniform (O(r^3)) count of these *joint partial-graph metrics*, or a different global structural argument. The existing sources do not provide it. CS3 may itself be false; no proof or asymptotic counterexample is established.

## 6. Independent adversarial review and claim classification

| Claim | Classification | Scope / reason |
|---|---|---|
| Beaudou et al. treewidth bound (O_t(r^{t+1}k)) | Published theorem | All graphs of ordinary treewidth at most fixed (t). |
| Outerplanar bound (1+(2r+2)^2k) | Published theorem | Outerplanar graphs; proof uses circular BFS-layer monotonicity. |
| Simple-treewidth conjecture (O_t(r^t k)) | Explicit unresolved conjecture in checked source | The source proves it only for (t=1,2). |
| Joret–Rambaud lower graph at (t=3) refutes the simple-treewidth-3 target | Disproved | The construction contains a (K_{3,3}) minor and is nonplanar; every simple 3-tree is planar. |
| A valid size-(p) guard determines a truncated profile from (p) distances | Proven elementary implication | Requires the guard to hit all short paths globally and distances to be measured in the same graph. |
| (O(k)) guards of size at most three exist for every stw-3 graph | Unresolved; not a false conjecture on evidence here | The treewidth-3 source construction only yields guards of size at most eight. No valid counterexample to every possible guard family was found. |
| Maximal simple 3-tree host bound (O(r^2k)) above | Proven restricted lemma; novelty low | Does not extend to subgraphs by completion. It is an elementary LCA/clique-signature corollary. |
| Corridor-signature statement CS3 | Plausible but unproved conjectural lemma | Would imply the desired bound through the standard guards; finite examples and the general-tw lower construction do not settle it. |
| Main stw-3 conjecture disproved | No | No source-eligible asymptotic counterexample or full proof was found. |

The maximal-host lemma's proof uses the LCA guard theorem exactly within its scope (treewidth 3) and clique bags only for the *host's* own distances. The independent audit found no transfer to partial graphs. The (K_{3,3}) minor model uses three disjoint subtrees and three distinct left branch sets; no terminal/path is treated as a single branch on both sides. Lower-bound asymptotics are only those in the primary construction, not extrapolated from finite tests.

## 7. Novelty, publication value, and decision

The main target remains explicitly stated as a conjecture in the checked v3 primary text, with (t=1,2) known and (t=3) the first open case. This is evidence of source-level unresolved status, not an exhaustive forward-citation proof through 2026. There is a source metadata anomaly: the arXiv HTML header labels the manuscript v3 dated 13 Dec 2025, while its body says “Date: August 24, 2026.” This note cites the version currently served and does not infer when that body date was introduced.

No nontrivial theorem for all simple-treewidth-3 subgraphs was proved. The host-only (O(r^2k)) lemma is correct but follows from a familiar guarding-set construction and clique-distance counting; without a transfer to partial graphs, its independent publication value is low. The guard-existence claim remains unresolved, not validated as plausible by evidence and not falsified. The treewidth lower bound does not conflict with the conjecture because its t=3 construction is nonplanar.

**Decision: NO-GO for claiming progress on the main conjecture; bounded cycle complete.** Preserve CS3 as one precise, unproved obligation rather than enqueueing another task. The decisive next mathematical obligation, if separately authorized later, is either (i) prove CS3 for all standard LCA regions in partial simple 3-tree subgraphs, including two-sided corridors, or (ii) give an asymptotic (G\subseteq H) family violating it. A proof of three-vertex global guards is an alternative but stronger route. The present work does not justify a publication claim.

## Sources

* Beaudou, Bok, Foucaud, Quiroz, Raymond, [*Profile and neighbourhood complexity of graphs excluding a minor and tree-structured graphs*](https://arxiv.org/abs/2501.08895v3), especially Definitions 1–3, Lemmas 13–15, Theorems 6–7, Theorem 16, and Conjecture 33.
* Joret and Rambaud, [*Neighborhood complexity of planar graphs*](https://doi.org/10.1007/s00493-024-00110-6), [arXiv v2](https://arxiv.org/abs/2302.12633v2), especially Theorem 5, Theorem 16, Theorem 36, Corollary 37, and the outerplanar/planar profile arguments.
* Repository screening context: [`ORIGINAL_RESEARCH_OPPORTUNITY_SCAN.md`](ORIGINAL_RESEARCH_OPPORTUNITY_SCAN.md). Its former claim that the treewidth-3 lower construction's simple-treewidth status was simply unknown is resolved for the cited construction here by the explicit (K_{3,3})-minor model.
