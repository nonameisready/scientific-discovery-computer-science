# CS3 corridor-signature stress test

**Decision: NO-GO on treating CS3 as an intermediate lemma.** With the source-standard LCA guards formed in a decomposition of the measured graph, CS3 is equivalent up to constants to the full simple-treewidth-3 profile conjecture. It is neither independently weaker nor a shortcut around that conjecture. No asymptotic counterexample or proof of the conjecture is established here.

## 1. Exact claim and definitions

All graphs are finite, simple, unweighted, and undirected. For a graph (G), vertex set (A\subseteq V(G)), and integer (r\geq 0), define
\[
 p_r^G(x,A)(a)=\operatorname{cap}_r(d_G(x,a)),\qquad
 \operatorname{cap}_r(d)=\begin{cases}d&d\leq r,\\+\infty&d>r.\end{cases}
\]
The profile complexity \(\mathrm{pc}_r(G,A)\) counts distinct such profiles except the all-\(+\infty\) profile, and \(\mathrm{pc}_r(G,k)=\max_{|A|=k}\mathrm{pc}_r(G,A)\).

A (t)-tree is built from (K_{t+1}) by repeatedly adding a vertex adjacent to the vertices of an existing (t)-clique. It is *simple* when each (t)-clique is used for at most one such insertion. A partial simple (t)-tree is any subgraph of a simple (t)-tree; (\operatorname{stw}(G)\leq t) means exactly this subgraph-containment property. In particular, a graph of ordinary treewidth three is not automatically a partial simple 3-tree.

The checked primary source states the conjecture: for each fixed (t\geq1), there is (C_t) such that every (G) with (\operatorname{stw}(G)\leq t), every (r,k\geq1), satisfies
\[
\mathrm{pc}_r(G,k)\leq C_t r^t k.
\]
At (t=3), the target is (O(r^3k)). The general treewidth theorem gives (O_t(r^{t+1}k)), hence (O(r^4k)) at width three; the outerplanar (t=2) result is (\mathrm{pc}_r(G,A)\leq1+(2r+2)^2|A|).

### The source-standard guards and the assigned regions

Use a width-at-most-3 tree decomposition ((T,(B_z))) of **(G)**, rooted at an arbitrary node. Such a decomposition is available for every (G\subseteq H) when (H) is a simple 3-tree: intersect each host bag with (V(G)). Edge deletion preserves the tree-decomposition axioms. The resulting bags need not be cliques, and no distance equality between (G) and (H) is assumed.

For each (a\in A), let (s_a) be the topmost node whose bag contains (a). Let (M=\{s_a:a\in A\}), and let (M^*\) be its LCA-closure (all LCAs of pairs of nodes in (M), including identical pairs). Then (|M^*|\leq2|A|), and each component of (T-M^*) has at most two neighbors in (M^*). For (b\in M^*\), let (p^*(b)) be the nearest strict ancestor of (b) in (M^*), or (b) if none exists. The source guard family is
\[
\mathcal S=\{B_b:b\in M^*\}\;\cup\;
\{B_b\cup B_{p^*(b)}:b\in M^*\}.
\]
It has at most (4|A|) members, each of size at most (8). The published lemma says each vertex has some guard in this family intersecting every (G)-path of length at most (r) from that vertex to (A).

The source does **not** assign a unique region (X_S) to each guard. For this audit, fix any ordering of \(\mathcal S\) and assign every vertex (x) to the first guard that has the stated path-hitting property for (x); call the resulting preimage (X_S\). The assignment may depend on (G,A,r). All arguments below hold for every such assignment and, in fact, for every subset (X_S\subseteq V(G)). If one instead builds guards from host bags, intersect them with (V(G)); absent host vertices are not distance coordinates in (G).

Thus the precise CS3 assertion under review is: there is an absolute (C) such that for every simple 3-tree (H), every subgraph (G\subseteq H), every (A\subseteq V(G)), every integer (r\geq1), every source-standard LCA guard (S\in\mathcal S), and every assignment region (X_S\subseteq V(G)),
\[
\left|\left\{(\operatorname{cap}_r(d_G(x,s)))_{s\in S}:x\in X_S\right\}\right|\leq C(r+2)^3.
\tag{CS3}
\]
The bound's constant must be uniform in (H,G,A,r,S), and the region assignment. The vector is measured in (G), not (H).

## 2. Main finding: CS3 is equivalent to the target conjecture

This equivalence is the substantive result of the cycle. In particular, counting local signatures is not an easier surrogate: because (S\subseteq V(G)), each such vector is literally a truncated distance profile with landmark set (S).

### Conjecture implies CS3

Assume the simple-treewidth-3 conjecture: there is (C_3) such that (\mathrm{pc}_r(G,q)\leq C_3r^3q) for every (G) with (\operatorname{stw}(G)\leq3), every (q\geq1), and (r\geq1). Fix any guard (S\subseteq V(G)), put (q=|S|\leq8), and consider any (X_S\subseteq V(G)). Its signature set is a subset of the full set of profiles on (S). At most one signature is all (+\infty), so
\[
|\{\text{signatures on }X_S\}|\leq \mathrm{pc}_r(G,S)+1
\leq 8C_3r^3+1\leq(8C_3+1)r^3.
\]
If (S=\varnothing), there is only the single empty vector, also satisfying the bound. This argument does not use that (S) is a guard or an LCA set; it holds for every set of at most eight vertices. It proves CS3 with an absolute constant.

### CS3 implies the conjecture

Assume CS3 with constant (C). For any (G\subseteq H), (A\subseteq V(G)), and (r\geq1), take the source-standard family (\mathcal S), with (|\mathcal S|\leq4|A|), and assign each vertex to a valid guard. For a vertex (x\in X_S) and landmark (a\in A):

* If (d_G(x,a)\leq r), every shortest (x)-to-(a) path has length at most (r), so the guard property makes it meet (S). For a point (s\in S) on that path, (d_G(x,a)=d_G(x,s)+d_G(s,a)). Conversely the triangle inequality gives (d_G(x,a)\leq d_G(x,s)+d_G(s,a)) for every (s\). Therefore
  \[
  d_G(x,a)=\min_{s\in S}(d_G(x,s)+d_G(s,a)).
  \]
* If (d_G(x,a)>r), no sum in that minimum can be at most (r), since such a sum would give an (x)-to-(a) walk of length at most (r).

Thus the complete truncated profile on (A) is determined by the signature to (S), with all distances taken in (G). This handles tied shortest paths because the guard hits **every** short path, not one selected geodesic. A profile with a finite coordinate has a finite signature coordinate at its assigned guard; the all-infinite profile is excluded by definition. Consequently
\[
\mathrm{pc}_r(G,A)\leq\sum_{S\in\mathcal S}|\{\text{signatures on }X_S\}|
\leq4C|A|(r+2)^3=O(r^3|A|).
\]
Taking the maximum over (|A|=k) proves the (t=3) conjecture. Constants are uniform, since (r+2\leq3r) for (r\geq1).

Therefore, under the source-standard guard construction and the explicit region assignment above, **CS3 holds if and only if the simple-treewidth-3 profile conjecture holds, up to absolute multiplicative constants**. In one direction the conjecture yields a bound for arbitrary constant-size landmark sets, not merely corridors. In the other, the guard implication is precisely the standard route from CS3 to the conjecture.

## 3. Local signatures can overcount the target profiles

Different guard signatures can encode the same profile on the original landmark set. Here is an example where the guard itself is a member of a source-standard LCA family.

Let (G) be the four-vertex tree with edges (ac,cx,cy), and let (A=\{a,c\}). Use the width-2 decomposition with adjacent bags (B_0=\{c,y\}) and (B_1=\{a,c,x\}), rooted at (B_0). The topmost bag nodes of (a,c) are respectively (B_1,B_0), so the LCA closure contains both nodes. The source family therefore includes the bag guard (S=B_1=\{a,c,x\}). It is a valid guard for both (x) and (y), because every path from either vertex to either member of (A) contains (a) or (c), both in (S).

For every (r\geq2), (x) and (y) have the same (A)-profile ((2,1)), but their signatures to (S), ordered as ((a,c,x)), are ((2,1,0)) and ((2,1,2)). This graph is a subgraph of the simple 3-tree (K_4) on ({a,c,x,y}). The example proves only that local signature count can be a strict overcount of profiles to (A); it is not an asymptotic counterexample to CS3 or to the conjecture.

The converse asymptotic distinction requested in the task has a sharp answer: an \(\Omega(r^4)\) count of signatures to an actual guard (S\subseteq V(G)) with (|S|\leq8) cannot coexist with the conjectured bound. Those signatures themselves are \(\Omega(r^4)\) profiles on the at-most-eight-element landmark set (S), violating (\mathrm{pc}_r(G,8)=O(r^3)\). A putative construction of this kind would refute the main conjecture, not merely expose an inefficient guard encoding.

## 4. Corridor geometry and attempted refutation

The LCA closure cuts the decomposition tree into components with at most two closure-node attachments. A vertex model wholly inside such a component is guarded by the bag at one boundary or the union of the bags at its two boundaries. This is the source of the one-/two-sided corridor language. It is a statement about separators in (G), not about a geometric embedding of a clique-tree corridor in (H). Edge deletion can make distances among vertices in either boundary bag arbitrarily larger than their host distances.

The t=3 lower construction of Joret–Rambaud has \(\Omega(r^4)\) profiles on a constant number of landmarks for ordinary treewidth three, but it is not eligible for CS3. For (t=3), their central coordinate tree has vertices ((x_0,x_1,x_2,x_3)\in[0,\ell-1]^4), with parent obtained by decrementing the last nonzero coordinate; the terminal attachment paths in their construction yield four coordinates that are injectively recovered from distances. For \(\ell\geq3\), take the spine
\(P=\{(j,0,0,0):0\leq j<\ell\}\)
and disjoint descendant branch sets (B_j) rooted at ((j,1,0,0)), for (j=0,1,2). Each (B_j) contains attachment endpoints for both terminals (a_2,a_3), at ((j,\ell-1,0,0)) and ((j,\ell-1,\ell-1,0)). The spine has an edge to each (B_j). Join a connected branch set containing (a_2) to the three (B_j) by the three internally disjoint attachment paths from (a_2), and analogously for (a_3). These six pairwise disjoint connected branch sets have all nine cross-edges, giving a (K_{3,3}) minor. The theorem's divisibility condition gives (ell=r/8\geq4) for positive admissible (r), so the three branch sets exist. Every simple 3-tree is planar: each insertion uses a previously unused 3-clique, which remains a facial triangle until used, and insertion into that face preserves planarity. Hence every partial simple 3-tree is planar, whereas this lower-bound family is not. It cannot refute CS3.

The source provides a planar lower bound \(\Omega(r^3)\) (its treewidth-2 instance) and a planar upper bound \(O(r^4)\), so it leaves room at the exponent relevant to CS3. No admissible \(\Omega(r^4)\) family was produced. The absence of one is not evidence that CS3 is true.

## 5. Adversarial review and classification

| Statement | Classification | Reason |
|---|---|---|
| The source-standard LCA family has at most (4|A|) sets of size at most 8 for width 3 | Previously published theorem | Beaudou et al., Lemma 15; it applies to a tree decomposition of (G). |
| Guard signature determines a truncated (A)-profile in the same graph | Fully proved elementary implication | Uses global short-path hitting and (G)-distances; ties and longer routes are covered above. |
| Main stw-3 conjecture implies CS3 | Fully proved conditional implication | A signature is a profile on (S), with at most eight landmarks. |
| CS3 implies the main stw-3 conjecture | Fully proved conditional implication | Apply the published (O(k)) LCA guard family and profile-determination formula. |
| CS3 is a strictly weaker or asymptotically easier intermediate target | Refuted | It is equivalent to the target conjecture up to constants. |
| Local signatures can differ while the target (A)-profiles agree | Fully proved finite example | Four-vertex tree and standard LCA bag above. |
| Joret–Rambaud's treewidth-3 lower graph refutes CS3 | Refuted for that construction | It contains a (K_{3,3}) minor and is not planar/simple-tw3. |
| CS3 or the main simple-tw3 conjecture | Unresolved | No proof or eligible asymptotic counterexample is established. |

Independent checks: guards are built from bags of a decomposition of (G), not by transferring host distances; edge deletion preserves the decomposition but not distances. The signature-to-profile identity uses all short paths. The finite example's decomposition, LCA closure, guard membership, distances, and host (K_4) were checked explicitly. The lower construction is outside the class by a branch-set certificate, not merely by a failed host embedding.

## 6. Prior-art and publication assessment

Beaudou et al. explicitly state the simple-treewidth conjecture, prove the general treewidth exponent (t+1), give the outerplanar (r^2k) theorem, and provide the (O(k))-guard/size-(2(t+1)) LCA construction. Joret–Rambaud give the matching general-treewidth lower exponent and the planar (\Omega(r^3)) lower / (O(r^4)) upper gap. The source material therefore establishes the setting and the exact unresolved exponent gap. This cycle adds a rigorous scope correction: the proposed local bound is not a new intermediate structural principle but a reformulation equivalent to the conjecture.

That equivalence and the finite overcount example are useful research-direction corrections, but are elementary consequences of the definitions and guard lemma. They have low standalone publication value. A meaningful next proof obligation would have to be genuinely more structured than “count every signature to a constant-size guard”: for example, prove a corridor-specific compression of only those guard signatures that can induce distinct profiles on the original (A), with a bound that does **not** already imply the conjecture for arbitrary constant landmark sets. The smallest open obstacle remains the partial-graph, two-boundary case where deleting host edges removes within-bag distance correlations. No successor is admitted in this bounded cycle.

## 7. Final decision

Outcome **D** applies in a precise sense: CS3 is mathematically coherent, but too strong to serve as a useful independent intermediate statement because it is equivalent to the full (t=3) conjecture. It is not refuted. The guard family exists by the cited theorem; the proposed signature count is exactly the missing exponent improvement. The source-stated conjecture remains unresolved in the checked primary text. The general \(\Omega(r^4)\) treewidth lower construction does not satisfy simple treewidth 3; the eligible planar lower bound is only \(\Omega(r^3)\). No new asymptotic structural lemma was proved. **NO-GO** on a theorem or novelty claim; stop this direction rather than enqueue a cosmetically renamed signature task.

## Sources

* Beaudou et al., [*Profile and neighbourhood complexity of graphs excluding a minor and tree-structured graphs*](https://arxiv.org/abs/2501.08895v3), especially Definitions 1–3, Lemmas 13–15, Theorems 6–7, and Conjecture 33.
* Joret and Rambaud, [*Neighborhood complexity of planar graphs*](https://doi.org/10.1007/s00493-024-00110-6), also [arXiv:2302.12633v2](https://arxiv.org/abs/2302.12633v2), especially Theorem 36 and its proof.
