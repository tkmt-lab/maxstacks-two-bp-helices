# Separate D13 certificates

Companion to maxstacks-two-bp-helices version 1.0.0. These eight files are outside
Git. They were placed by APFS clone; do not edit them in place. Original proof
certificates: copyright 2026 Tatsuhiko Takimoto, CC BY 4.0. The full license is
in the companion repository's CC-BY-4.0.txt. This is local preparation, not a
published deposit. Attachment splitting, identifiers and release require the
author's decision.

| File (DRAT in exact order, then LRAT) | Compressed bytes | SHA256 |
|---|---:|---|
| 01-input-deletions.drat.gz | 1626412 | `8cd9d1293303634532f638f2df56f28407286b5534789ded58eebc30d3562955` |
| 02-common.drat.gz | 49750 | `a42d0a1bcaedf8307d9ac0dc8a44eff91c8f783e35089aba0b0630d9bdbd8186` |
| 03-definitions-without-cases.drat.gz | 24704 | `2e2a9daa7c7880e182804747e8896b47f44bf97ad748071636582a0f25da0840` |
| 04-relations.drat.gz | 121670 | `eeb72b061c5126ecd3c72005e85d8c1bbdca0a383266fb11ffc69a1b08d444ef` |
| 05-context-cases.drat.gz | 563269 | `74c2148bbb15b760fc7cbb0eecdc9abc984bc28910b77522af30c9f3742ea150` |
| 06-physical-cases.drat.gz | 566266527 | `89a67464e2ec2877bf5d8dabf704d1e0c9bebd7ae86f03b110e817983e6368df` |
| 07-proof.drat.gz | 45279262 | `2e47e0403dabb096ea5dad688b1c4d3ad0655e4b7501510b7c9ad869e3e843af` |
| D13.lratb.gz | 1598317453 | `8705abc77e86aa52856ef6c36f4bc01037693e7ef57fda96e0bf48f56cbc523a` |

Expanded DRAT concatenation: 2,049,035,259 bytes, SHA256
`ef0a5a3cd19984a3f8973740d247ea229c57044a39d8b4068895e3493b0aa116`.
Expanded LRAT: 5,428,472,887 bytes, SHA256
`9b54d5df00f8db04a2d9d51688175ed75df683e54839c28db56fda714fddbd91`.
Per-part expanded hashes are in large-proofs.json. All files refer to original
F, SHA256 `4f8100bbe4362bf45db9b4be068eb115bf1c48c3f556ce5c3bceff1e7f5a4a6c`.

From the companion repository root, first run the light checks and build the
pinned official checker. Then:

```sh
nice -n 10 python3 -B checkers/verify_lrat.py --checker work/cake_lpr/cake_lpr \
  --scope D13 --large-dir ../maxstacks-two-bp-helices-large
```

The runner streams without writing the expanded file, with heap 4096 MB and
stack 128 MB. Require normal termination, exact `s VERIFIED UNSAT`, complete
stream delivery, and compressed/raw hash agreement. Exit 0 alone is insufficient.
The direct command, after verifying hashes, is:

```sh
set -o pipefail
nice -n 10 gzip -dc ../maxstacks-two-bp-helices-large/D13.lratb.gz |
  nice -n 10 work/cake_lpr/cake_lpr --CML_HEAP_SIZE=4096 --CML_STACK_SIZE=128 \
    work/checks/D13-rebuilt.cnf /dev/stdin
```

Optional binary DRAT replay, with assertions-enabled drat-trim revision
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` already built as `drat-trim-assertions`:

```sh
set -o pipefail
nice -n 10 gzip -dc ../maxstacks-two-bp-helices-large/01-input-deletions.drat.gz ../maxstacks-two-bp-helices-large/02-common.drat.gz ../maxstacks-two-bp-helices-large/03-definitions-without-cases.drat.gz ../maxstacks-two-bp-helices-large/04-relations.drat.gz ../maxstacks-two-bp-helices-large/05-context-cases.drat.gz ../maxstacks-two-bp-helices-large/06-physical-cases.drat.gz ../maxstacks-two-bp-helices-large/07-proof.drat.gz |
  nice -n 10 ./drat-trim-assertions work/checks/D13-rebuilt.cnf -i -f -t 10800 -w
```

The seven decompressed parts must form one stream in the listed order. Require
normal pipeline termination and drat-trim's `s VERIFIED` success output, plus
matching whole-stream hash. This optional run takes about 35 minutes in the
prior record. Package assembly checks its hashes but does not rerun it.
