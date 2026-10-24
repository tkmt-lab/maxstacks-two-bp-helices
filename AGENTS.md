# Entry point for a computational reader

Read README.md, claims.json, claims/STATEMENT-A.md and VERIFICATION-RECORD.md.
The article is paper/paper-v1.pdf with unchanged draft-v1 TeX alongside it.
Run python3 -B checkers/verify.py, then build the pinned official checker and
run checkers/verify_lrat.py as documented. Python 3.11+, standard library.
Optimized Python is refused. Generated files belong in ignored work/.

Preserve the fixed target family, j-i>=2, one-base hairpins, no isolated pairs,
GU compatibility and unique stack-maximization definition. Do not infer all
D<=12 are designable or extrapolate to arbitrary RNA trees, usual three-base
hairpins, Turner energies or experimental RNA. Credit Boury, Bulteau and Ponty.

Keep evidence distinct: DP and finite Python checks; accepted full-F LRAT;
U14 case coverage and LRATs; normalization and the general geometric proof.
The Python code is not formally verified. cake_lpr's theorem is about parsed
CNF unsatisfiability under the recorded trust boundary. Package assembly is
subsequent integration of a previously separate check, not new blind review.
No priority or human peer-review claim is authorized by passing these programs.

Large D13 proofs are separate from Git; stream them without expansion to disk.
Do not publish, upload, contact others or create remote repositories without
the author's instruction. A local commit or metadata does not imply publication.

For intentional edits, inspect diffs, then refresh manifest.json using
python3 -B tools/update_manifest.py and rerun relevant checks. Do not change
expected hashes just to suppress unexplained failures. Keep the exact success
line s VERIFIED UNSAT, normal exit, complete delivery and hash checks together.
