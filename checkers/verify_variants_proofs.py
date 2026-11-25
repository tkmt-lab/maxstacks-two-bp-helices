#!/usr/bin/env python3
"""Replay only the tiny A26 certificates; does not run the large D13 proof.
SPDX-License-Identifier: Apache-2.0
"""
from core import *
import argparse,subprocess,time


def run(checker,drat=None):
    v=ROOT/'variants/A26';out=ROOT/'work/variants-proofs';out.mkdir(parents=True,exist_ok=True)
    meta=json.loads((v/'normalization.json').read_text())
    for name,h in meta['distributed_sha256'].items(): assert sha(v/name)==h,name
    def invoke(label,command,marker,positive=True):
        start=time.monotonic();p=subprocess.run(command,capture_output=True,text=True,timeout=120)
        (out/(label+'.stdout.txt')).write_text(p.stdout);(out/(label+'.stderr.txt')).write_text(p.stderr)
        found=marker in p.stdout.splitlines()
        result={'label':label,'returncode':p.returncode,'exact_success_marker':found,'expected_marker':marker,
                'expected_accept':positive,'seconds':time.monotonic()-start,'command':command}
        # A rejected proof may exit 0. No signal/timeout is counted as a negative control.
        assert (p.returncode==0 and found) if positive else (p.returncode>=0 and not found),result
        return result
    results=[]
    results.append(invoke('A26-cake',[str(checker),'--CML_HEAP_SIZE=256','--CML_STACK_SIZE=64',str(v/'input.cnf'),str(v/'proof.lratb')],'s VERIFIED UNSAT'))
    empty=out/'empty.lrat';empty.write_bytes(b'')
    results.append(invoke('A26-cake-empty-control',[str(checker),'--CML_HEAP_SIZE=64','--CML_STACK_SIZE=64',str(v/'input.cnf'),str(empty)],'s VERIFIED UNSAT',False))
    if drat:
        results.append(invoke('A26-supplied-DRAT',[str(drat),str(v/'input.cnf'),str(v/'proof.drat'),'-t','60'],'s VERIFIED'))
        results.append(invoke('A26-normalized-RUP',[str(drat),str(v/'input.cnf'),str(v/'proof-deduplicated.drat'),'-W','-p','-U','-t','60'],'s VERIFIED'))
        assert 'WARNING' not in (out/'A26-normalized-RUP.stdout.txt').read_text()
        empty_drat=out/'empty.drat';empty_drat.write_bytes(b'')
        results.append(invoke('A26-DRAT-empty-control',[str(drat),str(v/'input.cnf'),str(empty_drat),'-t','60'],'s VERIFIED',False))
    result={'status':'PASS','checker_sha256':sha(checker),'drat_checker_sha256':sha(drat) if drat else None,
            'CNF_sha256':sha(v/'input.cnf'),'proof_sha256':sha(v/'proof.lratb'),'results':results,
            'scope':'Parsed CNF UNSAT. RNA correspondence uses prose and separate finite reconstruction, not cake_lpr.'}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: A26 certificates and rejection controls; no D13 replay.',flush=True)
    return result

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--checker',type=Path,required=True);a.add_argument('--drat',type=Path)
    args=a.parse_args();run(args.checker.resolve(),args.drat.resolve() if args.drat else None)
