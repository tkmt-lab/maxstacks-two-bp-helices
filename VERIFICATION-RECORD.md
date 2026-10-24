# Verification record

Author: Tatsuhiko Takimoto. Package assembly: literature-role Codex, 24 October
2026 JST. Original article input revision: `bb2e15b71` (draft v1). The current
article is Version 1.2, edited from research revision `1dc1d3883` (draft v1.1).
Version 1.2 changes the version label, clarifies definitions and actual package references, and adds the separate D=25 witness footnote; the theorem, proof, tables and certificate hashes are unchanged.
No maximum-25, exclusion-above-25 or priority claim is included.
Packaging is subsequent integration with research and verification records
available. It is not a new blind derivation or independent human review.

The v1.1 Scope addition received one fresh AI reading with only its PDF, TeX
and v1-to-v1.1 diff: ACCEPT for overclaiming and ACCEPT for distinguishing
the variant from the fixed-family bound 12. This reading did not independently
verify the D=25 design; that observation is outside this package's certificates.

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
| Verification Codex, R004 | 08:19–09:20 | Separately implemented model, DP, rivals, whole CNFs, coverage, symmetry and UCP; geometric argument read; full-F DRAT accepted in 2,197.75 s. |
| Research Codex | Before article v1 | DRAT-to-LRAT conversion and official cake_lpr acceptance of original F and all 34 U14 cases. D13 combined pipeline 2,281.960 s. |
| RNA subleader, Claude | 09:43–09:47 | Own official checker build, all 34 U14 LRATs and stored D13 LRAT replay, 209.90 s, peak RSS 4,296,015,872 bytes. |
| Literature Codex | Before package assembly | Article v1 preparation and visual checks of all 10 pages. An authorized fresh AI reader accepted four manuscript-review categories. No new computations in that editorial task. |

R004 received seven designated claim inputs (README, statement, SPEC, upper-bound
argument, two rival lists and manifest) plus named CNF/proof paths. It did not
read the producer's code/results or coordinating check code. It used the public
drat-trim implementation; agreement of the three DRAT runs is not three separate
checker implementations. R004 did not run cake_lpr. Its wall applies to that
earlier run, not this integrated package. Source code hashes and adaptations
are listed in PROVENANCE.json.

The final R004 drat-trim revision was `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
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
The final manifest and file inventory are checked separately. Linux x64 CI
is specified but has not run on a hosted service. Stored reports document
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
