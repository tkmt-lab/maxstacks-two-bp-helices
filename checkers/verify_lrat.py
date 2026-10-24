#!/usr/bin/env python3
"""Stream archived LRAT into an explicitly selected checker; fail closed.
SPDX-License-Identifier: Apache-2.0
"""
from core import *
import argparse, subprocess, time, datetime, resource, sys

def replay(binary,cnf,proof,meta,label,heap):
    assert sha(cnf)==meta['cnf_sha256'], 'CNF hash mismatch'
    assert sha(proof)==meta['gzip_sha256'] and proof.stat().st_size==meta['gzip_bytes'], 'Gzip hash mismatch'
    out=ROOT/'work'/'lrat';out.mkdir(parents=True,exist_ok=True)
    command=[str(binary),f'--CML_HEAP_SIZE={heap}','--CML_STACK_SIZE=128',str(cnf),'/dev/stdin']
    start=time.monotonic(); stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    h=hashlib.sha256(); size=sent=0; broken=False
    stdout=out/(label+'.stdout.txt');stderr=out/(label+'.stderr.txt')
    with stdout.open('wb') as so,stderr.open('wb') as se:
        proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=so,stderr=se)
        try:
            with gzip.open(proof,'rb') as f:
                for block in iter(lambda:f.read(65536),b''):
                    h.update(block);size+=len(block)
                    if not broken:
                        try:
                            proc.stdin.write(block);proc.stdin.flush();sent+=len(block)
                        except BrokenPipeError: broken=True
            try: proc.stdin.close()
            except BrokenPipeError: broken=True
            rc=proc.wait()
        except BaseException:
            proc.terminate();proc.wait();raise
    raw_ok=(h.hexdigest()==meta['raw_sha256'] and size==meta['raw_bytes'])
    verified='s VERIFIED UNSAT' in stdout.read_text().splitlines()
    ok=rc==0 and verified and raw_ok and not broken and sent==size
    result={'status':'PASS' if ok else 'FAIL','label':label,'started_utc':stamp,
        'seconds':time.monotonic()-start,'returncode':rc,'exact_success_line':verified,
        'raw_sha256':h.hexdigest(),'raw_bytes':size,'bytes_sent':sent,'broken_pipe':broken,
        'checker_sha256':sha(binary),'cnf_sha256':sha(cnf),'gzip_sha256':sha(proof),
        'command':[binary.name,*command[1:3],cnf.name,'/dev/stdin'],
        'child_maxrss':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'maxrss_unit':'bytes' if sys.platform=='darwin' else 'KiB'}
    (out/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(label,result['status'],f"{result['seconds']:.3f}s",flush=True)
    assert ok, result
    return result

def controls(binary):
    out=ROOT/'work'/'lrat-controls';out.mkdir(parents=True,exist_ok=True)
    cnf=out/'xor.cnf';cnf.write_text('p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n')
    good=b'5 1 0 1 2 0\n6 -1 0 3 4 0\n7 0 5 6 0\n'
    bad=good.replace(b'7 0 5 6 0',b'7 0 5 0')
    for label,raw in [('control-valid',good),('control-invalid',bad)]:
        proof=out/(label+'.lrat.gz');proof.write_bytes(gzip.compress(raw,mtime=0))
        meta={'cnf_sha256':sha(cnf),'gzip_sha256':sha(proof),'gzip_bytes':proof.stat().st_size,
              'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw)}
        if label=='control-valid':replay(binary,cnf,proof,meta,label,64)
        else:
            try:replay(binary,cnf,proof,meta,label,64)
            except AssertionError:
                record=json.loads((ROOT/'work/lrat/control-invalid.json').read_text())
                assert not record['exact_success_line'] and record['raw_sha256']==meta['raw_sha256']
                print('Invalid hint control rejected (exit code alone is not acceptance)',flush=True)
            else:raise AssertionError('Invalid hint control accepted')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--checker',type=Path,required=True)
    ap.add_argument('--scope',choices=['U14','D13'],required=True)
    ap.add_argument('--large-dir',type=Path)
    a=ap.parse_args();binary=a.checker.resolve();m=manifest();results=[]
    if a.scope=='U14':
        controls(binary)
        for c in m['D_ge_14']['cases']:
            i=c['index'];meta={k:c['proof_'+k] for k in ['gzip_sha256','gzip_bytes','raw_sha256','raw_bytes']}
            meta['cnf_sha256']=c['cnf_sha256']
            results.append(replay(binary,SCRATCH/f'U14-case-{i:02}.cnf',ROOT/c['proof_path'],meta,f'U14-{i:02}',512))
    else:
        if a.large_dir is None: ap.error('--large-dir is required for D13')
        meta=json.loads((ROOT/'data/large-proofs.json').read_text())['LRAT'];meta['cnf_sha256']=m['D13']['cnf_sha256']
        results.append(replay(binary,SCRATCH/'D13-rebuilt.cnf',a.large_dir/meta['path'],meta,'D13',4096))
    (ROOT/'work'/'lrat'/(a.scope+'-summary.json')).write_text(json.dumps({'status':'PASS','cases':results},indent=2)+'\n')

if __name__=='__main__': main()
