# Supplement: zero separators and three-base hairpins

**Package 1.1.0 — 2026-11-12.** From the package root, with Python 3.11+:

```sh
python3 -B checkers/verify.py
```

Expected: exit 0 and `work/checks/verification.json` with `"status": "PASS"`.
Obtain the versioned package using the [main README Quick start](../README.md#quick-start).

These results are separate from the article's fixed separator-1/hairpin-1
maximum 12. Package **1.1.0** adds three certificates:

| Family | Exact target, D>=3 | Pair gap j-i | Result | Length |
|---|---|---:|---|---:|
| A | `'((' + '((.))'*(D-1) + '))'` | >=2 | Maximum designable D **25** | 124 at D25 |
| a | `'((.' + '((...)).'*(D-1) + '))'` | >=4 | Design at D **16**, lower bound only | 125 |
| b | `'((' + '((...))'*(D-1) + '))'` | >=4 | Design at D **21**, lower bound only | 144 |

D includes the enclosing two-base-pair helix. All structures are noncrossing,
allow AU/UA, CG/GC and GU/UG, have no isolated pair, and maximize stacks.
Gap 2 permits one-base hairpins; gap 4 requires at least three unpaired bases
in a hairpin. In each row, **every competitor pair** obeys that row's gap.
No maximum for a or b is claimed. None of these is a Turner or experimental
RNA result, and none changes the article's theorem. The positive sequences
and literal targets are in `designs/*.json`; the A25 upper argument is
[PROOF-A25.md](PROOF-A25.md).

## Reproduce from the package root

Use Python>=3.11 without `-O` or `PYTHONOPTIMIZE`:

```sh
nice -n 10 python3 -B checkers/verify.py
```

This checks the manifest and the original light mathematics, plus all three
variant designs, DP controls and A25 finite exclusion. Variant-only reruns
are possible with `python3 -B checkers/check_variants.py` (this shorter
command does not perform the full package manifest check). Outputs are
`work/checks/variants.json` and `work/checks/verification.json`, status PASS
with normal exit 0. Gap4 is compared with generic matching enumeration for
all 87,381 sequences of lengths 0..8 and 512 seeded sequences of lengths
9..12; gap2 has 5,461 exhaustive sequences through length 6 plus 768 seeded
samples through length 12. All 1,024 two-branch cases are also compared to
exhaustive structures, and all 68*1,267=86,156 state-set pairs are excluded.
The positive checks require optimum=D, exact count=1, target equality and
literal legality. All use the standard library and need no network or solver.

The added A26 LRAT is only 51,180 bytes; these commands do **not** run the
large D13 proof:

```sh
nice -n 10 python3 -B tools/build_cake.py
nice -n 10 python3 -B checkers/verify_variants_proofs.py \
  --checker work/cake_lpr/cake_lpr
```

The build needs Git, make, a C compiler and network access, uses unmodified
cake_lpr commit `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa`, and checks the
pinned source hashes. Reuse an existing build by skipping the build command;
its output directory must not exist for a new build. The proof runner uses
256 MB heap and 64 MB stack, requires normal exit 0 **and the exact stdout
line `s VERIFIED UNSAT`**, and rejects an empty-proof control even if its
exit status is 0. Proof and CNF hashes are checked before invocation.
Results and logs are under `work/variants-proofs/`.

For the supplied DRAT and a warning-strict additional replay:

```sh
nice -n 10 python3 -B tools/build_drat.py
nice -n 10 python3 -B checkers/verify_variants_proofs.py \
  --checker work/cake_lpr/cake_lpr --drat work/drat-trim/drat-trim
```

The builder downloads the unmodified official `drat-trim.c` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, verifies SHA256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`,
and compiles with `cc -std=c99 -D_DEFAULT_SOURCE -O2`, with assertions enabled.
`_DEFAULT_SOURCE` exposes `getc_unlocked` on Linux/glibc under strict C99;
the pinned upstream source is not modified. Skip this build if its work directory
already exists. DRAT-trim's exact success line is `s VERIFIED`, **not**
cake_lpr's marker. The unchanged binary DRAT is checked with `-t 60`, without warning-strict
options; it must be accepted, and its 25 duplicate-literal warnings are recorded.
Only `proof-deduplicated.drat` receives `-W -p -U -t 60` (warnings are errors,
retain deleted clauses, require RUP); it must be accepted with no warnings.
An empty DRAT control must be rejected.

## Normalization, provenance and assurance

Before distribution, one repeated literal was removed from each of 25 CNF
clauses, preserving all 5,608 clause numbers and the 930-variable header.
The resulting CNF SHA256 is
`131b683842f71366c793fb1833a23a481943177b2d617f30ac5eecc0a4246ff5`.
The supplied binary proofs are unchanged. The text DRAT copy similarly
removes 25 repeated literals in 25 of 4,990 steps, preserving pivots,
step order and additions/deletions. `A26/normalization.json` records both.

Cake_lpr certifies parsed CNF UNSAT under the main README's trust boundary.
The complete variable-to-RNA reconstruction for this archived encoding is
not independently checked here; the CNF-free finite enumeration and prose
proof provide the RNA upper argument. Neither that Python enumeration nor
the uniqueness DP is formally verified. Integration uses the earlier R004
independent verification and producer inputs together, so this is a fresh
reproduction, not a new blind derivation or human peer review.
`PROVENANCE.json` records pinned input hashes. Scientific results are kept
separate from the manuscript reading and literature search.

This supplement is included in package `v1.1.0` (2026-11-12); use the main
README's versioned acquisition command. The v1.0.0 archive does not contain
these files. The A26 files are included in this supplement and require none
of the separate large D13 attachments.
