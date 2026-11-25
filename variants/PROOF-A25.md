# Zero separators and one-base hairpins: maximum D = 25

The family here is `A_D = '((' + '((.))'*(D-1) + '))'`, for D>=3.
D counts the enclosing two-base-pair helix as well as D-1 inner helices.
Its length is 5D-1 and its stack score is D. Structures are noncrossing
matchings with no isolated pair, all pairs satisfy j-i>=2, and compatible
pairs are AU, UA, CG, GC, GU and UG. A design has this target as its
unique stack maximizer. The maximum designable D is exactly 25.
This statement does not classify every D<25.

## Attainment

`designs/A-D25.json` gives 124 bases and the target. The exact DP in
`checkers/check_variants.py` checks target legality, score 25, optimum 25,
count 1 and target equality. Its gap-2 answers are compared to `core.fold`;
small generic noncrossing-matchings enumeration controls both recurrences.
The DP counts structures, not derivations: each paired leftmost base chooses
its partner and its unique maximal helix. Forbidding the interior endpoint
pair prevents counting the same helix at multiple lengths. Counts multiply
on disjoint inside/right intervals and add only between disjoint choices.

## Normalization and the 32 states

For pairing neighborhoods, N(A)={U} is contained in N(G)={C,U}, and
N(C)={G} is contained in N(U)={A,G}. At a target-unpaired position, changing
G to A or U to C cannot create a new compatible structure. For a target
GU pair, change G to A; for UG, change G to A on the other endpoint. The
target remains compatible while no new competitor is added. Thus any
design implies a design with Watson-Crick target pairs and A/C unpaired
letters. GU/UG remains allowed in competing structures.

Each inner helix can then be written `a b z comp(b) comp(a)`, with
`a,b` in ACGU, `z` in AC, and comp(A)=U, comp(C)=G, comp(G)=C, comp(U)=A.
There are 32 states, numbered by lexicographic product in those stated
alphabet orders. Define symmetric R(s,t) if their first two letters are
equal, or if some three consecutive letters of s pair in reverse order
with three consecutive letters of t. Include the diagonal of R. Let G
be the graph on distinct states with an edge for R; it has 66 edges.

## Why nonadjacent states cannot collide

Suppose two inner branches have an intervening branch. Their start
positions differ by at least 10. Remove the four pairs of these two
branches, retaining every other target pair.

If their first two letters agree, write their starts as x<y. The new
pairs `(x,y+4),(x+1,y+3),(x+3,y+1),(x+4,y)` are compatible nested pairs.
They form two length-2 helices; the shortest new pair spans at least 6.
They use only the removed branches' endpoints and enclose every intervening
branch without crossing it. If R instead holds by compatible triplets
starting at x+p and y+q (p,q in {0,1,2}), insert
`(x+p+k,y+q+2-k)` for k=0,1,2. Their innermost span is at least 6;
the resulting length-3 helix has two stacks, and again crosses no retained
pair or uses a retained endpoint. In either case we remove two stacks and
add at least two; all retained helices remain legal. The result differs
from the target and scores at least D, contradicting unique optimality.
Thus colliding branches must be adjacent in the linear inner-branch order.

Consequently the odd-position states are all distinct and form an independent
set U of G, and the even-position states form an independent set V of G.
When U and V overlap, their occurrences are still different vertices.
The bipartite graph H with edges R between U and V is a subgraph of the
inner-branch path: each vertex has degree at most 2.

## Adjacent branches and the finite exclusion

For every ordered pair (s,t) of states, consider the ten-base sequence st
and target `((.))((.))`. If there is another legal structure of score at
least 2, those adjacent branches cannot occur in a design. Replacing the
ten-base interval by that structure leaves every outside branch and the
root unchanged, creates no crossing, and loses none of their stacks.
It therefore gives a competitor of score at least D in the full target.

The checker reconstructs all 1,024 pairs. It compares exact DP optimum,
exact count and representative with a generic exhaustive matching
enumeration. Exactly 152 ordered pairs are forbidden. If both (s,t) and
(t,s) are forbidden, an R edge between occurrences s and t is impossible:
it forces adjacency, but neither possible order works.

To exclude D>=26, choose any 13 odd-position branches and any 12 even-position
branches. There are enough since D-1>=25. Their sets must still be independent;
all edges R still have degree at most 2; and no both-orders-forbidden edge
can appear. These are hereditary necessary conditions, so restricting the
selected states preserves them. No monotonicity of RNA designability in D
is being assumed.

A disjoint increasing-first-vertex recursion enumerates all independent
13-sets and 12-sets: it branches on each available smallest next vertex,
then deletes its neighbors. Every independent set has exactly one increasing
vertex list, so no set is missed or repeated. There are 68 and 1,267 such
sets, respectively. For all 86,156 ordered pairs, the checker constructs H:
64,260 have a vertex of degree at least 3; the remaining 21,896 have an
R edge forbidden in both orders. There is no survivor. These weaker conditions
already suffice; no three-branch table or SAT solver is needed for this
finite enumeration. The general-D restriction above proves nonexistence for
all D>=26. Together with the 25 design, this proves the stated maximum.

## The archived CNF certificate and its boundary

`A26/input.cnf` is a supplied necessary-condition encoding with 930 variables
and 5,608 clauses. Variables represent the two 32-state memberships,
Boolean constants and prefix cardinality counters for |U|=13 and |V|=12.
The reported clause categories are:

| Condition | Clauses |
|---|---:|
| Constants and cardinality counters | 3,462 |
| Same-side independence | 132 |
| Degree at most two in H | 1,016 |
| Both orders forbidden on a cross edge | 108 |
| Both orientations forbidden on a two-edge path | 744 |
| Four-vertex cycles | 146 |

The counter identity `y = a OR (b AND c)` is expressible by
`(-a or y)`, `(-b or -c or y)`, `(a or b or -y)`, `(a or c or -y)`.
The archived certificate additionally excludes paths/cycles, beyond the
conditions sufficient for the direct enumeration above.

The distributed CNF has stable per-clause literal deduplication; clause
numbering, order and Boolean meaning are preserved. The supplied binary
DRAT and binary LRAT are unchanged. `normalization.json` gives hashes and
counts. Official DRAT-trim accepts the former with `s VERIFIED`; official
cake_lpr accepts the latter with `s VERIFIED UNSAT`. A deduplicated text
DRAT copy additionally passes warning-strict RUP-only checking while keeping
deleted clauses. The success markers are checker-specific.

Cake_lpr proves the parsed CNF UNSAT within its documented trust boundary;
it does not verify the RNA-to-CNF interpretation. This package does not
supply or claim an independently checked complete variable-by-variable
reconstruction of that archived encoding. Its separately executable finite
exclusion above avoids relying on that missing reconstruction for the RNA
upper bound. The normalization, local-move geometry, and general-D restriction
are prose arguments; they have not been formalized in a proof assistant.
