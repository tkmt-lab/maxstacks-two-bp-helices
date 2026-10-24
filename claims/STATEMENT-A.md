# Claim: twelve two-base-pair helices in a fixed family

This is the mathematical specification accompanying [article draft v1](../paper/paper-v1.pdf).
Verification dates, roles and limitations are in [VERIFICATION-RECORD.md](../VERIFICATION-RECORD.md).

## Model and target

A sequence uses A,C,G,U. Compatible ordered pairs are AU, UA, CG, GC, GU, UG.
A structure is a set of pairs `(i,j)` on positions `0,...,n-1`, with disjoint
endpoints, `i<j`, no crossing `i<k<j<l`, and `j-i>=2`. Every pair has an inner
neighbor `(i+1,j-1)` or an outer neighbor `(i-1,j+1)` in the structure. Thus
isolated pairs are forbidden. The score is the number of adjacent nested pair
pairs (stacks). Compare only structures whose pairs are compatible with the sequence.

The minimum hairpin has **one unpaired base**. This differs from the usual
three-base minimum. No Turner-model or experimental-RNA conclusion is asserted.

For integer `D>=2`, put `n=6D-1` and

```text
T_D = '((.' + '((.)).' * (D-1) + '))'
```

The root pairs are `(0,n-1),(1,n-2)`. For `j=1,...,D-1`, put `s=6j-3` and add
`(s,s+4),(s+1,s+3)`. The score is D. A design makes this target compatible and
makes every different compatible legal structure score strictly below D.
Let D₂ be the maximum designable D in this family.

**Claim:** T₁₂ is designable; every T_D with D≥13 is not designable. Hence D₂=12.
This does not classify every D≤12 or arbitrary RNA trees.

## A lower-bound witness

The [71-base sequence](../data/D12-sequence.txt) is

```text
GAAAGCCUAGGACCACCCGGACGACGAACAGUACAAUGAGUAACAUGACACUAAUAAAUAAUCGCAGCAUC
```

The package DP returns score 12, exact optimal-structure count 1, and T₁₂.
It decomposes a structure at its leftmost position into an unpaired position
or a maximal helix of length ℓ≥2, its interior, and its right remainder.
The interior forbids pairing its two boundary positions, making the helix
maximal and the decomposition unique. A helix contributes ℓ−1 stacks;
independent substructure counts multiply and tied optimal scores add counts.
Small exhaustive structural enumeration checks this recurrence separately.

## Normalization preserves existence

The neighbor sets satisfy `N(A)={U} ⊂ N(G)={C,U}` and
`N(C)={G} ⊂ N(U)={A,G}`. Replacing G by A or U by C never creates a new
compatible pair. Apply these replacements to target-unpaired positions, and
to the G endpoint of each target GU/UG pair to make it AU/UA. The target remains
compatible; no rival appears. Target pairs are disjoint, so these replacements
can be applied successively. Existence of a design therefore implies existence
of a design with all target pairs Watson–Crick (WC) and all unpaired positions A/C.
It does not imply that every design already has this form.

The involution τ exchanges A with C and G with U, preserving compatibility,
WC pairs and A/C. For D13 only, apply τ if necessary to fix position 2 to A.
U14 has no such separator fixing; its τ quotient is handled by case coverage.

## The two upper-bound steps

For D13, [SPEC.md](SPEC.md) defines a nucleotide-level CNF F. The supplied
227,280 rivals are each legal, different from T₁₃, and score at least 13.
A normalized design would satisfy F by avoiding them all. One proof against
this full F rules out a design. Exhaustiveness of the rival list is unnecessary.
The DRAT proof introduces auxiliary variables, whose RAT steps are checked;
the corresponding LRAT is checked against the same original F. A conditional
case or a derivation without a contradiction does not suffice.

For all D≥14, [RIVAL-UPPER.md](RIVAL-UPPER.md) gives a separate relaxation U14,
34 covering word cases, and a family-wise mapping from every U14 rival back to
a legal real rival. Finite tests supplement this mapping; the general geometric
argument is required. D13's exclusion alone does not establish larger-D exclusion.

Proof files, their order and compressed/expanded hashes are in
[manifest.json](../manifest.json). Formal proof checking concerns CNF
unsatisfiability. The RNA model, normalization, rival validity, DP, encoding,
case coverage and geometric mapping require the other checks and mathematical arguments.
