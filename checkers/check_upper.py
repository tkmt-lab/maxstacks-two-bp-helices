"""U14 families, word coverage, symmetries, finite embedding supplements and UCP. SPDX-License-Identifier: Apache-2.0"""
from core import *
from math import comb
import time

def stem(s): return {(s,s+4),(s+1,s+3)}
def triple(a,b): return {(a+k,b+2-k) for k in range(3)}

def families():
    t=u_target(); tp=parse(t); n=len(t)
    root={(0,n-1),(1,n-2)}
    local_target=parse('.((.)).')
    local=[p for p,v in legal_matchings(7) if v>=1 and p!=local_target]
    assert len(local)==6
    rows=[]
    def add(name,p,details):
        check_pairs(p,n)
        assert p!=tp and check_pairs(p,n)>=14
        rows.append({'family':name,'pairs':frozenset(p),'details':details})
    for k in range(13):
        s=4+7*k
        for p in local:
            add('local',tp-stem(s)|{(i+s-1,j+s-1) for i,j in p},[k])
        add('outer_swap',tp-root-stem(s)|{(0,s+1),(1,s),(s+3,n-1),(s+4,n-2)},[k])
        for r in range(1,4):
            add('left_triplet',tp-root-stem(s)|triple(0,s+r),[k,r])
        for r in range(-1,2):
            add('right_triplet',tp-root-stem(s)|triple(s+r,n-3),[k,r])
    for k,l in combinations(range(13),2):
        s,u=4+7*k,4+7*l
        rest=tp-stem(s)-stem(u)
        add('inner_swap',rest|{(s,u+4),(s+1,u+3),(s+3,u+1),(s+4,u)},[k,l])
        for r,q in product(range(-1,4),repeat=2):
            if abs(r-q)<=2:
                add('inner_triplet',rest|triple(s+r,u+q),[k,l,r,q])
    add('root_shift',tp-root|{(0,n-2),(1,n-3)},[0])
    add('root_shift',tp-root|{(1,n-1),(2,n-2)},[1])
    assert len(rows)==1731 and len({row['pairs'] for row in rows})==1731
    actual={parse(r) for r in read_rivals('rivals-U14.txt.gz')}
    assert {row['pairs'] for row in rows}==actual
    return rows

def word_coverage(rows):
    # All pairs of outer stem letters, and the two normalized hairpin letters.
    words=sorted(a+b+h+WC[b]+WC[a] for a,b in product(ABC,repeat=2) for h in 'AC')
    assert len(words)==32
    bad={}; witnesses={}
    for i,j in combinations(range(32),2):
        w,z=words[i],words[j]
        witness=[]
        if w[:2]==z[:2]: witness.append(('inner_swap',))
        for r,q in product(range(3),repeat=2):
            if all(w[r+k]+z[q+2-k] in PAIRS for k in range(3)):
                witness.append(('inner_triplet',r,q))
        if witness:
            bad[i,j]=True; witnesses[i,j]=witness
    # Check the abstract incompatibilities against actual rival differences at
    # EVERY slot pair, using only the ten fixed letters, not separator guesses.
    tp=parse(u_target())
    checks=0
    for k,l in combinations(range(13),2):
        relevant=[row for row in rows if row['family'] in ('inner_swap','inner_triplet') and row['details'][:2]==[k,l]]
        for i,j in combinations(range(32),2):
            for wi,wj in ((i,j),(j,i)):
                assignment={4+7*k+q:a for q,a in enumerate(words[wi])}
                assignment.update({4+7*l+q:a for q,a in enumerate(words[wj])})
                forced=[]
                for row in relevant:
                    q=row['pairs']-tp
                    if all(a in assignment and b in assignment and assignment[a]+assignment[b] in PAIRS for a,b in q):
                        forced.append(row)
                assert bool(forced)==bool(bad.get((i,j))), (k,l,words[i],words[j])
                checks+=1
    groups=[[i for i,w in enumerate(words) if w[:2]==a+b] for a,b in product(ABC,repeat=2)]
    accepted=[]; stats=Counter()
    # Three possibilities in each of 16 groups: omit, use h=A, use h=C.
    # Exactly 13 selected groups. Pruning counts every rejected full candidate.
    def descendants(groups_left,need):
        return comb(groups_left,need)*2**need if 0<=need<=groups_left else 0
    def visit(g,chosen):
        stats['nodes']+=1
        need=13-len(chosen); remaining=16-g
        if need<0 or need>remaining: return
        if not remaining:
            assert need==0
            accepted.append(tuple(words[i] for i in chosen)); stats['accepted']+=1; return
        visit(g+1,chosen)
        if need:
            for i in groups[g]:
                incompatible=next((j for j in chosen if bad.get(tuple(sorted((i,j))))),None)
                if incompatible is not None:
                    stats['rejected_candidates']+=descendants(remaining-1,need-1)
                else:
                    visit(g+1,chosen+(i,))
    visit(0,())
    assert stats['accepted']+stats['rejected_candidates']==comb(16,13)*2**13==4587520
    assert len(accepted)==68
    sets={tuple(sorted(s)) for s in accepted}
    def tau_set(s): return tuple(sorted(w.translate(TAU) for w in s))
    assert {tau_set(s) for s in sets}==sets
    assert all(tau_set(s)!=s for s in sets)
    reps={min(s,tau_set(s)) for s in sets}
    assert len(reps)==34
    supplied={tuple(c['sorted_words']) for c in manifest()['D_ge_14']['cases']}
    assert len(supplied)==34 and {min(s,tau_set(s)) for s in supplied}==reps
    assert all(s in sets for s in supplied)
    result={'words':words,'incompatible_pairs':len(bad),'all_slot_orientation_checks':checks,
            'candidate_count':4587520,'enumeration':dict(stats),'accepted_sets':sorted(sets),
            'tau_representatives':sorted(reps),'manifest_covers_each_orbit_once':True,
            'incompatibility_witnesses':[{'words':[words[i],words[j]],'rivals':w} for (i,j),w in witnesses.items()]}
    save('word-coverage.json',result)
    return {k:v for k,v in result.items() if k not in ('words','accepted_sets','tau_representatives','incompatibility_witnesses')}

def symmetry(clauses):
    n=97; p=variable_map(n,1); inverse={v:ij for ij,v in p.items()}; original=clause_multiset(clauses)
    out=[]
    permutations=[]
    for k in range(12):
        perm=list(range(n))
        for q in range(7):
            a,b=3+7*k+q,3+7*(k+1)+q; perm[a],perm[b]=b,a
        permutations.append((f'blocks_{k}_{k+1}',perm,False))
    permutations.append(('tau',list(range(n)),True))
    for name,perm,tau in permutations:
        mapping={}
        for v in range(1,4*n+1):
            i,a=divmod(v-1,4); letter=ABC[a].translate(TAU) if tau else ABC[a]
            mapping[v]=x(perm[i],letter)
        for v,(i,j) in inverse.items(): mapping[v]=p[tuple(sorted((perm[i],perm[j])))]
        assert len(set(mapping.values()))==5044
        transformed=Counter(tuple(sorted((1 if z>0 else -1)*mapping[abs(z)] for z in c)) for c in clauses)
        assert transformed==original,name
        out.append({'generator':name,'full_clause_multiset_preserved':True})
    save('symmetries.json',out)
    return out

def embeddings(rows):
    examples=[]; total=0
    for d in (14,15,16,17,20,32,64,101):
        choices={tuple(range(1,14)),tuple(range(d-13,d)),tuple(1+k*(d-2)//12 for k in range(13))}
        if d>=15: choices.add(tuple(range(1,7))+tuple(range(d-7,d)))
        for selected in sorted(choices):
            assert len(set(selected))==13 and min(selected)>=1 and max(selected)<d
            n=6*d-1; realtarget=parse(target(d)); virtualtarget=parse(u_target())
            mapping={0:0,1:1,95:n-2,96:n-1,2:2,94:n-3}
            for k,j in enumerate(selected):
                mapping.update({3+7*k+r:6*j-4+r for r in range(7)})
            selected_target={tuple(sorted((mapping[i],mapping[j]))) for i,j in virtualtarget}
            untouched=realtarget-selected_target
            minscore=999; alias=97-len(set(mapping.values()))
            for row in rows:
                mapped=[tuple(sorted((mapping[i],mapping[j]))) for i,j in row['pairs']]
                assert len(mapped)==len(set(mapped)), 'duplicate mapped pair'
                mapped.extend(untouched)
                score=check_pairs(mapped,n)
                assert score>=d and frozenset(mapped)!=realtarget
                minscore=min(minscore,score); total+=1
            examples.append({'D':d,'selected_branches':selected,'duplicated_virtual_positions':alias,'all_rivals':len(rows),'minimum_score':minscore})
    save('embedding-examples.json',{'note':'Finite supplements only; general argument is in claims/RIVAL-UPPER.md and the article.','total_rival_embeddings':total,'examples':examples})
    return {'total_rival_embeddings':total,'selections':len(examples)}

def propagate(clauses):
    assignment={}; trace=[]
    while True:
        changed=False
        for ci,c in enumerate(clauses):
            if any(assignment.get(abs(z))==(z>0) for z in c): continue
            open_literals=[z for z in c if abs(z) not in assignment]
            if not open_literals: return trace,ci
            if len(open_literals)==1:
                z=open_literals[0]; assignment[abs(z)]=z>0
                trace.append((z,ci)); changed=True
        if not changed: raise AssertionError('No unit propagation contradiction')

def replay(clauses,trace,conflict):
    # Independent replay: remove already falsified literals; exactly one remains.
    values={}
    for z,ci in trace:
        assert abs(z) not in values
        remaining=[]
        for literal in clauses[ci]:
            if abs(literal) not in values:
                remaining.append(literal)
            else:
                assert values[abs(literal)] != (literal>0)
        assert remaining==[z]
        values[abs(z)]=z>0
    assert all(abs(z) in values and values[abs(z)]!=(z>0) for z in clauses[conflict])

def unit_cases(clauses):
    results=[]
    out=SCRATCH/'ucp-certificates'; out.mkdir(exist_ok=True)
    for case in manifest()['D_ge_14']['cases']:
        units=[(x(4+7*k+q,a),) for k,w in enumerate(case['sorted_words']) for q,a in enumerate(w)]
        cc=clauses+units
        trace,conflict=propagate(cc); replay(cc,trace,conflict)
        data={'case':case['index'],'clause_order':'core.formula(U14) then 65 units in manifest order',
              'trace_literal_clause_index':trace,'conflict_clause_index':conflict}
        (out/f"case-{case['index']:02}.json").write_text(json.dumps(data,separators=(',',':'))+'\n')
        results.append({'case':case['index'],'unit_steps':len(trace),'conflict_clause_index':conflict,'replay':True})
    save('ucp-cases.json',results)
    return results

def run():
    start=time.monotonic(); rows=families()
    result={'family_counts':dict(Counter(r['family'] for r in rows))}
    print('Families exactly match all 1731 rivals',result['family_counts'],flush=True)
    result['words']=word_coverage(rows)
    print('Word coverage',result['words'],flush=True)
    _,clauses,_=formula(u_target(),read_rivals('rivals-U14.txt.gz'),1)
    result['symmetries']=symmetry(clauses)
    print('All 13 symmetry generators preserve full clause multisets',flush=True)
    result['embeddings']=embeddings(rows)
    print('Finite mapping supplement',result['embeddings'],flush=True)
    result['unit_cases']=unit_cases(clauses)
    result['elapsed_seconds']=time.monotonic()-start
    save('upper-checks.json',result)
    print('All 34 cases UCP UNSAT, traces replayed',flush=True)

if __name__=='__main__': run()
