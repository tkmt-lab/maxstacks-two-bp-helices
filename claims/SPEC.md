# Canonical D13 CNF F

F has 3,158 variables and 268,408 clauses. It contains only nucleotide and
compatibility variables. The model and normalization are in
[STATEMENT-A.md](STATEMENT-A.md); the ordered rivals are in
[../data/rivals-D13.txt.gz](../data/rivals-D13.txt.gz).

Positions are 0,...,76. The target is `'((.' + '((.)).'*12 + '))'`.
Allowed sequence pairs are AU, UA, CG, GC, GU, UG; legal structural pairs
have `j-i>=2` and belong to a helix of at least two base pairs.

## Variables

Letters A,C,G,U have indices 0,1,2,3. Nucleotide variable `x(i,a)=4i+a+1`.
For every `j>=i+2`, order `(i,j)` lexicographically and set

```text
p(i,j) = 308 + 75*i - i*(i-1)/2 + j-i-1.
```

The 2,850 compatibility variables have numbers 309,...,3158. They mean
actual nucleotide compatibility, not selection of a structural pair.

## All clauses and their order

Use increasing position and pair order and letter order A,C,G,U. WC means
AU, UA, CG, GC. Write each clause with the displayed literal order.

1. For each position, the four-letter OR followed by six exclusions
   `-x(i,a),-x(i,b)` for `a<b`: 539 clauses.
2. For each target pair in lexicographic order and each non-WC ordered letter
   pair `(a,b)` in lexicographic order, `-x(i,a),-x(j,b)`: 312 clauses.
3. For each target-unpaired position, `-x(i,G)` then `-x(i,U)`: 50 clauses.
4. The unit `x(2,A)`, namely `9 0`: 1 clause.
5. For each compatibility variable, six forward clauses
   `-x(i,a),-x(j,b),p(i,j)` for compatible `(a,b)` in letter-pair order.
   Then, for each letter a, the two support clauses
   `-p(i,j),-x(i,a),OR_{b:ab compatible} x(j,b)` and
   `-p(i,j),-x(j,a),OR_{b:ab compatible} x(i,b)`, with b increasing:
   39,900 clauses. Under one-hot constraints these give exact equivalence.
6. Positive units for target p variables in pair order, then negative units
   for all pairs of target-unpaired positions in pair order: 326 clauses.

These 41,128 base clauses include redundant units implied by preceding clauses.
For each rival P, append `OR_{(i,j) in P minus T13} -p(i,j)`, listing its
pairs lexicographically. The difference must be nonempty. Shared target
compatibilities are true, so omitting them preserves the avoidance condition.

The rivals are ASCII dot-bracket strings in lexicographic order, one 77-character
string followed by LF per line. Check balance, endpoint uniqueness, noncrossing,
minimum separation 2, no isolated pairs, target inequality, and score at least 13.
The score histogram is 227,255 at 13 and 25 at 14. No claim that the list includes
all structures is needed. A SAT assignment would only avoid this finite list;
it would not itself certify a design.

DIMACS bytes are ASCII with header `p cnf 3158 268408` followed by LF.
Each clause is space-separated signed decimal integers followed by ` 0` and LF.
The file has 20,535,942 bytes and SHA256
`4f8100bbe4362bf45db9b4be068eb115bf1c48c3f556ce5c3bceff1e7f5a4a6c`.

The proof may introduce variables beyond 3158. Those are proof steps, not
extra assumptions in F. Acceptance must be against this reconstructed full F.
