"""Separate min-gap variants; original T_D mathematics is unchanged.
Adapted in part from R004's separate A25 verification (see variants/PROVENANCE).
SPDX-License-Identifier: Apache-2.0
"""
from core import *
import random, time


def variant_target(family, d):
    assert d >= 3
    if family == 'A': return '((' + '((.))' * (d-1) + '))'
    if family == 'a': return '((.' + '((...)).' * (d-1) + '))'
    if family == 'b': return '((' + '((...))' * (d-1) + '))'
    raise ValueError('unknown family')


def inspect(sequence, structure, gap):
    assert gap in (2,4) and len(sequence) == len(structure)
    p = parse(structure)
    score = check_pairs(p, len(sequence))
    assert all(j-i >= gap and sequence[i]+sequence[j] in PAIRS for i,j in p)
    return score


def fold_gap(sequence, gap):
    """Exact unique maximal-helix DP with every innermost gap >= gap.

    For length L, k-i-2(L-1) >= gap, hence L <= floor((k-i-gap)/2)+1.
    As in core.fold, forbid=True prevents continuation of the chosen helix.
    """
    assert gap in (2,4) and set(sequence) <= set(ABC)
    @lru_cache(None)
    def f(i,j,forbid):
        if i>j: return 0,1,''
        score,count,rep=f(i+1,j,False);rep='.'+rep
        for k in range(i+gap+2,j+1):
            if forbid and k==j: continue
            for length in range(1,(k-i-gap)//2+2):
                if sequence[i+length-1]+sequence[k-length+1] not in PAIRS: break
                if length<2: continue
                inside=f(i+length,k-length,True);after=f(k+1,j,False)
                value=length-1+inside[0]+after[0]; ways=inside[1]*after[1]
                if value>score:
                    score,count=value,ways
                    rep='('*length+inside[2]+')'*length+after[2]
                elif value==score: count+=ways
        return score,count,rep
    answer=f(0,len(sequence)-1,False)
    f.cache_clear()
    return answer


def brute_shapes(n,gap):
    # Generic noncrossing matchings, then filter. No maximal-helix recurrence.
    return [(p,score) for p,score in legal_matchings(n) if all(j-i>=gap for i,j in p)]


def brute(sequence,shapes):
    best=-1; reps=[]
    for p,score in shapes:
        if all(sequence[i]+sequence[j] in PAIRS for i,j in p):
            if score>best: best,reps=score,[dotbracket(p,len(sequence))]
            elif score==best: reps.append(dotbracket(p,len(sequence)))
    return best,len(reps),frozenset(reps)


def dp_controls():
    counts={}
    for gap in (2,4):
        count=0
        # Exhaustive through 8 bases for gap4; gap2 through 6, then seeded 7..12.
        stop=8 if gap==4 else 6
        for n in range(stop+1):
            shapes=brute_shapes(n,gap)
            for letters in product(ABC,repeat=n):
                s=''.join(letters); a=fold_gap(s,gap); b=brute(s,shapes)
                assert a[:2]==b[:2] and a[2] in b[2],(gap,s,a,b)
                if gap==2: assert a==fold(s)
                count+=1
        rng=random.Random(17025+gap)
        for n in range(stop+1,13):
            shapes=brute_shapes(n,gap)
            for _ in range(128):
                s=''.join(rng.choices(ABC,k=n));a=fold_gap(s,gap);b=brute(s,shapes)
                assert a[:2]==b[:2] and a[2] in b[2],(gap,s,a,b)
                if gap==2: assert a==fold(s)
                count+=1
        counts[str(gap)]={'sequences':count,'exhaustive_max_length':stop,'seeded_samples_per_extra_length':128,'seeded_max_length':12}
    # Model distinction: the same target can be legal at gap2 and forbidden at gap4.
    assert inspect('AAAUU','((.))',2)==1
    try: inspect('AAAUU','((.))',4)
    except AssertionError: pass
    else: raise AssertionError('gap4 accepted a one-base hairpin')
    return counts


def independent_sets(neighbors,size):
    out=[]
    def visit(prefix,available,need):
        if need==0: out.append(tuple(prefix));return
        while available.bit_count()>=need:
            bit=available&-available;available^=bit;v=bit.bit_length()-1
            visit(prefix+[v],available&~neighbors[v],need-1)
    visit([],(1<<len(neighbors))-1,size)
    assert len(set(out))==len(out)
    return out


def upper25():
    """Reconstruct sufficient necessary conditions, without reading a CNF.

    A design's nonadjacent branch states cannot collide. Thus odd/even sets
    are independent, all cross-collisions must be adjacent along a path
    (degree<=2), and a collision forbidden in both adjacent orders is impossible.
    These conditions alone exclude every 13/12 independent-set pair.
    """
    states=[a+b+z+WC[b]+WC[a] for a,b,z in product(ABC,ABC,'AC')]
    assert len(set(states))==32
    relation=[]
    for s in states:
        relation.append([s[:2]==t[:2] or any(all(s[p+k]+t[q+2-k] in PAIRS for k in range(3)) for p,q in product(range(3),repeat=2)) for t in states])
    assert all(relation[i][i] for i in range(32))
    assert all(relation[i][j]==relation[j][i] for i,j in product(range(32),repeat=2))
    neighbors=[sum(1<<j for j in range(32) if i!=j and relation[i][j]) for i in range(32)]
    forbidden=set();pair_shapes=brute_shapes(10,2)
    for i,j in product(range(32),repeat=2):
        seq=states[i]+states[j];target='((.))((.))'
        assert inspect(seq,target,2)==2
        a=fold_gap(seq,2); b=brute(seq,pair_shapes)
        assert a[:2]==b[:2] and a[2] in b[2]
        if a[0]>2 or a[1]>1: forbidden.add((i,j))
        else: assert a==(2,1,target)
    us=independent_sets(neighbors,13);vs=independent_sets(neighbors,12)
    assert len(us)==68 and len(vs)==1267 and len(forbidden)==152
    counts=Counter(); proof_hash=hashlib.sha256()
    for ui,u in enumerate(us):
        for vi,v in enumerate(vs):
            # Side-tagging retains distinct occurrences of any shared state.
            verts=[(0,x) for x in u]+[(1,x) for x in v]
            adj={x:[y for y in verts if x[0]!=y[0] and relation[x[1]][y[1]]] for x in verts}
            reason=None
            for x in verts:
                if len(adj[x])>=3: reason=['degree3',x,adj[x][:3]];break
            if reason is None:
                for x in verts:
                    for y in adj[x]:
                        if (x[1],y[1]) in forbidden and (y[1],x[1]) in forbidden:
                            reason=['both_orders_forbidden',x,y];break
                    if reason is not None: break
            assert reason is not None,('unexcluded state pair',u,v)
            counts[reason[0]]+=1
            proof_hash.update((json.dumps([ui,vi,reason],separators=(',',':'))+'\n').encode())
    return {'status':'PASS','states':32,'offdiagonal_edges':sum(m.bit_count() for m in neighbors)//2,
        'two_branch_cases_checked_against_brute_force':1024,'forbidden_two_branch_cases':len(forbidden),
        'independent_sets_size_13':len(us),'independent_sets_size_12':len(vs),
        'all_set_pairs_excluded':len(us)*len(vs),'exclusion_counts':dict(counts),
        'exclusion_witness_stream_sha256':proof_hash.hexdigest(),'reads_CNF_or_proof':False,
        'boundary':'Prose proves normalization, local-move geometry and restriction for all D>=26; not a formal RNA proof.'}


def proof_normalization():
    # Reconstruct the derived text proof from the unchanged binary proof.
    folder=ROOT/'variants/A26';meta=json.loads((folder/'normalization.json').read_text())
    raw=(folder/'proof.drat').read_bytes();i=0;lines=[];duplicates=steps=0
    while i<len(raw):
        action=chr(raw[i]);assert action in 'ad';i+=1;clause=[]
        while True:
            number=shift=0
            while True:
                byte=raw[i];i+=1;number|=(byte&127)<<shift
                if byte<128: break
                shift+=7
            if not number: break
            assert number>=2
            clause.append(-(number//2) if number%2 else number//2)
        unique=list(dict.fromkeys(clause));duplicates+=len(clause)-len(unique);steps+=1
        assert not set(unique)&{-x for x in unique}
        lines.append(('d ' if action=='d' else '')+' '.join(map(str,unique+[0]))+'\n')
    assert ''.join(lines).encode()==(folder/'proof-deduplicated.drat').read_bytes()
    assert steps==meta['DRAT_steps']==4990 and duplicates==meta['DRAT_repeated_literals_removed_in_text_copy']==25
    variables,clauses=read_cnf_for_comparison(folder/'input.cnf')
    assert variables==930 and len(clauses)==5608 and all(len(c)==len(set(c)) for c in clauses)
    for name,h in meta['distributed_sha256'].items(): assert sha(folder/name)==h
    return {'binary_steps':steps,'proof_duplicates_removed':duplicates,'CNF_has_no_duplicate_literals':True}


def run():
    start=time.monotonic();normalization=proof_normalization();controls=dp_controls();designs=[]
    for family,d,gap,n in [('A',25,2,124),('a',16,4,125),('b',21,4,144)]:
        p=ROOT/'variants/designs'/f'{family}-D{d}.json';cert=json.loads(p.read_text())
        assert (cert['family'],cert['D'],cert['minimum_pair_separation'],cert['length'])==(family,d,gap,n)
        seq=cert['sequence'];t=variant_target(family,d)
        assert cert['target']==t and len(seq)==len(t)==n and set(seq)<=set(ABC)
        assert inspect(seq,t,gap)==d
        result=fold_gap(seq,gap);assert result==(d,1,t),(family,result)
        if gap==2: assert result==fold(seq)
        designs.append({'family':family,'D':d,'length':n,'minimum_pair_separation':gap,'optimum':result[0],'count':result[1],'target_equal':True,'certificate_sha256':sha(p)})
        print('Variant',family,d,'PASS',flush=True)
    upper=upper25()
    result={'status':'PASS','normalization':normalization,'DP_controls':controls,'designs':designs,'A25_upper':upper,'elapsed_seconds':time.monotonic()-start,
        'not_claimed':'No maximum for gap4 families a or b. Cake/DRAT replays use separate commands.'}
    save('variants.json',result);print('All variant checks PASS',flush=True)
    return result

if __name__=='__main__':run()
