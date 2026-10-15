# Terminal-bearing series-parallel interface compression: proof audit

Task: `THEORY-ZEROEXT-SP-TERMINAL-COMPRESSION-004`. Audit date: 2026-10-15.

This is a mathematical proof audit only. No experiment, network search,
supervisor start, state/queue/ledger/status update, production change, or
external source was used. The preceding Multiway-Cut feasibility theorem and
the exact series-parallel interface are treated as inputs.

## 1. Exact interface and quantifiers

Let (N=(V_N,E_N;s,t)) be a finite undirected two-terminal multigraph.
Parallel edges are separate edge terms and loops contribute zero cost and
zero crossings. Let (R_N\subseteq V_N\setminus\{s,t\}) be the terminals
strictly internal to the module. Let ((D,\mu)) be any finite metric and let
\(\rho:R_N\to D\) be injective. Boundary labels (a,b\in D) are arguments;
if a boundary is an ambient terminal, its label is fixed by the ambient
assignment rather than minimized over.

For \(\phi:V_N\to D\), define

\[
 C_N(\phi)=\sum_{uv\in E_N}\mu(\phi(u),\phi(v)),\qquad
 X_N(\phi)=|\{uv\in E_N:\phi(u)\ne\phi(v)\}|.
\]

The exact at-most-crossing interface is

\[
 I_N(q;a,b,\rho)=\min\{C_N(\phi):
 \phi(s)=a,\ \phi(t)=b,\ \phi|_{R_N}=\rho,
 X_N(\phi)\le q\},
 \tag{1}
\]

with value (+\infty) if the feasible set is empty. The quantifiers are
universal over finite (N), finite metrics, injective terminal assignments,
and every integer (q\ge0). The upper-budget semantics are essential.

The dependency proves the exact composition laws. If (N=A\circ B), with
nonterminal glued vertex (x), then

\[
 I_N(q;a,b,\rho_A\cup\rho_B)=
 \min_{z\in D,\ q_A+q_B\le q}
 \bigl(I_A(q_A;a,z,\rho_A)+I_B(q_B;z,b,\rho_B)\bigr).
 \tag{S}
\]

If (N=A\parallel B), then

\[
 I_N(q;a,b,\rho_A\cup\rho_B)=
 \min_{q_A+q_B\le q}
 \bigl(I_A(q_A;a,b,\rho_A)+I_B(q_B;a,b,\rho_B)\bigr).
 \tag{P}
\]

Both identities hold in both directions: restriction of a feasible global
labeling gives a right-hand-side competitor; gluing minimizing branch
labelings gives a global labeling with additive cost and crossing count.

## 2. Restricted compression lemma

**Lemma (terminal-free scalar closure).** If (R_N=\varnothing), define

\[
 \lambda_N=\min\{|F|:F\subseteq E_N,
 s\text{ and }t\text{ are disconnected in }N-F\}.
\]

Then, for every finite metric and (a,b\in D),

\[
 I_N(q;a,b,\varnothing)=
 \begin{cases}
 0,&a=b,\\
 \lambda_N\mu(a,b),&a\ne b\text{ and }q\ge\lambda_N,\\
 +\infty,&a\ne b\text{ and }q<\lambda_N.
 \end{cases}
 \tag{T}
\]

For (a=b), the constant labeling proves the upper bound and nonnegativity
proves equality. For (a\ne b), crossing edges separate (s) from (t),
so there are at least \(\lambda_N\). Put

\[
 d(v)=\mu(a,\phi(v)),\qquad L=\mu(a,b).
\]

The triangle inequality gives
\(\mu(\phi(u),\phi(v))\ge|d(u)-d(v)|\). For every (r\in(0,L)),
\(U_r=\{v:d(v)\le r\}\) contains (s) and excludes (t), so
\(|\delta(U_r)|\ge\lambda_N\). Therefore the layer-cake identity gives

\[
 C_N(\phi)\ge\sum_{uv\in E_N}|d(u)-d(v)|
 =\int_0^\infty|\delta(U_r)|\,dr
 \ge\int_0^L|\delta(U_r)|\,dr\ge\lambda_N L.
\]

A minimum (s\)-(t) cut labeled (a) on one side and (b) on the other
attains the bound with exactly \(\lambda_N\) crossings. The same argument did
not use series-parallel structure: (T) holds for every finite undirected
unweighted multigraph with distinguished s,t and no internal terminals.
Series-parallel recursion only computes the cut parameter conveniently. This
is a standard metric/min-cut consequence, not a new series-parallel
sparsification theorem. This proves both directions of (T). Under series and
parallel composition,

\[
 \lambda_{A\circ B}=\min(\lambda_A,\lambda_B),\qquad
 \lambda_{A\parallel B}=\lambda_A+\lambda_B.
\]

Thus terminal-free series-parallel modules have an exact one-scalar
structural interface. This is restricted to (R_N=\varnothing).

## 3. Feasible terminal-bearing obstruction

Consider the series-parallel path (s--x--t), with all three vertices
terminals and (x\in R_N). Its two-terminal connectivity is \(\lambda_N=1\).
For prescribed distinct labels (a,c,b), the only labeling is the terminal
labeling, hence

\[
 I_N(q;a,b,\{x\mapsto c\})=
 \begin{cases}
 \mu(a,c)+\mu(c,b),
 &q\ge\mathbf 1[a\ne c]+\mathbf 1[c\ne b],\\
 +\infty,&\text{otherwise}.
 \end{cases}
 \tag{3}
\]

Injectivity makes both edges crossing. Thus the instance is feasible for
every (k\ge2): deleting both edges is a terminal Multiway Cut of size two,
and the unique terminal labeling obeys the budget. No infeasible instance is
used.

The dependence on the internal label is numerically nonvacuous. Use two valid
metrics on \(D=\{a,b,c\}\):

\[
 \mu_1(a,b)=2,\quad \mu_1(a,c)=1,\quad \mu_1(c,b)=2,
 \qquad
 \mu_2(a,b)=2,\quad \mu_2(a,c)=2,\quad \mu_2(c,b)=2.
\]

Both are metrics: the first has the triangle sum \(1+2\ge2\), and the
second is equilateral. They have the same endpoint distance
\(\mu_i(a,b)=2\), but different internal sums, 3 and 4. With the same graph,
endpoint labels (a,b), and budget (q=k=2), the two metric instances give

\[
 I_N^{\mu_1}(2;a,b,\{x\mapsto c\})=3,
 \qquad
 I_N^{\mu_2}(2;a,b,\{x\mapsto c\})=4.
\]

Therefore a state retaining only endpoint labels, two-terminal connectivity,
and budget cannot be exact for every terminal-bearing series-parallel module.
The check uses only the two edge terms and stays in the feasible (k\ge2)
regime.

## 4. Scope and explicit size dependence

The proved obstruction is narrow:

> No exact compression that discards all internal terminal labels and retains
> only endpoint labels, connectivity, and crossing budget represents every
> terminal-bearing series-parallel interface for arbitrary finite metrics.

It does not rule out a symbolic or metric-aware representation retaining (c)
and the expression \(\mu(a,c)+\mu(c,b)\). It therefore does not prove that
every label-dependent compression has (|D|)- or (s)-dependent size.

For fixed (D), direct representation of (1) has at most

\[
 (|E_N|+1)|D|^{|R_N|+2}
 \tag{4}
\]

raw argument/value positions before pruning. With budgets truncated to (k),
the first factor is (k+1). Formula (4) is only a direct-table upper bound;
it is not a sparsifier lower bound, representative-set lower bound, quotient
lower bound, or contraction lower bound. The dependence on (|D|) and the
number of internal terminals is displayed rather than hidden.

No pairwise-signature inference is used. No infeasible-instance shortcut is
used. No conclusion transfers to arbitrary terminal-preserving sparsifiers,
and no feasible superlinear contraction-only lower bound is claimed. The
predecessor Multiway-Cut feasibility theorem and its negative contraction
route are unchanged.

## 5. Final status and next falsifiable action

The terminal-free compression lemma (T) is proved in both directions. For
terminal-bearing modules, the feasible (k\ge2) path is an independently
checkable obstruction to label-blind scalar closure. The broader question of
a label-dependent, metric-aware interface with no hidden (|D|)- or
(s)-dependent exponent remains open.

Next, specify a candidate metric-aware state class and prove both reconstruction
directions for (S) and (P). If it omits internal-label information, (2)--(3)
must be a failing test. If it retains symbolic labels, any lower bound must
quantify over that representation class and use a feasible family; raw table
cardinality, infeasibility, and pairwise signatures are insufficient.

Paper 3 Target A and Target B remain unchanged.
