# Verification record

Author: Tatsuhiko Takimoto. Package assembly: literature-role Codex, 24 October
2026 JST. Original article input revision: `bb2e15b71` (draft v1). The current
article is Version 1.4. The following Version 1.2 notes are historical;
Version 1.2 was edited from research revision `1dc1d3883` (draft v1.1).
Version 1.2 changes the version label, clarifies definitions and actual package references, and adds the separate D=25 witness footnote; the theorem, proof, tables and certificate hashes are unchanged.
No maximum-25, exclusion-above-25 or priority claim was included in Version 1.2.
Packaging is subsequent integration with research and verification records
available. It is not a new blind derivation or independent human review.

The v1.1 Scope addition received one fresh AI reading with only its PDF, TeX
and v1-to-v1.1 diff: ACCEPT for overclaiming and ACCEPT for distinguishing
the variant from the fixed-family bound 12. This reading did not independently
verify the D=25 design; that observation was outside the v1.0.0 package's certificates.

## Editorial revision (6 November 2026)

The current Version 1.4 retains its manuscript date of 5 November 2026.
The editorial revision moves explicit thanks to the README, groups the
current assurance in article Section 7 and moves the detailed verification
workflow here. The separate variant is described as a completed supplement.
The theorem, definitions, proof arguments, tables, sequences, mathematical
code, input data and certificates are unchanged. The current TeX/PDF and
historical v1.3-to-v1.4 diff are identified in PROVENANCE.json. The current
distribution is hashed by manifest.json.

The separate model-verification implementation used the statement, model
and CNF specifications, auxiliary embedding description, rival lists and
certificate manifest. Producer generation code, auxiliary proof-lifting
explanation, prior check results and the coordinator's implementation were
withheld. Public checker documentation and parser source were available.
It recovered the 71-base design, checked every rival, regenerated both input
CNFs byte for byte and all seven auxiliary rival families, checked word-set
coverage and full-formula symmetries, and reproduced the 34 contradictions.
It checked the seven-part proof hashes and complete raw stream, accepted
the D13 DRAT refutation and reviewed the embedding family by family.

The three initial DRAT runs used the same public drat-trim implementation.
The separate model-verification implementation did not run cake_lpr.
Other runs built cake_lpr separately and replayed the stored LRAT certificates
without rerunning their converter, obtaining the same success result.
For U14, drat-trim accepts by unit propagation on the inputs, so this does
not establish that every supplied DRAT addition was exercised. Separate
propagation traces and replay check the finite step as well.

As of 5 November 2026, hosted CI had not run for package 1.1.0.
The earlier package checks are local results, not hosted CI results.

## Distribution cleanup (6 November 2026)

The distribution contains only the current Version 1.4 article. Earlier
manuscripts and their diffs remain byte-for-byte in Git history at package
commit `54b3f751c0290ca38bf71569bcbd81161369c0af`; PROVENANCE.json
records their historical paths and hashes. This preserves the original
manuscripts, including their draft labels, outside the current file inventory.
The historical reader reports in `validation/v110/` describe the
28 October review, not the current acquisition instructions.

Public source IDs replace private source paths in provenance records and
design metadata. Original input hashes are preserved; checker changes only
replace the introductory source attribution. The mathematical algorithms,
sequences, structures, formulas and proof certificates are unchanged.
The current PDF was rebuilt from the unchanged Version 1.4 TeX.

## Article 1.4 (5 November 2026; before the editorial revision)

A blind reading of the Version 1.3 article alone found no counterexample to
the mathematical reductions and independently reproduced the 71-base design
result and the 32-vertex graph counts; it asked for a retrievable permanent
package reference, a publication identifier for the separate maximum-25
result, and a short mathematical reason for the U14 clause symmetries.
Version 1.4 adds these three items (Appendix A, the D=25 footnote and
Section 5.2). The historical `paper/v1.3-to-v1.4.diff` also includes
the editorial revision described above. Theorem, proofs, tables, data, certificates and checkers are
unchanged, so the package checks below still apply.

## Package 1.1.0 / article 1.3 (28 October 2026)

The article edit is limited to version/date metadata, the D25 footnote's
reference to the variants supplement, and one Scope sentence pointing to
the three-base-hairpin lower designs; the sequence, theorem, proof and tables
are unchanged. The historical `paper/v1.2-to-v1.3.diff` gives the exact textual change.

The separately scoped supplement checks A25 at gap 2, a16 and b21 at gap 4.
Its positive results are optimum D, exact count one and target equality.
For gap 4, all 87,381 sequences through length 8 and 512 seeded samples
through length 12 are compared to generic exhaustive structural enumeration;
gap 2 uses 5,461 exhaustive and 768 seeded sequences, also compared to the
existing core DP. All 1,024 adjacent-state cases are checked exhaustively.
The CNF-free A25 upper reconstruction excludes all 68*1,267=86,156 set
pairs: 64,260 by degree three, 21,896 by an edge forbidden in both orders.

The CNF normalization removes 25 repeated literals from 25 clauses, preserving
all 5,608 clause numbers and the 930 variables. On that normalized CNF,
the unchanged supplied binary DRAT passes official DRAT-trim (exact line
`s VERIFIED`); the unchanged binary LRAT passes pinned official cake_lpr
(exact line `s VERIFIED UNSAT`, exit 0). A text DRAT copy removes 25 repeated
literals in 25 of 4,990 steps and additionally passes `-W -p -U` without
warnings. The raw DRAT's duplicate warnings are not hidden. Empty DRAT
and LRAT controls are rejected; the LRAT control exits 0 and has no success
line. No solver proof regeneration is needed. Source revisions and input
hashes are in `variants/PROVENANCE.json` and `variants/A26/normalization.json`.

The earlier independent A25 verification established the positive design
and the finite upper argument without interpreting this CNF. This package's
integration uses both sides' records and is not a new blind verification.
Cake_lpr checks parsed CNF UNSAT, not the RNA mapping; the package's separate
finite enumeration and prose provide that upper argument. No complete
variable-level reconstruction of the archived A26 CNF is represented here.
The fresh manuscript reading and fresh-clone measurements are in
`validation/v110/`. The fresh clone of `20db8d3de2a85b7ecd948ec2c671de7a309f4f10`
passed all light checks (106 files, 14.784 s; peak RSS 305,397,760 bytes).
It rebuilt pinned cake_lpr in 1.77 s and pinned DRAT-trim in 0.54 s, then
passed the three positive proof replays and two rejection controls in 0.74 s
(peak RSS 50,741,248 bytes). All 34 original U14 LRATs and their valid/invalid
hint controls also passed. The package CFF passed the official 1.2.0 schema.
Later changes add these records and clarify documentation; the tested
mathematical code, inputs and proofs are unchanged.

The one fresh manuscript reader returned ACCEPT for scope and models,
MINOR for reproduction, MAJOR 0. Two minor documentation comments were
applied: checker-specific DRAT flags and the actual acquisition routes.
The PDF/TeX were unchanged after that reading. At the 28 October 2026 review,
a version-specific v1.1.0 download link was still a release-maintainer action;
the supplied input was a local repository with a fresh-clone command. For the
current versioned acquisition route, see README.md. No new D13 replay was part
of that revision. No maximum is asserted for the gap-4 families.

## Version 1.2 preparation checks

One fresh AI reader received only the Version 1.2 PDF, TeX, v1.1-to-v1.2 diff
and package filename list. It returned ACCEPT for overclaiming, Appendix A
filename consistency and preservation of the central mathematical claims.
The D=25 existence statement was already present in v1.1; the new footnote
adds a particular sequence and target assertion, not a maximum or priority claim.
This reading did not independently verify that witness and is not human review.

A fresh local clone of `42ed28212b18871a88a432f55ff26b620d5ea4ec` passed every
light check (85 files; 13.054 seconds) and all 34 U14 LRATs, with the valid and
missing-hint controls (2.709 seconds). The already pinned official ARM checker
executable was reused after checking its SHA-256; it was not rebuilt for this
revision. All eight compressed D13 proof files matched their recorded sizes and
SHA-256 hashes. No new D13 DRAT or LRAT replay was performed for Version 1.2.
The theorem, checker programs, mathematical data and proof files are unchanged.

## Prior evidence used by the article

| Role | Date/time (JST, 24 October 2026 unless noted) | Scope |
|---|---|---|
| Research Codex | 23–24 October; final DRAT accepted 07:22 | D12 design, rivals, formulas, coverage and proofs. Original full-F binary DRAT accepted in 1,998.526 s. |
| RNA subleader, Claude | Review logged 08:08 | Separate F/rival reconstruction, fresh public-checker build and full DRAT replay in about 1,947 s; earlier design and upper-bound checks. |
| Verification Codex | 08:19–09:20 | Separately implemented model, DP, rivals, whole CNFs, coverage, symmetry and UCP; geometric argument read; full-F DRAT accepted in 2,197.75 s. |
| Research Codex | Before article v1 | DRAT-to-LRAT conversion and official cake_lpr acceptance of original F and all 34 U14 cases. D13 combined pipeline 2,281.960 s. |
| RNA subleader, Claude | 09:43–09:47 | Own official checker build, all 34 U14 LRATs and stored D13 LRAT replay, 209.90 s, peak RSS 4,296,015,872 bytes. |
| Literature Codex | Before package assembly | Article v1 preparation and visual checks of all 10 pages. An authorized fresh AI reader accepted four manuscript-review categories. No new computations in that editorial task. |

The separate verification received seven designated claim inputs (README, statement, SPEC, upper-bound
argument, two rival lists and manifest) plus named CNF/proof paths. It did not
read the producer's code/results or coordinating check code. It used the public
drat-trim implementation; agreement of the three DRAT runs is not three separate
checker implementations. The separate verification did not run cake_lpr. Its access boundary applies to that
earlier run, not this integrated package. Source code hashes and adaptations
are listed in PROVENANCE.json.

The final drat-trim revision for the separate verification was `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
source SHA256 `d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
It was compiled with assertions enabled, using Apple clang 21.0.0, and run in
binary forward mode (`-i -f`). Earlier parser-invocation and interrupted runs
were not used as accepted evidence. The assertions-enabled final executable
SHA256 was `de81b70c4ea5f2ac2c4356542c22365e2ef1470af675abf4c162a42fc760fe37`.

## Package validation

The package checks reproduce the D12 result, all rival and formula checks,
U14 family reconstruction, coverage, symmetries, UCP and finite mapping supplements.
All original large gzip hashes and the expanded concatenated DRAT hash were
rechecked after APFS clone placement. This packaging task does not rerun DRAT.
The fresh local clone of `57f66b8` passed all light checks in 12.764 seconds.
It fetched and built the pinned official ARM checker in 1.711 seconds. All 34
U14 LRATs passed in 2.218 seconds total; the valid control passed and the missing-
hint control was rejected even though it exited 0. Optimized Python was refused.

The same clone replayed the stored D13 LRAT in 223.154 seconds, with peak child
RSS 4,295,933,952 bytes, a 4,096 MB heap and 128 MB stack. It delivered all
5,428,472,887 raw bytes, matched both gzip/raw hashes and obtained the exact
success line with normal exit 0. The run began at `2026-10-24T01:31:46.504302+00:00`.
No other heavy package check ran concurrently. The six checkers and all
mathematical inputs remain unchanged from the validated clone.

Detailed records are in [validation/summary.json](validation/summary.json).
`control-invalid.json` intentionally records FAIL for a rejected proof; this
is the expected negative control, not a failed theorem certificate. Final
package changes add documentation, manifest maintenance and these records.
The final manifest and file inventory are checked separately. As of the 24 October 2026 package validation, Linux x64 CI
was specified but had not run on a hosted service. Stored reports document
execution; rerun the commands for a new machine's check.

## Official checker and remaining trust

Pinned cake_lpr: `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa`, from
https://github.com/tanyongkiam/cake_lpr . The build script uses the unmodified
Makefile and precompiled assembly, plus its C FFI wrapper. The ARM assembly
SHA256 is `95b64883edc0cb09feedbcb1ebec233e2490f5b458fdda9dc29c212ed916f00c`.
The actual pinned C-wrapper SHA256 is
`8e30d84fdcb2177aa5571d7fa6661a2fae5ecfd56baa0ce49c65f9233a9f87cb`.
The wrapper's entry in upstream cake_lpr.sha256 is stale at this revision;
the build script requires equality with the pinned Git blob and actual hash.

Pinned HOL4: `0ae7030322cdf2b0d46dc9d5503e2d5eae2fa726`.
Pinned CakeML: `fb377b4bb704497c921cde68ccc8da3b4f0e9132`.
The ARM theorem `lpr_arrayProofARM8.machine_code_sound`, with compilation theorem
`lpr_arrayCompileARM8.lpr_array_compiled`, links successful ordinary two-argument
checker execution to the parsed CNF's unsatisfiability under its execution,
FFI and filesystem assumptions. See the [formal source](https://github.com/CakeML/cakeml/blob/fb377b4bb704497c921cde68ccc8da3b4f0e9132/examples/lpr_checker/array/compilation/proofsARM8/lpr_arrayProofARM8Script.sml)
and [CakeML checker description](https://cakeml.org/checkers.html).

HOL4/CakeML proofs and distributed assembly were not rebuilt from the formal
sources here. Trust remains in HOL4's logic/kernel and formal semantics,
the architecture model's correspondence to the machine, distributed assembly
provenance, C FFI, compiler/assembler/linker, OS, I/O and hardware. The CI x64
path uses the upstream x64 build; an ARM run is not a local x64 execution test.
The solver and conversion program do not enter the accepted LRAT's UNSAT
implication. The runner requires the exact line `s VERIFIED UNSAT`, normal
exit, full delivery and matching hashes. A nontrivial four-clause control
checks a valid LRAT and rejection after removing a required conflict hint.

This does not formally prove the Python programs, RNA model correspondence,
normalization, unique-decomposition DP, word-case coverage or general-D mapping.
The 50,199 finite mapped rivals supplement the prose geometric proof, not replace it.
Attribution and exclusions remain those of the article and claim documents;
no complete priority search, external publication or human review is claimed.
