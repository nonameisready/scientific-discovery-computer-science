# Exact interfaces for two-terminal series-parallel Zero Extension networks

Task: `THEORY-ZEROEXT-SERIES-PARALLEL-INTERFACE-003`  
Audit date: 2026-10-15

This is a mathematical proof audit only. It uses no experiment, network search,
or supervisor start. It preserves the preceding Multiway-Cut feasibility
theorem and keeps contraction-only statements separate from statements about
arbitrary terminal-preserving sparsifiers.

## 1. Objective and conventions

Let \(G=(V,E)\) be a finite undirected multigraph. Parallel edges are separate
objective terms and loops have zero cost and zero crossing count. Let \(S\subseteq
V\) be the terminals, let \((D,\mu)\) be a finite metric, and let
(\tau:S\to D) be injective. For a labeling (phi:V\to D), write

\[
C_G(\phi)=\sum_{uv\in E}\mu(\phi(u),\phi(v)),\qquad
X_G(\phi)=|\{uv\in E:\phi(u)\ne\phi(v)\}|.
\]

The restricted objective is

\[
\operatorname{OPT}_{G,k}(\mu,\tau)=
\min\{C_G(\phi):\phi|_S=\tau, X_G(\phi)\le k\},
\]

with value \(+\infty\) when the feasible set is empty. The predecessor result
established, in both directions, that this value is finite exactly when the
terminal Multiway Cut number is at most \(k\). That fact is used below as a
feasibility gate; no infeasible instance is used as a lower-bound witness.

A two-terminal network is a graph \(N\) with distinguished boundary vertices
\((s_N,t_N)\). A series-parallel network is generated from one-edge networks by
series composition (identifying the right boundary of one network with the
left boundary of the next) and parallel composition (identifying both left
boundaries and both right boundaries). The two boundary vertices are not
implicitly terminals of the ambient instance; their labels are interface
arguments.

## 2. The exact general interface

The correct interface must retain both cost and crossing budget. Suppose that
(R_N) is the set of terminals strictly internal to (N), disjoint from its
two boundary vertices. For a fixed assignment (\rho:R_N\to D), define

\[
 I_N(q;a,b,\rho)=
 \min\{C_N(\phi):
 \phi(s_N)=a,\ \phi(t_N)=b,\ \phi|_{R_N}=\rho,
 \ X_N(\phi)\le q\}.
\]

Here (q\in\{0,1,\ldots,|E(N)|\}), and the value is (+infty) if no
labeling exists. If a boundary is itself an ambient terminal, its prescribed
label is simply fixed in the corresponding boundary argument. The interface
is therefore a finite table for a fixed finite \(D\), but it is a function of
the actual metric labels, not a label-free list of pairwise signatures.

The use of \(\le q\), rather than exactly \(q\), is essential: composition then
matches the global upper crossing budget without inventing crossings.

## 3. Exact series composition

Let (N=A\circ B), where (x=t_A=s_B) is the glued vertex. Assume first
that (x) is not an ambient terminal and that the internal terminal sets are
disjoint. Then

\[
 I_{A\circ B}(q;a,b,\rho_A\cup\rho_B)
 =
 \min_{\substack{z\in D\\q_A+q_B\le q}}
 \left[
 I_A(q_A;a,z,\rho_A)+
 I_B(q_B;z,b,\rho_B)
 \right].
 \tag{S}
\]

If (x) is an ambient terminal with prescribed label (z_0), the minimum
over (z) is replaced by the single value (z=z_0). If (x) is an internal
terminal of one of the modules, its prescribed label is likewise used and is
not minimized over.

### Proof of (S), forward direction

Take any feasible labeling (phi) of (A\circ B). Restrict it to (A) and
(B). The restrictions agree at (x), say with label (z). Since the edge
sets of the two modules are disjoint,

\[
 C_{A\circ B}(\phi)=C_A(\phi|_A)+C_B(\phi|_B),
\quad
 X_{A\circ B}(\phi)=X_A(\phi|_A)+X_B(\phi|_B).
\]

Thus the pair ((z,q_A,q_B)), with (q_i=X_i(phi|_i)), is among the
competitors on the right-hand side, and the right-hand side is no larger than
the cost of (phi). Taking the minimum over (phi) gives the inequality
“right side (le I_{A\circ B})”.

### Proof of (S), reverse direction

Choose a minimizing triple (z,q_A,q_B) and minimizing labelings for the two
interfaces. Identify their copies of (x). They agree there by construction,
and their internal terminal assignments agree with (\rho_A\cup\rho_B).
The glued labeling has cost equal to the sum and crossing count equal to the
sum, hence at most (q). It is a feasible labeling of (A\circ B), proving
“(I_{A\circ B}le) right side”. The (+infty) cases obey the same argument.

Thus series composition is exact for every finite metric, every prescribed
terminal assignment, and every crossing budget. The unavoidable operation is
the minimization over the glued label (z) when the glue is nonterminal.

## 4. Exact parallel composition

Let (N=A\parallel B), with the two modules sharing only the boundary
vertices (s,t). Assume their internal terminal sets are disjoint. Then

\[
 I_{A\parallel B}(q;a,b,\rho_A\cup\rho_B)
 =
 \min_{q_A+q_B\le q}
 \left[
 I_A(q_A;a,b,\rho_A)+
 I_B(q_B;a,b,\rho_B)
 \right].
 \tag{P}
\]

### Proof of (P), both directions

Restricting any feasible labeling of the parallel composition to the two
edge-disjoint modules gives the same boundary labels (a,b), additive costs,
and additive crossing counts. This proves that the right side is no larger
than the global optimum. Conversely, two interface minimizers already agree on
both identified boundary vertices, so they glue without any further choice.
Their costs and crossing counts add, giving a feasible global labeling. This
proves the opposite inequality and establishes (P), including infeasible
values.

The parallel law is a min-plus convolution in the crossing coordinate. Unlike
series composition, it introduces no new label minimization.

## 5. A closed scalar interface in the terminal-free case

When (R_N=\varnothing), the exact interface collapses further. Let

\[
 \lambda_N=\min\{|C|: C\subseteq E(N), s_N,t_N\text{ disconnected in }N-C\}
\]

be the two-terminal edge connectivity, with multiplicity.

**Lemma.** For every finite metric and (a,b\in D),

\[
 I_N(q;a,b,\varnothing)=
 \begin{cases}
 0, & a=b,\\
 \lambda_N\mu(a,b), & a\ne b\text{ and }q\ge\lambda_N,\\
 +\infty, & a\ne b\text{ and }q<\lambda_N.
 \end{cases}
 \tag{T}
\]

**Proof.** If (a\ne b), the crossing edges of any labeling disconnect (s_N)
from (t_N), so there are at least (lambda_N) of them. For the cost lower
bound, put (L=\mu(a,b)) and (d(v)=\mu(a,\phi(v))). For every edge,

\[
 \mu(\phi(u),\phi(v))\ge |d(u)-d(v)|
\]

by the triangle inequality. For each (r\in(0,L)), the threshold set
(U_r=\{v:d(v)\le r\}) contains (s_N) and excludes (t_N), so its edge
boundary has size at least (lambda_N). The layer-cake identity gives

\[
 \sum_{uv\in E}|d(u)-d(v)|
 =\int_0^L |\delta(U_r)|\,dr
 \ge\lambda_N L.
\]

Thus every labeling costs at least (lambda_N\mu(a,b)). A minimum
(s_N)-(t_N) cut, labeled (a) on one side and (b) on the other, attains
that cost and has exactly (lambda_N) crossings. The case (a=b) is the
constant labeling. This proves (T).

For terminal-free modules, the interface compositions reduce to

\[
 \lambda_{A\circ B}=\min(\lambda_A,\lambda_B),
 \qquad
 \lambda_{A\parallel B}=\lambda_A+\lambda_B,
\]

which is the standard series/parallel cut recursion. Hence arbitrary finite
series-parallel graphs with only their two outer terminals have an exact,
label-independent scalar interface, including the non-cactus theta graph
formed by three parallel (s\)-(t) paths. This is a valid extension beyond
cactus, but it is only the terminal-free interface theorem.

## 6. The obstruction to a label-independent interface with internal terminals

The scalar closure cannot be promoted to a general multi-terminal
series-parallel sparsifier interface. Consider the path (s-x-t), with all
three vertices terminals. Its underlying two-terminal graph has
(\lambda_N=1), but for prescribed, injective labels (a,c,b), the exact
interface is

\[
 I_N(q;a,b,\{x\mapsto c\})=
 \begin{cases}
 \mu(a,c)+\mu(c,b),&q\ge\mathbf 1[a\ne c]+\mathbf 1[c\ne b],\\
 +\infty,&\text{otherwise}.
 \end{cases}
\]

Its value depends on the internal terminal label (c) and on both metric
distances to (c), although the two-terminal connectivity is still one. For
example, on the line metric with (a=0,c=1,b=3), the value is (3) with two
crossings; changing the metric while retaining three distinct labels changes
the value. A state that retains only (\lambda_N), the boundary labels, and
the budget therefore loses exact information. The issue is feasible and
finite for (kge 2): with all three vertices terminal and injective labels,
both path edges cross and deleting both edges is a terminal Multiway Cut. It
is not an infeasible-instance or pair-bundle shortcut.

The full table (I_N(q;a,b,\rho)) repairs the loss exactly, but its raw state
space contains up to

\[
 (k+1)|D|^{|R_N|+2}
\]

entries before Pareto pruning. Since (|D|\le s), this displays an
(s^{|R_N|}) dependence. No label-independent representative-set bound has
been proved here, and hiding this table inside an alleged “finite state” would
violate the requested no-hidden-label-exponent condition.

## 7. Adversarial audit and scope conclusion

The following possible shortcuts are invalid:

1. Minimizing over a glued label in series while retaining only crossing counts
   is not valid when an internal terminal fixes that label.
2. Replacing a terminal-bearing module by its two-terminal edge connectivity
   preserves feasibility in some cases but not exact metric cost.
3. Pairwise endpoint signatures do not imply a joint contraction hitting-set
   lower bound.
4. A contraction quotient result, even if obtained for this interface, would
   not transfer to arbitrary terminal-preserving sparsifiers.

The completed result is therefore deliberately split. Equations (S) and (P)
prove an exact arbitrary-metric interface and both composition directions.
Equation (T) gives a label-independent scalar closure for terminal-free
two-terminal series-parallel modules, including non-cactus hosts. The explicit
three-terminal path is the smallest feasible obstruction to extending that
scalar closure to modules containing internal terminals. The unrestricted
series-parallel representative-size question remains open; no superlinear
lower bound and no unrestricted sparsifier theorem is claimed.

The Multiway-Cut feasibility theorem and the O7 negative route remain
unchanged. Paper 3 Targets A and B are unrelated to this proof audit and remain
unchanged.

## 8. Claim ledger

| Claim | Status |
|---|---|
| General cost/crossing interface is precisely defined | Proved |
| Series composition in both directions | Proved by (S) |
| Parallel composition in both directions | Proved by (P) |
| Scalar label-independent closure for terminal-free modules | Proved by (T) |
| Scalar closure for arbitrary internal-terminal modules | Refuted by feasible path (s-x-t) |
| Hidden-(s)-exponent-free unrestricted representative bound | Not established |
| Feasible superlinear contraction-only lower bound | Not established |
| Transfer to arbitrary sparsifiers | Not claimed |
