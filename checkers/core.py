"""Standard-library model checks, adapted from the R004 implementation.
Packaging is subsequent integration, not a new blind verification.
SPDX-License-Identifier: Apache-2.0
"""
import sys
if not __debug__:
    raise RuntimeError("Optimized Python disables required checks; do not use -O")
from pathlib import Path
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import gzip, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INPUT = ROOT / 'data'
SCRATCH = ROOT / 'work' / 'checks'
ABC = 'ACGU'
PAIRS = frozenset(('AU', 'UA', 'CG', 'GC', 'GU', 'UG'))
WC = dict(zip('ACGU', 'UGCA'))
TAU = str.maketrans('ACGU', 'CAUG')

def target(d):
    return '((.' + '((.)).' * (d - 1) + '))'

def u_target():
    return '((.' + '.((.)).' * 13 + '.))'

def parse(s):
    pending, pairs = [], []
    for i, c in enumerate(s):
        if c == '(':
            pending.append(i)
        elif c == ')':
            if not pending:
                raise ValueError('unmatched closing parenthesis')
            pairs.append((pending.pop(), i))
        elif c != '.':
            raise ValueError('non dot-bracket character')
    if pending:
        raise ValueError('unmatched opening parenthesis')
    return frozenset(pairs)

def check_pairs(pairs, n):
    pairs = list(pairs)
    used, stack = set(), []
    for i, j in sorted(pairs):
        if not (0 <= i < j < n and j - i >= 2):
            raise ValueError('pair separation or index')
        if i in used or j in used:
            raise ValueError('reused endpoint')
        used.update((i, j))
        while stack and i > stack[-1]:
            stack.pop()
        if stack and j > stack[-1]:
            raise ValueError('crossing')
        stack.append(j)
    p = frozenset(pairs)
    for i, j in p:
        if (i + 1, j - 1) not in p and (i - 1, j + 1) not in p:
            raise ValueError('isolated pair')
    return sum((i + 1, j - 1) in p for i, j in p)

def check_rival(s, t, minimum):
    if len(s) != len(t):
        raise ValueError('length')
    p, tp = parse(s), parse(t)
    score = check_pairs(p, len(t))
    if p == tp or score < minimum or not p - tp:
        raise ValueError('target equality, score, or empty difference')
    return p, score

def dotbracket(pairs, n):
    s = ['.'] * n
    for i, j in pairs:
        if s[i] != '.' or s[j] != '.':
            raise ValueError('reused endpoint')
        s[i], s[j] = '(', ')'
    result = ''.join(s)
    if parse(result) != frozenset(pairs):
        raise ValueError('crossing')
    return result

def fold(sequence):
    """Unique maximal-helix decomposition; returns optimum, exact count, witness.

    State (i,j,forbid) excludes the endpoint pair when forbid is true.
    A paired leftmost position determines its partner and unique maximal helix
    of length >=2. Forbidding the interior endpoint pair makes that helix maximal.
    Independent inside/right components give products of counts; ties add counts.
    """
    @lru_cache(None)
    def f(i, j, forbid):
        if i > j:
            return (0, 1, '')
        score, count, rep = f(i + 1, j, False)
        rep = '.' + rep
        for k in range(i + 4, j + 1):
            if forbid and k == j:
                continue
            for length in range(1, (k - i) // 2 + 1):
                a, b = i + length - 1, k - length + 1
                if sequence[a] + sequence[b] not in PAIRS:
                    break
                if length < 2:
                    continue
                inside = f(i + length, k - length, True)
                after = f(k + 1, j, False)
                value = length - 1 + inside[0] + after[0]
                ways = inside[1] * after[1]
                if value > score:
                    score, count = value, ways
                    rep = '(' * length + inside[2] + ')' * length + after[2]
                elif value == score:
                    count += ways
        return score, count, rep
    return f(0, len(sequence) - 1, False)

@lru_cache(None)
def all_matchings(i, j):
    """Brute-force noncrossing matchings, without a helix recurrence."""
    if i > j:
        return (frozenset(),)
    out = list(all_matchings(i + 1, j))
    for k in range(i + 2, j + 1):
        for left in all_matchings(i + 1, k - 1):
            for right in all_matchings(k + 1, j):
                out.append(left | right | {(i, k)})
    return tuple(out)

def legal_matchings(n):
    out = []
    for p in all_matchings(0, n - 1):
        try:
            score = check_pairs(p, n)
        except ValueError:
            continue
        out.append((p, score))
    return out

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def manifest():
    m = json.loads((ROOT / 'claims.json').read_text())
    m['D_ge_14']['cases'] = json.loads((ROOT / m['case_data']).read_text())
    return m

def read_rivals(name):
    with gzip.open(INPUT / name, 'rt', encoding='ascii') as f:
        return [line.rstrip('\n') for line in f]

def variable_map(n, separation):
    return {(i, j): 4*n + k + 1 for k, (i, j) in enumerate(
        (i, j) for i in range(n) for j in range(i + separation, n))}

def x(i, a):
    return 4 * i + ABC.index(a) + 1

def formula(t, rivals, separation, fix_first_separator=False):
    """Construct all clauses from SPEC.md / RIVAL-UPPER.md, no input CNF read."""
    n, tp = len(t), parse(t)
    p = variable_map(n, separation)
    clauses = []
    for i in range(n):
        clauses.append(tuple(x(i, a) for a in ABC))
        clauses.extend((-x(i, a), -x(i, b)) for a, b in combinations(ABC, 2))
    for i, j in sorted(tp):
        clauses.extend((-x(i, a), -x(j, b)) for a, b in product(ABC, repeat=2) if WC[a] != b)
    unpaired = [i for i, c in enumerate(t) if c == '.']
    for i in unpaired:
        clauses.extend(((-x(i, 'G'),), (-x(i, 'U'),)))
    if fix_first_separator:
        clauses.append((x(2, 'A'),))
    for (i, j), v in p.items():
        clauses.extend((-x(i, a), -x(j, b), v) for a, b in product(ABC, repeat=2) if a+b in PAIRS)
        for a in ABC:
            clauses.append((-v, -x(i, a)) + tuple(x(j, b) for b in ABC if a+b in PAIRS))
            clauses.append((-v, -x(j, a)) + tuple(x(i, b) for b in ABC if a+b in PAIRS))
    clauses.extend((p[pair],) for pair in sorted(tp))
    clauses.extend((-p[(i, j)],) for i, j in combinations(unpaired, 2))
    base = len(clauses)
    for r in rivals:
        difference = parse(r) - tp
        assert difference
        clauses.append(tuple(-p[pair] for pair in sorted(difference)))
    return 4*n + len(p), clauses, base

def write_cnf(path, variables, clauses):
    with open(path, 'w', encoding='ascii') as f:
        f.write(f'p cnf {variables} {len(clauses)}\n')
        for c in clauses:
            f.write(' '.join(map(str, c)) + ' 0\n')

def clause_multiset(clauses):
    return Counter(tuple(sorted(c)) for c in clauses)

def read_cnf_for_comparison(path):
    """Only machine inspection of permitted CNFs. Never emit their raw content."""
    clauses, current, header = [], [], None
    with open(path) as f:
        for line in f:
            if line.startswith('c') or not line.strip():
                continue
            if line.startswith('p'):
                _, fmt, v, c = line.split()
                assert fmt == 'cnf' and header is None
                header = int(v), int(c)
                continue
            for token in line.split():
                z = int(token)
                if z == 0:
                    clauses.append(tuple(current)); current = []
                else:
                    current.append(z)
    assert not current and header and len(clauses) == header[1]
    assert all(0 < abs(z) <= header[0] for c in clauses for z in c)
    return header[0], clauses

def save(name, data):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
