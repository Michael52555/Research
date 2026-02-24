from itertools import product, combinations
import math

def mods_from_exponents(p, exps): 
    return [p**a for a in exps]

def add(v, w, mods):
    return tuple((v[i] + w[i]) % mods[i] for i in range(len(mods)))

def scalar_mul(c, v, mods):
    return tuple((c * v[i]) % mods[i] for i in range(len(mods)))

def generate_subgroup(gens, mods):
    H = {tuple([0]*len(mods))}
    changed = True
    while changed:
        changed = False
        for x in list(H):
            for g in gens:
                y = add(x, g, mods)
                if y not in H:
                    H.add(y)
                    changed = True
    return H

def endomorphism_matrices(p, exps):
    n = len(exps)
    mods = mods_from_exponents(p, exps)
    allowed = []
    for i in range(n):
        row = []
        for j in range(n):
            min_pow = max(0, exps[i] - exps[j])
            step = p**min_pow
            row.append(list(range(0, mods[i], step)))
        allowed.append(row)

    for rows in product(*[product(*allowed[i]) for i in range(n)]):
        yield rows

def apply_matrix(M, v, mods):
    out = []
    for i in range(len(v)):
        s = 0
        for j in range(len(v)):
            s += M[i][j] * v[j]
        out.append(s % mods[i])
    return tuple(out)

def p_torsion_sizes(H, p, mods, m):
    # sizes[i-1] = |H[p^i]|
    sizes = []
    for i in range(1, m+1):
        pi = p**i
        killed = sum(
            1 for x in H
            if all((pi * x[k]) % mods[k] == 0 for k in range(len(mods)))
        )
        sizes.append(killed)
    return sizes

def type_from_torsion_sizes(p, sizes):
    # If log_p |H[p^i]| = sum_j min(i, lambda_j), recover partition lambda
    s = [0] + [int(round(math.log(sz, p))) for sz in sizes]  # s_i
    mvals = [s[i] - s[i-1] for i in range(1, len(s))]        # m_i = #{parts >= i}
    parts = []
    for i in range(len(mvals), 0, -1):
        nxt = mvals[i] if i < len(mvals) else 0
        count = mvals[i-1] - nxt   # #{parts == i}
        parts += [i] * count
    parts.sort(reverse=True)
    return tuple(parts)

def quotient_coset_reps(G_elems, H, mods):
    un = set(G_elems)
    reps = []
    while un:
        rep = next(iter(un))
        coset = set(add(rep, h, mods) for h in H)
        reps.append(rep)
        un -= coset
    return reps

def quotient_torsion_sizes(p, G_elems, H, mods, m):
    reps = quotient_coset_reps(G_elems, H, mods)
    sizes = []
    for i in range(1, m+1):
        pi = p**i
        sizes.append(sum(1 for rep in reps if scalar_mul(pi, rep, mods) in H))
    return sizes

def count_stabilizer(p, exps, H_gens):
    mods = mods_from_exponents(p, exps)
    H = generate_subgroup(H_gens, mods)

    cnt = 0
    for M in endomorphism_matrices(p, exps):
        if all(apply_matrix(M, h, mods) in H for h in H_gens):
            cnt += 1
    return cnt, len(H)

def test_many_H(p, exps, target_H_type, target_Q_type, max_subgroups=10):
    mods = mods_from_exponents(p, exps)
    G_elems = list(product(*[range(m) for m in mods]))
    mG = max(exps)

    seen = set()
    counts = []

    for g1, g2 in combinations(G_elems, 2):
        H = generate_subgroup([g1, g2], mods)
        if len(H) != p**sum(target_H_type):
            continue

        H_type = type_from_torsion_sizes(p, p_torsion_sizes(H, p, mods, mG))
        if H_type != target_H_type:
            continue

        Q_sizes = quotient_torsion_sizes(p, G_elems, H, mods, mG)
        Q_type  = type_from_torsion_sizes(p, Q_sizes)
        if Q_type != target_Q_type:
            continue

        key = frozenset(H)
        if key in seen:
            continue
        seen.add(key)

        stab_cnt, H_size = count_stabilizer(p, exps, [g1, g2])
        counts.append((g1, g2, H_size, stab_cnt))

        if len(counts) >= max_subgroups:
            break

    return counts

# Example model test:
p = 2
exps = [4, 2, 1]
target_H_type = (3, 1)
target_Q_type = (2, 1)

out = test_many_H(p, exps, target_H_type, target_Q_type, max_subgroups=8)
for (g1, g2, H_size, stab_cnt) in out:
    print("gens:", g1, g2, " |H|=", H_size, " stabilizers=", stab_cnt)
