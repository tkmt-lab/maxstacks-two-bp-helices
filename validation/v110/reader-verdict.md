> Historical record: 28 October 2026 review. Statements about preparation
> and acquisition describe that input; see the main README for current use.

> Historical review record (28 October 2026), referring to the then-supplied
> package. Current acquisition instructions are in the root README.md.

**Overall: MINOR.** The scope and model distinctions are clear. Two reproduction clarifications remain. This is a six-file textual audit, not independent mathematical verification.

| Requested assessment | Verdict | Reason |
|---|---|---|
| **1. Overclaiming** | **ACCEPT** | §9 explicitly says the three-base-hairpin designs are “as lower bounds only.” The maximum-25 footnote says, “This result is separate from the theorem of this article.” Both READMEs agree. No change needed. |
| **2. `j-i>=2` versus `j-i>=4`, including competitors** | **ACCEPT** | §2 applies gap 2 to every legal structure, including competitors. The supplement assigns each family its gap and explicitly states: “In each row, **every competitor pair** obeys that row's gap.” No change needed. |
| **3. Reproduction instructions** | **MINOR** | Commands, prerequisites, outputs and acceptance criteria are substantially documented. Acquisition instructions and the DRAT warning policy need clarification below. |

- **Ambiguous DRAT replay instructions** — [variants-README.md, lines 73–76](../../variants/README.md):

  > “The runner checks both the unchanged binary DRAT and `proof-deduplicated.drat` with `-W -p -U` (warnings are errors, retain deleted clauses, require RUP), plus a rejected empty DRAT.”

  This conflicts with the immediately following statement:

  > “The supplied binary proof has duplicate-literal warnings; the normalized text copy has none.”

  **Minimal change:** specify flags and expected outcomes separately for the two files. If only the normalized proof receives the strict flags, say so explicitly. The present wording leaves readers unsure whether binary-proof rejection is expected.

- **Acquisition route remains undocumented** — [README.md, lines 118–120](../../README.md):

  > “The large proofs will be distributed separately as release attachments.”

  > “This local v1.1.0 preparation has no new release identifier.”

  The only archive link identifies v1.0.0; no acquisition route for the current supplement is documented. This is understandable for an explicitly unpublished preparation, but public reproduction is not yet documented end to end.

  **Minimal change:** add current-package and companion-proof download locations when released. Meanwhile, align Appendix A’s “The large proofs **are distributed** separately as release attachments” with the README’s stated availability.

These are consequential documentation issues; neither establishes a checker defect or a mathematical error.