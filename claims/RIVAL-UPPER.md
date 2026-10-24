# A finite relaxation for every D≥14

This argument uses a 97-position problem U14 and a mapping of rival families.
It is not a direct proof for the canonical T₁₄ CNF. See the article for the same
argument in its mathematical context.

## U14 and its rivals

The target is `'((.' + '.((.)).'*13 + '.))'`, with pairs `(0,96),(1,95)` and
13 inner branches. Exterior separators are 2 and 94. Block k, for k=0,...,12,
has positions `3+7k,...,9+7k`, written `L a b h c d R`. Its branch starts at
`u=4+7k`, with pairs `(u,u+4),(u+1,u+3)`. Every unpaired position is A/C;
every target pair is WC. Blocks have distinct private separator positions.

Nucleotide variables are `x(i,a)=4i+a+1` in A,C,G,U order. Compatibility
variables cover all `i<j`, including adjacent positions, and have numbers
`p(i,j)=4n+i(n-1)-i(i-1)/2+j-i`, n=97. This is a bookkeeping choice:
rival structures still require separation at least 2. There are 5,044 variables.
Use SPEC's one-hot, WC, AC, compatibility equivalences and redundant target/
unpaired units, with **no separator fixed to A**. There are 67,129 base clauses.

Let `H(u)={(u,u+4),(u+1,u+3)}` and
`K(x,y)={(x,y+2),(x+1,y+1),(x+2,y)}`. Every following rival retains all target
pairs except those explicitly replaced:

- In one seven-position block replace `.((.)).` by each of
  `((.))..`, `..((.))`, `((..)).`, `.((..))`, `((...))`, `(((.)))`: 78 rivals.
- For starts s<t, replace H(s),H(t) by
  `(s,t+4),(s+1,t+3),(s+3,t+1),(s+4,t)`: 78 inner swaps.
- Replace the root and H(s) by `(0,s+1),(1,s),(s+3,96),(s+4,95)`:
  13 outer swaps.
- Replace H(s),H(t) by K(s+r,t+q), for r,q in −1,...,3 and |r−q|≤2:
  1,482 inner triplets.
- Replace the root and H(s) by K(0,s+r), r=1,2,3: 39 left outer triplets.
- Replace the root and H(s) by K(s+r,94), r=−1,0,1: 39 right outer triplets.
- Replace the root by `(0,95),(1,94)` or `(1,96),(2,95)`: two root shifts.

All 1,731 rivals are distinct legal structures, different from the target,
with score at least 14. The checker generates the families from these definitions
and compares the full set with the supplied list. Each rival gives one avoidance
clause, as in SPEC, for a total of 68,860 clauses.

For reproducible clause identifiers, use SPEC's ordered construction (omit
its step 4, use all i<j), then append rival clauses in the exact line order of
[data/rivals-U14.txt.gz](../data/rivals-U14.txt.gz). Its expanded SHA256 is
`0ad72ae92ae2ab1f141d6a4ed213a0ac6df72cd154430fdccae30a64e370374c`.
The canonical DIMACS SHA256 is
`5ff81ea47c5fa1f66300587ea0d036cae32598c2070374e8ee423056f89f715f`.
This serialization convention fixes otherwise immaterial clause order for LRAT.

## Covering word cases

A normalized five-base branch word is `(a,b,h,WC(b),WC(a))`: 32 possibilities.
Repeated `(a,b)` gives an inner-swap rival. For two different words, any compatible
internal triplet gives an inner-triplet rival. The checker tests all 32-choose-2
word pairs, both orientations, in each of the 13-choose-2 slot pairs against the
actual rival differences, without assigning the separators. The incompatibility
graph has 66 edges.

Select 13 of 16 `(a,b)` groups and one of two h letters per selected group.
There are `binom(16,13)*2^13=4,587,520` candidates. Exhaustive enumeration, with
counted pruning, leaves 68 sets. τ (A↔C,G↔U) has 34 two-element orbits.
The 34 supplied sets in [data/U14-cases.json](../data/U14-cases.json) cover
each orbit once. The checker compares the full sets, not only their number.

Each of the 12 adjacent exchanges of entire seven-position blocks, and τ,
preserves the full clause multiset. These exchanges generate all block
permutations, allowing the words of every potential model to be sorted.
Together with τ this proves coverage by the supplied 34 cases. No extra
separator fixing is used. Append 65 positive nucleotide units to U14 in block
order k=0,...,12, then word-position order 0,...,4. Each case has 68,925 clauses.
The case hashes identify this exact order. Stored LRATs prove their
unsatisfiability; the package also derives and replays unit-propagation traces.

## Mapping back to arbitrary D

Assume a normalized design of T_D for D≥14. Choose 13 inner branches with
indices `1≤j_0<...<j_12≤D-1`; put n_D=6D−1. Assign U14 positions by

```text
0 -> 0; 1 -> 1; 95 -> n_D-2; 96 -> n_D-1;
2 -> 2; 94 -> n_D-3;
3+7k+r -> 6*j_k-4+r, for r=0,...,6.
```

Copy letters along this map. Virtual separators can share a real position,
including adjacent blocks and the exterior separators. This is harmless for
letter assignments but requires checking endpoints of every mapped rival.
Restore all target helices outside the selected replacement.

A local seven-position replacement uses a consecutive real window and only
the replaced branch or originally unpaired positions. It preserves at least
one stack and crosses no other branch.

For two inner triplets the real branch starts differ by at least six. Since
|r−q|≤2, their starts differ by at least four and the innermost pair separation
is at least two. A shared separator could be used twice only with left offset
3 and right offset −1; this offset pair is excluded. The six endpoints are
distinct. Replacing two two-pair helices by a three-pair helix preserves two
stacks; intermediate unselected branches lie inside its pairs.

For a left outer triplet, positions 0,1,2 are consecutive and r≥1 keeps the
other triplet's start at least four away even at the first branch. For a right
outer triplet, positions n_D−3,n_D−2,n_D−1 are consecutive and r≤1 provides
the same bound at the last branch. These restrictions also avoid repeated
separator endpoints. The two replaced stacks remain two stacks.

Swaps use the branch endpoints only. Start difference at least six gives
minimum new pair separation two. For an outer swap the shortest pairs are
`(1,s)` and `(s+4,n_D-2)`, again of separation at least two. The two new
helices and all retained target helices are noncrossing.

Root shifts use consecutive root endpoints and exterior separators, so they
map to legal two-pair helices while retaining all inner branches.

Thus every virtual rival maps to a distinct-from-target, noncrossing real
structure with no isolated pairs and score at least D. Extra stacks can only
increase that score. Compatibility of a virtual rival would imply compatibility
of the real rival, contradicting design. The copied assignment must therefore
satisfy every U14 avoidance clause, contradicting the covering UNSAT cases.
Hence all D≥14 are excluded.

The checker's 50,199 finite embedding examples supplement this family-wise
argument. They do not replace its universal quantifier. D13 requires its
separate full-F proof; the general-D argument here alone gives D₂≤13.
