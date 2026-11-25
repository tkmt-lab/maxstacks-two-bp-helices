#!/usr/bin/env python3
"""Build unmodified pinned official DRAT-trim source; no installed service.
SPDX-License-Identifier: Apache-2.0
"""
from pathlib import Path
import hashlib,subprocess,urllib.request,json
ROOT=Path(__file__).resolve().parents[1]
REV='2e3b2dc0ecf938addbd779d42877b6ed69d9a985'
SOURCE_SHA256='d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee'
def main():
    out=ROOT/'work/drat-trim';out.mkdir(parents=True,exist_ok=False)
    raw=urllib.request.urlopen('https://raw.githubusercontent.com/marijnheule/drat-trim/'+REV+'/drat-trim.c',timeout=60).read()
    assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA256
    source=out/'drat-trim.c';source.write_bytes(raw);binary=out/'drat-trim'
    cmd=['cc','-std=c99','-O2',str(source),'-o',str(binary)]
    subprocess.run(cmd,check=True)
    (out/'build.json').write_text(json.dumps({'revision':REV,'source_sha256':SOURCE_SHA256,'command':cmd,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'assertions_enabled':True},indent=2)+'\n')
    print(binary)
if __name__=='__main__':main()
