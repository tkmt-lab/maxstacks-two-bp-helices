#!/usr/bin/env python3
"""Build official pinned assembly and C wrapper. No HOL/CakeML proof rebuild.
SPDX-License-Identifier: Apache-2.0
"""
from pathlib import Path
import subprocess,json,hashlib,platform,time,datetime
ROOT=Path(__file__).resolve().parents[1]
REV='a36874a8b750b43fe4b385b8ddbf5b033e46a3fa'
EXPECTED={'Makefile':'57f5c407a9274560d8cfe31d60ee8095ac4a8046bbe960b9d706d37006d3ba10',
'basis_ffi.c':'8e30d84fdcb2177aa5571d7fa6661a2fae5ecfd56baa0ce49c65f9233a9f87cb',
'cake_lpr.S':'2f3af32d55083839b3fa0e693afd817679c0b8944bef41def05a8b0ec72b7d4a',
'cake_lpr_arm8.S':'95b64883edc0cb09feedbcb1ebec233e2490f5b458fdda9dc29c212ed916f00c'}
def main():
    if not __debug__: raise RuntimeError('Do not use optimized Python')
    d=ROOT/'work/cake_lpr';d.mkdir(parents=True,exist_ok=False)
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    log=ROOT/'work/cake-build.log'
    with log.open('w') as f:
        def run(cmd):
            f.write('$ '+' '.join(cmd)+'\n');f.flush()
            return subprocess.run(cmd,cwd=d,stdout=f,stderr=subprocess.STDOUT,check=True)
        run(['git','init']);run(['git','remote','add','origin','https://github.com/tanyongkiam/cake_lpr.git'])
        run(['git','fetch','--depth','1','origin',REV]);run(['git','checkout','--detach',REV])
        assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()==REV
        for name,h in EXPECTED.items():
            assert hashlib.sha256((d/name).read_bytes()).hexdigest()==h,name
            assert (d/name).read_bytes()==subprocess.check_output(['git','show',f'HEAD:{name}'],cwd=d)
        arch=platform.machine().lower()
        if arch in ('arm64','aarch64'):target='cake_lpr_arm8'
        elif arch in ('x86_64','amd64'):target='cake_lpr'
        else:raise RuntimeError('Unsupported architecture: '+arch)
        run(['make','-j1',target])
    binary=d/'cake_lpr'
    assert binary.is_file()
    record={'revision':REV,'retrieved_and_built_utc':started,'seconds':time.monotonic()-t,
        'platform':platform.platform(),'target':target,'compiler':subprocess.check_output(['gcc','--version'],text=True),
        'source_hashes':EXPECTED,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),
        'binary_bytes':binary.stat().st_size,'proof_rebuild':False,
        'upstream_manifest_note':'basis_ffi.c hash in upstream cake_lpr.sha256 is stale at this commit; exact pinned git blob hash above is required.'}
    (ROOT/'work/cake-build.json').write_text(json.dumps(record,indent=2)+'\n')
    print('Built',binary,record['binary_sha256'],flush=True)
if __name__=='__main__':main()
