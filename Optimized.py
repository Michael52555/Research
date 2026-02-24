from itertools import product

def build_support_masks(mapping, stindic, indic, outdic, pos, size, total):
    # variable id for each mapped entry
    var_id = { (mapping[t][0]-1, mapping[t][1]-1): t for t in range(total) }

    # precompute candidate lists once
    cand = [[None]*size for _ in range(size)]
    for i in range(size):
        k = stindic[i]
        for j in range(size):
            if k == -1:
                cand[i][j] = (-1, [])
                continue
            res = []
            for l in outdic[k]:
                if l != i:
                    res.append((l, j))
            for m in indic[j]:
                res.append((k, m))
            cand[i][j] = (k, res)

    support = [[0]*size for _ in range(size)]
    state   = [[0]*size for _ in range(size)]  # 0=unseen, 1=visiting, 2=done

    def dfs(i, j):
        if state[i][j] == 2:
            return support[i][j]
        if state[i][j] == 1:
            raise ValueError(f"cycle at {(i,j)}")

        state[i][j] = 1

        # forced-solved region (your pos rule)
        if pos[j+1] > pos[i+1]:
            support[i][j] = 0
            state[i][j] = 2
            return 0

        # mapped variable cell
        if (i, j) in var_id:
            support[i][j] = 1 << var_id[(i, j)]
            state[i][j] = 2
            return support[i][j]

        k, deps = cand[i][j]
        if k == -1:
            # stays whatever constant you set; in your code it's 0 unless mapped
            support[i][j] = 0
            state[i][j] = 2
            return 0

        if not deps:
            support[i][j] = 0
            state[i][j] = 2
            return 0

        mask = 0
        for (u, v) in deps:
            mask ^= dfs(u, v)

        support[i][j] = mask
        state[i][j] = 2
        return mask

    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                dfs(i, j)

    return support


def fast_experiment(mapping, arrows, starrows, pos, size, total, mu):
    stindic = {a: -1 for a in range(size)}
    stoutdic = {a: -1 for a in range(size)}
    indic = {a: [] for a in range(size)}
    outdic = {a: [] for a in range(size)}

    for a,b in arrows:
        indic[b-1].append(a-1)
        outdic[a-1].append(b-1)

    for a,b in starrows:
        stindic[b-1] = a-1
        stoutdic[a-1] = b-1

    support = build_support_masks(mapping, stindic, indic, outdic, pos, size, total)

    # Only check forbidden block cells that could ever become nonzero
    forbidden = []
    for i in range(mu):
        for j in range(mu, size):
            m = support[i][j]
            if m != 0:
                forbidden.append(m)

    ans = 0
    for bits in range(1 << total):
        ok = True
        for m in forbidden:

            if ((m & bits).bit_count() & 1) == 1:
                ok = False
                break
        if ok:
            ans += 1
    return ans

#



# mapping = [(7,1), (7,2), (7,5), (7,3), (7,6), (7,7), (6,1), (6,2), (6,5), (6,3), (6,6), (6,7), (8,1), (8,2), (8,5), (8,3), (8,6), (8,7), (8, 4), (8,8)]
# arrows = [(3,1), (4,3), (8,4), (6,2), (7,5), (8,7)]
# starrows = [(3, 1), (4, 3), (8,4), (6,2), (7,5)]

# arrows_1 = [(3,1), (4,3), (8,4), (6,2), (7,5), (8,7), (8,6)]

# pos = {1: 1, 2: 1, 5: 1, 3: 2, 6: 2, 7: 2, 4: 3, 8: 4}


mapping = [(9,1), (9,2), (9,7), (9,3), (9,4), (9, 9), (8,1), (8,2), (8,7), (8,3), (8,4), (8, 9), (8,5), (8,8), (10,1), (10,2), (10,7), (10,3), (10,4), (10, 9), (10,5), (10,8), (10, 6), (10,10)]
arrows = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 9), (10, 8)]
starrows = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7)]

arrows_1 = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 9)]
arrows_2 = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 9), (10, 8), (10, 7)]

pos = {1: 1, 2: 1, 7: 1, 3: 2, 4: 2, 9: 2, 5: 3, 8: 3, 6: 4, 10: 5}

print(fast_experiment(mapping, arrows, starrows, pos, 10, 24, 6))
print(fast_experiment(mapping, arrows_1, starrows, pos, 10, 24, 6))
print(fast_experiment(mapping, arrows_2, starrows, pos, 10, 24, 6))

# mapping = [(5, 1), (5, 2), (5, 5), (6, 1), (6, 2), (6, 5), (6, 3), (6, 6), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
# arrows = [(3, 1), (4, 3), (6, 2), (7, 4), (7, 5), (7,6)]
# starrows = [(3, 1), (4, 3), (6, 2), (7, 4)]

# pos = {1: 1, 2: 1, 3: 2, 4: 3, 5: 1, 6: 2, 7: 4}

# print(fast_experiment(mapping, arrows, starrows, pos, 7, 15, 4))

# print(fast_experiment(mapping, arrows, starrows, pos, 8, ))
# print(fast_experiment(mapping, arrows_1, starrows, pos, 7, 15, 4))
