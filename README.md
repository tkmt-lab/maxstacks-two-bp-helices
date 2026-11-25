# Twelve two-base-pair helices in the maxStacks model

For the fixed target family

```text
T_D = '((.' + '((.)).' * (D-1) + '))',   D >= 2,
```

the largest designable D is **12**. A 71-base sequence uniquely designs T₁₂;
T_D has no design for every D≥13. This package contains the
[article, Version 1.3](paper/paper-v1.3.pdf), its [TeX source](paper/paper-v1.3.tex),
the [claim specification](claims/STATEMENT-A.md), data and reproducible checks.

The question and maxStacks framework come from **Théo Boury, Laurent Bulteau
and Yann Ponty**, [RNA Inverse Folding Under Stacked Base Pair Maximization,
WABI 2026](https://doi.org/10.4230/LIPIcs.WABI.2026.12).
We acknowledge their work and the DRAT-trim and CakeML/cake_lpr contributors.
The cited authors did not participate in or endorse this work.

## Model and scope

Structures are noncrossing matchings, allow AU/UA, CG/GC and GU/UG pairs,
and have no isolated pair. The score counts adjacent nested pair pairs
(stacks); a helix of two base pairs contributes one stack. A design makes
the target the unique score maximizer among all compatible legal structures.

Every pair has `j-i>=2`, so a hairpin has **at least one unpaired base**.
This differs from the usual minimum of three unpaired bases in RNA models.
The target has one enclosing two-base-pair helix and D−1 inner two-base-pair
helices, with one-base hairpins and separators.

The article result concerns this fixed family. It does not classify every D≤12
or arbitrary RNA trees. Package **1.1.0** adds the separate [variants supplement](variants/README.md):

- **A**, zero separators, one-base hairpins, **j-i>=2**: maximum designable D is
  exactly **25**, with the 124-base design and exclusion of every D>=26.
- **a** and **b**, three-base hairpins, **j-i>=4**: designs at **16** and **21**
  helices respectively, as **lower bounds only**.

D counts the enclosing helix. These supplement results do not change the
article theorem. No Turner-model, experimental, priority or human peer-review
claim is made.

## Obtain the preparation

Version 1.1.0 is currently a local repository preparation supplied for review;
there is no public download for it yet. The v1.0.0 archive does not contain
the new supplement. Given the supplied local Git repository, check a clean
copy with:

```sh
git clone --no-hardlinks /path/to/supplied/maxstacks-two-bp-helices maxstacks-check
cd maxstacks-check
```

Use the exact supplied commit when comparing results. A release maintainer
must add the versioned v1.1.0 repository/archive link before distribution.
The following commands run in that clone. Only the optional D13 replay needs
the separately archived large files; all added A26 files are already included.

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

These finite computations do not mechanize the general-D geometric argument
or normalization proof. The Python programs are not formally verified.

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
Download the seven named DRAT gzip parts and `D13.lratb.gz` to the companion
directory, preserving their names; their checksums are in `data/large-proofs.json`.
They are not needed for the light checks or the added A26 proof.
The v1.0.0 package was archived as [DOI 10.5281/zenodo.23679268](https://doi.org/10.5281/zenodo.23679268).
This local v1.1.0 preparation has no new release identifier.

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
A DRAT replay is optional; this package preparation verifies its hashes and
uses the archived LRAT for the required full-F replay. It does not claim a new
DRAT replay. CI specifies the light checks, all U14 LRATs, and the added A26 LRAT/DRAT
checks; D13 remains a separate local check. Hosted CI has not run for v1.1.0.

## Assurance and provenance

The checker build uses official precompiled assembly and the C wrapper, not a
local rebuild of HOL4/CakeML proofs. The trust boundary includes HOL4's logic
and kernel, the formal parsing/CNF and machine models, the correspondence of
distributed assembly to the verified compilation, the C FFI, compiler/assembler/
linker, OS, file I/O and hardware. The upstream checksum table's C-wrapper entry
is stale at this revision; this package checks the actual pinned Git blob hash.
See [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md) for exact revisions and scope.

A successful cake_lpr run certifies the parsed CNF's unsatisfiability under
that boundary. It does not certify the RNA-to-CNF interpretation, uniqueness
DP, arbitrary-D mapping, novelty or empirical usefulness. The SAT solver and
DRAT-to-LRAT converter need not be trusted for an accepted LRAT's conclusion.

The standard-library mathematics code was adapted from the lab's earlier
separate verification. That effort received the claim inputs but withheld
producer code and reports. Package assembly used both result sets and is
**not a new blind verification**. [PROVENANCE.json](PROVENANCE.json) records
input and adaptation hashes. Verification was computational/AI-assisted;
no independent human review is represented here.

## Files, citation and maintenance

[claims.json](claims.json) lists the scope and exclusions. All distributable
files except the self-referential manifest are hashed by `manifest.json`;
Git records the manifest itself. Never refresh hashes to conceal an unexplained
mismatch. After a reviewed intentional edit, use `python3 -B tools/update_manifest.py`
and rerun the relevant checks.

The included current PDF and TeX are **Version 1.3**. Relative to v1.2, only
version/date metadata, the D=25 footnote's package reference and one Scope
sentence about the gap-4 lower designs change. The 124-base sequence, main
theorem, proofs and tables are unchanged; the maximum 25 is a supplement
result, not a theorem of the article. Earlier drafts are retained in `paper/`,
and [the exact diff](paper/v1.2-to-v1.3.diff) records the edit. To rebuild
with an existing LaTeX installation, use the preamble's packages and run
`pdflatex` twice, sending output to `work/paper/`. PDF bytes may differ
across engines. Certificate checks do not need a TeX installation.

Tatsuhiko Takimoto. Package version **1.1.0**; article **Version 1.3**.
See [CITATION.cff](CITATION.cff). Code is Apache-2.0; original prose, data and
proof certificates are CC BY 4.0. Full license texts and third-party boundaries
are in [LICENSE](LICENSE). Version 1.0.0 remains archived unchanged. Version 1.1.0 is prepared locally
and has not been pushed or published.
