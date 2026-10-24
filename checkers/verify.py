#!/usr/bin/env python3
"""Run every small, exact package check. SPDX-License-Identifier: Apache-2.0."""
from core import *
import time
import check_finite, check_upper

def inventory():
    m=json.loads((ROOT/'manifest.json').read_text())
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and not any(s in ('.git','work','__pycache__') for s in p.relative_to(ROOT).parts)
            and p.name not in ('manifest.json','.DS_Store')}
    assert actual=={r['path'] for r in m['files']}, 'File set differs from manifest'
    for r in m['files']:
        p=ROOT/r['path']; assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'], r['path']
    for r in m['expanded_gzip']:
        h=hashlib.sha256(); size=0
        with gzip.open(ROOT/r['path'],'rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''):
                h.update(block); size+=len(block)
        assert h.hexdigest()==r['raw_sha256'] and size==r['raw_bytes'], r['path']
    return len(m['files'])

def main():
    t=time.monotonic(); count=inventory(); print('File and expanded gzip hashes PASS',count,flush=True)
    check_finite.run(); check_upper.run()
    save('verification.json',{'status':'PASS','files_checked':count,'elapsed_seconds':time.monotonic()-t,
        'scope':'Hashes, exhaustive small DP controls, D12, rivals, exact F/U14 reconstruction, all case hashes, family generation, word coverage, symmetries, finite mapping supplements, UCP traces.',
        'excludes':'LRAT replay and general-D geometric proof; run verify_lrat.py and read the article.'})
    print('PASS: all light checks; LRAT replay is a separate command.',flush=True)

if __name__=='__main__': main()
