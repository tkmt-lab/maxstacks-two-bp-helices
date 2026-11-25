# Twelve two-base-pair helices in the maxStacks model

**Package 1.1.0 — 2026-11-25. Article Version 1.4.**
All-versions DOI: [10.5281/zenodo.23679267](https://doi.org/10.5281/zenodo.23679267).

In the maxStacks model, the maximum number of two-base-pair helices in the
fixed one-base-hairpin, one-base-separator family below is **12**.
Researchers studying RNA inverse folding can use the design, exclusion
arguments and certificate checks to examine this exact boundary.

## Quick start

With Git and Python 3.11+ on Linux or macOS:

```sh
git clone --branch v1.1.0 --single-branch https://github.com/tkmt-lab/maxstacks-two-bp-helices.git maxstacks-check
cd maxstacks-check
python3 -B checkers/verify.py
```

Expected: exit 0 and `work/checks/verification.json` containing
`"status": "PASS"` (D12 optimum 12, exact count 1, target equality).
All light-check inputs are included and use Python’s standard library.
Run the remaining commands below from this clone; reuse completed checker builds.

For the fixed target family

```text
T_D = '((.' + '((.)).' * (D-1) + '))',   D >= 2,
```

the largest designable D is **12**. A 71-base sequence uniquely designs T₁₂;
T_D has no design for every D≥13. This package contains the
[article, Version 1.4](paper/paper-v1.4.pdf), its [TeX source](paper/paper-v1.4.tex),
the [claim specification](claims/STATEMENT-A.md), data and reproducible checks.

## Model and results

Structures are noncrossing matchings, allow AU/UA, CG/GC and GU/UG pairs,
and have no isolated pair. The score counts adjacent nested pair pairs
(stacks); a helix of two base pairs contributes one stack. A design makes
the target the unique score maximizer among all compatible legal structures.

Every pair has `j-i>=2`, so a hairpin has **at least one unpaired base**.
This differs from the usual minimum of three unpaired bases in RNA models.
The target has one enclosing two-base-pair helix and D−1 inner two-base-pair
helices, with one-base hairpins and separators.

The article result concerns this fixed family. Package **1.1.0** adds the
separate [variants supplement](variants/README.md):

- **A**, zero separators, one-base hairpins, **j-i>=2**: maximum designable D is
  exactly **25**, with the 124-base design and exclusion of every D>=26.
- **a** and **b**, three-base hairpins, **j-i>=4**: designs at **16** and **21**
  helices respectively, as **lower bounds only**.

D counts the enclosing helix. The supplement and the article have separate claims.

## Scope

The maximum 12 applies to the stated fixed family; it does not classify every
D≤12 or arbitrary RNA trees. The supplement's maximum 25 belongs to the
zero-separator family, while its gap-4 results are lower bounds only.
No Turner-model, experimental or priority claim is made. This work has not
undergone independent human peer review, and the cited authors have not
participated in or endorsed it.

Certificate checking establishes parsed CNF unsatisfiability, not the
RNA-to-CNF interpretation, uniqueness DP, normalization or arbitrary-D
embedding. These rely on the stated algorithms, finite checks and prose
arguments; the Python programs and the full RNA theorem are not formally
verified. The archived A26 CNF has no complete independently checked
variable-to-RNA reconstruction; its RNA upper bound uses the separate
CNF-free enumeration and prose proof. The scope of the prior separate
verification is recorded in [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md).

## Obtain version 1.1.0

The versioned source is the `v1.1.0` tag at
[tkmt-lab/maxstacks-two-bp-helices](https://github.com/tkmt-lab/maxstacks-two-bp-helices/tree/v1.1.0).
The Quick start above obtains that version. Keep the exact tag/commit when
comparing results. The added supplement is included from v1.1.0 onward.
Only the optional D13 replay needs separately archived large files; all added
A26 files are included.

## Run the light checks

Use Python 3.11 or later on macOS or Linux. These checks use only the standard
library; they need no network or SAT solver. Run from the package root:

```sh
nice -n 10 python3 -B checkers/verify.py
```

Success is exit 0 and `work/checks/verification.json` with `"status": "PASS"`.
Do not use `python -O` or `PYTHONOPTIMIZE`: the programs refuse optimized
Python because assertions perform mathematical checks. Output is written to
ignored `work/`. The programs reconstruct, rather than trust stored verdicts:

- D12's exact optimum 12, count 1 and target equality, with small exhaustive
  structural controls for the maximal-helix DP (22,485 sequences).
- Legality, target inequality and score of all 227,280 D13 rivals and 1,731
  U14 rivals; the latter are also regenerated from their family definitions.
- The full D13 CNF F, U14 and all 34 case CNFs, including exact serialized
  hashes, variable counts and clause counts. A case is also compared as a
  clause multiset with the reconstructed base plus its 65 nucleotide units.
- All 4,587,520 word-set candidates by exhaustive counted pruning, the 68
  surviving sets, their 34 τ-orbits, and all 13 symmetry generators on the
  full U14 clause multiset. Word incompatibilities are checked against actual
  rival differences in every pair of branch slots and both orientations.
- Unit-propagation contradictions for all 34 U14 cases, independently replayed
  from emitted traces; 50,199 finite embedding examples supplement the
  general geometric proof in [RIVAL-UPPER.md](claims/RIVAL-UPPER.md).

- The separate variant designs, exact optimum/count/target tests, exhaustive
  small gap-4 DP controls, all 1,024 adjacent-state cases and all 86,156 A25
  state-set exclusions. Details and separate certificate commands are in
  [variants/README.md](variants/README.md).

The general-D geometric argument and normalization proof are given in prose;
see Scope for the distinction between these arguments and finite checks.

## Check all 34 U14 LRATs

Git, make and a C compiler are needed to build the official checker. The build
script downloads exactly cake_lpr commit
`a36874a8b750b43fe4b385b8ddbf5b033e46a3fa`, verifies the assembly/C-wrapper hashes,
and invokes its unmodified Makefile with `-j1`. It selects ARMv8 on Apple Silicon
or x64 on Linux x86_64; other architectures are refused.

```sh
nice -n 10 python3 -B tools/build_cake.py
nice -n 10 python3 -B checkers/verify_lrat.py \
  --checker work/cake_lpr/cake_lpr --scope U14
```

Run the light checks first to generate the CNFs. The build directory must not
already exist; reuse a completed build by running only the second command.
The 34 compressed proofs occupy 4,861,050 bytes. Results and stdout/stderr logs
are in `work/lrat/`. Acceptance requires the exact stdout line
`s VERIFIED UNSAT`, normal exit 0,
complete stream delivery, and the expected compressed and expanded hashes.
Exit 0 alone is insufficient: rejected proofs can also return it.

The case CNFs use the ordered clauses from [SPEC.md](claims/SPEC.md), with
U14's positions and all `i<j` compatibility variables, omitting the fixed-A
separator unit. Rival clauses follow the supplied U14 list's line order.
For each case, append units in increasing branch number and then word-position
order. [RIVAL-UPPER.md](claims/RIVAL-UPPER.md) and `core.formula` specify this
serialization because LRAT refers to clause numbers. The formulas themselves
are unchanged by reordering clauses, but the archived LRAT references are not.

## Check D13 with the separate large files

The companion directory `maxstacks-two-bp-helices-large/` contains eight gzip
files totalling **2,212,249,047 bytes**: seven DRAT parts (613,931,594 bytes)
and one LRAT (1,598,317,453 bytes). They are outside Git. Their filenames,
compressed/expanded hashes and the DRAT order are in
[data/large-proofs.json](data/large-proofs.json) and [manifest.json](manifest.json).
The unchanged large D13 proofs are available as eight separate attachments
at the [v1.0.0 archive](https://doi.org/10.5281/zenodo.23679268).
The same named files are also available from the
[GitHub v1.0.0 release](https://github.com/tkmt-lab/maxstacks-two-bp-helices/releases/tag/v1.0.0);
check them against the fixed hashes below or in `data/large-proofs.json`.
Download the seven named DRAT gzip parts and `D13.lratb.gz` to the companion
directory, preserving their names; their checksums are in `data/large-proofs.json`.
They are not needed for the light checks or the added A26 proof.
The v1.0.0 package was archived as [DOI 10.5281/zenodo.23679268](https://doi.org/10.5281/zenodo.23679268).
The source release identifier for this package is `v1.1.0` at the repository above.
The linked v1.0.0 DOI identifies the original package and unchanged large proofs.

With the companion directory beside this repository, run:

```sh
nice -n 10 python3 -B checkers/verify_lrat.py \
  --checker work/cake_lpr/cake_lpr --scope D13 \
  --large-dir ../maxstacks-two-bp-helices-large
```

This streams the 5,428,472,887-byte expanded LRAT without saving it to disk,
using a 4,096 MB CakeML heap and 128 MB stack. Allow about five minutes and
at least 5 GB available RAM; run it without other heavy checks. Local resource
measurements are recorded in [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md).
The runner verifies the full stream hash and saves exact output and exit status.
The underlying shell form is:

```sh
set -o pipefail
nice -n 10 gzip -dc ../maxstacks-two-bp-helices-large/D13.lratb.gz |
  nice -n 10 work/cake_lpr/cake_lpr --CML_HEAP_SIZE=4096 --CML_STACK_SIZE=128 \
    work/checks/D13-rebuilt.cnf /dev/stdin
```

For the shell form, inspect both normal pipeline termination and the exact
`s VERIFIED UNSAT` line; use the Python runner for hash and complete-delivery checks.
The companion README also gives the seven-part binary DRAT replay order.
A DRAT replay is optional. CI specifies the light checks, all U14 LRATs and
the added A26 LRAT/DRAT checks; D13 is a separate local check. Historical
replay measurements and hosted CI status are in VERIFICATION-RECORD.md.

## Assurance and provenance

The checker build uses official precompiled assembly and the C wrapper.
The trust boundary includes HOL4's logic and kernel, the formal parsing/CNF
and machine models, the correspondence of distributed assembly to the
verified compilation, the C FFI, compiler/assembler/linker, OS, file I/O and
hardware. The upstream checksum table's C-wrapper entry is stale at this
revision; this package checks the actual pinned Git blob hash.
See [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md) for exact revisions,
the scope of the separate checks and the distributed-assembly build.

A successful cake_lpr run certifies the parsed CNF's unsatisfiability under
that boundary. Its conclusion is independent of the SAT solver and
DRAT-to-LRAT converter. The model-level obligations are described in Scope.

The standard-library mathematics code was adapted from an earlier separate
verification implementation. [PROVENANCE.json](PROVENANCE.json) records
input and adaptation hashes. Codex and Claude assisted the mathematical
arguments, search, software, verification, literature comparison and writing.
Tatsuhiko Takimoto is responsible for the manuscript.

## Acknowledgments

Théo Boury, Laurent Bulteau and Yann Ponty introduced the maxStacks
inverse-folding framework and degree–length obstruction that motivate this
question in [RNA Inverse Folding Under Stacked Base Pair Maximization,
WABI 2026](https://doi.org/10.4230/LIPIcs.WABI.2026.12).
Marijn J. H. Heule and the DRAT-trim contributors provide the DRAT proof
checker; the cake_lpr contributors and the CakeML project provide the
verified LRAT checker used here. We are grateful for these foundations
and tools.

## Files, citation and maintenance

[claims.json](claims.json) lists the scope and exclusions. All distributable
files except the self-referential manifest are hashed by `manifest.json`;
Git records the manifest itself. Never refresh hashes to conceal an unexplained
mismatch. After a reviewed intentional edit, use `python3 -B tools/update_manifest.py`
and rerun the relevant checks.

The current PDF and TeX are **Version 1.4**. Article history is recorded in
[CHANGELOG.md](CHANGELOG.md) and [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md).
Earlier manuscripts and their diffs are preserved in Git history; the
distributed `paper/` directory contains the current article only. To rebuild
with an existing LaTeX installation, use the preamble's packages and run
the following from the package root:

```sh
mkdir -p work/paper
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=work/paper paper/paper-v1.4.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=work/paper paper/paper-v1.4.tex
```

PDF bytes may differ
across engines. Certificate checks do not need a TeX installation.

Tatsuhiko Takimoto. Package version **1.1.0**; article **Version 1.4**.
Research contact: [research@tatsuhikotakimoto.com](mailto:research@tatsuhikotakimoto.com).
See [CITATION.cff](CITATION.cff). Code is Apache-2.0; original prose, data and
proof certificates are CC BY 4.0. Full license texts and third-party boundaries
are in [LICENSE](LICENSE). Version 1.0.0 remains archived unchanged.
See [CHANGELOG.md](CHANGELOG.md) for package 1.1.0 (2026-11-25).
