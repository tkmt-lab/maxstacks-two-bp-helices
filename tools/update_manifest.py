#!/usr/bin/env python3
"""Refresh hashes after an intentional reviewed change. SPDX-License-Identifier: Apache-2.0."""
from pathlib import Path
import json,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
    files=[];expanded=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if not p.is_file() or any(s in ('.git','work','__pycache__') for s in rel.parts) or p.name in ('manifest.json','.DS_Store'):continue
        raw=p.read_bytes();files.append({'path':rel.as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        if p.suffix=='.gz':
            plain=gzip.decompress(raw);expanded.append({'path':rel.as_posix(),'raw_bytes':len(plain),'raw_sha256':hashlib.sha256(plain).hexdigest()})
    m={'schema':'maxstacks.manifest.v1','version':'1.0.0','files':files,'expanded_gzip':expanded,
       'total_bytes_without_manifest':sum(f['bytes'] for f in files),
       'large_proofs':json.loads((ROOT/'data/large-proofs.json').read_text()),
       'large_location':'Separate companion directory or archive; see README.md. Not in Git.',
       'success_criteria':{'LRAT':'Exact stdout line s VERIFIED UNSAT, normal exit 0, full stream delivery and matching compressed/raw hashes; exit 0 alone is insufficient.',
                           'light':'Normal exit 0 and work/checks/verification.json status PASS.'},
       'manifest_self_hash':'Excluded to avoid self-reference; Git records manifest.json. All other distributable files are listed.'}
    (ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
if __name__=='__main__':main()
